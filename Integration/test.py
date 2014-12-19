from modulation import Signal
from demodulator import Demodulator

def get_max(arr):
	temp = [0] * len(src)
	i = 0
	for r in src:
		for s in r:
			if abs(s) > temp[i]:
				temp[i] = s
		i += 1
	return temp

# Examples
input = '21'
sig = Signal(2)#, True)
# Need to compare QAM with excel spreadsheet... YAY!
res, src = sig.generate(input, True)

temp = get_max(src)

print "Source"
for i in temp:
	print i

print "Demodulate"
dem = Demodulator()
dem.build(4)#, True)

out = dem.generate(temp)

#print "Result"
#for i in res:
#	print i

print "Res:"
print out