from __future__ import annotations
import OpenGL.GL
import OpenGL.GL.shaders
import glfw
import glfw.GLFW as GLFW_CONSTANTS
import numpy as np
import ctypes
import glm
import time
import math


class GraphicsCore:
    def __init__(self) -> None:
        """

        Handles the graphics logic like the render loop, terminate memory, initzialaze opengl...

        """        
        
        # Varibles that can be edited by user
        self.window_width  = 500
        self.window_height = 500
        self.window_title = "Lightbulb Engine"
        self.max_fps = 60
        self.nearPlane = 0.1
        self.farPlane  = 100
        self.shader_fragment_source = "frag.glsl"
        self.shader_vertex_source   = "vert.glsl"
        self.fovY = 45

        # Internel varibles dont touch as user
        self.running = True
        self.window = None
        self.frameTime = 0
        self.shaderProgram = None
        self.fps = 0
    
    def start(self) -> None:
        """

        Initzialze, run the renderloop and terminate the logic (frees up memory)

        """        

        self.initzialze()
        self.renderLoop()
        self.terminate()
    
    def stop(self) -> None:
        """

        Stops the running render thread

        """        
        self.running = False

    def initzialze(self) -> None:
        """

        Initzialzes GLFW and OPENGL

        """        
        self.initzialzeGLFW()
        self.initzialzeOpenGL()

    def renderLoop(self) -> None:
        """

        Starts the renderloop

        """        
        
        self.running = True
        self.frameStartTime = time.time()

        while(self.running):

            self.pollEvents()
            self.render()
            self.pollTime()
        
        self.terminate()
    
    def terminate(self) -> None:
        """

        De iniziales glfw and opengl,
        Frees up memory by destrying things like shaderPrograms, objects...

        """        
        glfw.terminate()

    def initzialzeGLFW(self) -> None:
        """

        Initizalses GLFW and creates an window

        """        
        glfw.init()

        # set opengl version to 3.3 core ( modern opengl )
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR,3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR,3)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_PROFILE, GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE)
        glfw.window_hint(GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT, GLFW_CONSTANTS.GLFW_TRUE )

        # create an window
        self.window = glfw.create_window( self.window_width , self.window_height , self.window_title, None, None)

        # set the opengl context to his new window
        glfw.make_context_current(self.window)

    def initzialzeOpenGL(self) -> None:
        """

        Initzialzes OPENGL

        """

        # Load and compile shaders to an shaderProgram
        vertexShaderText   = open(self.shader_vertex_source,   "r").read()
        fragmentShaderText = open(self.shader_fragment_source, "r").read()
        self.shaderProgram = self.compileShaderProgram( vertexShaderText, fragmentShaderText )

        # Set active shader to this shader
        OpenGL.GL.glUseProgram( self.shaderProgram )

        # Enable depth and set clear color
        OpenGL.GL.glClearColor( 0.1, 0.1, 0.1, 0 ) # red green blue, transparancy ( 1 = transparent )
        OpenGL.GL.glEnable( OpenGL.GL.GL_DEPTH_TEST )

    def pollEvents(self) -> None:
        """

        Polls the events

        """        
        glfw.poll_events()

        if (glfw.window_should_close(self.window)):
            self.stop()

    def pollTime(self) -> None:
        """

        Caclurtes times and so forth

        """        
        # Calcurate frametime
        frameEndTime   = time.time()
        frameStartTime = self.frameStartTime
        frameTime = frameEndTime - frameStartTime
        
        # Adjust frame time if the fps is too high
        targetFrameTime = 1 / self.max_fps
        if ( frameTime < targetFrameTime ):
            time.sleep( targetFrameTime - frameTime )
        
        # Set the frame time for the other functions to the adjusted frame time ( the actual frame time )
        adjustedFrameTime = frameStartTime - time.time()
        self.frameTime = adjustedFrameTime
        self.fps = 1 / self.frameTime

        # For next frame
        self.frameStartTime = time.time()

    def render(self) -> None:
        """

        Renders the scene

        """        
        OpenGL.GL.glClear( OpenGL.GL.GL_COLOR_BUFFER_BIT ) # Clear previous screen
        OpenGL.GL.glClear( OpenGL.GL.GL_DEPTH_BUFFER_BIT ) # Clear previous depth buffer

        glfw.swap_buffers( self.window ) # Draw to the screen

    def compileShaderProgram(self,vertexShaderText:str,fragmentShaderText:str) -> OpenGL.GL.shaders.ShaderProgram:
        """
        Given the vertexShader in text and the fragmentShader in text it will return an compiled ShaderProgram

        Args:
            vertexShaderText (str): The vertex shader in text
            fragmentShaderText (str): The fragment shader in text

        Returns:
            OpenGL.GL.shaders.ShaderProgram: The compiled shaderprogram
        """        
        vertexShader   = OpenGL.GL.shaders.compileShader( vertexShaderText,   OpenGL.GL.GL_VERTEX_SHADER   )
        fragmentShader = OpenGL.GL.shaders.compileShader( fragmentShaderText, OpenGL.GL.GL_FRAGMENT_SHADER )

        shaderProgram = OpenGL.GL.shaders.compileProgram( vertexShader, fragmentShader )

        OpenGL.GL.glDeleteShader(vertexShader)
        OpenGL.GL.glDeleteShader(fragmentShader)

        return shaderProgram
    
if __name__ == "__main__":

    # Create an new graphics engine core
    demoGraphicsEngine = GraphicsCore()

    # Settings u can adjust
    demoGraphicsEngine.window_width  = 600 # Window width in pixels
    demoGraphicsEngine.window_height = 600 # Window height in pixels
    demoGraphicsEngine.window_title = "DEMO PROGRAM" # The tiltle of the window
    demoGraphicsEngine.max_fps = 75 # The target or max fps
    demoGraphicsEngine.nearPlane = 0.1 # Anything closer will not render
    demoGraphicsEngine.farPlane  = 100 # Anything further will not ender
    demoGraphicsEngine.shader_fragment_source = "frag.glsl" # The fragment shader path
    demoGraphicsEngine.shader_vertex_source   = "vert.glsl" # The vertex   shader path
    demoGraphicsEngine.fovY = 45 # The fov of view verticly

    # Start the engine
    demoGraphicsEngine.start()