# Import necessary libraries and modules
import pygame as pg
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import ctypes

# Define the version of the application
__version__ = "DEV 0.0.0"

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

        # Initialize pygame and set OpenGL context attributes
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        self.display = pg.display.set_mode(self.windSize, pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)

        # Create a pygame clock for controlling frame rate
        self.pgClock = pg.time.Clock()

        # Compile shaders and set up OpenGL settings
        self.shaderProgram = self.compileShaders("shader.vert", "shader.frag")
        glUseProgram(self.shaderProgram)
        glViewport(0, 0, *self.windSize)
        glClearColor(*self.clearColor)

        # Create the scene
        self.scene = Mesh()

        # Start the main loop
        self.run()

    # Function to compile vertex and fragment shaders into a shader program
    def compileShaders(self, vertShaderPath, fragShaderPath):
        with open(vertShaderPath) as vertShaderFile:
            vertShader = compileShader(vertShaderFile.read(), GL_VERTEX_SHADER)

        with open(fragShaderPath) as fragShaderFile:
            fragShader = compileShader(fragShaderFile.read(), GL_FRAGMENT_SHADER)

        shaderProgram = compileProgram(vertShader, fragShader)
        glDeleteShader(vertShader)
        glDeleteShader(fragShader)
        return shaderProgram

    # Function to render the scene
    def render(self):
        glUseProgram(self.shaderProgram)
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
        glDeleteProgram(self.shaderProgram)
        pg.quit()

# Create a Mesh class to manage geometry and rendering
class Mesh:
    def __init__(self) -> None:
        # Define vertex data and indices for a triangle
        self.vertices = np.array([
            # positions        # colors
             0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
            -0.5, -0.5, 0.0,  0.0, 1.0, 0.0,
             0.0,  0.5, 0.0,  0.0, 0.0, 1.0
        ], np.float32)

        self.indices = np.array([
            0, 1, 2,  # First Triangle
        ], np.int32)

        # Generate OpenGL objects for the mesh
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)

        # Bind the Vertex Array Object, Vertex Buffer, and Element Buffer
        glBindVertexArray(self.VAO)

        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 2 * 4, ctypes.c_void_p(4*0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 3 * 2 * 4, ctypes.c_void_p(4*3))
        glEnableVertexAttribArray(1)

        # Unbind VBO and VAO
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    # Function to render the mesh
    def render(self):
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

    # Function to clean up and delete OpenGL objects
    def terminate(self):
        glDeleteVertexArrays(1, (self.VAO,))
        glDeleteBuffers(1, (self.VBO,))

if __name__ == "__main__":
    # Create an instance of the Engine class and start the application
    demoEngine = Engine()
