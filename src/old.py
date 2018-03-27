import math


def ceilLog2(num):
    return math.ceil(math.log(num, 2))


xMaskBase = 0x55555555
yMaskBase = 0xAAAAAAAA


def swizzle(width, height):
    result = []

    log2Width = ceilLog2(width)
    log2Height = ceilLog2(height)

    maxMask = 1 << (log2Width << 1)
    xMask = (xMaskBase | -maxMask)
    yMask = yMaskBase & (maxMask - 1)

    transFormY = []
    currentY = 0

    for i in range(height):
        transFormY.append(currentY)
        currentY = (currentY - yMask) & yMask

    def getTransFormXInLineY(y, times):

        transFormX = []
        offsX = times * maxMask

        for i in range(width):
            transFormX.append(offsX + y + times * maxMask)
            offsX = (offsX - xMask) & xMask

        return transFormX

    timesArray = []
    times = -1

    for i in range(height):
        if (transFormY[i] == 0):
            times += 1
        timesArray.append(times)

    for i in range(len(transFormY)):
        result.extend(getTransFormXInLineY(transFormY[i], timesArray[i]))

    return result


# test

def convert(arr, maskMutex, isSwizzled):
    newArr = [0] * len(maskMutex)

    for i in range(len(maskMutex)):
        if (isSwizzled):
            newArr[maskMutex[i]] = arr[i]
        else:
            newArr[i] = arr[maskMutex[i]]

    return newArr


'''
test = list(range(256))


maskMutex = swizzle(16, 16)
print('maskMutex')
print(maskMutex)
arr = convert(test, maskMutex,True)
print('arr')
print(arr)
reArr = convert(arr, maskMutex,False)
print('reArr')
print(reArr)
'''
