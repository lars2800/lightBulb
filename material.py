from libs import *

class Material:
    def __init__(self,texture,objectColor,shader) -> None:
        self.texture     = texture
        self.objectColor = objectColor
        self.shader      = shader
    
    def terminate(self):
        self.texture.terminate()
    
    def use(self):
        self.texture.use()
        self.shader.setVec3("objectColor",self.objectColor)