import pygame as pg
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import ctypes

__version__ = "DEV 0.0.0"

class Engine:
    def __init__(self) -> None:
        """
        
        Main engineClass of Lightbulb

        """
        self.windSize  = (800,600)
        self.windTitle = "Lightbulb " + __version__
        self.clearColor = (0.1 ,0.2 ,0.2 ,  1.0)
        self.maxFps = 120 # 0 = unlimeted

        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION,3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION,3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,pg.GL_CONTEXT_PROFILE_CORE)
        self.display = pg.display.set_mode(self.windSize, pg.OPENGL| pg.DOUBLEBUF | pg.RESIZABLE)
        
        self.pgClock = pg.time.Clock()

        self.shaderProgram = self.compileShaders("shader.vert","shader.frag")
        glUseProgram(self.shaderProgram)
        glViewport(0, 0, *self.windSize)
        glClearColor(*self.clearColor)

        self.scene = Mesh()

        self.run()

    def compileShaders(self,vertShaderPath,fragShaderPath):
        with open(vertShaderPath) as vertShaderFile:
            vertShader = compileShader(vertShaderFile.read(),GL_VERTEX_SHADER)

        with open(fragShaderPath) as fragShaderFile:
            fragShader = compileShader(fragShaderFile.read(),GL_FRAGMENT_SHADER)

        shaderProgram = compileProgram(vertShader,fragShader)
        glDeleteShader(vertShader)
        glDeleteShader(fragShader)
        return shaderProgram

    def render(self):
        glUseProgram(self.shaderProgram)
        glClear(GL_COLOR_BUFFER_BIT)

        self.scene.render()

        pg.display.flip()
    
    def pollEvents(self):

        for event in pg.event.get(): # loop over all events

            if event.type == pg.QUIT:
                self.running = False # stop running
            
            if event.type == pg.VIDEORESIZE: # Window resize
                self.windSize = event.dict['size'] # new size
                glViewport(0,0, *self.windSize)    # Pass to OpenGL
                print(self.windSize)

    def run(self):
        self.running = True

        while self.running:
            self.pollEvents()    
            self.render()

            self.pgClock.tick(self.maxFps)
            self.fps = round(self.pgClock.get_fps(),1)
            pg.display.set_caption(self.windTitle+" fps: "+str(self.fps))
        
        self.terminate()
    

    def terminate(self):
        self.scene.terminate()
        glDeleteProgram(self.shaderProgram)
        pg.quit()

class Mesh:
    def __init__(self) -> None:
        
        self.vertices = np.array([
             0.5,  0.5, 0.0,  # top right
             0.5, -0.5, 0.0,  # bottom right
            -0.5, -0.5, 0.0,  # bottom left
            -0.5,  0.5, 0.0   # top left 
        ],np.float32)
         
        self.indices = np.array([
            0, 1, 3,  # first Triangle
            1, 2, 3   # second Triangle
        ],np.int32)

        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)
        # bind the Vertex Array Object first, then bind and set vertex buffer(s), and then configure vertex attributes(s).
        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # note that this is allowed, the call to glVertexAttribPointer registered VBO as the vertex attribute's bound vertex buffer object so afterwards we can safely unbind
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        # remember: do NOT unbind the EBO while a VAO is active as the bound element buffer object IS stored in the VAO; keep the EBO bound.
        #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);

        # You can unbind the VAO afterwards so other VAO calls won't accidentally modify this VAO, but this rarely happens. Modifying other
        # VAOs requires a call to glBindVertexArray anyways so we generally don't unbind VAOs (nor VBOs) when it's not directly necessary.
        glBindVertexArray(0)

        # uncomment this call to draw in wireframe polygons.
        #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
    
    def render(self):
        glBindVertexArray(self.VAO); # seeing as we only have a single VAO there's no need to bind it every time, but we'll do so to keep things a bit more organized
        #glDrawArrays(GL_TRIANGLES, 0, 6);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        # glBindVertexArray(0); // no need to unbind it every time 
    
    def terminate(self):
        glDeleteVertexArrays(1, (self.VAO,))
        glDeleteBuffers(1, (self.VBO,))


if __name__ == "__main__":
    demoEngine = Engine()