from Tkinter import *
import threading
import time

import pyaudio
import struct
import math
from myfunctions import clip16, clip16_arr, clip16_flt
from scipy.signal import butter, lfilter
import numpy as np

#####Color table#####
RED = (200,0,0)
GREEN = (0,200,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (200,200,200)

class Parameters():
	def __init__(self):
		# initialize all parameter values
		self.GAIN = 1

		# parameters for Flanger effect
		self.flanger_f = 30
		self.flanger_w = 0.1
		self.flanger_gain = 0.5

		# parameters for WahWah effect
		self.wahwah_f_lfo = 2
		self.wahwah_fc_min = 250
		self.wahwah_w = 0.01

		# parameters for Delay effect
		self.delay_Gfb = 0.55
		self.delay_Gdp = 1
		self.delay_Gff = 0.5
		self.delay_sec = 2.0
		self.d = 88200 # index for delay buffer calculated from delay_sec

		# parameters for Fuzzy effect
		self.fuzzy_mix = 1
		self.fuzzy_gain = 1

	def Print_prmtr(self):
		print self.GAIN

parameters = Parameters()

class App(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.MODE = "Normal"
		print "Initial Mode is ", self.MODE
		self.start()
	
	def Pressed(self):                          # effect passing function
		self.MODE = self.v.get()
		# print self.v.get()

	######## Effect paramter passing functions ########
	## Trigger when the scale is moved
	def Parameter0(self,scaleValue):                          # flanger_f
		parameters.flanger_f = int(scaleValue)

	def Parameter1(self,scaleValue):                          # flanger_w
		# print float(scaleValue)
		parameters.flanger_w = float(scaleValue)
	
	def Parameter2(self,scaleValue):                          # flanger_gain
		parameters.flanger_gain = float(scaleValue)

	def Parameter3(self,scaleValue):                          # wahwah_f_lfo
		parameters.wahwah_f_lfo = float(scaleValue)

	def Parameter4(self,scaleValue):                          # wahwah_fc_min
		parameters.wahwah_fc_min = int(scaleValue)
	
	def Parameter5(self,scaleValue):                          # wahwah_w
		parameters.wahwah_w = float(scaleValue)

	def Parameter6(self,scaleValue):                          # delay_Gfb
		parameters.delay_Gfb = float(scaleValue)
	
	def Parameter7(self,scaleValue):                          # delay_Gdp
		parameters.delay_Gdp = float(scaleValue)

	def Parameter8(self,scaleValue):                          # delay_Gff
		parameters.delay_Gff = float(scaleValue)
	
	def Parameter9(self,scaleValue):                          # delay_sec
		parameters.delay_sec = float(scaleValue) 
		parameters.d = int( math.floor( 44100 * parameters.delay_sec ) )

	def Parameter10(self,scaleValue):                          # empty function parameter passing
		parameters.fuzzy_mix = float(scaleValue)
	
	def Parameter11(self,scaleValue):                          # empty function parameter passing
		parameters.fuzzy_gain = float(scaleValue)

	def Parameter12(self,scaleValue):                          # empty function parameter passing
		print float(scaleValue)


	def callback(self):
		self.root.quit()

	def run(self):
		self.root = Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.callback)
		self.root.geometry("1000x480+300+200")
		self.root.title("Guitar Effect Box")
		self.v = StringVar()
		self.v.set("Normal")

		self.s = [0 for n in range(0, 12)]
		for n in range(0,12):
			self.s[n] = DoubleVar()
			self.s[n].set(0.0)
		
		label = Label(self.root, text="DSP final project Guitar Effect Box ver.prototype")	#Title
		label.pack(anchor=N, fill=X, expand=False)

		frame0 = Frame(self.root, relief = RAISED, borderwidth = 2)
		frame3 = Frame(self.root, relief = RAISED, borderwidth = 2)
		frame1 = Frame(frame3, relief = RAISED, borderwidth = 2)
		frame2 = Frame(frame3, relief = RAISED, borderwidth = 2)
		

		# Options using radio buttons
		rad0 = Radiobutton(frame0, text='Delay', value='Delay', variable=self.v, command=self.Pressed)
		rad1 = Radiobutton(frame0, text='Flanger', value='Flanger', variable=self.v, command=self.Pressed)
		rad2 = Radiobutton(frame0, text='WahWah', value='WahWah', variable=self.v, command=self.Pressed)
		rad3 = Radiobutton(frame0, text='Fuzzy', value='Fuzzy', variable=self.v, command=self.Pressed)
		rad4 = Radiobutton(frame0, text='Normal', value='Normal', variable=self.v, command=self.Pressed)
		rad9 = Radiobutton(frame0, text='Stop', value='Stop', variable=self.v, command=self.Pressed)
		
		scale0 = Scale(frame1, orient=VERTICAL, label='flanger_f', length=150, from_=200.0, to=1.0,
		 resolution=-1.0, variable=self.s[0], command=self.Parameter0)
		scale1 = Scale(frame1, orient=VERTICAL, label='flanger_w', length=150, from_=1.0, to=0.0,
		 resolution=-0.01, variable=self.s[1], command=self.Parameter1)
		scale2 = Scale(frame1, orient=VERTICAL, label='flanger_gain', length=150, from_=1.0, to=0.0,
		 resolution=-0.01, variable=self.s[2], command=self.Parameter2)
		scale3 = Scale(frame1, orient=VERTICAL, label='wahwah_f_lfo', length=150, from_=5, to=0.2,
		 resolution=-0.1, variable=self.s[3], command=self.Parameter3)
		scale4 = Scale(frame1, orient=VERTICAL, label='wahwah_fc_min', length=150, from_=500.0, to=250.0,
		 resolution=-1.0, variable=self.s[4], command=self.Parameter4)
		scale5 = Scale(frame1, orient=VERTICAL, label='wahwah_w', length=150, from_=0.2, to=0.001,
		 resolution=-0.005, variable=self.s[5], command=self.Parameter5)
		scale6 = Scale(frame1, orient=VERTICAL, label='delay_Gfb', length=150, from_=1.0, to=0.0,
		 resolution=-0.1, variable=self.s[6], command=self.Parameter6)
		scale7 = Scale(frame2, orient=VERTICAL, label='delay_Gdp', length=150, from_=1.0, to=0.0,
		 resolution=-0.1, variable=self.s[7], command=self.Parameter7)
		scale8 = Scale(frame2, orient=VERTICAL, label='delay_Gff', length=150, from_=1.0, to=0.0,
		 resolution=-0.1, variable=self.s[8], command=self.Parameter8)
		scale9 = Scale(frame2, orient=VERTICAL, label='delay_sec', length=150, from_=2.0, to=0.0,
		 resolution=-0.1, variable=self.s[9], command=self.Parameter9)
		scale10 = Scale(frame2, orient=VERTICAL, label='fuzzy_gain', length=150, from_=30.0, to=1.0,
		 resolution=-1.0, variable=self.s[10], command=self.Parameter10)
		scale11 = Scale(frame2, orient=VERTICAL, label='fuzzy_mix', length=150, from_=10.0, to=1.0,
		 resolution=-0.1, variable=self.s[11], command=self.Parameter11)
		scale12 = Scale(frame2, orient=VERTICAL, label='empty', length=150, from_=100.0, to=1.0,
		 resolution=-0.1, variable=parameters.GAIN, command=self.Parameter12)

		scale0.set(parameters.flanger_f)
		scale1.set(parameters.flanger_w)
		scale2.set(parameters.flanger_gain)
		scale3.set(parameters.wahwah_f_lfo)
		scale4.set(parameters.wahwah_fc_min)
		scale5.set(parameters.wahwah_w)
		scale6.set(parameters.delay_Gfb)
		scale7.set(parameters.delay_Gdp)
		scale8.set(parameters.delay_Gff)
		scale9.set(parameters.delay_sec)
		scale10.set(parameters.fuzzy_gain)
		scale11.set(parameters.fuzzy_mix)

		scale0.pack(side=RIGHT, expand=True)
		scale1.pack(side=RIGHT, expand=True)
		scale2.pack(side=RIGHT, expand=True)
		scale3.pack(side=RIGHT, expand=True)
		scale4.pack(side=RIGHT, expand=True)
		scale5.pack(side=RIGHT, expand=True)
		scale6.pack(side=RIGHT, expand=True)
		scale7.pack(side=RIGHT, expand=True)
		scale8.pack(side=RIGHT, expand=True)
		scale9.pack(side=RIGHT, expand=True)
		scale10.pack(side=RIGHT, expand=True)
		scale11.pack(side=RIGHT, expand=True)
		scale12.pack(side=RIGHT, expand=True)

		frame0.pack(side=RIGHT, anchor=N, fill=BOTH, expand=False)
		frame1.pack(side=TOP, anchor=N, fill=BOTH, expand=True)
		frame2.pack(side=TOP, anchor=N, fill=BOTH, expand=True)
		frame3.pack(side=RIGHT, anchor=W, fill=BOTH, expand=True)
		
		rad0.pack(side=TOP, anchor=N, fill=X, expand=True)
		rad1.pack(side=TOP, anchor=N, fill=X, expand=True)
		rad2.pack(side=TOP, anchor=N, fill=X, expand=True)
		rad3.pack(side=TOP, anchor=N, fill=X, expand=True)
		rad4.pack(side=TOP, anchor=N, fill=X, expand=True)
		rad9.pack(side=TOP, anchor=N, fill=X, expand=True)
		self.root.mainloop()

app = App()

print('Now we can continue running code while mainloop runs!')
############

######  wah_version_2 ######
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=3):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def wah_effect():
	RECORD_SECONDS = 500
	BLOCKSIZE = 1024     # Number of frames per block

	gain = 1
	fc_max = 1200 # initial

	p = pyaudio.PyAudio()
	WIDTH = 2           # bytes per sample
	RATE = 44100    # Sampling rate (samples/second)

	stream = p.open(format = p.get_format_from_width(WIDTH),
					channels = 2,
					rate = RATE,
					input = True,
					output = True)

	# Create a buffer (delay line) for past values
	# Create block (initialize to zero)
	output_block = [0.0 for n in range(0, 2*BLOCKSIZE)]
	output_block_filt = [0.0 for n in range(0, 2*BLOCKSIZE)]
	bandpass = [0.0 for n in range(0, 2*BLOCKSIZE)]
	mix = [0.0 for n in range(0, 2*BLOCKSIZE)]

	# Create a buffer (delay line) for past values
	buffer = [0.0 for i in range(BLOCKSIZE)]   # Initialize to zero
	buffer2 = [0.0 for i in range(BLOCKSIZE)]   # Initialize to zero

	# Buffer (delay line) indices
	kr = 0  # read index
	kw = int(0.5 * BLOCKSIZE)  # write index (initialize to middle of buffer)
	kw = BLOCKSIZE/2

	output_all = ''            # output signal in all (string)
	fc_bandpass = 0.0

	# Initialize angle
	theta = 0.0

	num_blocks = int(RATE / BLOCKSIZE * RECORD_SECONDS)

	print ('**** Playing Auto-Wah ****')

    # Loop through wave file 
	for i in range(0, num_blocks):
		if app.MODE != "WahWah":
			break
		# Block-to-block angle increment <----reduce calculation
		theta_del = (float(BLOCKSIZE*parameters.wahwah_f_lfo)/RATE - math.floor(BLOCKSIZE*parameters.wahwah_f_lfo/RATE)) * 2.0 * math.pi

		# Get sample from wave file
		input_string = stream.read(BLOCKSIZE)

		# Convert string to number
		input_value = struct.unpack('hh'* BLOCKSIZE, input_string)
		bandpass = butter_bandpass_filter(input_value,parameters.wahwah_fc_min,fc_max,RATE,order = 1)

		# Go through block
		for n in range(0, BLOCKSIZE):

			# Amplitude modulation  (f0 Hz cosine)
			# Get previous and next buffer values (since kr is fractional)
			kr_prev = int(math.floor(kr))               
			kr_next = kr_prev + 1
			frac = kr - kr_prev    # 0 <= frac < 1
			#print frac
			if kr_next >= BLOCKSIZE:
			    kr_next = kr_next - BLOCKSIZE

			# Compute output value using interpolation
			k = buffer[kr_prev] * (1-frac)
			r = buffer[kr_next] * frac
			k2 = buffer2[kr_prev] * (1-frac)
			r2 = buffer2[kr_next] * frac

			output_block[2*n] = k + r + k2 +r2
			output_block[2*n] = clip16(output_block[2*n])
			output_block[2*n+1] = output_block[2*n]

			# buffer

			buffer[kw] = input_value[2*n]
			buffer2[kw] = bandpass[2*n]
			# Increment read index
			kr = kr + 1 + parameters.wahwah_w * math.sin( 2 * math.pi * parameters.wahwah_f_lfo * n  / RATE + theta)     
			# Note: kr is fractional (not integer!)

			# Ensure that 0 <= kr < buffer_MAX
			if kr >= BLOCKSIZE:
			# End of buffer. Circle back to front.
				kr = 0
            # Increment write index    
			kw = kw + 1
			if kw == BLOCKSIZE:
			# End of buffer. Circle back to front.
				kw = 0

			fc_bandpass = parameters.wahwah_fc_min + 0.5 * parameters.wahwah_w * (1 + math.sin(2 * math.pi * parameters.wahwah_f_lfo * n /RATE ))
			f_max = 2 * fc_bandpass + parameters.wahwah_fc_min

		theta = theta + theta_del

		output_string = struct.pack('hh'* BLOCKSIZE , *output_block)

		# Write output to audio stream
		stream.write(output_string)

		output_all = output_all + output_string


	print('* Done')

	stream.stop_stream()
	stream.close()
	p.terminate()

