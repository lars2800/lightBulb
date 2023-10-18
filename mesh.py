from libs import *


# Create a Mesh class to manage geometry and rendering
class cube:
    def __init__(self) -> None:
        # Define vertex data and indices for a triangle
        self.vertices = np.array([
            # positions           # colors       # tex cords  # norm cords
            -0.5,  0.5,  0.5,   1.0, 1.0, 1.0,     0.0, 1.0,   0.0, 0.0, 1.0,
            -0.5, -0.5,  0.5,   1.0, 1.0, 1.0,     0.0, 0.0,   0.0, 0.0, 1.0,
             0.5,  0.5,  0.5,   1.0, 1.0, 1.0,     1.0, 1.0,   0.0, 0.0, 1.0,
            
             0.5,  0.5,  0.5,   1.0, 1.0, 1.0,     1.0, 1.0,   0.0, 0.0, 1.0,
            -0.5, -0.5,  0.5,   1.0, 1.0, 1.0,     0.0, 0.0,   0.0, 0.0, 1.0,
             0.5, -0.5,  0.5,   1.0, 1.0, 1.0,     1.0, 0.0,   0.0, 0.0, 1.0,


            -0.5,  0.5, -0.5,   1.0, 1.0, 1.0,     0.0, 1.0,   0.0, 0.0, -1.0,
            -0.5, -0.5, -0.5,   1.0, 1.0, 1.0,     0.0, 0.0,   0.0, 0.0, -1.0,
             0.5,  0.5, -0.5,   1.0, 1.0, 1.0,     1.0, 1.0,   0.0, 0.0, -1.0,
            
             0.5,  0.5, -0.5,   1.0, 1.0, 1.0,     1.0, 1.0,   0.0, 0.0, -1.0,
            -0.5, -0.5, -0.5,   1.0, 1.0, 1.0,     0.0, 0.0,   0.0, 0.0, -1.0,
             0.5, -0.5, -0.5,   1.0, 1.0, 1.0,     1.0, 0.0,   0.0, 0.0, -1.0,

            

            -0.5,  0.5, -0.5,   1.0, 1.0, 1.0,     0.0,0.0,    0.0, 1.0, 0.0,
            -0.5,  0.5,  0.5,   1.0, 1.0, 1.0,     1.0,0.0,    0.0, 1.0, 0.0,
             0.5,  0.5,  0.5,   1.0, 1.0, 1.0,     1.0,1.0,    0.0, 1.0, 0.0,
            
             0.5,  0.5,  0.5,   1.0, 1.0, 1.0,     1.0,1.0,    0.0, 1.0, 0.0,
            -0.5,  0.5, -0.5,   1.0, 1.0, 1.0,     0.0,0.0,    0.0, 1.0, 0.0,
             0.5,  0.5, -0.5,   1.0, 1.0, 1.0,     0.0,1.0,    0.0, 1.0, 0.0,


            -0.5, -0.5, -0.5,   1.0, 1.0, 1.0,     0.0,0.0,    0.0, -1.0, 0.0,
            -0.5, -0.5,  0.5,   1.0, 1.0, 1.0,     1.0,0.0,    0.0, -1.0, 0.0,
             0.5, -0.5,  0.5,   1.0, 1.0, 1.0,     1.0,1.0,    0.0, -1.0, 0.0,
            
             0.5, -0.5,  0.5,   1.0, 1.0, 1.0,     1.0,1.0,    0.0, -1.0, 0.0,
            -0.5, -0.5, -0.5,   1.0, 1.0, 1.0,     0.0,0.0,    0.0, -1.0, 0.0,
             0.5, -0.5, -0.5,   1.0, 1.0, 1.0,     0.0,1.0,    0.0, -1.0, 0.0,



            -0.5,  0.5,  0.5,   1.0, 1.0, 1.0,     0.0,1.0,    -1.0, 0.0, 0.0,
            -0.5, -0.5,  0.5,   1.0, 1.0, 1.0,     0.0,0.0,    -1.0, 0.0, 0.0,
            -0.5, -0.5, -0.5,   1.0, 1.0, 1.0,     1.0,0.0,    -1.0, 0.0, 0.0,

            -0.5,  0.5,  0.5,   1.0, 1.0, 1.0,     0.0,1.0,    -1.0, 0.0, 0.0,
            -0.5,  0.5, -0.5,   1.0, 1.0, 1.0,     1.0,1.0,    -1.0, 0.0, 0.0,
            -0.5, -0.5, -0.5,   1.0, 1.0, 1.0,     1.0,0.0,    -1.0, 0.0, 0.0,


             0.5,  0.5,  0.5,   1.0, 1.0, 1.0,     0.0,1.0,     1.0, 0.0, 0.0,
             0.5, -0.5,  0.5,   1.0, 1.0, 1.0,     0.0,0.0,     1.0, 0.0, 0.0,
             0.5, -0.5, -0.5,   1.0, 1.0, 1.0,     1.0,0.0,     1.0, 0.0, 0.0,

             0.5,  0.5,  0.5,   1.0, 1.0, 1.0,     0.0,1.0,     1.0, 0.0, 0.0,
             0.5,  0.5, -0.5,   1.0, 1.0, 1.0,     1.0,1.0,     1.0, 0.0, 0.0,
             0.5, -0.5, -0.5,   1.0, 1.0, 1.0,     1.0,0.0,     1.0, 0.0, 0.0,
        ], np.float32)

        self.indices = np.array([
            0,  1 , 2 ,
            3,  4 , 5 ,
            6,  7 , 8 ,
            9,  10, 11,
            12, 13, 14,
            15, 16, 17,
            18, 19, 20,
            21, 22, 23,
            24, 25, 26,
            27, 28, 29,
            30, 31, 32,
            33, 34, 35
        ], np.int32)
        self.vertNum = 36

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


        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, (3+3+2+3) * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, (3+3+2+3) * 4, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, (3+3+2+3) * 4, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)

        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, (3+3+2+3) * 4, ctypes.c_void_p(32))
        glEnableVertexAttribArray(3)

        # Unbind VBO and VAO
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    # Function to render the mesh
    def render(self):
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, self.vertNum, GL_UNSIGNED_INT, None)

    # Function to clean up and delete OpenGL objects
    def terminate(self):
        glDeleteVertexArrays(1, (self.VAO,))
        glDeleteBuffers(1, (self.VBO,))

