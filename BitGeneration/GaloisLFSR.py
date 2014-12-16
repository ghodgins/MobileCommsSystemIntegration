import sys

def lfsr(seed, taps, y) :
  for i in range(0, y):
    nxt = sum([ seed[x] for x in taps]) % 2
    yield nxt
    seed = ([nxt] + seed)[:max(taps)+1]
    
lfsr_list = []
y = int(sys.argv[1])

for x in lfsr([1,0,1,1,1,0,1,0,0],[1,5,6], y) :
  lfsr_list.append(x);

for p in lfsr_list: print p
