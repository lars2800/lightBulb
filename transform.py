from libs import *

class Transform:
    def __init__(self,posX,posY,posZ,rotX,rotY,rotZ) -> None:
        self.posX = posX
        self.posY = posY
        self.posZ = posZ
        self.rotX = rotX
        self.rotY = rotY
        self.rotZ = rotZ
    
    def use(self,shader):
        model = glm.mat4(1.0)
        model = glm.translate(model,glm.vec3(self.posX,self.posY,self.posZ))
        model = glm.rotate(model,self.rotX ,glm.vec3(1.0,0.0,0.0) )
        model = glm.rotate(model,self.rotY ,glm.vec3(0.0,1.0,0.0) )
        model = glm.rotate(model,self.rotZ ,glm.vec3(0.0,0.0,1.0) )
        shader.setMat4("model",model)