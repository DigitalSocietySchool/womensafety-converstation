from Tkinter import *
import PIL
import sys
import wave
import getopt
import alsaaudio
from PIL import Image, ImageTk
import time
from os import system, path
import os.path
from tkFileDialog import askopenfilename
import threading
import getopt
#from playwav import player
import time
import RPi.GPIO as GPIO
import tkFont

playThread = None
completed = True
solution = 9
base = 150.0
Option = []
Archive = []
root = question = section = option = None
selected = []
buttonVar = None
slide = sliderImage = None
currentImage = '1lang_r.png'
speaker =  speakerImage = speakerButton = None
buttonFunction = []
slideNames = []
slideCounter = 0
reportString = [0 for i in range(0, 11)]
currentSelection = 0
reports = []
thumbSize = [None for i in range(0, 11)]
thumbnail = [None for i in range(0, 11)]
thumb = [None for i in range(0, 11)]
outfile = None
reportIndex = 0
continueRecording = False
playFilename = ''

def play(device, f):

    global completed
    sys.stdout.write('%d channels, %d sampling rate\n' % (f.getnchannels(),
                                                          f.getframerate()))
    # Set attributes
    device.setchannels(f.getnchannels())
    device.setrate(f.getframerate())

    # 8bit is unsigned in wav files
    if f.getsampwidth() == 1:
        device.setformat(alsaaudio.PCM_FORMAT_U8)
    # Otherwise we assume signed data, little endian
    elif f.getsampwidth() == 2:
        device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    elif f.getsampwidth() == 3:
        device.setformat(alsaaudio.PCM_FORMAT_S24_LE)
    elif f.getsampwidth() == 4:
        device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
    else:
        raise ValueError('Unsupported format')

    device.setperiodsize(320)

    data = f.readframes(320)
    while data and not completed:
        # Read data from stdin
        device.write(data)
        data = f.readframes(320)

def player(filepath):

    card = 'default'

    opts, args = getopt.getopt(filepath[0:], 'c:')
    for o, a in opts:
        if o == '-c':
            card = a

    if not args:
        usage()

    f = wave.open(filepath, 'rb')
    device = alsaaudio.PCM(card=card)

    play(device, f)

    f.close()




def recordInto():
	global outputfilename
	global continueRecording
	card = 'default'
	f = wave.open(outputfilename, 'wb')
	f.setnchannels(1)
	f.setsampwidth(2)
	f.setframerate(44100)
	inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, card)
	inp.setchannels(1)
	inp.setrate(44100)

def recordingsDirectory():
	global outfile
	global reportIndex
	directory = sys.argv[1]
	if not os.path.exists(directory): os.mkdir(directory)
	outfile = open(directory+'/reportList', 'a')
	indexer = open(directory+'/reportList', 'r')
	for i in indexer:
		reportIndex = reportIndex + 1
	indexer.close()
	if reportIndex > 0:
		reportIndex = reportIndex - 1

def initButtonFunctions():
	global buttonFunction
	global slideNames
	for i in range(0, 5):
		buttonFunction.append('L'+str(i))
	for i in range(0, 5):
		buttonFunction.append('R'+str(i))
	
	metaSlides = open('slides/pimetaslides', 'r')
	for i in metaSlides:
		slideNames.append(i[:len(i)-1])
	metaSlides.close()

def playFile(filepath):
	print filepath
	global playThread
	player(filepath)
	playThread = None

def playAudio():
	global playFilename
	playFile(playFilename)

#-------------------------------Utilities to Refresh Screen------------------------------#
	

def loadImage():
	global root
	global base
	global slideImage
	global slide
	global currentImage
	global speaker
	global speakerImage
	global speakerButton
	reqdImage = Image.open('slides/'+currentImage)
	reqdImage = reqdImage.resize((1100, 1024), Image.ANTIALIAS)
        slideImage = ImageTk.PhotoImage(reqdImage)
        slide = Label(root, image = slideImage)
        #slide.grid(row = 5, column = 3)
	slide.place(x = 0, y = 0)
	
	speakerButton = Image.open('slides/speaker_r.png')
	speakerButton = speakerButton.resize((80, 1024), Image.ANTIALIAS)
	speakerImage = ImageTk.PhotoImage(speakerButton)
	speaker = Label(root, image = speakerImage)
	speaker.place(x = 1200, y = 0)

