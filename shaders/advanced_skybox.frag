#version 330 core

in vec4 clipCoords;

out vec4 fragColor;

uniform samplerCube u_texture_skybox;
uniform mat4 m_invProjView;

void main() {
    vec4 worldCoords = m_invProjView * clipCoords;
    vec3 texCubeCoords = normalize(worldCoords.xyz / worldCoords.w);
    fragColor = texture(u_texture_skybox, texCubeCoords);
}
