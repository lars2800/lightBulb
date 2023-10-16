# Import necessary libraries and modules
from libs import *
from mesh import cube,lightMesh
from texture import Texture
from shader import ShaderProgram
from transform import Transform
from graphicsObject import GraphicsObject
from scene import Scene
from camera import Camera
from material import Material

# Define the version of the application
__version__ = "DEV 0.0.4"

# Create an Engine class to manage the main application logic
class Engine:
    #Initlizatian
    def __init__(self) -> None:
        """
        Initialize the Engine class.

        This is the main class for the Lightbulb application.
        """
        # Define initial window properties
        self.windSize = (1920, 1080)
        self.windTitle = "Lightbulb " + __version__
        self.clearColor = (0.1, 0.2, 0.2, 1.0)
        self.maxFps = 0  # Maximum frames per second (0 for unlimited)
        self.deltaTime = 0
        self.startTime = round(time.time(),2)
        self.lastFrame = 0
        self.cameraSpeed = 0.1
        self.mouseSens   = 0.1
        self.camFov = 75

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
        self.shaderProgram.setFloat("width", self.windSize[0])
        self.shaderProgram.setFloat("height",self.windSize[1])
        self.shaderProgram.setVec3("objectColor",glm.vec3(0.0,0.0,1.0))

        glViewport(0, 0, *self.windSize)
        glEnable(GL_DEPTH_TEST)
        glClearColor(*self.clearColor)
        pg.mouse.set_visible(False)

        #pg.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        pg.mouse.set_pos([400,400])

        # Create the scene
        self.camera = Camera()
        self.scene = Scene(self.shaderProgram,self.camera)


        self.lightTransform = Transform(5.0, 0.0, 0.0,  0.0, 0.0, 0.0)
        self.lightMesh      = lightMesh()
        self.lightTexture   = Texture("assets/light.png")
        self.lightMaterial  = Material(self.lightTexture,glm.vec3(1.0,0.8,0.2),self.shaderProgram)
        self.light          = GraphicsObject(self.lightMesh,self.lightTransform,self.lightMaterial,self.shaderProgram)

        self.cubeTransform  = Transform(0.0 ,0.0 , 0.0   ,0.0 ,0.0 ,0.0)
        self.cubeMesh       = cube()
        self.cubeTexture    = Texture("assets/brick.png")
        self.cubeMaterial   = Material(self.cubeTexture,glm.vec3(0.0,1.0,0.0),self.shaderProgram)
        self.cube           = GraphicsObject(self.cubeMesh,self.cubeTransform,self.cubeMaterial,self.shaderProgram)
        

        self.scene.objects.append(self.light)
        self.scene.objects.append(self.cube)

        # Start the main loop
        self.run()
   
    # Main loop function
    def run(self):
        self.running = True

        while self.running:
            self.pollEvents()
            self.handleInput()
            self.render()
            self.updateTime()
            self.updateUniforms()
            self.update()

        self.terminate()
    
    # update time related things
    def updateTime(self):
        self.lastFrame = round(self.pgClock.tick_busy_loop(self.maxFps)/1000,5)
        self.fps = round(self.pgClock.get_fps(), 1)
        pg.display.set_caption(self.windTitle + " fps: " + str(self.fps))

        self.deltaTime = round(round(time.time(),2) - self.startTime,2)
    
    # update uniforms
    def updateUniforms(self):
        projection = glm.perspective( glm.radians(self.camFov), self.windSize[0]/self.windSize[1], 0.01, 100 )
        self.shaderProgram.setMat4("projection",projection)

        self.shaderProgram.setFloat("width", self.windSize[0])
        self.shaderProgram.setFloat("height",self.windSize[1])

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
    
    # handels input
    def handleInput(self):

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
        
    # update function
    def update(self):
        self.cubeTransform.rotY = self.cubeTransform.rotY + self.lastFrame * 0.25
        self.cubeTransform.rotZ = self.cubeTransform.rotZ + self.lastFrame * 0.10
        self.cameraSpeed = self.lastFrame * 2.5
        
    # Function to clean up and terminate the application
    def terminate(self):
        self.cubeTexture.terminate()
        self.cubeMesh.terminate()
        glDeleteProgram(self.shaderProgram.ID)
        pg.quit()

if __name__ == "__main__":
    # Create an instance of the Engine class and start the application
    demoEngine = Engine()