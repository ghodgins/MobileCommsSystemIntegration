from struct import *

floatsOriginal = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
floatsNoise = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

# pass in two arrays of floats
def calculateBER(floats1, floats2):

    errors = 0
    totalBits = float( 32 )

    errors += bitDifference(floats1, floats2)

    BER = (errors/totalBits) * 100
    return BER

# calculate bit difference for float
def bitDifference(float1, float2):
    difference = 0

    binary1 = floatToBinaryInteger(float1)
    binary2 = floatToBinaryInteger(float2)

    mask = 1
    while (binary1 > 0 or binary2 > 0):
        bmask1 = binary1 & mask
        bmask2 = binary2 & mask

        if(bmask1 != bmask2):
            difference += 1

        binary1 = binary1 >> 1
        binary2 = binary2 >> 1

    #print difference
    return difference

# Convert floats to binary values
def floatToBinaryInteger(float):
    # convert float to a string of bits
    bitString = pack('>f', float)
    # convert the string of bits into an integer for manipulation
    bits = unpack('>i', bitString)[0]
    return bits

if __name__ == '__main__':
    BER = calculateBER(floatsOriginal, floatsNoise)
    print "BER = " + str(BER)