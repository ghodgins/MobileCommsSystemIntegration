import random
import math

def box_muller():
	u1 = random.random()
	u2 = random.random()
	z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
	z2 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
	z = z1+z2
	return z
	
x = []
i = 0
n = 10
for i in range(0,n):
	x.append(random.randint(2,7))
	print "Random input before noise: ",x[i]
	x[i] = x[i] + box_muller()
	print "Random input after noise has been added: ",x[i]