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

uniform vec3 cameraPos;

uniform vec3 objectColor;
uniform vec3 ambientColor;
uniform vec3 objectSpecular;
uniform vec3 objectDiffuse;

uniform vec3[256] lights;

vec3 calcLight(vec3 lightPosition,vec3 lightColor){
  	
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

    return (diffuse + specular);
}

void main()
{
    //flatColor
    vec4 textureColor = texture(textureSampler,TexCoord);
    vec3 objectColor  = objectColor;
    vec3 vertexColor  = VertexColor;
    vec3 flatColor    = textureColor.rgb * objectColor * vertexColor;

    vec3 lightsum = vec3(0.0,0.0,0.0);
    for (int i = 0; i < lights.length(); i++){
        lightsum = lightsum + calcLight(lights[i*2],lights[i*2+1]);
    }

    FragColor = vec4( ( (ambientColor * ambientStrength) + lightsum) * flatColor , 1.0 );
}