def updateStrip(selection):
	global slideNames
	global slideCounter
	global thumbSize
	global thumbnail
	global base
	global thumb
	if 2 <= slideCounter <= 12:
		question = slideNames[slideCounter]
		question = question[:len(question)-4]
		thumbSize[slideCounter-2] = Image.open('slides/thumbnails/'+question[:-2]+'/'+selection+'.png')
		thumbSize[slideCounter-2] = thumbSize[slideCounter-2].resize((100, 93), Image.ANTIALIAS)
		thumbnail[slideCounter-2] = ImageTk.PhotoImage(thumbSize[slideCounter-2])
		thumb[slideCounter-2] = Label(root, image = thumbnail[slideCounter-2])
		thumb[slideCounter-2].place(x = 1100, y = 927 - (slideCounter - 2)*93)

def clearThumbnails():
	global slideNames
        global slideCounter
        global thumbSize
        global thumbnail
        global thumb
	for i in range(0, len(thumb)):
		thumbnail[i] = ImageTk.PhotoImage(Image.open('slides/nothing.png'))
		thumb[i].config(image = thumbnail[i])

def recordReport():
	global outputfilename
	global continueRecording
	outputfilename = sys.argv[1] + '/recording_' + str(reportIndex) + '.wav'
	continueRecording = True
	recordThread = threading.Thread(target = recordInto)
	recordThread.start()

def audioInstruct():	
	global slideNames
	global slideCounter
	global playFilename
	global playThread
	global completed
	#if slideCounter <= 1:
	playFilename = 'recordings/'+(slideNames[slideCounter])[:len(slideNames[slideCounter])-6]+'.wav'
	if slideCounter == 0 and not completed:
		playFilename = 'recordings/'+'H1.wav'
	completed = False
	if playThread != None:
		completed = True
		time.sleep( 0.5 )
	completed = False
	playThread = threading.Thread(target = playAudio)
	playThread.start()
	


#-------------------------------------Button Events-------------------------------------#

def R0():
	print 'Stop'
	sys.exit(-1)

def R1():
	updateStrip('r1')
	global currentSelection
	global buttons
	global slideCounter
	#buttons[9].config(background = 'yellow')
	currentSelection = 3
	if slideCounter == 14:
		#buttons[9].config(background = 'red')
		recordReport()

def R2():
	updateStrip('r2')
	global currentSelection
	global buttons
	#buttons[9].config(background = 'yellow')
	currentSelection = 4

def R3():
	updateStrip('r3')
	global currentSelection
	global buttons
	#buttons[9].config(background = 'yellow')
	currentSelection = 5

def R4():
	print 'Next'
	global slideNames
	global currentImage
	global slideCounter
	global outfile
	global currentSelection
	global reportString
	global reports
	global solution
	global buttons
	global thumb
	global reportIndex
	global continueRecording
	#buttons[9].config(background = 'white')
	print slideCounter
	if 1 < slideCounter <= 12:
		reportString[slideCounter-2] = currentSelection
		print reportString
	if slideCounter == 13:
		temp = []
		for i in reportString:
			temp.append(i)
		reports.append(temp)
		reportIndex = reportIndex + 1
		if currentSelection == 1 or currentSelection == 0:
			slideCounter = 1
			clearThumbnails()
	elif slideCounter == 11:
		if currentSelection == 3 or currentSelection == 4:
			slideCounter = 12
			updateStrip('r3')
			reportString[slideCounter-2] = 9
	elif slideCounter == 9:
		if currentSelection == 0:
			slideCounter = 10
			reportString[slideCounter-2] = 9
			updateStrip('r3')
	elif slideCounter == 14:
			solution = currentSelection
			continueRecording = False
	slideCounter = slideCounter + 1
	if slideCounter < len(slideNames):
		currentImage = slideNames[slideCounter]
		loadImage()
		audioInstruct()
	else:
		for i in reports:
			for j in i:
				outfile.write(str(j))
			outfile.write(str(solution)+'\n')
		sys.exit(-1)

def L0():
	print 'Help'
	playFile('recordings/H1.wav')

def L1():
	updateStrip('l1')
	global currentSelection
	global buttons
	#buttons[9].config(background = 'yellow')
	currentSelection = 0

def L2():
	updateStrip('l2')
	global currentSelection
	global buttons
	#buttons[9].config(background = 'yellow')
	currentSelection = 1

def L3():
	updateStrip('l3')
	global currentSelection
	global buttons
	#buttons[9].config(background = 'yellow')
	currentSelection = 2