def delay_effect(Gfb,Gdp,Gff,delay_sec):
	BLOCKSIZE = 1024     # Number of frames per block

	RECORD_SECONDS = 500
	# delay_sec = 0.5
	p = pyaudio.PyAudio()
	WIDTH = 2           # bytes per sample
	RATE = 44100    # Sampling rate (samples/second)

	parameters.d = int( math.floor( RATE * parameters.delay_sec ) ) 
	# Open an output audio stream
	p = pyaudio.PyAudio()
	stream = p.open(format      = p.get_format_from_width(WIDTH),
					channels    = 2,
					rate        = RATE,
					input       = True,
					output      = True )

	output_block = [0.0 for n in range(0, 2*BLOCKSIZE)]
	delay_buff = [0.0 for n in range(0, parameters.d)]
	num_blocks = int(RATE / BLOCKSIZE * RECORD_SECONDS)
	k = 0

	print ("**** Playing Delay effect****")

	for i in range(0, num_blocks):
		if app.MODE != "Delay":
			break
		# Get sample from wave file
		input_string = stream.read(BLOCKSIZE)

		# Convert string to number
		input_value = struct.unpack('hh'* BLOCKSIZE, input_string)

		for n in range(0, BLOCKSIZE):

			# Update buffer
			delay_buff[k] = input_value[2*n] + parameters.delay_Gfb * delay_buff[k]
			k = k + 1
			if k >= parameters.d:
				# We have reached the end of the buffer. Circle back to front.
				k = 0
			output_block[2*n] = parameters.delay_Gdp * input_value[2*n] + parameters.delay_Gff * delay_buff[k];
			output_block[2*n] = clip16(output_block[2*n])
			output_block[2*n+1] = clip16(output_block[2*n])

		# Clip output value to 16 bits and convert to binary string
		output_string = struct.pack('hh'* BLOCKSIZE , *output_block)

		# Write output value to audio stream
		stream.write(output_string)

	print("**** Done ****")

	stream.stop_stream()
	stream.close()
	p.terminate()


