import math


def Compact1By1(x):
    x &= 0x55555555
    x = (x ^ (x >> 1)) & 0x33333333
    x = (x ^ (x >> 2)) & 0x0f0f0f0f
    x = (x ^ (x >> 4)) & 0x00ff00ff
    x = (x ^ (x >> 8)) & 0x0000ffff
    return x


def DecodeMorton2X(code):
    return Compact1By1(code >> 0)


def DecodeMorton2Y(code):
    return Compact1By1(code >> 1)


def UnswizzleTexture(pixelData, width, height,swizzled):

    unswizzled = [(0, 0, 0, 0)] * len(pixelData)

    if (width < height):
        min = width
    else:
        min = height

    k = int(math.log(min, 2))

    print(min, k)

    for i in range(width * height):

        if (height < width):
            j = int(((i >> (2 * k) << (2 * k)) | ((DecodeMorton2Y(i) & (min - 1)) << k) | ((DecodeMorton2X(i) & (min - 1)) << 0)))
            x = int(j // height)
            y = int(j % height)
        else:
            j = int(((i >> (2 * k) << (2 * k)) | ((DecodeMorton2X(i) & (min - 1)) << k) | ((DecodeMorton2Y(i) & (min - 1)) << 0)))
            x = int(j // width)
            y = int(j % width)

        if (y >= height or x >= width): continue

        #unswizzled[((y * width) + x)] = pixelData[i]

        if(swizzled):
            unswizzled[i] = pixelData[((y * width) + x)]
        else:
            unswizzled[((y * width) + x)] = pixelData[i]


    return unswizzled


pixelData = [];

for y in range(64):
    pixelData.append((y, y, y, 255))

print(pixelData)

swPixelData = UnswizzleTexture(pixelData, 8, 8,True)

print(swPixelData)

origin = UnswizzleTexture(swPixelData, 8, 8,False)

print(origin)
