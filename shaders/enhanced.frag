#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;
in vec4 shadowCoord;
in vec3 tangent;
in vec3 bitangent;

struct Light {
    vec3 position;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

uniform Light light;
uniform sampler2D u_texture_0;     // Base texture
uniform sampler2D u_normal_0;      // Normal map
uniform sampler2D u_ao_0;          // Ambient occlusion map
uniform sampler2D u_smoothness_0;  // Smoothness map
uniform sampler2D u_metallic_0;    // Metallic map
uniform sampler2D u_height_0;      // Height map for parallax mapping
uniform vec3 camPos;
uniform sampler2DShadow shadowMap;
uniform vec2 u_resolution;

// Parameters for parallax occlusion mapping
uniform float parallaxScale = 0.05;  // Reduced scale for less aggressive effect
uniform float parallaxBias = 0.00;    // Set bias to 0 to avoid color loss
uniform int numSteps = 4;           // Increase steps for better quality

// Function for Parallax Occlusion Mapping
vec2 parallaxOcclusionMapping(vec2 texCoords, vec3 viewDir, mat3 TBN) {
    // Transform the view direction into tangent space
    vec3 viewDirTangent = normalize(TBN * viewDir);

    // Initialize UV coordinates
    vec2 currentTexCoords = texCoords;
    float currentHeight = texture(u_height_0, currentTexCoords).r;

    // Calculate step size
    float stepSize = 1.0 / float(numSteps);
    vec2 deltaTexCoords = viewDirTangent.xy * parallaxScale * stepSize;

    // Initialize variables for the loop
    float layerDepth = 0.0;
    float currentLayerDepth = 0.0;
    vec2 finalTexCoords = currentTexCoords;
    float finalHeight = currentHeight;

    // Ray marching loop to sample heights along the view direction
    for (int i = 0; i < numSteps; i++) {
        // Move to the next layer in depth and UV space
        currentTexCoords -= deltaTexCoords;
        currentLayerDepth += stepSize;

        // Sample height at new texture coordinates
        currentHeight = texture(u_height_0, currentTexCoords).r;

        // Check if we've hit the surface
        if (currentHeight < currentLayerDepth) {
            finalTexCoords = currentTexCoords;
            finalHeight = currentHeight;
            break;
        }
    }

    // Interpolate between the last two samples for a smoother result
    vec2 prevTexCoords = currentTexCoords + deltaTexCoords;
    float prevHeight = texture(u_height_0, prevTexCoords).r;
    float interpolationFactor = (currentLayerDepth - finalHeight) / (finalHeight - prevHeight);

    return mix(finalTexCoords, prevTexCoords, clamp(interpolationFactor, 0.0, 1.0));
}

float lookup(float ox, float oy) {
    vec2 pixelOffset = 1 / u_resolution;
    return textureProj(shadowMap, shadowCoord + vec4(ox * pixelOffset.x * shadowCoord.w,
                                                     oy * pixelOffset.y * shadowCoord.w,
                                                     0.0, 0.0));
}

float getSoftShadowX16() {
    float shadow = 0.0;
    float swidth = 1.0;
    float endp = swidth * 1.5;
    for (float y = -endp; y <= endp; y += swidth) {
        for (float x = -endp; x <= endp; x += swidth) {
            shadow += lookup(x, y);
        }
    }
    return shadow / 16.0;
}

// Corrected parallax mapping function
vec2 parallaxMapping(vec2 texCoords, vec3 viewDir, mat3 TBN) {
    // Transform the view direction into tangent space
    vec3 viewDirTangent = normalize(TBN * viewDir);

    // Sample the height map (grayscale)
    float height = texture(u_height_0, texCoords).r;

    // Calculate the parallax offset
    float parallax = (height * parallaxScale + parallaxBias);

    // Adjust the UV coordinates based on the view direction in tangent space
    return texCoords - viewDirTangent.xy * parallax;
}

vec3 getLight(vec3 baseColor, vec2 displacedUV) {
    // Normalize the input vectors
    vec3 N = normalize(normal);
    vec3 T = normalize(tangent);
    vec3 B = normalize(bitangent);

    // Construct the TBN matrix
    mat3 TBN = mat3(T, B, N);

    // Sample the normal map and transform it to [-1, 1]
    vec3 normalColor = texture(u_normal_0, displacedUV).rgb;
    vec3 normalMap = normalize(normalColor * 2.0 - 1.0);

    // Transform the normal from tangent space to world space
    vec3 newNormal = normalize(TBN * normalMap) * 1.02;

    // Proceed with lighting calculations using newNormal
    vec3 ambient = light.ambient;
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(dot(lightDir, newNormal), 0.0);
    vec3 diffuse = diff * light.diffuse;
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, newNormal);

    // Sample the metallic and smoothness maps using displaced UV
    float smoothness = texture(u_smoothness_0, displacedUV).r;
    float roughness = 1.0 - smoothness;
    float metallic = texture(u_metallic_0, displacedUV).r;

    // Calculate F0 (reflectivity at normal incidence)
    vec3 F0 = mix(vec3(0.04), baseColor, metallic);  // Non-metals have 4% reflectivity, metals use base color for specular reflection

    // Schlick's approximation for Fresnel effect
    float fresnelFactor = pow(1.0 - max(dot(viewDir, newNormal), 0.0), 5.0);
    vec3 fresnel = F0 + (1.0 - F0) * fresnelFactor;

    // Specular reflection calculation
    float specPower = mix(2.0, 64.0, smoothness);  // Sharper specular for smoother surfaces
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), specPower);
    vec3 specular = fresnel * spec * light.specular;

    // Shadow calculation
    float shadow = getSoftShadowX16();
    float ambientShade = texture(u_ao_0, displacedUV).r;

    // Final color: combine ambient, diffuse, and specular with shadow
    return baseColor * ((ambient * ambientShade) + (diffuse * (1.0 - metallic) + specular) * shadow);
}

void main() {
    float gamma = 2.2;
    vec3 viewDir = normalize(camPos - fragPos);

    // Normalize the input vectors and construct TBN matrix
    vec3 N = normalize(normal);
    vec3 T = normalize(tangent);
    vec3 B = normalize(bitangent);
    mat3 TBN = mat3(T, B, N);

    // Adjust UV coordinates based on parallax mapping
    vec2 displacedUV = parallaxOcclusionMapping(uv_0, viewDir, TBN);

    // Sample the base texture with the displaced UV coordinates
    vec3 color = texture(u_texture_0, displacedUV).rgb;
    color = pow(color, vec3(gamma));  // Apply gamma correction before lighting

    // Calculate lighting with the displaced UV coordinates
    color = getLight(color, displacedUV);

    color = pow(color, 1.0 / vec3(gamma));  // Inverse gamma correction
    fragColor = vec4(color, 1.0);           // Output the final color
}
