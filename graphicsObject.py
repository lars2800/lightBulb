from libs import *

class GraphicsObject:
    def __init__(self,mesh,transform,meshMaterial,shader) -> None:
        self.mesh = mesh
        self.meshMaterial = meshMaterial
        self.transform = transform
        self.shader = shader
    
    def render(self):
        self.shader.use()
        self.transform.use(self.shader)
        self.mesh.render()