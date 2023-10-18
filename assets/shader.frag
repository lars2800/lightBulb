#version 330 core

out vec4 FragColor;

in vec3 VertexColorIn;
in vec2 TexCoordIn;
in vec3 NormalCoord;
in vec3 FragPos;


uniform sampler2D ourTexture;
uniform vec3  objectColorIn;

uniform vec3  ambientColor;
uniform float ambientStrength;

uniform vec3  lightPosition;
uniform vec3  lightColor;

uniform vec3  cameraPos;

uniform float specularStrength;
uniform float diffuseStrength;
uniform float shininess;


    

void main()
{
    //base values
    vec3 resultTextureColor   = vec3(texture(ourTexture,TexCoordIn).x, texture(ourTexture,TexCoordIn).y, texture(ourTexture,TexCoordIn).z);
    vec3 resultObjectColor    = vec3(objectColorIn);
    vec3 resultVertexColor    = vec3(VertexColorIn);
    vec3 baseFlatColor = resultObjectColor * resultTextureColor * resultVertexColor;

    vec3 normal = normalize(NormalCoord);

    // Ambient lightning
    vec3 ambient   = vec3(ambientColor*ambientStrength);

    // difuse
    vec3 lightDir = normalize(lightPosition - FragPos);
    vec3 diffuse  = (max( dot(NormalCoord,lightDir) ,0)) * lightColor * diffuseStrength;
    
    // specular o boy
    vec3 viewSource    = normalize(cameraPos);
    vec3 reflectSource = normalize(reflect(-lightPosition,normal));
    float spec         = max(0.0, dot(viewSource, reflectSource));
    vec3 specular      = pow(spec,shininess) * lightColor * specularStrength;

    vec3 result = (specular + diffuse + ambient) * baseFlatColor;
    FragColor = vec4(result,1.0);
} 