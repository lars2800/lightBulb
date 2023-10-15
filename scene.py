from libs import *

class Scene:
    def __init__(self,shader,cam) -> None:
        self.objects = []
        self.camera  = cam
        self.shader = shader
    
    def render(self):
        self.camera.use(self.shader)

        for i in self.objects:
            i.render()

    def terminate(self):
        for j in self.objects:
            j.terminate()