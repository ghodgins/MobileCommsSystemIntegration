from struct import *
import binascii

floatsOriginal = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
floatsNoise = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

stringOriginal = 'thisisatest'
stringNoise = 'thiswdjtest'

# BER% = (NumberofBitErrors/TotalBits)*100
# pass in two arrays of floats
def calculateBER(floats1, floats2):
    #assert ( len(floats1) == len(floats2) )
    assert ( len(stringOriginal) == len(stringNoise) )

    errors = 0
    #totalBits = float( len(floats1)*32 )
    totalBits = float( len(stringOriginal)*8 )

    #for i in range(len(floats1)):
    #    errors += bitDifference(floats1[i], floats2[i])

    for i in range(len(stringOriginal)):
        errors += bitDifference(stringOriginal[i], stringNoise[i])

    #print "Errors = " + str(errors)
    #print "totalBits = " + str(totalBits)

    BER = (errors/totalBits) * 100
    return BER

def BERreturn(errors, totalBits):
    BER = (errors/totalBits) * 100
    return BER

# calculate bit difference for float
def bitDifference(float1, float2):
    difference = 0

    #binary1 = floatToBinaryInteger(float1)
    #binary2 = floatToBinaryInteger(float2)

    binary2 = bin(ord(float1))[2:].zfill(8)
    binary1 = bin(ord(float2))[2:].zfill(8)

    binary2 = int(binary2)
    binary1 = int(binary1)

    print binary2

    mask = 1
    while (binary1 > 0 or binary2 > 0):
        bmask1 = binary1 & mask
        bmask2 = binary2 & mask

        #print "bmask1:" + str(bmask1) + str(bmask2) + ":bmask2"

        if(bmask1 != bmask2):
            difference += 1

        binary1 = binary1 >> 1
        binary2 = binary2 >> 1
    #difference = 2
    print difference
    return difference

# Convert floats to binary values
def floatToBinaryInteger(float):
    # convert float to a string of bits
    bitString = pack('>f', float)
    # convert the string of bits into an integer for manipulation
    bits = unpack('>i', bitString)[0]
    return bits

if __name__ == '__main__':
    #BER = calculateBER(floatsOriginal, floatsNoise)
    BER = calculateBER(stringOriginal, stringNoise)
    print "BER = " + str(BER)