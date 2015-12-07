from Tkinter import *
from flanger import *
import threading
import time
# from ttk import *

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
		rad1 = Radiobutton(self.root, text='Flanger', value='Flanger', variable=self.v, command=self.Pressed)
		rad2 = Radiobutton(self.root, text='WahWah', value='WahWah', variable=self.v, command=self.Pressed)
		rad3 = Radiobutton(self.root, text='Normal', value='Normal', variable=self.v, command=self.Pressed)
		rad4 = Radiobutton(self.root, text='Stop', value='Stop', variable=self.v, command=self.Pressed)
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
		rad1.pack(anchor=N, fill=X, expand=True)
		rad2.pack(anchor=N, fill=X, expand=True)
		rad3.pack(anchor=N, fill=X, expand=True)
		rad4.pack(anchor=N, fill=X, expand=True)
		self.root.mainloop()


app = App()

print('Now we can continue running code while mainloop runs!')

# time.sleep(10)
# print "Final Mode is ", app.MODE
print_Normal_counter = 1
print_WahWah_counter = 1
print_Flanger_counter = 1

while(1):
	if app.MODE == "Stop":
		print "loop broken"
		break

	if app.MODE == "Normal":
		# reset counters
		print_WahWah_counter = 1
		print_Flanger_counter = 1
		
		if print_Normal_counter == 1:	# print only one time
			print app.MODE
			print_Normal_counter = 0

	if app.MODE == "WahWah":
		# reset counters
		print_Normal_counter = 1
		print_Flanger_counter = 1

		if print_WahWah_counter == 1:	# print only one time
			print app.MODE
			print_WahWah_counter = 0

	if app.MODE == "Flanger":
		# reset counters
		print_Normal_counter = 1
		print_WahWah_counter = 1

		if print_Flanger_counter == 1:	# print only one time
			print app.MODE
			print_Flanger_counter = 0



print "Program Ended"	


# p = pyaudio.PyAudio()
# WIDTH = 2           # bytes per sample
# RATE = 44100    # Sampling rate (samples/second)

# # number_of_devices = p.get_device_count()
# # print('There are {0:d} devices'.format(number_of_devices))
# # property_list = ['defaultSampleRate', 'maxInputChannels', 'maxOutputChannels']
# # for i in range(0, number_of_devices):
# #     print('Device {0:d} has:'.format(i))
# #     for s in property_list:
# #         print ' ', s, '=', p.get_device_info_by_index(i)[s]

# stream = p.open(format = p.get_format_from_width(WIDTH),
# 				channels = 2,
# 				rate = RATE,
# 				input = True,
# 				output = True)
# output_block = [0.0 for n in range(0, 2*BLOCKSIZE)]

# buffer = [0.0 for i in range(BLOCKSIZE)]   # Initialize to zero

# # Buffer (delay line) indices
# kr = 0  # read index
# kw = int(0.5 * BLOCKSIZE)  # write index (initialize to middle of buffer)
# kw = BLOCKSIZE/2

# output_all = ''            # output signal in all (string)

# # Initialize angle
# theta = 0.0

# # Block-to-block angle increment
# theta_del = (float(BLOCKSIZE*f)/RATE - math.floor(BLOCKSIZE*f/RATE)) * 2.0 * math.pi

# print ('* Playing...')








# # Loop through wave file 
# while(1):

# 	# Get sample from wave file
# 	input_string = stream.read(BLOCKSIZE)

# 	# Convert string to number
# 	input_value = struct.unpack('hh'* BLOCKSIZE, input_string)

# 	# Go through block
# 	for n in range(0, BLOCKSIZE):
# 		# Amplitude modulation  (f0 Hz cosine)
# 		# Get previous and next buffer values (since kr is fractional)
# 		kr_prev = int(math.floor(kr))               
# 		kr_next = kr_prev + 1
# 		frac = kr - kr_prev    # 0 <= frac < 1

# 		if kr_next >= BLOCKSIZE:
# 			kr_next = kr_next - BLOCKSIZE

# 		# Compute output value using interpolation
# 		k = buffer[kr_prev] * (1-frac)
# 		r = buffer[kr_next] * frac

# 		output_block[2*n] = k + r + input_value[2*n] * gain

# 		output_block[2*n] = clip16(output_block[2*n])
# 		output_block[2*n+1] = output_block[2*n]

# 		# buffer
# 		# print '--------------'
# 		buffer[kw] = input_value[2*n]

# 		# Increment read index
# 		kr = kr + 1 + w * math.sin( 2 * math.pi * f * n  / RATE + theta)     
# 		# Note: kr is fractional (not integer!)

# 		# Ensure that 0 <= kr < buffer_MAX
# 		if kr >= BLOCKSIZE:
# 		# End of buffer. Circle back to front.
# 			kr = 0
# 		# Increment write index    
# 		kw = kw + 1
# 		if kw == BLOCKSIZE:
# 		 # End of buffer. Circle back to front.
# 			kw = 0

# 	theta1 = theta + theta_del
# 	# print output_block

# 	output_string = struct.pack('hh'* BLOCKSIZE , *output_block)

# 	# Write output to audio stream
# 	stream.write(output_string)

# 	output_all = output_all + output_string


# print('* Done')

# stream.stop_stream()
# stream.close()
# p.terminate()