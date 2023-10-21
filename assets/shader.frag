#version 330 core
out vec4 FragColor;

in vec3 Normal;  
in vec3 FragPos;
in vec3 VertexColor;
in vec2 TexCoord; 

uniform sampler2D textureSampler;

uniform float specularStrength;
uniform float diffuseStrength;
uniform float ambientStrength;
uniform float shininess;

uniform vec3 lightPosition; 
uniform vec3 cameraPos; 
uniform vec3 lightColor;

uniform vec3 objectColor;
uniform vec3 ambientColor;
uniform vec3 objectSpecular;
uniform vec3 objectDiffuse;

void main()
{
    //flatColor
    vec4 textureColor = texture(textureSampler,TexCoord);
    vec3 objectColor  = objectColor;
    vec3 vertexColor  = VertexColor;
    vec3 flatColor    = textureColor.rgb * objectColor * vertexColor;

    // ambient
    vec3 ambient = ambientStrength * ambientColor;
  	
    // diffuse 
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPosition - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = (diff*objectDiffuse) * lightColor * diffuseStrength;
    
    // specular
    vec3 viewDir = normalize(cameraPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);  
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    vec3 specular = specularStrength * (spec*objectSpecular) * lightColor;  
        
    vec3 result = (ambient + diffuse + specular) * flatColor;
    FragColor = vec4(result, 1.0);
} 