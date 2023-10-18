#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
layout (location = 2) in vec2 aTexCoord;
layout (location = 3) in vec3 aNormal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform float width;
uniform float height;
uniform vec3 cameraPos;

out vec3 VertexColorIn;
out vec2 TexCoordIn;
out vec3 NormalCoord;
out vec3 FragPos;

void main()
{
    gl_Position = projection * view * model * (vec4(aPos, 1.0) * (width/height));

    VertexColorIn = aColor;
    TexCoordIn = aTexCoord;
    FragPos     = vec3(model * vec4(aPos,   1.0));
    NormalCoord = normalize(mat3(transpose(inverse(model))) * aNormal);
}