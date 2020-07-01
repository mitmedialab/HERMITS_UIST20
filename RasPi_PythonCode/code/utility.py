import Constants


def mapping(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def getIDfromADDR(ADDR):
        
    for x, add in enumerate(Constants.toioADDR):
        if add == ADDR:
            return x
    
    print("unknown ID with address of toio: " +ADDR)
    
