# Import necessary libraries and modules
from libs import *
from mesh import Mesh
from texture import Texture
from shader import ShaderProgram
from transform import Transform
from graphicsObject import GraphicsObject
from scene import Scene
from camera import Camera

# Define the version of the application
__version__ = "DEV 0.0.3C"

# Create an Engine class to manage the main application logic
class Engine:
    def __init__(self) -> None:
        """
        Initialize the Engine class.

        This is the main class for the Lightbulb application.
        """
        # Define initial window properties
        self.windSize = (950, 950)
        self.windTitle = "Lightbulb " + __version__
        self.clearColor = (0.1, 0.2, 0.2, 1.0)
        self.maxFps = 60  # Maximum frames per second (0 for unlimited)
        self.deltaTime = 0
        self.startTime = round(time.time(),2)
        self.lastFrame = 0
        self.cameraSpeed = 0.1
        self.mouseSens   = 0.1

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
        self.shaderProgram = ShaderProgram("assets/shader.vert","assets/shader.frag")
        self.shaderProgram.use()
        self.shaderProgram.setMat4("model",     self.identyMat4)
        self.shaderProgram.setMat4("view" ,     self.identyMat4)
        self.shaderProgram.setMat4("projection",self.identyMat4)

        glViewport(0, 0, *self.windSize)
        glEnable(GL_DEPTH_TEST)
        glClearColor(*self.clearColor)
        pg.mouse.set_visible(False)

        #pg.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        pg.mouse.set_pos([400,400])

        # Create the scene
        self.camera = Camera()
        self.scene = Scene(self.shaderProgram,self.camera)

        self.cubeMaterial = Texture("assets/brick.png")
        self.cubeMesh = Mesh(self.cubeMaterial)
        self.cubeTransform = Transform(0.0 ,0.0 , 0.0   ,0.0 ,0.0 ,0.0)
        self.cube = GraphicsObject(self.cubeMesh,self.cubeTransform,self.cubeMaterial,self.shaderProgram)
        
        self.scene.objects.append(self.cube)

        # Start the main loop
        self.run()

    
    # Main loop function
    def run(self):
        self.running = True

        while self.running:
            self.pollEvents()
            self.handleKeys()
            self.render()
            self.updateTime()
            self.updateUniforms()
            self.update()

        self.terminate()
    
    # update time related things
    def updateTime(self):
        self.lastFrame = round(self.pgClock.tick(self.maxFps)/1000,2)
        self.fps = round(self.pgClock.get_fps(), 1)
        pg.display.set_caption(self.windTitle + " fps: " + str(self.fps))

        self.deltaTime = round(round(time.time(),2) - self.startTime,2)
    
    # update uniforms
    def updateUniforms(self):

        projection = glm.perspective( glm.radians(45.0), self.windSize[0]/self.windSize[1], 0.1, 100 )

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

    def handleKeys(self):

        keys = pg.key.get_pressed()
        mousePos = pg.mouse.get_pos()
        mouseMove = pg.mouse.get_rel()

        if keys[pg.K_z]:
            self.camera.cameraPos += self.cameraSpeed * self.camera.cameraFront
        
        if keys[pg.K_s]:
            self.camera.cameraPos -= self.cameraSpeed * self.camera.cameraFront
        
        if keys[pg.K_d]:
            self.camera.cameraPos += glm.normalize(glm.cross(self.camera.cameraFront, self.camera.cameraUp)) * self.cameraSpeed

        if keys[pg.K_q]:
            self.camera.cameraPos -= glm.normalize(glm.cross(self.camera.cameraFront, self.camera.cameraUp)) * self.cameraSpeed
        
        if keys[pg.K_SPACE]:
            self.camera.cameraPos += glm.vec3(0.0, 1.0*self.cameraSpeed, 0.0)
        
        if keys[pg.K_LSHIFT]:
            self.camera.cameraPos -= glm.vec3(0.0, 1.0*self.cameraSpeed, 0.0)
        
        if keys[pg.K_ESCAPE]:
            self.running = False
        
        if mousePos != (self.windSize[0]*0.5,self.windSize[1]*0.5):
            pg.mouse.set_pos([self.windSize[0]*0.5,self.windSize[1]*0.5])
            mouseMove = (mouseMove[0],-mouseMove[1])
            self.camera.yaw   = self.camera.yaw + (mouseMove[0]*self.mouseSens)
            self.camera.pitch = self.camera.pitch + (mouseMove[1]*self.mouseSens)
        
        if not pg.mouse.get_focused():
            pg.mouse.set_pos([self.windSize[0]*0.5,self.windSize[1]*0.5])

    
    def update(self):
        #self.cubeTransform.rotY = self.cubeTransform.rotY + self.lastFrame * 0.1
        self.cameraSpeed = self.lastFrame * 2.5
        

    # Function to clean up and terminate the application
    def terminate(self):
        self.cubeMaterial.terminate()
        self.cubeMesh.terminate()
        glDeleteProgram(self.shaderProgram.ID)
        pg.quit()

if __name__ == "__main__":
    # Create an instance of the Engine class and start the application
    demoEngine = Engine()