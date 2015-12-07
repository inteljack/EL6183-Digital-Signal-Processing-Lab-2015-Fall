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

class App(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.MODE = "Normal"
		print "Initial Mode is ", self.MODE
		self.start()
	
	def Pressed(self):                          #function
		self.MODE = self.v.get()
		# print self.v.get()

	def Parameter1(self,scaleValue):                          #function
		f = float(self.s1.get())
		w = 0.5
		print "Parameter1 is :", f
		
	def Parameter2(self,scaleValue):                          #function
		print "Parameter2 is :", float(self.s2.get())

	def Parameter3(self,scaleValue):                          #function
		print "Parameter3 is :", float(self.s3.get())

	def callback(self):
		self.root.quit()

	def run(self):
		self.root = Tk()
		self.root.protocol("WM_DELETE_WINDOW", self.callback)
		self.root.geometry("500x280+300+300")

		self.v = StringVar()
		self.v.set("Normal")
		self.s1 = DoubleVar()
		self.s1.set(0.0)
		self.s2 = DoubleVar()
		self.s2.set(0.0)
		self.s3 = DoubleVar()
		self.s3.set(0.0)

		label = Label(self.root, text="Hello World")	#Title
		label.pack(anchor=N, fill=X, expand=False)

		# Options using radio buttons
		rad0 = Radiobutton(self.root, text='Delay', value='Delay', variable=self.v, command=self.Pressed)
		rad1 = Radiobutton(self.root, text='Flanger', value='Flanger', variable=self.v, command=self.Pressed)
		rad2 = Radiobutton(self.root, text='WahWah', value='WahWah', variable=self.v, command=self.Pressed)
		rad3 = Radiobutton(self.root, text='Normal', value='Normal', variable=self.v, command=self.Pressed)
		
		rad9 = Radiobutton(self.root, text='Stop', value='Stop', variable=self.v, command=self.Pressed)
		
		frame = Frame(self.root, relief = RAISED, borderwidth = 2)
		# gui = Radiobar(root, ['flanger', 'WahWah', 'Normal'], side=TOP, anchor=NW)
		# gui.pack(side=RIGHT, fill=Y)
		# gui.config(relief=RIDGE,  bd=2)

		# button1 = Button(root, text = 'Press', command = Pressed)
		# button1.pack(side = RIGHT, pady = 5, padx = 5)
		# button2 = Button(root, text = 'Press', command = Pressed)
		# button2.pack(side = RIGHT, pady = 5, padx = 5)

		# button = Button(root, text = 'Press me', command = Call)
		# button.pack()
		scale1 = Scale(frame, orient=HORIZONTAL, length=200, from_=1.0, to=100.0, resolution=0.1, variable=self.s1, command=self.Parameter1)
		scale2 = Scale(frame, orient=HORIZONTAL, length=200, from_=1.0, to=100.0, resolution=0.1, variable=self.s2, command=self.Parameter2)
		scale3 = Scale(frame, orient=HORIZONTAL, length=200, from_=1.0, to=100.0, resolution=0.1, variable=self.s3, command=self.Parameter3)

		scale1.pack(expand=True)
		scale2.pack(expand=True)
		scale3.pack(expand=True)
		frame.pack(side=LEFT, fill=BOTH, expand=True)
		rad0.pack(anchor=N, fill=X, expand=True)
		rad1.pack(anchor=N, fill=X, expand=True)
		rad2.pack(anchor=N, fill=X, expand=True)
		rad3.pack(anchor=N, fill=X, expand=True)
		rad9.pack(anchor=N, fill=X, expand=True)
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
    print ('* Playing...')

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

def delay_effect():
    BLOCKSIZE = 1024     # Number of frames per block

    RECORD_SECONDS = 20
    delay_sec = 0.5
    p = pyaudio.PyAudio()
    WIDTH = 2           # bytes per sample
    RATE = 44100    # Sampling rate (samples/second)

    d = int( math.floor( RATE * delay_sec ) ) 
    # Set parameters of delay system
    Gfb = .55       # feed-back gain
    Gdp = 1.0       # direct-path gain
    Gff = .500     # feed-forward gain (set to zero for no effect)

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

    print ("**** Playing ****")

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


def flanger_effect(f,w,gain,Go_NoGo):

    BLOCKSIZE = 1024      # Number of frames per block

    RECORD_SECONDS = 10
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

    print ('* Playing...')

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
		
		if print_Normal_counter == 1:	# print only one time
			print app.MODE
			print_Normal_counter = 0

	if app.MODE == "WahWah":
		# reset counters
		print_Normal_counter = 1
		print_Flanger_counter = 1
		print_Delay_counter = 1

		if print_WahWah_counter == 1:	# print only one time
			print app.MODE
			wah_effect(2000,0.05)
			print_WahWah_counter = 0

	if app.MODE == "Flanger":
		# reset counters
		print_Normal_counter = 1
		print_WahWah_counter = 1
		print_Delay_counter = 1

		if print_Flanger_counter == 1:	# print only one time
			print app.MODE
			flanger_effect(50,0.5,1.2,1)
			print_Flanger_counter = 0

	if app.MODE == "Delay":
		# reset counters
		print_Normal_counter = 1
		print_WahWah_counter = 1
		print_Flanger_counter = 1

		if print_Delay_counter == 1:	# print only one time
			print app.MODE
			delay_effect()
			print_Delay_counter = 0

print "Program Ended"	
