from OpenGL.GL import *
import numpy
import Image
from struct import pack


class Texture:

    def __init__(self, style=GL_REPLACE):
        self.name = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.name)
        self.style = style
        self.create_texture()


    def __del__(self):
        """A descructor that makes sure we release the textures back to the wild and free their memory."""
        glDeleteTextures(self.name)


    def set(self):
        """This function should be called by the external source to 'switch on' this texture."""
        glDisable(GL_TEXTURE_1D)
        glEnable(GL_TEXTURE_2D)

        glBindTexture(GL_TEXTURE_2D, self.name)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, self.style)
        return

    def create_texture(self):
        pass


class Checker(Texture):
    """This is a texture class that displays a simple self generated checkboard."""
    def __init__(self, style=GL_MODULATE):
        Texture.__init__(self, style=style)

    def create_texture(self):
        self.data = numpy.zeros((64,64,4),'b')
        for i in range(64):
            for j in range(64):
                c = (((i & 0x8)== 0) ^ ((j & 0x8)==0)) * 255
                for k in range(3):
                    self.data[i][j][k] = c
                self.data[i][j][3] = 128
        glTexImage2Dub(GL_TEXTURE_2D, 0, GL_RGBA, 0, GL_RGBA,  self.data)



class Decal(Texture):
    """This texture is designed for loading images. By default, it uses the default style of application, but it can be modified."""
    def __init__(self, filename, style=GL_REPLACE):
        self.filename = filename
        Texture.__init__(self, style=style)


    def create_texture(self):
        image = Image.open(self.filename)
        (ix, iy) = image.size
        data = image.tostring("raw","RGBX")

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)


class Texture1D:

    def __init__(self, style=GL_REPLACE):
        self.name = glGenTextures(1)
        glBindTexture(GL_TEXTURE_1D, self.name)
        self.style = style
        self.create_texture()


    def __del__(self):
        """A descructor that makes sure we release the textures back to the wild and free their memory."""
        glDeleteTextures(self.name)


    def set(self):
        """This function should be called by the external source to 'switch on' this texture."""
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_TEXTURE_1D)
        glBindTexture(GL_TEXTURE_1D, self.name)
        glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, self.style)
        return

    def create_texture(self):

        self.data = ''
        for i in range(64):
            self.data += pack("B",255 * (i /64.))
            self.data += '\x00'
            self.data += pack("B",255 * (1 - i/64. ))
            self.data += '\xff'

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage1D(GL_TEXTURE_1D, 0, GL_RGBA,64, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.data)
        pass