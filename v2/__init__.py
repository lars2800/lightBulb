import OpenGL.GL
import OpenGL.GL.shaders
import glfw
import glfw.GLFW as GLFW_CONSTANTS
import numpy as np
import ctypes
import pyrr
import time

import threading

class Transform:
    def __init__(self) -> None:
        
        self.position = pyrr.vector3.create(0,0,0)
        self.eulerAngles = pyrr.vector3.create(0,0,0)

class GraphicsObject:
    def __init__(self) -> None:

        self.vertexDataRaw = (
            -0.5, -0.5, -0.5, 1, 0, 0,
             0.5, -0.5, -0.5, 0, 1, 0,
             0.5,  0.5, -0.5, 0, 0, 1,

             0.5,  0.5, -0.5, 1, 0, 0,
            -0.5,  0.5, -0.5, 0, 1, 0,
            -0.5, -0.5, -0.5, 0, 0, 1,

            -0.5, -0.5,  0.5, 1, 0, 0,
             0.5, -0.5,  0.5, 0, 1, 0,
             0.5,  0.5,  0.5, 0, 0, 1,

             0.5,  0.5,  0.5, 1, 0, 0,
            -0.5,  0.5,  0.5, 0, 1, 0,
            -0.5, -0.5,  0.5, 0, 0, 1,

            -0.5,  0.5,  0.5, 1, 0, 0,
            -0.5,  0.5, -0.5, 0, 1, 0,
            -0.5, -0.5, -0.5, 0, 0, 1,

            -0.5, -0.5, -0.5, 1, 0, 0,
            -0.5, -0.5,  0.5, 0, 1, 0,
            -0.5,  0.5,  0.5, 0, 0, 1,

             0.5,  0.5,  0.5, 1, 0, 0,
             0.5,  0.5, -0.5, 0, 1, 0,
             0.5, -0.5, -0.5, 0, 0, 1,

             0.5, -0.5, -0.5, 1, 0, 0,
             0.5, -0.5,  0.5, 0, 1, 0,
             0.5,  0.5,  0.5, 0, 0, 1,

            -0.5, -0.5, -0.5, 1, 0, 0,
             0.5, -0.5, -0.5, 0, 1, 0,
             0.5, -0.5,  0.5, 0, 0, 1,

             0.5, -0.5,  0.5, 1, 0, 0,
            -0.5, -0.5,  0.5, 0, 1, 0,
            -0.5, -0.5, -0.5, 0, 0, 1,

            -0.5,  0.5, -0.5, 1, 0, 0,
             0.5,  0.5, -0.5, 0, 1, 0,
             0.5,  0.5,  0.5, 0, 0, 1,

             0.5,  0.5,  0.5, 1, 0, 0,
            -0.5,  0.5,  0.5, 0, 1, 0,
            -0.5,  0.5, -0.5, 0, 0, 1,
        )
        self.vertexCount = int( 12 * 3 )
        self.transform = Transform()
    
    def getModelTransform(self) -> np.ndarray:
        
        model_transform = pyrr.matrix44.create_identity(dtype=np.float32)

        model_transform = pyrr.matrix44.multiply(
            m1=model_transform, 
            m2=pyrr.matrix44.create_from_axis_rotation(
                axis = [0, 1, 0],
                theta = np.radians(self.transform.eulerAngles[1]), 
                dtype = np.float32
            )
        )

        return pyrr.matrix44.multiply(
            m1=model_transform, 
            m2=pyrr.matrix44.create_from_translation(
                vec=np.array(self.transform.position),dtype=np.float32
            )
        )
    
    def render(self,shaderProgram) -> None:

        self.vertexData = np.array(self.vertexDataRaw, dtype=np.float32)

        # Generate Vertex Attribute Object
        self.vao = OpenGL.GL.glGenVertexArrays(1)
        OpenGL.GL.glBindVertexArray(self.vao)

        # Generate Vertex Buffer Object
        self.vbo = OpenGL.GL.glGenBuffers(1)

        # Bind the vertex data
        OpenGL.GL.glBindBuffer(OpenGL.GL.GL_ARRAY_BUFFER, self.vbo)
        OpenGL.GL.glBufferData(OpenGL.GL.GL_ARRAY_BUFFER, self.vertexData.nbytes, self.vertexData, OpenGL.GL.GL_STATIC_DRAW)

        # Define vertex data
        OpenGL.GL.glEnableVertexAttribArray(0)
        OpenGL.GL.glVertexAttribPointer(0, 3, OpenGL.GL.GL_FLOAT, OpenGL.GL.GL_FALSE, 24, ctypes.c_void_p(0))
        
        OpenGL.GL.glEnableVertexAttribArray(1)
        OpenGL.GL.glVertexAttribPointer(1, 3, OpenGL.GL.GL_FLOAT, OpenGL.GL.GL_FALSE, 24, ctypes.c_void_p(12))

        # Update uniforms
        self.modelTransform = self.getModelTransform()
        OpenGL.GL.glUniformMatrix4fv( OpenGL.GL.glGetUniformLocation(shaderProgram,"model") , 1, OpenGL.GL.GL_FALSE, self.modelTransform )

        # Render
        OpenGL.GL.glBindVertexArray(self.vao)
        OpenGL.GL.glDrawArrays(OpenGL.GL.GL_TRIANGLES, 0, self.vertexCount)
    
    def destroy(self) -> None:
        """
            Free any allocated memory.
        """
        
        OpenGL.GL.glDeleteVertexArrays(1,(self.vao,))
        OpenGL.GL.glDeleteBuffers(1,(self.vbo,))

