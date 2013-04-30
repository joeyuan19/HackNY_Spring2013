#Determine distance based on time stamps
import numpy as np

#ti - t initial: 	time sent
#tf - t final: 		time recieved
# d = (tf-ti) / s;  s = 300 m/s -> 0.3 m/ms
def distance(ti,tf):
	s = 330	#speed of sound [m/s]
 	return s*(tf-ti)

def mean(data):
	s = 0
	for i in data:
		s+=i
	return (s/len(data))
	
lA, rA 		= np.loadtxt("A.txt", unpack=True)
lB, rB 		= np.loadtxt("B.txt", unpack=True)
"""
np.abs(rB[0] - lA[0])
np.abs(rA[0] - lB[1])
np.abs(rB[1] - lA[1])
np.abs(rA[1] - lB[2])
np.abs(rB[2] - lA[2])
"""
L = lB.size

i = 0
j = 0
c = 0

sum = 0.0

while j < L:
  if c%2 == 0:
    sum += np.abs(rB[i] - lA[j])
    j += 1
  else:
    sum += np.abs(rA[i] - lB[j])
    i += 1
  c += 1
print sum/(L-1)

