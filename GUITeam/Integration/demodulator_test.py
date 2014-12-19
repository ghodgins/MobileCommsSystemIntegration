import math
#import numpy

OMEGA = math.pi/2
TPSK = 1 #samplingtime
T1QAM = 0.2 #samplingtime
T2QAM = 0.1 #samplingtime
FREQUENCY = 1.5707963268

#PSK lookup tables (Non Gray)
table2PSK = [[0,0], [-3.141592654,1]]
table4PSK = [[-0.392699082,0], [-1.178097245,1], [-1.963495408,2], [-2.748893572,3]]
table8PSK = [[0,0],[-0.392699082, 1], [-0.785398163,2], [-1.178097245,3], [-1.570796327,4], [-1.963495408,5], [-2.35619449,6], [-2.748893572,7]]
table16PSK = [[0,0],[-0.196349541,1], [-0.392699082,2], [-0.589048623,3], [-0.785398163,4], [-0.981747704,5], [-1.178097245,6], [-1.374446786,7], [-1.570796327,8], [-1.767145868,9], [-1.963495408,10], [-2.159844949,11], [-2.35619449,12], [-2.552544031,13], [-2.748893572,14], [-2.945243113,15]]

#PSK lookup tables (Gray)
table2PSKGRAY = [[0,0], [-3.141592654, 1]]
table4PSKGRAY = [[-0.392699082, 0], [-1.178097245, 1], [-1.963495408, 3], [-2.748893572, 2]]
table8PSKGRAY = [[0,0],[-0.392699082, 1], [-0.785398163,3], [-1.178097245,2], [-1.570796327,6], [-1.963495408,7], [-2.35619449,5], [-2.748893572,4]]
table16PSKGRAY = [[0,0],[-0.196349541,1], [-0.392699082,3], [-0.589048623,2], [-0.785398163,6], [-0.981747704,7], [-1.178097245,5], [-1.374446786,4], [-1.570796327,12], [-1.767145868,13], [-1.963495408,15], [-2.159844949,14], [-2.35619449,10], [-2.552544031,11], [-2.748893572,9], [-2.945243113,8]]

#QAM lookup tables
QAM16 = [[-1.44879868, -0.305724363, 0], [0.687866287, 0.549445932, 1], [0.28572896, 1.467034338 ,2 ], [-1.44879868, -1.141305418, 3], [-1.494741699,-0.152667402, 4], [0.805969892, 0.791939868, 5],[-0.260123802, -0.823666819, 6], [-1.494741699,-0.569925576, 7], [-1.44879868, 0.305724363, 8], [-0.641364286,2.641074832, 9], [0.687866287,-0.549445932, 10], [-1.44879868,1.141305418, 11], [-1.494741699,0.152667402, 12], [0.805969892, -0.791939868, 13], [-0.260123802,0.823666819, 14], [-1.494741699, 0.569925576, 15] ]

# Will accept these three constants as parameters later.....
TABLE = table2PSK
WAVES = [[0.8, 0.8], [0.4, -0.5]]
SYMBOLSIZE = 1

demodulatedBytes = []
bitArray = []
currentByte = 0
         
bitsLeft = 8

#Parameters: Wave we receive is input (floating point)
#w = Omega known frequency
#time = known time sampling
def demodulatePSK(wave):
    temp = math.asin(wave)
    result = temp - (OMEGA * TPSK)
    
    min = 1000
    code = 0

    for pair in TABLE:
        if (abs(pair[0] - result) < min):
            min = abs(pair[0] - result)
            code = pair[1]
    
    return code

def demodulateQAM(waveT1, waveT2):
    if (abs(waveT2) > abs(waveT1)):
        WAVE_1 = waveT1
        WAVE_2 = waveT2
        T1 = T1QAM
        T2 = T2QAM
    else:
         WAVE_1 = waveT2
         WAVE_2 = waveT1
         T1 = T2QAM
         T2 = T1QAM 

    
    min_phase = 1000    
    result =  ( ( (FREQUENCY * T2) * math.asin(WAVE_1 / WAVE_2)) - (FREQUENCY * T1) ) / (1 - math.asin(WAVE_1 / WAVE_2))
    #send that phase to lookup table and return closest value X NEXT STEP(only search the first parameter in each threes of the array:
    for pair in TABLE:
        if (abs(pair[0] - result) < min_phase):
            min_phase = abs(pair[0] - result)
            phase = pair[0]

    amp = waveT1 / math.sin((FREQUENCY * T1QAM) + phase)
 
    #send both the phase and amplitude to the lookup table
    #only examine the entries in the table where the phase equals the value we found. Compute the differences between corresponding amplitude entries for that exact phase and return closest one with its third entry, the symbol number
    min_amp = 1000
    for pair in TABLE:
        if ((abs(pair[1] - amp) < min_amp) and (phase == pair[0])):
            min_amp = abs(pair[1] - amp)
            code = pair[2]

    return code

