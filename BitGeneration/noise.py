import random
import math

random.seed()

def additiveGuassian(iterations):
	X = 0.0
	for i in range(0, iterations):
		r = random.random()
		X = X + r

	X = X - iterations / 2.0
	X = X * math.sqrt(12.0 / iterations)
	return X

print "additive guassian: "
print (additiveGuassian(100))
print "\n"

def noiseSequence(N):
	seq = []
	for i in range(0,N):
		seq.append(additiveGuassian(100))

	return seq


print noiseSequence(10)
