#=========================================#
# ImageConv Ver 1.00
#=========================================#
import io,os,struct
from math import sqrt,log
from PIL import Image # Version >= 2.6.1
from Swizzle import *
#=========================================#
# ImageLibs Ver 1.30
# 
# 1:Add Option to control transposion.
# 2:Set Endian Format ('>','rgba')
# 3:Add NewIndex8 Mode (Experimental)
# 4:Add Index2 Mode (Experimental)
#
#=========================================#
#
#=========================================#
class GetPalMode():
    
    def RGBA5650(self,P,Q,RGBA):
        L = (P&0x1f) << 3
        M = (Q&0x07) << 5 | (P&0xe0) >> 3
        N = (Q&0xf8)
        O = 0xff
        
        Dict = dict()
        for i in range(4):
            Dict[RGBA[i]] = [L,M,N,O][i]
        return (Dict['r'],Dict['g'],Dict['b'],Dict['a'])
        
    def RGBA5551(self,P,Q,RGBA):
        L = (P&0x1f) << 3
        M = (Q&0x03) << 6 | (P&0xe0) >> 2
        N = (Q&0x7c) << 1
        O = (Q&0x80) if 0xff else 0
        
        Dict = dict()
        for i in range(4):
            Dict[RGBA[i]] = [L,M,N,O][i]
        return (Dict['r'],Dict['g'],Dict['b'],Dict['a'])
        
    def RGBA4444(self,P,Q,RGBA):
        L = (P&0x0f) << 4
        M = (P&0xf0)
        N = (Q&0x0f) << 4
        O = (Q&0xf0)
        
        Dict = dict()
        for i in range(4):
            Dict[RGBA[i]] = [L,M,N,O][i]
        return (Dict['r'],Dict['g'],Dict['b'],Dict['a'])
        
    def RGBA8888(self,P,Q,R,S,RGBA):
        L = P
        M = Q
        N = R
        O = S
        
        Dict = dict()
        for i in range(4):
            Dict[RGBA[i]] = [L,M,N,O][i]
        return (Dict['r'],Dict['g'],Dict['b'],Dict['a'])
        
    def DXT(self,P): # RGBA5650
        r = ((P >> 0xB)&0x1f) << 3
        g = ((P >> 0x5)&0x3f) << 2
        b = ((P >> 0x0)&0x1f) << 3
        a = 0xff
        return (r,g,b,a)
#=========================================#
class GetPicMode():
    
    def RGBA5650(self,r,g,b,a=0xff):
        P = (r >> 3) | ((g << 3)&0xe0)
        Q = ((g >> 5)&0x07) | (b&0xf8)
        return P,Q
        
    def RGBA5551(self,r,g,b,a):
        P = (r >> 3) | ((g << 2)&0xe0)
        Q = ((g >> 6)&0x03) | ((b >> 1)&0x7c) | (a&0xff)
        return P,Q
        
    def RGBA4444(self,r,g,b,a):
        P = (r >> 4) | (g&0xf0)
        Q = (b >> 4) | (a&0xf0)
        return P,Q
        
    def RGBA8888(self,r,g,b,a):
        P = r
        Q = g
        R = b
        S = a
        return P,Q,R,S
#=========================================#
def GetPicDat(src,PicType,DatOffset,Width,Height):
    
    PicDat = io.BytesIO()
    src.seek(DatOffset)
    
    if PicType == 'Index8':
        PicDat.write(src.read(Width*Height))
    elif PicType == 'RGBA8888':
        PicDat.write(src.read(Width*Height*4))
    else:
        PicDat.write(src.read(Width*Height*2))
        
    PicDat.seek(0)
    return PicDat
