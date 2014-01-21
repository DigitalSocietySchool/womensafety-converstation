'''

The main program for the Raspberry Pi based prototype of Convers[t]ation,
the panel used to record reports of sexual harassment.

NextWave Project, Fields of View and MediaLAB Amsterdam

Revision: 16th January 2013

'''
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
import time
import RPi.GPIO as GPIO
import tkFont
bar = None

playThread = None
completed = True
solution = 9
root = question = section = option = None
selected = []
buttonVar = None
slide = sliderImage = None
currentImage = '1lang_r.png'
speaker =  speakerImage = speakerButton = None
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


#------------------------------------Audio Utilities-------------------------------------#

def play(device, f):
    '''
    Function that reads values from a .wav file and throws them to audio output (ALSA)
    Credit: pyALSA sample programs taken from SourceForge
    '''
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
    '''
    Function to initialize audio card and filepath, then call the wav player
    Credit: pyALSA sample programs taken from SourceForge
    '''
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
	'''
	Function to record audio into a wav file
	'''
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


def playFile(filepath):
	'''
	Function to create a new thread for audio playback
	'''
	print filepath
	global playThread
	player(filepath)
	playThread = None

def playAudio():
	global playFilename
	playFile(playFilename)

#---Utilities to initialize parameters of this instance of the program (slides and directory)--#

def recordingsDirectory():
	'''
	Function to set directory into which reports are stored.
	Report strings are stored in a file called 'reportList'
	They are indexed in the order of their creation, so that
	any audio recordings corresponding to them can be found
	easily (in the same folder).
	'''
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

def getSlideNames():
	'''
	Function to get the names of the slides, and store them
	in a list for easy access.
	'''
	global slideNames
	metaSlides = open('slides/pimetaslides', 'r')
	for i in metaSlides:
		slideNames.append(i[:len(i)-1])
	metaSlides.close()

#-------------------------------Utilities to Refresh Screen------------------------------#
	

def loadImage():
	'''
	Function to load, resize and display a new slide (and the speaker icon)
	on the screen.
	'''
	global root
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
	slide.place(x = 0, y = 0)
	
	speakerButton = Image.open('slides/speaker_r.png')
	speakerButton = speakerButton.resize((80, 1024), Image.ANTIALIAS)
	speakerImage = ImageTk.PhotoImage(speakerButton)
	speaker = Label(root, image = speakerImage)
	speaker.place(x = 1200, y = 0)

def getPos( selection ):
	'''
	Function to return where on the screen the selection box
	must be placed.
	Given the option that's selected, this function returns
	the x and y co-ordinates of the top-left corner of the
	selection box.
	'''
	x = y = 0
	if selection[0] == 'r':
		y = 10
	else:
		y = 510
	if selection[1] == '1':
		x = 200
	elif selection[1] == '2':
		x = 450
	else:
		x = 700
	return x , y


def drawBox(selection):
	'''
	This function draws a box around the selected option,
	so the user gets visual confirmation of his selection before
	moving on to the next slide.
	It accomplishes this task by placing four lines around
	the option.
	'''
	global bar
	bar = []
	xpos , ypos = getPos( selection )
	for i in range(0, 3, 2):
		bar.append( [] )
		bar[i].append( Image.open('slides/selectv.png') )
		bar[i][0] = bar[i][0].resize((250, 20), Image.ANTIALIAS)
		bar[i].append( ImageTk.PhotoImage( bar[i][0] ) )
		bar[i].append( Label(root, image = bar[i][1]) )
		bar[i][2].place(x = xpos , y =  i*250 + ypos)
		
		bar.append( [] )
		bar[i+1].append( Image.open('slides/selecth.png') )
		bar[i+1][0] = bar[i][0].resize((20, 520), Image.ANTIALIAS)
		bar[i+1].append( ImageTk.PhotoImage( bar[i+1][0] ) )
		bar[i+1].append( Label(root, image = bar[i+1][1]) )
		bar[i+1][2].place(x = xpos + i*115, y = ypos)





