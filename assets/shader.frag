#version 330 core

out vec4 FragColor;

in vec3 vertexColorIn;
in vec2 TexCoordIn;

uniform sampler2D ourTexture;
uniform vec3 objectColorIn;
uniform vec3 lightColorIn;

void main()
{
    vec4 textureColor = texture(ourTexture,TexCoordIn);
    vec4 objectColor  = vec4(objectColorIn,1.0);
    vec4 lightColor   = vec4(lightColorIn,1.0);
    vec4 vertexColor  = vec4(vertexColorIn, 1.0);

    FragColor = vertexColor * textureColor * objectColor * lightColor;
}