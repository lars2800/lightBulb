from libs import *

class Camera:
    def __init__(self) -> None:
        self.yaw   = -90.0
        self.pitch = 0

        self.cameraPos    = glm.vec3(0.0, 0.0,  3.0)
        self.cameraFront  = glm.vec3(0.0, 0.0, -1.0)
        self.cameraUp     = glm.vec3(0.0, 1.0,  0.0)
        self.direction    = glm.vec3(0.0, 0.0,  0.0)

        self.direction.x  = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        self.direction.y  = glm.sin(glm.radians(self.pitch))
        self.direction.z  = glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
    
    def use(self,shader) -> None:

        if (self.pitch > 89.0):
            self.pitch = 89.0
        if (self.pitch < -89.0):
            self.pitch = -89.0

        self.direction.x  = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        self.direction.y  = glm.sin(glm.radians(self.pitch))
        self.direction.z  = glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        self.cameraFront = glm.normalize(self.direction)

        viewMat = glm.lookAt(self.cameraPos,self.cameraPos + self.cameraFront, self.cameraUp)

        shader.setMat4("view",viewMat)