#=========================================#
def GetPicPal(src,PalType,PalOffset,PalSize,PalRGBA):
    
    if PalType != None:
        (Null,RGBA) = PalRGBA
        
        PalDat = io.BytesIO()
        PicPal = []
        PalMode = GetPalMode()
        
        src.seek(PalOffset)
        PalDat.write(src.read(PalSize))
        PalDat.seek(0)
        
        if PalType == 'RGBA8888':
            for i in range(0,PalSize,4):
                if Null == '>':
                    P,Q,R,S = struct.unpack('>4B',PalDat.read(4))
                else:
                    S,R,Q,P = struct.unpack('>4B',PalDat.read(4))
                PicPal.append(PalMode.RGBA8888(P,Q,R,S,RGBA))
        elif PalType == 'RGBATim2':#Index8 Tim2
            for h in range(0,PalSize//0x80,1):
                for i in range(2):
                    for j in range(2):
                        PalDat.seek(h*0x80+(i+j*2)*0x20)
                        for k in range(8):
                            if Null == '>':
                                P,Q,R,S = struct.unpack('>4B',PalDat.read(4))
                            else:
                                S,R,Q,P = struct.unpack('>4B',PalDat.read(4))
                            PicPal.append(PalMode.RGBA8888(P,Q,R,S,RGBA))
        elif PalType == 'RGBA4444':
            for i in range(0,PalSize,2):
                if Null == '>':
                    P,Q = struct.unpack('>2B',PalDat.read(2))
                else:
                    Q,P = struct.unpack('>2B',PalDat.read(2))
                PicPal.append(PalMode.RGBA4444(P,Q,RGBA))
        elif PalType == 'RGBA5551':
            for i in range(0,PalSize,2):
                if Null == '>':
                    P,Q = struct.unpack('>2B',PalDat.read(2))
                else:
                    Q,P = struct.unpack('>2B',PalDat.read(2))
                PicPal.append(PalMode.RGBA5551(P,Q,RGBA))
        elif PalType == 'RGBA5650':
            for i in range(0,PalSize,2):
                if Null == '>':
                    P,Q = struct.unpack('>2B',PalDat.read(2))
                else:
                    Q,P = struct.unpack('>2B',PalDat.read(2))
                PicPal.append(PalMode.RGBA5650(P,Q,RGBA))
        
        return PicPal
    else:
        return None
#=========================================#
# ExportPNG Ver 1.00
#=========================================#
def ImgExport(src,PicDat,outputname,PicType,Tilew,Tileh,Width,Height,PicRGBA,Option,PicPal,inputIsSwizzled):
    
    Export = ExportPic()
    ExportDxt = ExportDDS()

    if PicType == 'Index2':
        dest = Export.Index2(PicDat,Tilew,Tileh,Width,Height,PicPal,PicRGBA=None)
    elif PicType == 'Index4':
        dest = Export.Index4(PicDat,Tilew,Tileh,Width,Height,PicPal,PicRGBA=None)
    elif PicType in ['Index8','NewIndex8']:
        dest = Export.Index8(PicDat,Tilew,Tileh,Width,Height,PicPal,PicRGBA=None)
    elif PicType == 'RGBA5650':
        dest = Export.RGBA5650(PicDat,Tilew,Tileh,Width,Height,PicRGBA,PicPal=None)
    elif PicType == 'RGBA5551':
        dest = Export.RGBA5551(PicDat,Tilew,Tileh,Width,Height,PicRGBA,PicPal=None)
    elif PicType == 'RGBA4444':
        dest = Export.RGBA4444(PicDat,Tilew,Tileh,Width,Height,PicRGBA,PicPal=None)
    elif PicType == 'RGBA8888':
        dest = Export.RGBA8888(PicDat,Tilew,Tileh,Width,Height,PicRGBA,PicPal=None)
    elif PicType in ['DXT1','DXT1EXT']:
        dest = ExportDxt.DXT1(PicDat,Tilew,Tileh,Width,Height,PicType,PicRGBA,PicPal=None)
    elif PicType in ['DXT3','DXT3EXT']:
        dest = ExportDxt.DXT3(PicDat,Tilew,Tileh,Width,Height,PicType,PicRGBA,PicPal=None)
    elif PicType in ['DXT5','DXT5EXT']:
        dest = ExportDxt.DXT5(PicDat,Tilew,Tileh,Width,Height,PicType,PicRGBA,PicPal=None)
        
    im = Image.new('RGBA',(Width,Height))

    # TODO:Add Swizzle
    if(inputIsSwizzled):
        maskMutex = swizzle(Width,Height)
        tmp_desc = convert(dest[:Width*Height],maskMutex,False)
        im.putdata(tuple(tmp_desc))
    else:
        im.putdata(dest[:Width*Height])
    
    if Option == 1:
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
        
    im.save(outputname)
#=========================================#
class ExportPic():

    def Index2(self,PicDat,Tilew,Tileh,Width,Height,PicPal,PicRGBA=None):

        dest = [(0,0,0,0)]*(Width*Height*4)
        basex = 0
        
        for Y in range(0,Height,Tileh):
            for X in range(0,Width,Tilew):
                basey = 0
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,4):
                        P, = struct.unpack('>B',PicDat.read(1))
                        dest[basex+basey+x+0] = PicPal[(P&0x03) >> 0]
                        dest[basex+basey+x+1] = PicPal[(P&0x0C) >> 2]
                        dest[basex+basey+x+2] = PicPal[(P&0x30) >> 4]
                        dest[basex+basey+x+3] = PicPal[(P&0xC0) >> 6]
                    basey += Width
                basex += Tilew
            basex += Width*(Tileh-1)
            
        return dest
    #=========================================#
    def Index4(self,PicDat,Tilew,Tileh,Width,Height,PicPal,PicRGBA=None):
        
        dest = [(0,0,0,0)]*(Width*Height*2)
        basex = 0
        
        for Y in range(0,Height,Tileh):
            for X in range(0,Width,Tilew):
                basey = 0
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,2):
                        P, = struct.unpack('>B',PicDat.read(1))
                        dest[basex+basey+x+0] = PicPal[(P&0x0f) >> 0]
                        dest[basex+basey+x+1] = PicPal[(P&0xf0) >> 4]
                    basey += Width
                basex += Tilew
            basex += Width*(Tileh-1)
            
        return dest
    #=========================================#
    def Index8(self,PicDat,Tilew,Tileh,Width,Height,PicPal,PicRGBA=None):
        
        dest = [(0,0,0,0)]*(Width*Height)
        basex = 0
        
        for Y in range(0,Height,Tileh):
            for X in range(0,Width,Tilew):
                basey = 0
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,1):
                        P, = struct.unpack('>B',PicDat.read(1))
                        dest[basex+basey+x] = PicPal[P]
                    basey += Width
                basex += Tilew
            basex += Width*(Tileh-1)
            
        return dest
    #=========================================#
    def RGBA5650(self,PicDat,Tilew,Tileh,Width,Height,PicRGBA,PicPal=None):
        
        dest = [(0,0,0,0)]*(Width*Height)
        basex = 0
        PalMode = GetPalMode()
        
        (Null,RGBA) = PicRGBA # ('>','rgba')
        
        for Y in range(0,Height,Tileh):
            for X in range(0,Width,Tilew):
                basey = 0
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,1):
                        
                        if Null == '>':
                            P,Q = struct.unpack('>2B',PicDat.read(2))
                        else:
                            Q,P = struct.unpack('>2B',PicDat.read(2))
                       
                        dest[basex+basey+x] = PalMode.RGBA5650(P,Q,RGBA)
                    basey += Width
                basex += Tilew
            basex += Width*(Tileh-1)
            
        return dest
    #=========================================#
    def RGBA5551(self,PicDat,Tilew,Tileh,Width,Height,PicRGBA,PicPal=None):
        
        dest = [(0,0,0,0)]*(Width*Height)
        basex = 0
        PalMode = GetPalMode()
        
        (Null,RGBA) = PicRGBA # ('>','rgba')
        
        for Y in range(0,Height,Tileh):
            for X in range(0,Width,Tilew):
                basey = 0
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,1):
                        
                        if Null == '>':
                            P,Q = struct.unpack('>2B',PicDat.read(2))
                        else:
                            Q,P = struct.unpack('>2B',PicDat.read(2))
                        
                        dest[basex+basey+x] = PalMode.RGBA5551(P,Q,RGBA)
                    basey += Width
                basex += Tilew
            basex += Width*(Tileh-1)
            
        return dest
    #=========================================#
    def RGBA4444(self,PicDat,Tilew,Tileh,Width,Height,PicRGBA,PicPal=None):
        
        dest = [(0,0,0,0)]*(Width*Height)
        basex = 0
        PalMode = GetPalMode()
        
        (Null,RGBA) = PicRGBA # ('>','rgba')
        
        for Y in range(0,Height,Tileh):
            for X in range(0,Width,Tilew):
                basey = 0
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,1):
                        
                        if Null == '>':
                            P,Q = struct.unpack('>2B',PicDat.read(2))
                        else:
                            Q,P = struct.unpack('>2B',PicDat.read(2))
                
                        dest[basex+basey+x] = PalMode.RGBA4444(P,Q,RGBA)
                    basey += Width
                basex += Tilew
            basex += Width*(Tileh-1)
            
        return dest
    #=========================================#
    def RGBA8888(self,PicDat,Tilew,Tileh,Width,Height,PicRGBA,PicPal=None):
        
        dest = [(0,0,0,0)]*(Width*Height)
        basex = 0
        PalMode = GetPalMode()
        
        (Null,RGBA) = PicRGBA # ('>','rgba')
        
        for Y in range(0,Height,Tileh):
            for X in range(0,Width,Tilew):
                basey = 0
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,1):
                        
                        if Null == '>':
                            P,Q,R,S = struct.unpack('>4B',PicDat.read(4))
                        else:
                            S,R,Q,P = struct.unpack('>4B',PicDat.read(4))
                            
                        dest[basex+basey+x] = PalMode.RGBA8888(P,Q,R,S,RGBA)
                    basey += Width
                basex += Tilew
            basex += Width*(Tileh-1)
            
        return dest