def flanger_effect():

	BLOCKSIZE = 1024      # Number of frames per block

	RECORD_SECONDS = 500
	p = pyaudio.PyAudio()
	WIDTH = 2           # bytes per sample
	RATE = 44100    # Sampling rate (samples/second)

	stream = p.open(format = 	p.get_format_from_width(WIDTH),
					channels = 	2,
					rate = 		RATE,
					input = 	True,
					output = 	True)

	# Create a buffer (delay line) for past values
	# Create block (initialize to zero)
	output_block = [0.0 for n in range(0, 2*BLOCKSIZE)]

	# Number of blocks in wave file
	num_blocks = int(RATE / BLOCKSIZE * RECORD_SECONDS)
	# Create a buffer (delay line) for past values
	# buffer_MAX =  1024                          # Buffer length
	buffer = [0.0 for i in range(BLOCKSIZE)]   # Initialize to zero

	# Buffer (delay line) indices
	kr = 0  # read index
	kw = int(0.5 * BLOCKSIZE)  # write index (initialize to middle of buffer)
	kw = BLOCKSIZE/2

	output_all = ''            # output signal in all (string)

	# Initialize angle
	theta = 0.0

	

	print ('**** Playing Flanger effect****')

	# Loop through wave file 
	for i in range(0, num_blocks):
		# Block-to-block angle increment
		theta_del = (float(BLOCKSIZE*parameters.flanger_f)/RATE - math.floor(BLOCKSIZE*parameters.flanger_f/RATE)) * 2.0 * math.pi
		
		if app.MODE != "Flanger":
			break
		# Get sample from wave file
		input_string = stream.read(BLOCKSIZE)

		# Convert string to number
		input_value = struct.unpack('hh'* BLOCKSIZE, input_string)

		# Go through block
		for n in range(0, BLOCKSIZE):
			# Amplitude modulation  (f0 Hz cosine)
			# Get previous and next buffer values (since kr is fractional)
			kr_prev = int(math.floor(kr))               
			kr_next = kr_prev + 1
			frac = kr - kr_prev    # 0 <= frac < 1
			#print frac
			if kr_next >= BLOCKSIZE:
				kr_next = kr_next - BLOCKSIZE

			# Compute output value using interpolation
			k = buffer[kr_prev] * (1-frac)
			r = buffer[kr_next] * frac

			output_block[2*n] = k + r + input_value[2*n] * parameters.flanger_gain

			output_block[2*n] = clip16(output_block[2*n])
			output_block[2*n+1] = output_block[2*n]

			# buffer
			# print '--------------'
			buffer[kw] = input_value[2*n]

			# Increment read index
			kr = kr + 1 + parameters.flanger_w * math.sin( 2 * math.pi * parameters.flanger_f * n  / RATE + theta)
			# Note: kr is fractional (not integer!)

			# Ensure that 0 <= kr < buffer_MAX
			if kr >= BLOCKSIZE:
			# End of buffer. Circle back to front.
				kr = 0
			# Increment write index    
			kw = kw + 1
			if kw == BLOCKSIZE:
			 # End of buffer. Circle back to front.
				kw = 0

		theta1 = theta + theta_del
		# print output_block

		output_string = struct.pack('hh'* BLOCKSIZE , *output_block)

		# Write output to audio stream
		stream.write(output_string)

		output_all = output_all + output_string


	print('* Done')

	stream.stop_stream()
	stream.close()
	p.terminate()

