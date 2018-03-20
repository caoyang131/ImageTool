#=========================================#
# ExportPNG Ver1.10
#=========================================#
import io,os,struct,time,glob
from ConfigPNG import *
from ImageConv import *
from PIL import Image
#=========================================#
# Start
#=========================================#

print('============================================')
print('       Project ExportPNG Version 1.10       ')
print('           Written by caoyang131            ')
print('            '+time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))+'        ')
print('============================================')
print('')
print('                Let`s start!                ')
print('')
print('============================================')
print('')

#=========================================#

TypeA = ImageTypeA() # Index4
TypeB = ImageTypeB() # RGBA8888
TypeC = ImageTypeC() # Index8

#=========================================#
# All Type Start
#=========================================#

for Type in [TypeA,TypeB,TypeC]:
    srcfolder,pngfolder,srctype,pictype = Type.FolderConfig()

    picname = glob.iglob(srcfolder+'*.'+srctype)

    for pic in picname:
        dirname = os.path.dirname(pic)
        filename = os.path.basename(pic)
        filesize = os.path.getsize(pic)
        basename,extname = os.path.splitext(filename)
        src = open(pic,'rb')
    
        BmpValue = Type.CheckPic(src)
    
        if BmpValue == True:
        
            if srcfolder == pngfolder:
                outputname = str(dirname+'\\'+basename+'.'+pictype)
            else:
                outputname = str(pngfolder+basename+'.'+pictype)
            
            print(filename+' >> '+basename+'.'+pictype)
        
            t0 = time.clock()
        
            Width,Height,Tilew,Tileh = Type.ConfigA(src,filesize)
            DatOffset,PalOffset,PalSize = Type.ConfigB(src)
            PicType,PalType,PicRGBA,PalRGBA,Option,inputIsSwizzled = Type.ConfigC(src)
        
            PicDat = GetPicDat(src,PicType,DatOffset,Width,Height)
            PicPal = GetPicPal(src,PalType,PalOffset,PalSize,PalRGBA)
            ImgExport(src,PicDat,outputname,PicType,Tilew,Tileh,Width,Height,PicRGBA,Option,PicPal,inputIsSwizzled)
        
            t = (time.clock() - t0)
        
            print('Time:%.2f''s' % t)
        else:
            pass
        
        src.close()
#=========================================#
# All Type End
#=========================================#
print('')
print('============================================')
print('')
print('  Mission complete.Press any key to exit... ')
print('')
print('============================================')
input('')
#=========================================#
