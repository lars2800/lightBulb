# Import necessary libraries and modules
import pygame as pg
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import ctypes
import glm

# Define the version of the application
__version__ = "DEV 0.0.2A"

# Create an Engine class to manage the main application logic
class Engine:
    def __init__(self) -> None:
        """
        Initialize the Engine class.

        This is the main class for the Lightbulb application.
        """
        # Define initial window properties
        self.windSize = (800, 600)
        self.windTitle = "Lightbulb " + __version__
        self.clearColor = (0.1, 0.2, 0.2, 1.0)
        self.maxFps = 120  # Maximum frames per second (0 for unlimited)

        # transformation
        self.trans = glm.mat4(1.0)
        self.trans = glm.rotate(self.trans, glm.radians(90.0), glm.vec3(0.0,0.0,1.0))
        self.trans = glm.scale(self.trans, glm.vec3(0.5,0.5,0.5))

        # Initialize pygame and set OpenGL context attributes
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        self.display = pg.display.set_mode(self.windSize, pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)

        # Create a pygame clock for controlling frame rate
        self.pgClock = pg.time.Clock()

        # Compile shaders and set up OpenGL settings
        self.shaderProgram = shaderProgram("shader.vert","shader.frag")
        self.shaderProgram.use()
        self.shaderProgram.setMat4("transform",self.trans)

        glViewport(0, 0, *self.windSize)
        glClearColor(*self.clearColor)

        # Create the scene
        self.material = texture("brick.png")
        self.scene = Mesh(self.material)

        # Start the main loop
        self.run()

    # Function to render the scene
    def render(self):
        self.shaderProgram.use()
        glClear(GL_COLOR_BUFFER_BIT)

        self.scene.render()

        pg.display.flip()

    # Function to handle pygame events
    def pollEvents(self):
        for event in pg.event.get():  # Loop over all events
            if event.type == pg.QUIT:
                self.running = False  # Stop running

            if event.type == pg.VIDEORESIZE:  # Window resize
                self.windSize = event.dict['size']  # New size
                glViewport(0, 0, *self.windSize)  # Pass to OpenGL

    # Main loop function
    def run(self):
        self.running = True

        while self.running:
            self.pollEvents()
            self.render()

            self.pgClock.tick(self.maxFps)
            self.fps = round(self.pgClock.get_fps(), 1)
            pg.display.set_caption(self.windTitle + " fps: " + str(self.fps))

        self.terminate()

    # Function to clean up and terminate the application
    def terminate(self):
        self.scene.terminate()
        glDeleteProgram(self.shaderProgram.ID)
        pg.quit()

# Class for handeling and managing shaders
class shaderProgram:
    def __init__(self,vertPath:str = "shader.vert",fragPath:str = "shader.frag") -> None:

        with open(vertPath) as vertShaderFile:
            vertShader = compileShader(vertShaderFile.read(), GL_VERTEX_SHADER)

        with open(fragPath) as fragShaderFile:
            fragShader = compileShader(fragShaderFile.read(), GL_FRAGMENT_SHADER)

        shaderProgram = compileProgram(vertShader, fragShader)
        glDeleteShader(vertShader)
        glDeleteShader(fragShader)

        self.ID = shaderProgram
    
    def use(self):
        glUseProgram(self.ID)

    def setBool(self,name:str,value:bool):
        glUniform1i(glGetUniformLocation(self.ID, name), int(value))

    def setInt(self,name:str,value:int):
        glUniform1i(glGetUniformLocation(self.ID, name), int(value))

    def setFloat(self,name:str,value:int):
        glUniform1f(glGetUniformLocation(self.ID, name), float(value))
    
    def setMat4(self,name:str,value:glm.vec4):
        glUniformMatrix4fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, glm.value_ptr(value))

class texture:
    def __init__(self,filePath) -> None:

        self.texture = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image = pg.image.load(filePath).convert_alpha()
        image_width,image_height = image.get_rect().size
        img_data = pg.image.tostring(image,'RGBA')

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA,GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
    
    def terminate(self):
        glDeleteTextures(1,(self.texture, ))
    
    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

# Create a Mesh class to manage geometry and rendering
class Mesh:
    def __init__(self,text:texture) -> None:
        # Define vertex data and indices for a triangle
        self.vertices = np.array([
            # positions        # colors       # tex cords
             0.5, -0.5, 0.0,  1.0, 0.0, 0.0,  1.0,0.0,
            -0.5, -0.5, 0.0,  0.0, 1.0, 0.0,  0.0,0.0,
             0.0,  0.5, 0.0,  0.0, 0.0, 1.0,  0.5,1.0
        ], np.float32)

        self.indices = np.array([
            0, 1, 2,  # First Triangle
        ], np.int32)

        # Generate OpenGL objects for the mesh
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)
        self.text = text

        # Bind the Vertex Array Object, Vertex Buffer, and Element Buffer
        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)


        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, (3+3+2) * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, (3+3+2) * 4, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, (3+3+2) * 4, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)

        # Unbind VBO and VAO
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    # Function to render the mesh
    def render(self):
        self.text.use()
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    # Function to clean up and delete OpenGL objects
    def terminate(self):
        self.text.terminate()
        glDeleteVertexArrays(1, (self.VAO,))
        glDeleteBuffers(1, (self.VBO,))


if __name__ == "__main__":
    # Create an instance of the Engine class and start the application
    demoEngine = Engine()