def get_type_convert(np_type):
   convert_type = type(np.zeros(1,np_type).tolist()[0])
   return (convert_type)

def fuzz_effect():
	RECORD_SECONDS = 500
	BLOCKSIZE = 1024     # Number of frames per block
	p = pyaudio.PyAudio()
	WIDTH = 2           # bytes per sample
	RATE = 44100    # Sampling rate (samples/second)

	stream = p.open(format = p.get_format_from_width(WIDTH),
					channels = 2,
					rate = RATE,
					input = True,
					output = True)

	output_block = [0.0 for n in range(0, 2*BLOCKSIZE)]

	q = 0.0
	X = 0.0	
	y = 0.0
	z = 0.000001
	r = 0.0
	max_z = 0.000001
	max_r = 0

	output_all = ''            # output signal in all (string)
	num_blocks = int(RATE / BLOCKSIZE * RECORD_SECONDS)
	print ('#####  playing Fuzzy #####')

	# Loop through wave file 
	for i in range(0, num_blocks):
		if app.MODE != "Fuzzy":
			break
		# Get sample from wave file
		input_string = stream.read(BLOCKSIZE)

		# Convert string to number
		input_value = struct.unpack('hh'* BLOCKSIZE, input_string)

		X = np.fft.fft(input_value)
		max_val = abs(np.max(X))
		max_val = max_val.item()

		for n in range(0, BLOCKSIZE):
			x = input_value[2*n]
			q = x * parameters.fuzzy_gain / max_val

			if q == 0:
				z = 0
			else:
				z = -q/abs(q) * (1 - math.exp(-q*q/abs(q)))

			if z > max_z:
				max_z = z
				
			r = parameters.fuzzy_mix * z * max_val / abs(max_z) + (1 - parameters.fuzzy_mix) * x
			# k = np.asscalar(r)
			if r > max_r:
				max_r = r

			if abs(max_r) ==0:
				out = 0
			else:
				out = r * abs(x) / abs(max_r)
			
			output_block[2*n] = clip16_flt(out)
			output_block[2*n+1] = clip16_flt(out)

		output_string = struct.pack('hh'* BLOCKSIZE , *output_block)

		# Write output to audio stream
		stream.write(output_string)

		output_all = output_all + output_string

	print('* Done')

	stream.stop_stream()
	stream.close()
	p.terminate()