def test2PSK():
    testSet = [[1, 0], [-1, 1]]
    
    for pair in testSet:
        symbol = demodulatePSK(pair[0])
        
        if (symbol != pair[1]):
            print("Test 2PSK Failed!")
            return 1
    
    print("Test 2PSK Passed")
    return 0
    
def test4PSK():
    testSet = [[0.9238795325, 0], [0.3826834324, 1], [-0.3826834324, 2], [-0.9238795325, 3]]
    
    for pair in testSet:
        symbol = demodulatePSK(pair[0])
        
        if (symbol != pair[1]):
            print("Test 4PSK Failed!")
            return 1
    
    print("Test 4PSK Passed")
    return 0

def test8PSK():
    testSet = [[1,0], [0.9238795325, 1], [0.7071067812, 2], [0.3826834324, 3], [0.000000000000000122514845, 4], [-0.3826834324, 5], [-0.7071067812, 6], [-0.9238795325, 7]]
    
    for pair in testSet:
        symbol = demodulatePSK(pair[0])
        
        if (symbol != pair[1]):
            print("Test 8PSK Failed!")
            return 1
    
    print("Test 8PSK Passed")
    return 0

def test16PSK():
    testSet = [[1,0], [0.9807852804, 1], [0.9238795325, 2], [0.8314696123, 3], [0.7071067812, 4], [0.555570233, 5], [0.3826834324, 6], [0.195090322, 7], [0.000000000000000122514845, 8], [-0.195090322, 9], [-0.3826834324, 10], [-0.555570233, 11], [-0.7071067812, 12], [-0.8314696123, 13], [-0.9238795325, 14], [-0.9807852804, 15]]
    
    for pair in testSet:
        symbol = demodulatePSK(pair[0])
        
        if (symbol != pair[1]):
            print("Test 16PSK Failed!")
            return 1
    
    print("Test 16PSK Passed")
    return 0
    
def test16QAM():
    testSet = [[0.277103029, 0.2516042853, 0], [0.4629431798, 0.3457261466, 1], [0.8282145551, 0.8479294427, 2], [1.0344585746, 0.9392687305, 3], [0.1411910454, 0.1828012135, 4], [0.7128699828, 0.776513639, 5], [-0.0444855628, 0.0888491938, 6], [0.5270829702, 0.6824186779, 7], [-0.277103029, -0.2516042853, 8], [-0.8488351045, -0.8453436111, 9], [-0.4629431798, -0.3457261466, 10], [-1.0344585746, -0.9392687305, 11], [-0.1411910454, -0.1828012135, 12], [-0.7128699828, -0.776513639, 13], [0.0444855628, -0.0888491938, 14], [-0.5270829702, -0.6824186779, 15]]

    for pair in testSet:
        symbol = demodulateQAM(pair[0], pair[1])
        
        if (symbol != pair[2]):
            print("Test 16QAM Failed!")
            return 1
    
    print("Test 16QAM Passed")
    return 0

#Run tests
TABLE = table2PSK    
test2PSK()

TABLE = table4PSK    
test4PSK()

TABLE = table8PSK    
test8PSK()

TABLE = table16PSK    
test16PSK()

TABLE = QAM16   
test16QAM()

#Use this to demodulate WAVES array
for wave in WAVES:
    symbol = demodulateQAM(wave[0], wave[1])
    print symbol
    currentByte << SYMBOLSIZE
    currentByte = symbol
    bitsLeft -= SYMBOLSIZE
    
    if (bitsLeft == 0):
        demodulatedBytes.append(currentByte)
        bitsLeft = 8
        currentByte = 0

if (bitsLeft != 8):
    currentByte << bitsLeft
    demodulatedBytes.append(currentByte)