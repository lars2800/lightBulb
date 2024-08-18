from libs import *

class Transform:
    def __init__(self,posX=0.0,posY=0.0,posZ=0.0,rotX=0.0,rotY=0.0,rotZ=0.0,scaleX=1.0,scaleY=1.0,scaleZ=1.0) -> None:
        self.posX = posX
        self.posY = posY
        self.posZ = posZ
        self.rotX = rotX
        self.rotY = rotY
        self.rotZ = rotZ
        self.scaleX = scaleX
        self.scaleY = scaleY
        self.scaleZ = scaleZ
    
    def use(self,shader):
        model = glm.mat4(1.0)
        model = glm.scale(model,glm.vec3(self.scaleX,self.scaleY,self.scaleZ))
        model = glm.translate(model,glm.vec3(self.posX,self.posY,self.posZ))
        model = glm.rotate(model,self.rotX ,glm.vec3(1.0,0.0,0.0) )
        model = glm.rotate(model,self.rotY ,glm.vec3(0.0,1.0,0.0) )
        model = glm.rotate(model,self.rotZ ,glm.vec3(0.0,0.0,1.0) )
        shader.setMat4("model",model)