# time.sleep(10)
# print "Final Mode is ", app.MODE
print_Normal_counter = 1
print_WahWah_counter = 1
print_Flanger_counter = 1
print_Delay_counter = 1
print_Fuzzy_counter = 1
time.sleep(3)
print "loop started..."

while(1):
	if app.MODE == "Stop":
		print "loop broken"
		break

	if app.MODE == "Normal":
		# reset counters
		print_WahWah_counter = 1
		print_Flanger_counter = 1
		print_Delay_counter = 1
		print_Fuzzy_counter = 1
		
		if print_Normal_counter == 1:	# print only one time
			print app.MODE
			print_Normal_counter = 0

	if app.MODE == "WahWah":
		# reset counters
		print_Normal_counter = 1
		print_Flanger_counter = 1
		print_Delay_counter = 1
		print_Fuzzy_counter = 1

		if print_WahWah_counter == 1:	# print only one time
			print app.MODE
			wah_effect()
			print_WahWah_counter = 0

	if app.MODE == "Flanger":
		# reset counters
		print_Normal_counter = 1
		print_WahWah_counter = 1
		print_Delay_counter = 1
		print_Fuzzy_counter = 1

		if print_Flanger_counter == 1:	# print only one time
			print app.MODE
			flanger_effect()
			print_Flanger_counter = 0

	if app.MODE == "Delay":
		# reset counters
		print_Normal_counter = 1
		print_WahWah_counter = 1
		print_Flanger_counter = 1
		print_Fuzzy_counter = 1

		if print_Delay_counter == 1:	# print only one time
			print app.MODE
			delay_effect(0.55,1.0,0.5,0.5)
			print_Delay_counter = 0

	if app.MODE == "Fuzzy":
		# reset counters
		print_Normal_counter = 1
		print_WahWah_counter = 1
		print_Flanger_counter = 1
		print_Delay_counter = 1

		if print_Fuzzy_counter == 1:	# print only one time
			print app.MODE
			fuzz_effect()
			print_Fuzzy_counter = 0

print "Program Ended"	