def L4():
	print 'Previous'
	global slideNames
	global currentImage
	global slideCounter
	slideCounter = slideCounter - 1
	if slideCounter >= 0:
		currentImage = slideNames[slideCounter]
		loadImage()
	else:
		sys.exit(-1)

def speak():
	print 'Activate Speaker'



#------------------------------------Button Creation------------------------------------#
'''
def createButtons():
	global selected
	global Option
	global buttons
	global buttonFunction
	buttons = []
	
        buttons.append(Button(root, background = 'red', activebackground = "grey", activeforeground = "white", height = 8, width = 4, command = R0))
        buttons.append(Button(root, background = 'white', activebackground = "grey", activeforeground = "white", height = 8, width = 4, command = L1))
        buttons.append(Button(root, background = 'white', activebackground = "grey", activeforeground = "white", height = 8, width = 4, command = L2))
        buttons.append(Button(root, background = 'white', activebackground = "grey", activeforeground = "white", height = 8, width = 4, command = L3))
        buttons.append(Button(root, background = 'blue', activebackground = "grey", activeforeground = "white", height = 8, width = 4, command = L4))
        buttons.append(Button(root, background = 'green', activebackground = "grey", activeforeground = "white", height = 8, width = 4, command = L0))
        buttons.append(Button(root, background = 'white', activebackground = "grey", activeforeground = "white", height = 8, width = 4, command = R1))
        buttons.append(Button(root, background = 'white', activebackground = "grey", activeforeground = "white", height = 8, width = 4, command = R2))
        buttons.append(Button(root, background = 'white', activebackground = "grey", activeforeground = "white", height = 8, width = 4, command = R3))
        buttons.append(Button(root, background = 'white', activebackground = "grey", activeforeground = "white", height = 8, width = 4, command = R4))
	for i in range(0, 10):
                buttons[i].grid(row = 2 + i%5, column = 2 * ((i>=5) + 1))
        buttons.append(Button(root, background = 'white', activebackground = "grey", activeforeground = "black", height = 2, width = 42, command = lambda: playFile('recordings/'+(slideNames[slideCounter])[:len(slideNames[slideCounter])-3]+'wav')))
	Label(root, height = 1, background = "white").grid(row = 9, column = 2)
        buttons[10].grid(row = 10, column = 3)
'''




#-----------------------------------Button Simulation-----------------------------------#

def buttonLoop():
	print "Entering Button Loop"
	#inp = raw_input()
	inp = '000'
	while True:
		if GPIO.input(4):
			audioInstruct()
			time.sleep(0.5)
		elif GPIO.input(25):
			L4()
			time.sleep(0.4)
			audioInstruct()
		elif GPIO.input(18):
			L1()
			time.sleep(0.5)
			R4()
		elif GPIO.input(23):
			L2()
			time.sleep(0.5)
			R4()
		elif GPIO.input(24):
			L3()
			time.sleep(0.5)
			R4()
		elif GPIO.input(21):
			print '21'
			R1()
			time.sleep(0.5)
			R4()
		elif GPIO.input(17):
			print '17'
			R2()
			time.sleep(0.5)
			R4()
		elif GPIO.input(22):
			R3()
			time.sleep(0.5)
			R4()
		#inp = raw_input()

	print "Exiting Button Loop"

def initGPIO():
	pins = [ 4,  17, 21, 22, 23, 24, 25, 18]
	GPIO.setmode( GPIO.BCM )
	for i in pins:
		GPIO.setup(i , GPIO.IN )


#------------------------------------Window Creation------------------------------------#
def windowSetup():
	global slideNames
	global slideCounter
	global thumbSize
	global thumbnail
	global thumb
	global root
	global question
	global section
	global nextButtonText
	global option
	global buttonVar
	global selected
	global slide
	global slideImage
	global currentImage
	global speaker
	global speakerImage
	global speakerButton
	print "Entered wS"
	root = Tk()
	root.geometry('1280x1024')
	root.title('Reporting Panel Prototype v1.2')
	root.configure(background = 'white')
	# Initialize Labels:
	loadImage()
	#createButtons()
	#audioInstruct()
	root.mainloop()

if __name__=='__main__':
	initGPIO()
	initButtonFunctions()
	recordingsDirectory()
	buttonThread = threading.Thread( target = buttonLoop )	
	buttonThread.start()
	windowSetup()
