import numpy as np
import pyaudio
import time
import winsound
import sys
import struct

nFFT = 512
BUF_SIZE = 4 * nFFT
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
#Store Data
send    = []
recieve = []
 
def listen(stream, MAX_y): 
  # Read n*nFFT frames from stream, n > 0
  N = max(stream.get_read_available() / nFFT, 1) * nFFT
  data = stream.read(N)
 
  # Unpack data, LRLRLR...
  y = np.array(struct.unpack("%dh" % (N * CHANNELS), data)) / MAX_y
  y_L = y[::2]
  y_R = y[1::2]
 
  Y_L = np.fft.fft(y_L, nFFT)
  Y_R = np.fft.fft(y_R, nFFT)
 
  # Sewing FFT of two channels together, DC part uses right channel's
  Y = abs(np.hstack((Y_L[-nFFT/2:-1], Y_R[:nFFT/2])))
  
  #	Lower kHz Limit = 15000 Hz -> Y[429]
  fOi = Y[429:]
  # LOOK FOR 20 000 Hz 
  if fOi.argmax() == 35 and fOi[35]>=1.00:
  	t = time.clock()
	#print "Amp:\t", fOi[58]
  	print "\tTIME:\t", str(t)
	#print "\t\tSEND:\n\t\t\t",send
	recieve.append(t)
	return 1
  else:
	return 0


def speak(freq,dur):
	print "Freq:\t",freq
	#time.sleep(1.0)
	t = time.clock()
	#winsound.PlaySound('../media/WHAT20k2.wav',0)
	print "\tTIME:\t",str(t)
	winsound.Beep(freq,dur)#20kHz, 50ms
	send.append(t)
	#print "\t\tRECEIVE:\n\t\t\t",recieve
	return 0

 
def main():
  #START TIMER
  print time.clock()
  p = pyaudio.PyAudio()
  		

  #print "-"*10, "0 : SPEAK"
  #print "-"*10, "1 : LISTEN"  
  speaker = int(sys.argv[1])
  # Frequency range
  #print "You chose to: "
  
  count 	 = 0	 	# Pass counter
  passes     = 6		# Listen/Hear 10  times then quit
  phase      = 0		# Run speaker or listener

  if int(sys.argv[1]) == 0:
    phase = 0				#SPEAK
  else: 
    phase = 1				#LISTEN
    
  while(count<passes):
    count +=1
    if phase == 0:
      print "SPEAK\t", str(count)
      time.sleep(2.0)
      Durr = 100 	# Set Duration To 1000 ms == 1 second
      Freak = 18000			#Freq in Hz
      speaker = speak(Freak,Durr)
      time.sleep(2.0)
      phase = 1
    else:
      print "LISTEN\t", str(count)
      stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,frames_per_buffer=BUF_SIZE)
      # Used for normalizing signal. If use paFloat32, then it's already -1..1.
      # Because of saving wave, paInt16 will be easier.
      MAX_y = 2.0**(p.get_sample_size(FORMAT) * 8 - 1)
 
      while(phase == 1):
        #print "Listening"
        k = listen(stream, MAX_y)
        if (k==1):
          #"BREAK"
          phase = 0
          stream.stop_stream()
          stream.close()		  
  print "\n\n\n"
  print "SPEAK:",send
  print "RECEIVE",recieve
  
  
  print "\n\n\t\t", len(send)
  print "\n\n\t\t", len(recieve)
  
  
  p.terminate()
  
  fileName = "A.txt"
  DataOut = np.column_stack((send, recieve))
  np.savetxt(fileName, DataOut, fmt=('%.6f','%.6f'))

  
  
if __name__ == '__main__':
  main()
