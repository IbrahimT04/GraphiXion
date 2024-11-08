#version 330 core

in vec2 v_uv;
out vec4 fragColor;

uniform sampler2D u_color_0;

void main() {
    vec3 color = texture(u_color_0, v_uv).rgb;
    float gray = dot(color, vec3(0.299, 0.587, 0.114));  // Grayscale effect
    fragColor = vec4(vec3(gray), 1.0);
    // fragColor = vec4(color, 1.0);
}
