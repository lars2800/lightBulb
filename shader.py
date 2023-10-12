from libs import *

# Class for handeling and managing shaders
class ShaderProgram:
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
    
    def setMat4(self,name:str,value:glm.mat4):
        glUniformMatrix4fv(glGetUniformLocation(self.ID, name), 1, GL_FALSE, glm.value_ptr(value))