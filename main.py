# Import necessary libraries and modules
from libs import *
from mesh import Mesh
from texture import Texture
from shader import ShaderProgram
from transform import Transform
from graphicsObject import GraphicsObject

# Define the version of the application
__version__ = "DEV 0.0.3B"

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
        self.maxFps = 60  # Maximum frames per second (0 for unlimited)
        self.deltaTime = 0
        self.startTime = round(time.time(),2)

        # identyMat4
        self.identyMat4 = glm.mat4(
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0
        )

        # Initialize pygame and set OpenGL context attributes
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        self.display = pg.display.set_mode(self.windSize, pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)

        # Create a pygame clock for controlling frame rate
        self.pgClock = pg.time.Clock()

        # Compile shaders and set up OpenGL settings
        self.shaderProgram = ShaderProgram("shader.vert","shader.frag")
        self.shaderProgram.use()
        self.shaderProgram.setMat4("model",     self.identyMat4)
        self.shaderProgram.setMat4("view" ,     self.identyMat4)
        self.shaderProgram.setMat4("projection",self.identyMat4)

        glViewport(0, 0, *self.windSize)
        glEnable(GL_DEPTH_TEST)
        glClearColor(*self.clearColor)

        # Create the scene
        self.cubeMaterial = Texture("brick.png")
        self.cubeMesh = Mesh(self.cubeMaterial)
        self.cubeTransform = Transform(0,0,-3,0,0,0)
        self.cube = GraphicsObject(self.cubeMesh,self.cubeTransform,self.cubeMaterial,self.shaderProgram)
        self.scene  = self.cube

        # Start the main loop
        self.run()
    
    # Main loop function
    def run(self):
        self.running = True

        while self.running:
            self.pollEvents()
            self.render()
            self.updateTime()
            self.updateUniforms()
            self.update()

        self.terminate()
    
    # update time related things
    def updateTime(self):
        self.pgClock.tick(self.maxFps)
        self.fps = round(self.pgClock.get_fps(), 1)
        pg.display.set_caption(self.windTitle + " fps: " + str(self.fps))

        self.deltaTime = round(round(time.time(),2) - self.startTime,2)
    
    # update uniforms
    def updateUniforms(self):
        view = glm.mat4(1.0)
        view = glm.translate(view, glm.vec3(0.0, 0.0 ,0.0))

        projection = glm.perspective( glm.radians(45.0), self.windSize[0]/self.windSize[1], 0.1, 100 )

        self.shaderProgram.setMat4("view" ,view)
        self.shaderProgram.setMat4("projection",projection)

    # Function to render the scene
    def render(self):
        self.shaderProgram.use()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

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
    
    def update(self):
        self.cube.transform.rotY = self.deltaTime * 0.5

    # Function to clean up and terminate the application
    def terminate(self):
        self.cubeMaterial.terminate()
        self.cubeMesh.terminate()
        glDeleteProgram(self.shaderProgram.ID)
        pg.quit()

if __name__ == "__main__":
    # Create an instance of the Engine class and start the application
    demoEngine = Engine()