#=========================================#
# ImportPNG Ver 1.00
#=========================================#
def ImgImport(src,PicDat,PalOffset,DatOffset,PicType,Tilew,Tileh,Width,Height,PicRGBA,Option,PicPal,inputIsSwizzled):
    
    Import = ImportPic()
    ImportDxt = ImportDDS()
    ImgDat = Image.open(PicDat).convert('RGBA')


    im = Image.new('RGBA',(Width,Height))

    # TODO:Add Swizzle
    if(inputIsSwizzled):
        maskMutex = swizzle(Width,Height)
        tmp_desc = convert(ImgDat.getdata(),maskMutex,True)
        ImgDat = im.putdata(tuple(tmp_desc))
    else:
        pass
    
    if Option == 1:
        ImgDat = ImgDat.transpose(Image.FLIP_TOP_BOTTOM)

    if PicType == 'Index2':
        file = Import.Index2(ImgDat,Tilew,Tileh,Width,Height,PicPal,PicRGBA=None)    
    elif PicType == 'Index4':
        file = Import.Index4(ImgDat,Tilew,Tileh,Width,Height,PicPal,PicRGBA=None)
    elif PicType == 'Index8':
        file = Import.Index8(ImgDat,Tilew,Tileh,Width,Height,PicPal,PicRGBA=None)
    elif PicType == 'RGBA5650':
        file = Import.RGBA5650(ImgDat,Tilew,Tileh,Width,Height,PicRGBA,PicPal=None)
    elif PicType == 'RGBA5551':
        file = Import.RGBA5551(ImgDat,Tilew,Tileh,Width,Height,PicRGBA,PicPal=None)
    elif PicType == 'RGBA4444':
        file = Import.RGBA4444(ImgDat,Tilew,Tileh,Width,Height,PicRGBA,PicPal=None)
    elif PicType == 'RGBA8888':
        file = Import.RGBA8888(ImgDat,Tilew,Tileh,Width,Height,PicRGBA,PicPal=None)
    elif PicType in ['DXT1','DXT1EXT']:
        file = ImportDxt.DXT1(ImgDat,Tilew,Tileh,Width,Height,PicType,PicRGBA,PicPal=None)
    elif PicType in ['DXT3','DXT3EXT']:
        file = ImportDxt.DXT3(ImgDat,Tilew,Tileh,Width,Height,PicType,PicRGBA,PicPal=None)
    elif PicType in ['DXT5','DXT5EXT']:
        file = ImportDxt.DXT5(ImgDat,Tilew,Tileh,Width,Height,PicType,PicRGBA,PicPal=None)
    elif PicType == 'NewIndex8':
        file,NewPal = Import.NewIndex8(ImgDat,Tilew,Tileh,Width,Height,PicPal,PicRGBA=None)
        src.seek(PalOffset)
        src.write(NewPal.getvalue())

    src.seek(DatOffset)
    src.write(file.getvalue())
