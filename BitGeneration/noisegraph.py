import random
import math

# If matplotlib is available uncomment this:
#import matplotlib.pyplot as plot

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

def box_muller():
	u1 = random.random()
	u2 = random.random()
	z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
	z2 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
	return z1,z2


print noiseSequence(10)
print "\n"

def biasNoise(values,sigma = 0.01):
	x = 0.0
	out = []
	for i in values:
		x= x + random.gauss(0,sigma)
		out.append(i + x)
	return out

def additiveGaussian2(values,mu = 0.0,sigma = 0.1):
	x= 0.0 
	out = []
	for i in values:
		x = 0.0
		r = random.gauss(mu,sigma)
		x = i + r
		out.append(x)
	return out

def spikeNoise(values,occurence = 0.0001,strenght=0.0009):
	out = []
	for i in values:
		x= 0.0
		r = random.random()
		if r < occurence :
		 	x =  strenght + random.random()*0.1
			out.append(x)
		else: 
			out.append(i)
	return out

def multiplicative(values,sigma = 0.0,mu = 0.0):
	x= 0.0
	out = []
	for i in values:
		sigma = sigmaGen(i)
		r = i*random.gauss(mu,sigma)
		x = i+r
#		print "x :",x
#		print "sigma :",sigma
#		print "r :",r
#		print "i :",i
		out.append(x)
	return out

def sigmaGen(x):
	return  math.pow(x,4)/10000

def clip(signal,maximum= 3,minimum = -3):
	out = []
	for i in signal:
		if i > maximum:
			out.append(maximum)
		if i < minimum:
			out.append(minimum)
		else:
			out.append(i)
	return out

def FullNoise(maximum = 3, minimum = -3,signal = []):	
	#must apply muliplicative first  
	signal = multiplicative(signal)
	signal = biasNoise(signal)
	signal = additiveGaussian2(signal)
	signal = spikeNoise(signal)
	clip(signal)
	#print signal

def demo(signal = []):
	signal = noiseSequence(100)
	x = range(0,100)
	store = signal
#	plot.plot(x,store, linewidth=2.0)
#	plot.show()
	print signal	
	signal = multiplicative(signal)
#	plot.plot(x,signal, linewidth=2.0)
#	plot.show()	
	signal = biasNoise(signal)
#	plot.plot(x,signal, linewidth=2.0)
#	plot.show()	
	signal = additiveGaussian2(signal)
#	plot.plot(x,signal, linewidth=2.0)
#	plot.show()
	signal = spikeNoise(signal)
	print signal
#	plot.plot(x,signal, linewidth=2.0)
#	plot.show()



demo()
