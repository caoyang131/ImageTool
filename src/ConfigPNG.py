# ConfigPNG Ver1.00

#=========================================#
import os,struct,codecs
#=========================================
# Config Image TypeA(CG)
#=========================================
class ImageTypeA():
    
    def FolderConfig(self):
        
        srcfolder = 'src\\Index4\\'
        pngfolder = 'png\\Index4\\'
        srctype = '*'
        pictype = 'png'
        
        return srcfolder,pngfolder,srctype,pictype
    #=========================================
    def CheckPic(self,src):
        
        BmpValue = 1
        
        return BmpValue
    #=========================================
    def ConfigA(self,src,filesize):
        
        # (Tilew,Tileh) = [(Width,1):None,(8,8):OtherMode,(4,8):RGBA8888,(32,8):Index4,(16,8):Index8]
        
        Width = 1024
        Height = 1024
        (Tilew,Tileh) = (Width,1)
        
        return Width,Height,Tilew,Tileh
    #=========================================
    def ConfigB(self,src):
        PalOffset = 0
        PalSize = 0x40
        DatOffset = 0x40
        return DatOffset,PalOffset,PalSize
    #=========================================
    def ConfigC(self,src):
        '''
        PalValue = [-1:None,0:RGBA5650,1:RGBA5551,2:RGBA4444,3:RGBA8888,4:RGBATim2]
        PicValue = [-1:None,
                    0:RGBA5650,1:RGBA5551,2:RGBA4444,3:RGBA8888,
                    4:Index4,5:Index8,6:Index16,7:Index32,
                    8:DXT1,9:DXT3,10:DXT5,
                    264:DXT1Ext,265:DXT3Ext,266:DXT5Ext]
        Option = [0:None,1:TOP_BOTTOM,2:???]
        '''
        PicType = 'Index4'
        PalType = 'RGBA8888'
        PalRGBA = ('>','rgba')
        PicRGBA = ('>','rgba')
        Option = 0
        inputIsSwizzled = 1
        
        return PicType,PalType,PicRGBA,PalRGBA,Option,inputIsSwizzled
#=========================================
# Config Image TypeB(FONT)
#=========================================
class ImageTypeB():
    
    def FolderConfig(self):
        
        srcfolder = 'src\\RGBA8888\\'
        pngfolder = 'png\\RGBA8888\\'
        srctype = '*'
        pictype = 'png'
        
        return srcfolder,pngfolder,srctype,pictype
    #=========================================
    def CheckPic(self,src):
        
        BmpValue = 1
        
        return BmpValue
    #=========================================
    def ConfigA(self,src,filesize):
        
        # (Tilew,Tileh) = [(Width,1):None,(8,8):OtherMode,(4,8):RGBA8888,(32,8):Index4,(16,8):Index8]
        src.seek(0x8+0xC)
        Width, = struct.unpack('<I',src.read(4))
        Height, = struct.unpack('<I',src.read(4))
        (Tilew,Tileh) = (Width,1)
        
        return Width,Height,Tilew,Tileh
    #=========================================
    def ConfigB(self,src):
        
        PalOffset = 0
        PalSize = 0
        DatOffset = 0x10+0xC
        
        return DatOffset,PalOffset,PalSize
    #=========================================
    def ConfigC(self,src):
        '''
        PalValue = [-1:None,0:RGBA5650,1:RGBA5551,2:RGBA4444,3:RGBA8888,4:RGBATim2]
        PicValue = [-1:None,
                    0:RGBA5650,1:RGBA5551,2:RGBA4444,3:RGBA8888,
                    4:Index4,5:Index8,6:Index16,7:Index32,
                    8:DXT1,9:DXT3,10:DXT5,
                    264:DXT1Ext,265:DXT3Ext,266:DXT5Ext]
        Option = [0:None,1:TOP_BOTTOM,2:???]
        '''
        PicType = 'RGBA8888'
        PalType = 'None'
        PalRGBA = ('>','rgba')
        PicRGBA = ('>','rgba')
        Option = 0,
        inputIsSwizzled = 0
        
        return PicType,PalType,PicRGBA,PalRGBA,Option,inputIsSwizzled
#=========================================
# ConfigPNG End
#=========================================
class ImageTypeC():
    
    def FolderConfig(self):
        
        srcfolder = 'src\\Index8\\'
        pngfolder = 'png\\Index8\\'
        srctype = '*'
        pictype = 'png'
        
        return srcfolder,pngfolder,srctype,pictype
    #=========================================
    def CheckPic(self,src):
        
        BmpValue = 1
        
        return BmpValue
    #=========================================
    def ConfigA(self,src,filesize):
        
        # (Tilew,Tileh) = [(Width,1):None,(8,8):OtherMode,(4,8):RGBA8888,(32,8):Index4,(16,8):Index8]
        idstring = src.read(8)
        
        if(idstring==b'Texture '):
            src.seek(0x8+0xC)
        else:
            src.seek(0x8)
            
        Width, = struct.unpack('<I',src.read(4))
        Height, = struct.unpack('<I',src.read(4))
        (Tilew,Tileh) = (Width,1)
        
        return Width,Height,Tilew,Tileh
    #=========================================
    def ConfigB(self,src):
        src.seek(0x4+0xC)
        PalOffset, = struct.unpack('<I',src.read(4))
        PalSize = 0x400
        DatOffset = 0x10+0xC
        PalOffset -= PalSize
        PalOffset += DatOffset
        
        return DatOffset,PalOffset,PalSize
    #=========================================
    def ConfigC(self,src):
        '''
        PalValue = [-1:None,0:RGBA5650,1:RGBA5551,2:RGBA4444,3:RGBA8888,4:RGBATim2]
        PicValue = [-1:None,
                    0:RGBA5650,1:RGBA5551,2:RGBA4444,3:RGBA8888,
                    4:Index4,5:Index8,6:Index16,7:Index32,
                    8:DXT1,9:DXT3,10:DXT5,
                    264:DXT1Ext,265:DXT3Ext,266:DXT5Ext]
        Option = [0:None,1:TOP_BOTTOM,2:???]
        '''
        PicType = 'Index8'
        PalType = 'RGBA8888'
        PalRGBA = ('>','rgba')
        PicRGBA = ('>','rgba')
        Option = 0
        inputIsSwizzled = 0        
        return PicType,PalType,PicRGBA,PalRGBA,Option,inputIsSwizzled
