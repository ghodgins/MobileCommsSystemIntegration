import modulator
import random
import math

# Defaults:
levels = 4
msg = '01'

theta = 2 * 3.14/10240
QAM16 = [
			{'amplitude' : 0.311, 'omega': -135, 'theta': theta},
			{'amplitude' : 0.850, 'omega': -165, 'theta': theta},
			{'amplitude' : 0.311, 'omega': -45, 'theta': theta},
			{'amplitude' : 0.850, 'omega': -15, 'theta': theta},
			{'amplitude' : 0.850, 'omega': -105, 'theta': theta},
			{'amplitude' : 1.161, 'omega': -135, 'theta': theta},
			{'amplitude' : 0.850, 'omega': -75, 'theta': theta},
			{'amplitude' : 1.161, 'omega': -45, 'theta': theta},
			{'amplitude' : 0.311, 'omega': 135, 'theta': theta},
			{'amplitude' : 0.850, 'omega': 165, 'theta': theta},
			{'amplitude' : 0.311, 'omega': 45, 'theta': theta},
			{'amplitude' : 0.850, 'omega': 15, 'theta': theta},
			{'amplitude' : 0.850, 'omega': 105, 'theta': theta},
			{'amplitude' : 1.161, 'omega': 135, 'theta': theta},
			{'amplitude' : 0.850, 'omega': 75, 'theta': theta},
			{'amplitude' : 1.161, 'omega': 45, 'theta': theta},
		]

# Mask around QAM16, so we can use the same functions.
class QAM:
	def __init__(this):
		this.value = QAM16
	def get(this, input):
		if input < len(this.value):
			return this.value[input]

class Signal:
	mean = 0
	std = 1
	period = 1
	dt = 0.1
	def __init__(this, num_levels = levels, qam = False):
		this.size = math.pow(2, num_levels)
		# Modulator
		this.m = modulator.Modulator(num_levels, this.size)
		# Lookup data
		if qam is False:
			this.l = modulator.Lookup_Data(this.size) 
			this.l.build()
		else:
			this.l = QAM()	

	def signal(this, sig_data): # amplitude, frequency, phase
		size = int(math.ceil(this.period / this.dt))
		s = [ [0.0 for x in xrange(0, size)] for x in xrange(0, 4) ] # Blank array

		global amp
		global phase

		a = sig_data['amplitude']
		w = math.radians(sig_data['omega'])
		p = math.radians(sig_data['theta'])
		step = 0.0

		for t in xrange(0, size):
			# Signal
			#print t
			step += this.dt
			s[0][t] = a*math.sin(w*step + p)
			# With noise
			s[1][t] = s[0][t] + rand(this.mean, this.std)
			s[2][t] = a
			s[3][t] = p

		return s

	def build(this, input = msg):
		this.m.build(input)

	def generate(this, input = msg, build = False):
		if build is True:
			this.build(input)
		res = []
		src = []
		amp = []
		phase = []
		for i in xrange(0, this.m.size()):
			temp = this.l.get( this.m.get(i) )
			s, r, a, p = this.signal(temp)

			src.append(s)
			res.append(r)
			phase.append(p)
			amp.append(a)
			
		return [res, src, amp, phase]

# Random Gaussian with mean = 0, std = 1
# See Knuth
def rand(mean = 0, std = 1):
	s = 1.0
	while s >= 1.0:
		v1 = 2.0 * random.random() - 1
		v2 = 2.0 * random.random() - 1
		s = v1*v1 + v2*v2
	if s == 0.0:
		return 0.0 + mean
	res = v1 * math.sqrt( -2.0 * math.log(s)/s)
	return (res * std) + mean

def rangef(start, stop, step):
	while start < stop:
		yield start
		start += step