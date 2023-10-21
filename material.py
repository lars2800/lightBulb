from libs import *

class Material:
    def __init__(self,texture,shader,objectColor:glm.vec3=glm.vec3(1.0,1.0,1.0),ambient:glm.vec3=glm.vec3(1.0,1.0,1.0),diffuse:glm.vec3=glm.vec3(1.0,1.0,1.0),specular:glm.vec3=glm.vec3(1.0,1.0,1.0),shininess:float=32) -> None:
        self.texture     = texture
        self.objectColor = objectColor
        self.shader      = shader
        self.ambient     = ambient
        self.diffuse     = diffuse
        self.specular    = specular
        self.shininess   = shininess
    
    def terminate(self):
        self.texture.terminate()
    
    def use(self):
        self.texture.use()
        self.shader.setVec3 ("ambientColor"    ,self.ambient)
        self.shader.setVec3 ("objectSpecular"  ,self.specular)
        self.shader.setVec3 ("objectDiffuse"   ,self.diffuse)
        self.shader.setFloat("shininess"       ,self.shininess)