def updateStrip(selection):
	'''
	This function updates the strip at the below the options
	with the latest selection of the user,
	It calculates the position to be placed, fetches the
	required thumbnail image, resizes it and places it in
	the appropriate position.
	'''
	global slideNames
	global slideCounter
	global thumbSize
	global thumbnail
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
	'''
	This function clears the strip below the options in case
	the user wishes to report again.
	'''
	global slideNames
        global slideCounter
        global thumbSize
        global thumbnail
        global thumb
	for i in range(0, len(thumb)):
		thumbnail[i] = ImageTk.PhotoImage(Image.open('slides/nothing.png'))
		thumb[i].config(image = thumbnail[i])

def recordReport():
	'''
	This function starts a thread for the purpose of recording
	audio feedback into a file.
	'''
	global outputfilename
	global continueRecording
	outputfilename = sys.argv[1] + '/recording_' + str(reportIndex) + '.wav'
	continueRecording = True
	recordThread = threading.Thread(target = recordInto)
	recordThread.start()

def audioInstruct():
	'''
	This function activates the audio layer for a slide. It is
	called when a slide is arrived at, and whenever the speaker
	button is pressed.
	'''	
	global slideNames
	global slideCounter
	global playFilename
	global playThread
	global completed
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
	# Currently unused in this prototype
	print 'Stop'
	sys.exit(-1)

def R1():
	updateStrip('r1')
	global currentSelection
	global buttons
	global slideCounter
	currentSelection = 3
	if slideCounter == 14:
		recordReport()

def R2():
	updateStrip('r2')
	global currentSelection
	global buttons
	currentSelection = 4

def R3():
	updateStrip('r3')
	global currentSelection
	global buttons
	currentSelection = 5

def R4():
	'''
	This function was mapped to the 'Next' button in the
	software prototype. That button was later removed in
	hardware due to its redundancy and unnecessary added
	complexity, but for the sake of compatibility, this
	function was retained to handle the transition when
	the next slide has to be loaded.
	'''
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
	# Currently does nothing in this prototype.
	print 'Help'
	playFile('recordings/H1.wav')

def L1():
	updateStrip('l1')
	global currentSelection
	global buttons
	currentSelection = 0

def L2():
	updateStrip('l2')
	global currentSelection
	global buttons
	currentSelection = 1

def L3():
	updateStrip('l3')
	global currentSelection
	global buttons
	currentSelection = 2

def L4():
	'''
	Takes the user one slide back, to change a
	previously entered option.
	'''
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



#---------------------------------Button-Event-Handling--------------------------------#

def buttonLoop():
	'''
	Basically keeps checking which button(s) is/are pressed
	indefinitely (by checking the state of the GPIO ports),
	and calls the appropriate function.
	'''
	print "Entering Button Loop"
	while True:
		if GPIO.input(4):
			audioInstruct()
			time.sleep(0.5)
		elif GPIO.input(25):
			L4()
			time.sleep(0.4)
			audioInstruct()
		elif GPIO.input(18):
			drawBox( 'l1' )
			L1()
			time.sleep(0.5)
			R4()
		elif GPIO.input(23):
			drawBox( 'l2' )
			L2()
			time.sleep(0.5)
			R4()
		elif GPIO.input(24):
			drawBox( 'l3' )
			L3()
			time.sleep(0.5)
			R4()
		elif GPIO.input(21):
			drawBox( 'r1' )
			R1()
			time.sleep(0.5)
			R4()
		elif GPIO.input(17):
			drawBox( 'r2' )
			R2()
			time.sleep(0.5)
			R4()
		elif GPIO.input(22):
			drawBox( 'r3' )
			R3()
			time.sleep(0.5)
			R4()


def initGPIO():
	'''
	Inititalizes GPIO pins.
	'''
	pins = [ 4,  17, 21, 22, 23, 24, 25, 18]
	GPIO.setmode( GPIO.BCM )
	for i in pins:
		GPIO.setup(i , GPIO.IN )


#------------------------------------Window-Creation------------------------------------#
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
	global bar
	print "Entered wS"
	root = Tk()
	root.geometry('1280x1024')
	root.title('Reporting Panel Prototype v1.2')
	root.configure(background = 'white')
	loadImage()
	root.mainloop()

if __name__=='__main__':
	initGPIO()
	getSlideNames()
	recordingsDirectory()
	buttonThread = threading.Thread( target = buttonLoop )	
	buttonThread.start()
	windowSetup()