class GraphicsEngine:
    def __init__(self) -> None:
        """

        An object that litarly does everything for rendering

        use the run() function to run thje program and the stop() function to stop the program pre-maturly

        """        
        
        self.window_name = str("Lightbulb window") # The window title
        self.window_size = (int(500),int(500)) # The window size in
        self.fov_y = float(45)
        self.nearPlane = 0.1
        self.farPlane  = 100
        self.objects = []
        self.maxFps = 256
    
    def graphicsTick(self) -> None:
        pass

    def compileShaders(self,fragmentSource:str,vertexSource:str) -> OpenGL.GL.shaders.ShaderProgram:
        """
        Compiles an shader program from the sources

        Args:
            fragmentSource (str): The fragment shader source
            vertexSource (str): The vertex shader source

        Returns:
            OpenGL.GL.shaders.ShaderProgram: The compiled shader program
        """        

        fragmentShader = OpenGL.GL.shaders.compileShader( fragmentSource, OpenGL.GL.GL_FRAGMENT_SHADER )
        vertexShader   = OpenGL.GL.shaders.compileShader( vertexSource,   OpenGL.GL.GL_VERTEX_SHADER   )
        shaderProgram  = OpenGL.GL.shaders.compileProgram( vertexShader, fragmentShader )

        OpenGL.GL.glDeleteShader( fragmentShader )
        OpenGL.GL.glDeleteShader( vertexShader )

        return shaderProgram
    
    def setup(self) -> None:
        """

        Initzialze glfw and opengl

        """        
        
        #
        # init c libs
        #

        glfw.init()

        # set opengl version to 3.3 core ( modern opengl )
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR,3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR,3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_PROFILE, GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE )

        # create an window
        self.window = glfw.create_window( self.window_size[0] , self.window_size[1] , self.window_name, None, None)

        # set the opengl context to his new window
        glfw.make_context_current(self.window)

        # Compile shader
        fsrc = open("frag.glsl","r").read()
        vsrc = open("vert.glsl","r").read()
        self.shaderProgram = self.compileShaders( fsrc, vsrc )
        OpenGL.GL.glUseProgram(self.shaderProgram)

        # set the 'background' to black
        OpenGL.GL.glClearColor(0.0, 0.0, 0.0, 0.0)
        OpenGL.GL.glEnable( OpenGL.GL.GL_DEPTH_TEST )

        self.frameDelta = 0

    def setUniforms(self) -> None:

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy = self.fov_y, aspect = self.window_size[0]/self.window_size[1], 
            near = self.nearPlane, far = self.farPlane, dtype=np.float32
        )
        OpenGL.GL.glUniformMatrix4fv( OpenGL.GL.glGetUniformLocation(self.shaderProgram,"projection"), 1, OpenGL.GL.GL_FALSE, projection_transform )

    def render(self) -> None:
        """

        Renders an frame

        """

        self.graphicsTick()

        self.frameStart = time.time()

        glfw.poll_events()

        OpenGL.GL.glUseProgram(self.shaderProgram)
        OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT | OpenGL.GL.GL_DEPTH_BUFFER_BIT ) # type:ignore

        self.setUniforms()

        for e in self.objects:
            e.render( self.shaderProgram )
        
        glfw.swap_buffers( self.window )

    def handleTimings(self):

        self.unAjustedFrameDelta = time.time() - self.frameStart
        targetFrameDelta = (1/self.maxFps)

        if (self.unAjustedFrameDelta < targetFrameDelta ):
            time.sleep( targetFrameDelta - self.unAjustedFrameDelta )

        self.frameDelta = time.time() - self.frameStart

    def isForcedToStop(self) -> bool:
        """
        Returns an value wether the window is forced to stop

        Returns:
            bool: If the window is forced to stop
        """

        a = glfw.window_should_close(self.window)

        return a
    
    def run(self) -> None:
        """

        Begins the renderng thread use the stop() function to end it ( it will also end if u press the little x )

        """

        self.setup()

        self.running = True

        while ( self.running ):

            self.render()
            self.handleTimings()

            if ( self.isForcedToStop() ):
                self.running = False
        
        self.terminate()

    def terminate(self) -> None:
        """
        Frees up memory after the window has been closed
        """

        for e in self.objects:
            e.destroy()

        glfw.destroy_window(self.window)
        glfw.terminate()

    def stop(self) -> None:
        """
        Stops the curent running thread ( terminate is somthing else )
        """        
        self.running = False



if __name__ == "__main__":

    def Update() -> None:

        # rotate cube
        DEMO_renderEngine.objects[0].transform.eulerAngles[1] = DEMO_renderEngine.objects[0].transform.eulerAngles[1] + ( 250 ) * DEMO_renderEngine.frameDelta
        
        # update title
        try:
            fps = 1 / DEMO_renderEngine.frameDelta
            glfw.set_window_title( DEMO_renderEngine.window, f"Demo window {round(fps,3)}fps" )

        except ZeroDivisionError:
            glfw.set_window_title( DEMO_renderEngine.window, f"Demo window ∞ fps" )            

    DEMO_renderEngine = GraphicsEngine()
    DEMO_renderEngine.window_name = "Demo window"
    DEMO_renderEngine.window_size = (600,600) # Width, height
    DEMO_renderEngine.objects.append( GraphicsObject() )
    DEMO_renderEngine.objects[0].transform.position[2] = -10
    DEMO_renderEngine.graphicsTick = Update
    DEMO_renderEngine.run()