#=========================================#
class ImportPic():

    def Index2(self,ImgDat,Tilew,Tileh,Width,Height,PicPal,PicRGBA=None):

        im = ImgDat
        file = io.BytesIO()
        PalDict = {};PalList = []
        NewDict = {};NewList = []
        AlphaDict = {};AlphaList = []
        
        for n in range(0,len(PicPal),1):
            PalDict[PicPal[n]] = n
            PalList.append(PicPal[n])
            if PicPal[n][3] == 0:
                AlphaDict[PicPal[n]] = n
                AlphaList.append(PicPal[n])
                
        NewAlphaDict = sorted(AlphaDict.items(),key = lambda asd:asd[0])
        
        for Y in range(0,Height//Tileh,1):
            for X in range(0,Width//Tilew,1):
                im2 = im.crop(((X*Tilew),(Y*Tileh),((X+1)*Tilew),((Y+1)*Tileh)))

                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,4):
                        im3 = im2.crop((x,y,x+4,y+1))
                        pal1 = list(im3.getdata())[0]
                        pal2 = list(im3.getdata())[1]
                        pal3 = list(im3.getdata())[2]
                        pal4 = list(im3.getdata())[3]

                        if pal1 in PalDict and pal2 in PalDict and pal3 in PalDict and pal4 in PalDict:
                            file.write(struct.pack('>B',
                                                   ((PalDict[pal4] << 6) & 0xC0) |
                                                   ((PalDict[pal3] << 4) & 0x30) |
                                                   ((PalDict[pal2] << 2) & 0x0C) |
                                                   ((PalDict[pal1] << 0) & 0x03)))
                        else:
                            TmpDict1 = {}
                            TmpDict2 = {}
                            TmpDict3 = {}
                            TmpDict4 = {}
                            
                            if pal1[3] == 0:
                                pal1 = NewAlphaDict[0][0]
                            
                            if pal2[3] == 0:
                                pal2 = NewAlphaDict[0][0]

                            if pal3[3] == 0:
                                pal3 = NewAlphaDict[0][0]
                            
                            if pal4[3] == 0:
                                pal4 = NewAlphaDict[0][0]

                            for n in range(0,len(PicPal),1):
                                value1 = 0
                                value2 = 0
                                value3 = 0
                                value4 = 0
                                
                                for p in range(0,3,1):
                                    V1 = PicPal[n][p] - pal1[p]
                                    V2 = PicPal[n][p] - pal2[p]
                                    V3 = PicPal[n][p] - pal3[p]
                                    V4 = PicPal[n][p] - pal4[p]
                                    value1 += V1*V1
                                    value2 += V2*V2
                                    value3 += V3*V3
                                    value4 += V4*V4
                                
                                TmpDict1[(abs(sqrt(value1)),abs(PicPal[n][3] - pal1[3]))] = n
                                TmpDict2[(abs(sqrt(value2)),abs(PicPal[n][3] - pal2[3]))] = n
                                TmpDict3[(abs(sqrt(value3)),abs(PicPal[n][3] - pal3[3]))] = n
                                TmpDict4[(abs(sqrt(value4)),abs(PicPal[n][3] - pal4[3]))] = n

                            NewTmpDict1 = sorted(TmpDict1.items(),key = lambda asd:asd[0])
                            NewTmpDict2 = sorted(TmpDict2.items(),key = lambda asd:asd[0])
                            NewTmpDict3 = sorted(TmpDict3.items(),key = lambda asd:asd[0])
                            NewTmpDict4 = sorted(TmpDict4.items(),key = lambda asd:asd[0])
                            file.write(struct.pack('>B',((NewTmpDict4[0][1] << 6) & 0xC0) |
                                                        ((NewTmpDict3[0][1] << 4) & 0x30) |
                                                        ((NewTmpDict2[0][1] << 2) & 0x0C) |
                                                        ((NewTmpDict1[0][1] << 0) & 0x03)))
                            
                                 
                            

        return file
    #=========================================#
    def Index4(self,ImgDat,Tilew,Tileh,Width,Height,PicPal,PicRGBA=None):
        
        im = ImgDat
        file = io.BytesIO()
        PalDict = {};PalList = []
        NewDict = {};NewList = []
        AlphaDict = {};AlphaList = []
        
        for n in range(0,len(PicPal),1):
            PalDict[PicPal[n]] = n
            PalList.append(PicPal[n])
            if PicPal[n][3] < 0x10:
                AlphaDict[PicPal[n]] = n
                AlphaList.append(PicPal[n])
                
        NewAlphaDict = sorted(AlphaDict.items(),key = lambda asd:asd[0])
        
        for Y in range(0,Height//Tileh,1):
            for X in range(0,Width//Tilew,1):
                im2 = im.crop(((X*Tilew),(Y*Tileh),((X+1)*Tilew),((Y+1)*Tileh)))
                
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,2):
                        im3 = im2.crop((x,y,x+2,y+1))
                        pal1 = list(im3.getdata())[0]
                        pal2 = list(im3.getdata())[1]
                        
                        if pal1 in PalDict and pal2 in PalDict:
                            file.write(struct.pack('>B',(PalDict[pal2] << 4) |
                                                        (PalDict[pal1]&0x0f)))
                        else:
                            TmpDict1 = {}
                            TmpDict2 = {}
                            
                            if pal1[3] < 0x10:
                                pal1 = NewAlphaDict[0][0]
                            
                            if pal2[3] < 0x10:
                                pal2 = NewAlphaDict[0][0]
                            
                            for n in range(0,len(PicPal),1):
                                value1 = 0
                                value2 = 0
                                
                                for p in range(0,3,1):
                                    V1 = PicPal[n][p] - pal1[p]
                                    V2 = PicPal[n][p] - pal2[p]
                                    value1 += V1*V1
                                    value2 += V2*V2
                                
                                TmpDict1[(abs(sqrt(value1)),abs(PicPal[n][3] - pal1[3]))] = n
                                TmpDict2[(abs(sqrt(value2)),abs(PicPal[n][3] - pal2[3]))] = n
                                
                            NewTmpDict1 = sorted(TmpDict1.items(),key = lambda asd:asd[0])
                            NewTmpDict2 = sorted(TmpDict2.items(),key = lambda asd:asd[0])
                            file.write(struct.pack('>B',(NewTmpDict2[0][1] << 4) |
                                                        (NewTmpDict1[0][1]&0x0f)))
                            
        return file
    #=========================================#
    def Index8(self,ImgDat,Tilew,Tileh,Width,Height,PicPal,PicRGBA=None):
        
        im = ImgDat
        file = io.BytesIO()
        PalDict = {};PalList = []
        NewDict = {};NewList = []
        AlphaDict = {};AlphaList = []
        
        for n in range(0,len(PicPal),1):
            PalDict[PicPal[n]] = n
            PalList.append(PicPal[n])
            if PicPal[n][3] == 0:
                AlphaDict[PicPal[n]] = n
                AlphaList.append(PicPal[n])
                
        NewAlphaDict = sorted(AlphaDict.items(),key = lambda asd:asd[0])
        
        for Y in range(0,Height//Tileh,1):
            for X in range(0,Width//Tilew,1):
                im2 = im.crop(((X*Tilew),(Y*Tileh),((X+1)*Tilew),((Y+1)*Tileh)))
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,1):
                        im3 = im2.crop((x,y,x+1,y+1))
                        pal = list(im3.getdata())[0]
                        
                        if pal in PalList:
                            file.write(struct.pack('>B',PalDict[pal]))
                        else:
                            TmpDict = {}
                            
                            if pal in NewList:
                                file.write(struct.pack('>B',NewDict[pal]))
                            else:
                                if pal[3] == 0:
                                    file.write(struct.pack('>B',NewAlphaDict[0][1]))
                                    NewDict[pal] = NewAlphaDict[0][1]
                                    NewList.append(pal)
                                else:
                                    for n in range(0,len(PicPal),1):
                                        value = 0
                                        
                                        for p in range(0,3,1):
                                            V = PicPal[n][p] - pal[p]
                                            value += V*V
                                            
                                        TmpDict[(abs(sqrt(value)),abs(PicPal[n][3] - pal[3]))] = n
                                        
                                    NewTmpDict = sorted(TmpDict.items(),key = lambda asd:asd[0])
                                    file.write(struct.pack('>B',NewTmpDict[0][1]))
                                    NewDict[pal] = NewTmpDict[0][1]
                                    NewList.append(pal)
                                    
        return file
    #=========================================#
    def NewIndex8(self,ImgDat,Tilew,Tileh,Width,Height,PicPal,PicRGBA=None):
        
        im = ImgDat
        file = io.BytesIO()
        NewPal = io.BytesIO()
        PalList = []
        
        im = im.convert('P',palette=Image.ADAPTIVE)
        im = im.convert('RGBA')
        
        for Y in range(0,Height//Tileh,1):
            for X in range(0,Width//Tilew,1):
                im2 = im.crop(((X*Tilew),(Y*Tileh),((X+1)*Tilew),((Y+1)*Tileh)))
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,1):
                        im3 = im2.crop((x,y,x+1,y+1))
                        pal = list(im3.getdata())[0]

                        if pal not in PalList:
                            PalList.append(pal)
                            (r,g,b,a) = pal
                            NewPal.write(struct.pack('4B',r,g,b,a))
                        
                        file.write(struct.pack('>B',PalList.index(pal)))
                        
        return file,NewPal
    #=========================================#
    def RGBA5650(self,ImgDat,Tilew,Tileh,Width,Height,PicRGBA,PicPal=None):
        
        im = ImgDat
        file = io.BytesIO()
        PicMode = GetPicMode()
        
        (Null,RGBA) = PicRGBA # ('>','rgba')
        
        for Y in range(0,Height//Tileh,1):
            for X in range(0,Width//Tilew,1):
                im2 = im.crop(((X*Tilew),(Y*Tileh),((X+1)*Tilew),((Y+1)*Tileh)))
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,1):
                        im3 = im2.crop((x,y,x+1,y+1))
                        (r,g,b,a) = list(im3.getdata())[0]
                        
                        if Null == '>':
                            P,Q = PicMode.RGBA5650(r,g,b,a)
                        else:
                            Q,P = PicMode.RGBA5650(b,g,r,a)
                            
                        file.write(struct.pack('>2B',P,Q))
                        
        return file
    #=========================================#
    def RGBA5551(self,ImgDat,Tilew,Tileh,Width,Height,PicRGBA,PicPal=None):
        
        im = ImgDat
        file = io.BytesIO()
        PicMode = GetPicMode()
        
        (Null,RGBA) = PicRGBA # ('>','rgba')
        
        for Y in range(0,Height//Tileh,1):
            for X in range(0,Width//Tilew,1):
                im2 = im.crop(((X*Tilew),(Y*Tileh),((X+1)*Tilew),((Y+1)*Tileh)))
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,1):
                        im3 = im2.crop((x,y,x+1,y+1))
                        (r,g,b,a) = list(im3.getdata())[0]
                        
                        if Null == '>':
                            P,Q = PicMode.RGBA5551(r,g,b,a)
                        else:
                            Q,P = PicMode.RGBA5551(b,g,r,a)
                            
                        file.write(struct.pack('>2B',P,Q))
                    
        return file
    #=========================================#
    def RGBA4444(self,ImgDat,Tilew,Tileh,Width,Height,PicRGBA,PicPal=None):
        
        im = ImgDat
        file = io.BytesIO()
        PicMode = GetPicMode()
        
        (Null,RGBA) = PicRGBA # ('>','rgba')
        
        for Y in range(0,Height//Tileh,1):
            for X in range(0,Width//Tilew,1):
                im2 = im.crop(((X*Tilew),(Y*Tileh),((X+1)*Tilew),((Y+1)*Tileh)))
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,1):
                        im3 = im2.crop((x,y,x+1,y+1))
                        (r,g,b,a) = list(im3.getdata())[0]
                        
                        if Null == '>':
                            P,Q = PicMode.RGBA4444(r,g,b,a)
                        else:
                            Q,P = PicMode.RGBA4444(b,g,r,a)
                            
                        file.write(struct.pack('>2B',P,Q))
                    
        return file
    #=========================================#
    def RGBA8888(self,ImgDat,Tilew,Tileh,Width,Height,PicRGBA,PicPal=None):
        
        im = ImgDat
        file = io.BytesIO()
        PicMode = GetPicMode()
        
        (Null,RGBA) = PicRGBA # ('>','rgba')
        
        for Y in range(0,Height//Tileh,1):
            for X in range(0,Width//Tilew,1):
                im2 = im.crop(((X*Tilew),(Y*Tileh),((X+1)*Tilew),((Y+1)*Tileh)))
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,1):
                        im3 = im2.crop((x,y,x+1,y+1))
                        (r,g,b,a) = list(im3.getdata())[0]
                        
                        if Null == '>':
                            P,Q,R,S = PicMode.RGBA8888(r,g,b,a)
                        else:
                            P,Q,R,S = PicMode.RGBA8888(b,g,r,a)
                            
                        file.write(struct.pack('>4B',P,Q,R,S))
                        
        return file
#=========================================#
# ExpImp RGBA End
#=========================================#
class ExportDDS():
    
    def DXT1(self,PicDat,Tilew,Tileh,Width,Height,PicType,PicRGBA,PicPal=None):
        
        dest = [(0,0,0,0)]*(Width*Height*2)
        basex = 0
        PalMode = GetPalMode()
        (Tilew,Tileh) = (4,4)
        
        for Y in range(0,Height,Tileh):
            for X in range(0,Width,Tilew):
                basey = 0
                if PicType == 'DXT1':
                    colour0,colour1,bits = struct.unpack('<2HI',PicDat.read(8))
                else:
                    bits,colour0,colour1 = struct.unpack('<I2H',PicDat.read(8))
                (r0,g0,b0,a0) = PalMode.DXT(colour0)
                (r1,g1,b1,a1) = PalMode.DXT(colour1)
                
                if colour0 > colour1:
                    #colour2 = (2*colour0 + colour1) // 3
                    #colour3 = (2*colour1 + colour0) // 3
                    (r2,g2,b2,a2) = ((2*r0+r1)//3,(2*g0+g1)//3,(2*b0+b1)//3,0xff)
                    (r3,g3,b3,a3) = ((2*r1+r0)//3,(2*g1+g0)//3,(2*b1+b0)//3,0xff)
                else:
                    #colour2 = (colour0 + colour1) // 2
                    #colour3 = 0
                    (r2,g2,b2,a2) = ((r0+r1)//2,(g0+g1)//2,(g0+g1)//2,0xff)
                    (r3,g3,b3,a3) = (0,0,0,0xff)
                    
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,1):
                        control = bits & 3
                        bits = bits >> 2
                        
                        if control == 0:
                            dest[basex+basey+x] = (r0,g0,b0,a0)
                        elif control == 1:
                            dest[basex+basey+x] = (r1,g1,b1,a1)
                        elif control == 2:
                            dest[basex+basey+x] = (r2,g2,b2,a2)
                        elif control == 3:
                            dest[basex+basey+x] = (r3,g3,b3,a3)
                            
                    basey += Width
                basex += Tilew
            basex += Width*(Tileh-1)
            
        return dest
    #=========================================#
    def DXT3(self,PicDat,Tilew,Tileh,Width,Height,PicType,PicRGBA,PicPal=None):
        
        dest = [(0,0,0,0)]*(Width*Height)
        basex = 0
        PalMode = GetPalMode()
        (Tilew,Tileh) = (4,4)
        
        for Y in range(0,Height,Tileh):
            for X in range(0,Width,Tilew):
                basey = 0
                if PicType == 'DXT3':
                    bits = struct.unpack('<8B',PicDat.read(8))
                    colour0,colour1,code = struct.unpack('<2HI',PicDat.read(8))
                else:
                    code,colour0,colour1 = struct.unpack('<I2H',PicDat.read(8))
                    bits = struct.unpack('<8B',PicDat.read(8))
                      
                (r0,g0,b0,a0) = PalMode.DXT(colour0)
                (r1,g1,b1,a1) = PalMode.DXT(colour1)
                #colour2 = (2*colour0 + colour1) // 3
                #colour3 = (2*colour1 + colour0) // 3
                (r2,g2,b2,a2) = ((2*r0+r1)//3,(2*g0+g1)//3,(2*b0+b1)//3,0xff)
                (r3,g3,b3,a3) = ((2*r1+r0)//3,(2*g1+g0)//3,(2*b1+b0)//3,0xff)
                
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,1):
                        AlphaIndex = (4*y+x)//2
                        AlphaValue = bits[AlphaIndex]
                        AlphaValue >>= 4
                        AlphaValue *= 17
                        
                        control = ((code >> 2*(4*y+x)) & 0x03)
                        
                        if control == 0:
                            dest[basex+basey+x] = (r0,g0,b0,AlphaValue)
                        elif control == 1:
                            dest[basex+basey+x] = (r1,g1,b1,AlphaValue)
                        elif control == 2:
                            dest[basex+basey+x] = (r2,g2,b2,AlphaValue)
                        elif control == 3:
                            dest[basex+basey+x] = (r3,g3,b3,AlphaValue)
                            
                    basey += Width
                basex += Tilew
            basex += Width*(Tileh-1)
            
        return dest
    #=========================================#
    def DXT5(self,PicDat,Tilew,Tileh,Width,Height,PicType,PicRGBA,PicPal=None):
        
        dest = [(0,0,0,0)]*(Width*Height)
        basex = 0
        PalMode = GetPalMode()
        (Tilew,Tileh) = (4,4)
        
        for Y in range(0,Height,Tileh):
            for X in range(0,Width,Tilew):
                basey = 0
                if PicType == 'DXT5':
                    alpha0,alpha1 = struct.unpack('<2B',PicDat.read(2))
                    bits = struct.unpack('<6B',PicDat.read(6))
                    colour0,colour1,code = struct.unpack('<2HI',PicDat.read(8))
                else:
                    code,colour0,colour1 = struct.unpack('<I2H',PicDat.read(8))
                    bits = struct.unpack('<6B',PicDat.read(6))
                    alpha0,alpha1 = struct.unpack('<2B',PicDat.read(2))
                     
                
                alphaCode1 = bits[2] | (bits[3] << 8) | (bits[4] << 16) | (bits[5] << 24)
                alphaCode2 = bits[0] | (bits[1] << 8)
                
                (r0,g0,b0,a0) = PalMode.DXT(colour0)
                (r1,g1,b1,a1) = PalMode.DXT(colour1)
                #colour2 = (2*colour0 + colour1) // 3
                #colour3 = (2*colour1 + colour0) // 3
                (r2,g2,b2,a2) = ((2*r0+r1)//3,(2*g0+g1)//3,(2*b0+b1)//3,0xff)
                (r3,g3,b3,a3) = ((2*r1+r0)//3,(2*g1+g0)//3,(2*b1+b0)//3,0xff)
                
                for y in range(0,Tileh,1):
                    for x in range(0,Tilew,1):
                        AlphaIndex = 3*(4*y+x)
                        
                        if AlphaIndex <= 12:
                            alphaCode = ((alphaCode2 >> AlphaIndex) & 0x07)
                        elif AlphaIndex == 15:
                            alphaCode = (alphaCode2 >> 15) | ((alphaCode1 << 1) & 0x06)
                        else: # AlphaCodeIndex >= 18 and AlphaCodeIndex <= 45
                            alphaCode = ((alphaCode1 >> (AlphaIndex - 16)) & 0x07)
                            
                        if alphaCode == 0:
                            AlphaValue = alpha0
                        elif alphaCode == 1:
                            AlphaValue = alpha1
                        else:
                            if alpha0 > alpha1:
                                AlphaValue = ((8-alphaCode)*alpha0 + (alphaCode-1)*alpha1)//7
                            else:
                                if alphaCode == 6:
                                    AlphaValue = 0
                                elif alphaCode == 7:
                                    AlphaValue = 255
                                else:
                                    AlphaValue = ((6-alphaCode)*alpha0 + (alphaCode-1)*alpha1)//5
                        
                        control = ((code >> 2*(4*y+x)) & 0x03)
                        
                        if control == 0:
                            dest[basex+basey+x] = (r0,g0,b0,AlphaValue)
                        elif control == 1:
                            dest[basex+basey+x] = (r1,g1,b1,AlphaValue)
                        elif control == 2:
                            dest[basex+basey+x] = (r2,g2,b2,AlphaValue)
                        elif control == 3:
                            dest[basex+basey+x] = (r3,g3,b3,AlphaValue)
                            
                    basey += Width
                basex += Tilew
            basex += Width*(Tileh-1)
            
        return dest
#=========================================#
# ExportDDS End
#=========================================#
# Next:Import DDS
#=========================================#
class ImportDDS():
    
    def DXT1(self,ImgDat,Tilew,Tileh,Width,Height,PicType,PicRGBA,PicPal=None):
        
        im = ImgDat
        im.save('__pycache__\\tmp.png')
        os.system('@echo off')
        os.system('@__pycache__\\nvdxt.exe>nul 2>nul -nomipmap -file __pycache__\\tmp.png -dxt1 -output __pycache__\\tmp.dds')
        dds = open('__pycache__\\tmp.dds','rb')
        dds.seek(0x80)
        file = io.BytesIO()
        file.write(dds.read(Width*Height//2))
        dds.close()
        os.remove('__pycache__\\tmp.png')
        os.remove('__pycache__\\tmp.dds')
        
        return file
    #=========================================#
    def DXT3(self,ImgDat,Tilew,Tileh,Width,Height,PicType,PicRGBA,PicPal=None):
        
        im = ImgDat
        im.save('__pycache__\\tmp.png')
        os.system('@echo off')
        os.system('@__pycache__\\nvdxt.exe>nul 2>nul -nomipmap -file __pycache__\\tmp.png -dxt3 -output __pycache__\\tmp.dds')
        dds = open('__pycache__\\tmp.dds','rb')
        dds.seek(0x80)
        file = io.BytesIO()
        file.write(dds.read(Width*Height))
        dds.close()
        os.remove('__pycache__\\tmp.png')
        os.remove('__pycache__\\tmp.dds')
        
        return file
    #=========================================#
    def DXT5(self,ImgDat,Tilew,Tileh,Width,Height,PicType,PicRGBA,PicPal=None):
        
        im = ImgDat
        im.save('__pycache__\\tmp.png')
        os.system('@echo off')
        os.system('@__pycache__\\nvdxt.exe>nul 2>nul -nomipmap -file __pycache__\\tmp.png -dxt5 -output __pycache__\\tmp.dds')
        dds = open('__pycache__\\tmp.dds','rb')
        dds.seek(0x80)
        file = io.BytesIO()
        file.write(dds.read(Width*Height))
        dds.close()
        os.remove('__pycache__\\tmp.png')
        os.remove('__pycache__\\tmp.dds')
        
        return file
#=========================================#
# ImageConv End
#=========================================#
