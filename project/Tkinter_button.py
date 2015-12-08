from Tkinter import *
from flanger import *
import threading
import time

import pyaudio
import struct
import math
from myfunctions import clip16,clip16_arr
from scipy.signal import butter, lfilter

#####Color table#####
RED = (200,0,0)
GREEN = (0,200,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (200,200,200)

class Parameters():
	def __init__(self):
		# initialize all parameter values
		self.GAIN = 0.5

		# parameter for Delay effect
		self.delay_Gfb = 0.55
		self.delay_Gdp = 1
		self.delay_Gff = 0.5
		self.delay_sec = 0.5

		# parameter for Flanger effect
		self.flanger_f = 50
		self.flanger_w = 0.5

		# parameter for WahWah effect
		self.wahwah_w = 0.05
		self.wahwah_f_lfo = 2
		self.wahwah_fc_min = 1000

	def Print_prmtr(self):
		print self.GAIN

parameters = Parameters()

class App(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.MODE = "Normal"
		print "Initial Mode is ", self.MODE
		self.start()
	
	def Pressed(self):                          #function
		self.MODE = self.v.get()
		# print self.v.get()


	def Parameter0(self,scaleValue):                          #function
		print float(scaleValue)

	def Parameter1(self,scaleValue):                          #function
		print float(scaleValue)
	
	def Parameter2(self,scaleValue):                          #function
		float(scaleValue)

	def Parameter3(self,scaleValue):                          #function
		float(scaleValue)

	def Parameter4(self,scaleValue):                          #function
		float(scaleValue)
	
	def Parameter5(self,scaleValue):                          #function
		float(scaleValue)

	def Parameter6(self,scaleValue):                          #function
		float(scaleValue)
	
	def Parameter7(self,scaleValue):                          #function
		float(scaleValue)

	def Parameter8(self,scaleValue):                          #function
		float(scaleValue)
	
	def Parameter9(self,scaleValue):                          #function
		float(scaleValue)

	def Parameter10(self,scaleValue):                          #function
		float(scaleValue)
	
	def Parameter11(self,scaleValue):                          #function
		float(scaleValue)

	def Parameter12(self,scaleValue):                          #function
		print float(scaleValue)
	# def Parameter2(self,scaleValue):                          #function
	# 	print "Parameter2 is :", float(self.s2.get())

	# def Parameter3(self,scaleValue):                          #function
	# 	print "Parameter3 is :", float(self.s3.get())






	def callback(self):
		self.root.quit()

	def run(self):
		self.root = Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.callback)
		self.root.geometry("500x280+300+300")

		self.v = StringVar()
		self.v.set("Normal")

		self.s = [0 for n in range(0, 12)]
		for n in range(0,12):
			self.s[n] = DoubleVar()
			self.s[n].set(0.0)
		
		# self.s0 = DoubleVar()
		# self.s0.set(0.0)
		# self.s1 = DoubleVar()
		# self.s1.set(0.0)
		# self.s2 = DoubleVar()
		# self.s2.set(0.0)
		# self.s3 = DoubleVar()
		# self.s3.set(0.0)
		# self.s4 = DoubleVar()
		# self.s4.set(0.0)
		# self.s5 = DoubleVar()
		# self.s5.set(0.0)
		# self.s6 = DoubleVar()
		# self.s6.set(0.0)
		# self.s7 = DoubleVar()
		# self.s7.set(0.0)
		# self.s8 = DoubleVar()
		# self.s8.set(0.0)
		# self.s9 = DoubleVar()
		# self.s9.set(0.0)
		# self.s10 = DoubleVar()
		# self.s10.set(0.0)
		# self.s11 = DoubleVar()
		# self.s11.set(0.0)
		# self.s12 = DoubleVar()
		# self.s12.set(0.0)

		label = Label(self.root, text="Hello World")	#Title
		label.pack(anchor=N, fill=X, expand=False)

		frame0 = Frame(self.root, relief = RAISED, borderwidth = 2)
		frame1 = Frame(self.root, relief = RAISED, borderwidth = 2)
		frame2 = Frame(self.root, relief = RAISED, borderwidth = 2)

		# Options using radio buttons
		rad0 = Radiobutton(frame0, text='Delay', value='Delay', variable=self.v, command=self.Pressed)
		rad1 = Radiobutton(frame0, text='Flanger', value='Flanger', variable=self.v, command=self.Pressed)
		rad2 = Radiobutton(frame0, text='WahWah', value='WahWah', variable=self.v, command=self.Pressed)
		rad3 = Radiobutton(frame0, text='Fuzzy', value='Fuzzy', variable=self.v, command=self.Pressed)
		rad4 = Radiobutton(frame0, text='Normal', value='Normal', variable=self.v, command=self.Pressed)
		rad9 = Radiobutton(frame0, text='Stop', value='Stop', variable=self.v, command=self.Pressed)
		

		# gui = Radiobar(root, ['flanger', 'WahWah', 'Normal'], side=TOP, anchor=NW)
		# gui.pack(side=RIGHT, fill=Y)
		# gui.config(relief=RIDGE,  bd=2)

		# button1 = Button(root, text = 'Press', command = Pressed)
		# button1.pack(side = RIGHT, pady = 5, padx = 5)
		# button2 = Button(root, text = 'Press', command = Pressed)
		# button2.pack(side = RIGHT, pady = 5, padx = 5)

		# button = Button(root, text = 'Press me', command = Call)
		# button.pack()
		scale0 = Scale(frame1, orient=HORIZONTAL, label='scale0', length=200, from_=1.0, to=100.0,
		 resolution=0.1, variable=self.s[0], command=self.Parameter0)
		scale1 = Scale(frame1, orient=HORIZONTAL, label='scale1', length=200, from_=1.0, to=100.0,
		 resolution=0.1, variable=self.s[1], command=self.Parameter1)
		scale2 = Scale(frame1, orient=HORIZONTAL, label='scale2', length=200, from_=1.0, to=100.0,
		 resolution=0.1, variable=self.s[2], command=self.Parameter2)
		scale3 = Scale(frame1, orient=HORIZONTAL, label='scale3', length=200, from_=1.0, to=100.0,
		 resolution=0.1, variable=parameters.GAIN, command=self.Parameter12)

		scale0.pack(expand=True)
		scale1.pack(expand=True)
		scale2.pack(expand=True)
		scale3.pack(expand=True)
		frame0.pack(side=RIGHT, anchor=N, fill=BOTH, expand=False)
		frame1.pack(side=TOP, anchor=W, fill=BOTH, expand=True)
		frame2.pack(side=TOP, anchor=W, fill=BOTH, expand=True)
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

def wah_effect(fw,damp):

	RECORD_SECONDS = 15
	BLOCKSIZE = 1024     # Number of frames per block
	p = pyaudio.PyAudio()
	WIDTH = 2           # bytes per sample
	RATE = 44100    # Sampling rate (samples/second)

	# damp = 0.015
	gain = 1
	# w = 1
	# f = 1
	fw_min = 300
	fw_max = 9000
	# fw = 2000
	delta = fw / RATE

	stream = p.open(format = p.get_format_from_width(WIDTH),
					channels = 2,
					rate = RATE,
					input = True,
					output = True)

	# Create a buffer (delay line) for past values
	# Create block (initialize to zero)
	yh = [0.0 for n in range(0, 2*BLOCKSIZE)]
	yb = [0.0 for n in range(0, 2*BLOCKSIZE)]
	yl = [0.0 for n in range(0, 2*BLOCKSIZE)]

	output_block = [0.0 for n in range(0, 2*BLOCKSIZE)]
	output_all = ''            # output signal in all (string)

	num_blocks = int(RATE / BLOCKSIZE * RECORD_SECONDS)
	print ('**** Playing WahWah effect****')

	# Loop through wave file 
	for i in range(0, num_blocks):
		if app.MODE != "WahWah":
			break
		# Get sample from wave file
		input_string = stream.read(BLOCKSIZE)

		# Convert string to number
		input_value = struct.unpack('hh'* BLOCKSIZE, input_string)
		fc = fw_min
		f1 = 2 * math.sin(math.pi*fc/RATE)

        # Go through block
		for n in range(0, BLOCKSIZE):

			if fc >= fw_max:
				delta = -delta
			if fc <= fw_min:
				delta = -delta

			f1 = 2 * math.sin(math.pi*fc/RATE)
			Q1 = 2 * damp

			yh[2*n] = input_value[2*n] - yl[2*(n-1)] - Q1 * yb[2*(n-1)]
			yb[2*n] = f1 * yh[2*n] + yb[2*(n-1)]
			yl[2*n] = f1 * yb[2*n] + yl[2*(n-1)]

			fc = fc + delta
			yb[2*n] = clip16(yb[2*n])
			yb[2*n+1] = clip16(yb[2*n])

		output_string = struct.pack('hh'* BLOCKSIZE , *yb)

		# Write output to audio stream
		stream.write(output_string)

		output_all = output_all + output_string

	print('* Done')

	stream.stop_stream()
	stream.close()
	p.terminate()

def delay_effect(Gfb,Gdp,Gff,delay_sec):
	BLOCKSIZE = 1024     # Number of frames per block

	RECORD_SECONDS = 20
	# delay_sec = 0.5
	p = pyaudio.PyAudio()
	WIDTH = 2           # bytes per sample
	RATE = 44100    # Sampling rate (samples/second)

	d = int( math.floor( RATE * delay_sec ) ) 
	# Set parameters of delay system
	# Gfb = .55       # feed-back gain
	# Gdp = 1.0       # direct-path gain
	# Gff = .500     # feed-forward gain (set to zero for no effect)

	# Open an output audio stream
	p = pyaudio.PyAudio()
	stream = p.open(format      = p.get_format_from_width(WIDTH),
					channels    = 2,
					rate        = RATE,
					input       = True,
					output      = True )

	output_block = [0.0 for n in range(0, 2*BLOCKSIZE)]
	delay_buff = [0.0 for n in range(0, d)]
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
			delay_buff[k] = input_value[2*n] + Gfb * delay_buff[k]
			k = k + 1
			if k == d:
				# We have reached the end of the buffer. Circle back to front.
				k = 0
			output_block[2*n] = Gdp * input_value[2*n] + Gff * delay_buff[k];
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


def flanger_effect(f,w,gain):

	BLOCKSIZE = 1024      # Number of frames per block

	RECORD_SECONDS = 10
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

	# Block-to-block angle increment
	theta_del = (float(BLOCKSIZE*f)/RATE - math.floor(BLOCKSIZE*f/RATE)) * 2.0 * math.pi

	print ('**** Playing Flanger effect****')

	# Loop through wave file 
	for i in range(0, num_blocks):
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

			output_block[2*n] = k + r + input_value[2*n] * gain

			output_block[2*n] = clip16(output_block[2*n])
			output_block[2*n+1] = output_block[2*n]

			# buffer
			# print '--------------'
			buffer[kw] = input_value[2*n]

			# Increment read index
			kr = kr + 1 + w * math.sin( 2 * math.pi * f * n  / RATE + theta)     
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

# time.sleep(10)
# print "Final Mode is ", app.MODE
print_Normal_counter = 1
print_WahWah_counter = 1
print_Flanger_counter = 1
print_Delay_counter = 1
print_Fuzzy_counter = 1
time.sleep(3)

while(1):
	if app.MODE == "Stop":
		print "loop broken"
		break

	if app.MODE == "Normal":
		# reset counters
		print_WahWah_counter = 1
		print_Flanger_counter = 1
		print_Delay_counter = 1
		print_Fuzzy_counter == 1
		
		if print_Normal_counter == 1:	# print only one time
			print app.MODE
			print_Normal_counter = 0

	if app.MODE == "WahWah":
		# reset counters
		print_Normal_counter = 1
		print_Flanger_counter = 1
		print_Delay_counter = 1
		print_Fuzzy_counter == 1

		if print_WahWah_counter == 1:	# print only one time
			print app.MODE
			wah_effect(2000,0.05)
			print_WahWah_counter = 0

	if app.MODE == "Flanger":
		# reset counters
		print_Normal_counter = 1
		print_WahWah_counter = 1
		print_Delay_counter = 1
		print_Fuzzy_counter == 1

		if print_Flanger_counter == 1:	# print only one time
			print app.MODE
			flanger_effect(50,0.5,1.2)
			print_Flanger_counter = 0

	if app.MODE == "Delay":
		# reset counters
		print_Normal_counter = 1
		print_WahWah_counter = 1
		print_Flanger_counter = 1
		print_Fuzzy_counter == 1

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
			fuzzy_effect()
			print_Fuzzy_counter = 0

print "Program Ended"	