class lightMesh:
    def __init__(self) -> None:
        # Define vertex data and indices for a triangle
        self.vertices = np.array([
            # positions            # colors           # tex cords #normal cords
            -0.25,  0.25,  0.25,   1.0, 1.0, 1.0,     0.0, 1.0,   0.0, 0.0, 1.0,
            -0.25, -0.25,  0.25,   1.0, 1.0, 1.0,     0.0, 0.0,   0.0, 0.0, 1.0,
             0.25,  0.25,  0.25,   1.0, 1.0, 1.0,     1.0, 1.0,   0.0, 0.0, 1.0,
            
             0.25,  0.25,  0.25,   1.0, 1.0, 1.0,     1.0, 1.0,   0.0, 0.0, 1.0,
            -0.25, -0.25,  0.25,   1.0, 1.0, 1.0,     0.0, 0.0,   0.0, 0.0, 1.0,
             0.25, -0.25,  0.25,   1.0, 1.0, 1.0,     1.0, 0.0,   0.0, 0.0, 1.0,


            -0.25,  0.25, -0.25,   1.0, 1.0, 1.0,     0.0, 1.0,   0.0, 0.0, -1.0,
            -0.25, -0.25, -0.25,   1.0, 1.0, 1.0,     0.0, 0.0,   0.0, 0.0, -1.0,
             0.25,  0.25, -0.25,   1.0, 1.0, 1.0,     1.0, 1.0,   0.0, 0.0, -1.0,
            
             0.25,  0.25, -0.25,   1.0, 1.0, 1.0,     1.0, 1.0,   0.0, 0.0, -1.0,
            -0.25, -0.25, -0.25,   1.0, 1.0, 1.0,     0.0, 0.0,   0.0, 0.0, -1.0,
             0.25, -0.25, -0.25,   1.0, 1.0, 1.0,     1.0, 0.0,   0.0, 0.0, -1.0,

            

            -0.25,  0.25, -0.25,   1.0, 1.0, 1.0,     0.0,0.0,   0.0, 1.0, 0.0,
            -0.25,  0.25,  0.25,   1.0, 1.0, 1.0,     1.0,0.0,   0.0, 1.0, 0.0,
             0.25,  0.25,  0.25,   1.0, 1.0, 1.0,     1.0,1.0,   0.0, 1.0, 0.0,
            
             0.25,  0.25,  0.25,   1.0, 1.0, 1.0,     1.0,1.0,   0.0, 1.0, 0.0,
            -0.25,  0.25, -0.25,   1.0, 1.0, 1.0,     0.0,0.0,   0.0, 1.0, 0.0,
             0.25,  0.25, -0.25,   1.0, 1.0, 1.0,     0.0,1.0,   0.0, 1.0, 0.0,


            -0.25, -0.25, -0.25,   1.0, 1.0, 1.0,     0.0,0.0,   0.0, -1.0, 0.0,
            -0.25, -0.25,  0.25,   1.0, 1.0, 1.0,     1.0,0.0,   0.0, -1.0, 0.0,
             0.25, -0.25,  0.25,   1.0, 1.0, 1.0,     1.0,1.0,   0.0, -1.0, 0.0,
            
             0.25, -0.25,  0.25,   1.0, 1.0, 1.0,     1.0,1.0,   0.0, -1.0, 0.0,
            -0.25, -0.25, -0.25,   1.0, 1.0, 1.0,     0.0,0.0,   0.0, -1.0, 0.0,
             0.25, -0.25, -0.25,   1.0, 1.0, 1.0,     0.0,1.0,   0.0, -1.0, 0.0,



            -0.25,  0.25,  0.25,   1.0, 1.0, 1.0,     0.0,1.0,   -1.0, 0.0, 0.0,
            -0.25, -0.25,  0.25,   1.0, 1.0, 1.0,     0.0,0.0,   -1.0, 0.0, 0.0,
            -0.25, -0.25, -0.25,   1.0, 1.0, 1.0,     1.0,0.0,   -1.0, 0.0, 0.0,

            -0.25,  0.25,  0.25,   1.0, 1.0, 1.0,     0.0,1.0,   -1.0, 0.0, 0.0,
            -0.25,  0.25, -0.25,   1.0, 1.0, 1.0,     1.0,1.0,   -1.0, 0.0, 0.0,
            -0.25, -0.25, -0.25,   1.0, 1.0, 1.0,     1.0,0.0,   -1.0, 0.0, 0.0,


             0.25,  0.25,  0.25,   1.0, 1.0, 1.0,     0.0,1.0,   1.0, 0.0, 0.0,
             0.25, -0.25,  0.25,   1.0, 1.0, 1.0,     0.0,0.0,   1.0, 0.0, 0.0,
             0.25, -0.25, -0.25,   1.0, 1.0, 1.0,     1.0,0.0,   1.0, 0.0, 0.0,

             0.25,  0.25,  0.25,   1.0, 1.0, 1.0,     0.0,1.0,   1.0, 0.0, 0.0,
             0.25,  0.25, -0.25,   1.0, 1.0, 1.0,     1.0,1.0,   1.0, 0.0, 0.0,
             0.25, -0.25, -0.25,   1.0, 1.0, 1.0,     1.0,0.0,   1.0, 0.0, 0.0,
        ], np.float32)

        self.indices = np.array([
            0,  1 , 2 ,
            3,  4 , 5 ,
            6,  7 , 8 ,
            9,  10, 11,
            12, 13, 14,
            15, 16, 17,
            18, 19, 20,
            21, 22, 23,
            24, 25, 26,
            27, 28, 29,
            30, 31, 32,
            33, 34, 35
        ], np.int32)
        self.vertNum = 36

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


        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, (3+3+2+3) * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, (3+3+2+3) * 4, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, (3+3+2+3) * 4, ctypes.c_void_p(24))
        glEnableVertexAttribArray(2)

        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, (3+3+2+3) * 4, ctypes.c_void_p(32))
        glEnableVertexAttribArray(3)

        # Unbind VBO and VAO
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    # Function to render the mesh
    def render(self):
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, self.vertNum, GL_UNSIGNED_INT, None)

    # Function to clean up and delete OpenGL objects
    def terminate(self):
        glDeleteVertexArrays(1, (self.VAO,))
        glDeleteBuffers(1, (self.VBO,))