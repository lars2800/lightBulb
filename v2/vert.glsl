#version 330 core

layout (location=0) in vec3 vertexPos;
layout (location=1) in vec3 vertexCol;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec3 fragCol;

void main()
{
    vec3 actualVert = vertexPos;
    gl_Position = projection * view * model * vec4(actualVert, 1.0);
    fragCol = vertexCol;
}