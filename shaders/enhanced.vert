#version 330 core

layout (location = 0) in vec2 in_texture_coord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position;
layout (location = 3) in vec3 in_tangent;     // New input
layout (location = 4) in vec3 in_bitangent;   // New input

out vec2 uv_0;
out vec3 normal;
out vec3 fragPos;
out vec4 shadowCoord;
out vec3 tangent;      // Pass to fragment shader
out vec3 bitangent;    // Pass to fragment shader

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_view_light;
uniform mat4 m_model;

mat4 m_shadow_bias = mat4(
    0.5, 0.0, 0.0, 0.0,
    0.0, 0.5, 0.0, 0.0,
    0.0, 0.0, 0.5, 0.0,
    0.5, 0.5, 0.5, 1.0
);


void main(){
    uv_0 = in_texture_coord_0;
    fragPos = vec3((m_model) * vec4(in_position, 1.0));

    // Compute normal matrix
    mat3 normalMatrix = transpose(inverse(mat3(m_model)));

    // Transform normals, tangents, and bitangents to world space
    normal = normalize(normalMatrix * in_normal);
    tangent = normalize(normalMatrix * in_tangent);
    bitangent = normalize(normalMatrix * in_bitangent);

    // normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);

    mat4 shadowMVP = m_proj * m_view_light * m_model;
    shadowCoord = m_shadow_bias * shadowMVP * vec4(in_position, 1.0);
    shadowCoord.z -= 0.0005;
}