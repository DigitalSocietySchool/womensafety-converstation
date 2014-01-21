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
import playwav
import time
import tkFont
import playing

solution = 9
selector = selectorImage = selectionImage = None
Option = []
Archive = []
root = question = section = option = None
selected = []
buttonVar = None
slide = sliderImage = None
currentImage = '1lang.png'
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
bar = None

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
	inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
	inp.setperiodsize(160)
	loops = 1000000
	print outputfilename
	while continueRecording:
		l, data = inp.read()
		f.writeframes(data)


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
	
	metaSlides = open('slides/meta', 'r')
	for i in metaSlides:
		slideNames.append(i[:len(i)-1])
	metaSlides.close()

def playFile(filepath):
	print filepath
	global completed
	if not completed:
		completed = True
		time.sleep(0.5)
	completed = False
	playwav.player(filepath)
	completed = True

def playAudio():
	global playFilename
	playFile(playFilename)

#-------------------------------Utilities to Refresh Screen------------------------------#
	

def loadImage():
        # To be done
	global root
	global slideImage
	global slide
	global currentImage
	global speaker
	global speakerImage
	global speakerButton
	reqdImage = Image.open('slides/'+currentImage)
	reqdImage = reqdImage.resize((363, 600), Image.ANTIALIAS)
        slideImage = ImageTk.PhotoImage(reqdImage)
        slide = Label(root, image = slideImage)
        #slide.grid(row = 5, column = 3)
	slide.place(x = 60, y = 3)
	
	speakerButton = Image.open('slides/speakers.png')
	speakerButton = speakerButton.resize((363, 37), Image.ANTIALIAS)
	speakerImage = ImageTk.PhotoImage(speakerButton)
	speaker = Label(root, image = speakerImage)
	speaker.place(x = 60, y = 653)

def getPos( selection ):
	x = y = 0
	if selection[0] == 'l':
		x = 60
	else:
		x = 235
	if selection[1] == '1':
		y = 125
	elif selection[1] == '2':
		y = 250
	else:
		y = 375
	return x , y

def drawBox(xpos, ypos):
	global bar
	bar = []
	loadImage()
	for i in range(0, 3, 2):
		bar.append( [] )
		bar[i].append( Image.open('slides/selecth.png') )
		bar[i][0] = bar[i][0].resize((180, 10), Image.ANTIALIAS)
		bar[i].append( ImageTk.PhotoImage( bar[i][0] ) )
		bar[i].append( Label(root, image = bar[i][1]) )
		bar[i][2].place(x = xpos, y = ypos + i*70)
		
		bar.append( [] )
		bar[i+1].append( Image.open('slides/selectv.png') )
		bar[i+1][0] = bar[i][0].resize((10, 150), Image.ANTIALIAS)
		bar[i+1].append( ImageTk.PhotoImage( bar[i+1][0] ) )
		bar[i+1].append( Label(root, image = bar[i+1][1]) )
		bar[i+1][2].place(x = xpos + i*85, y = ypos)

def updateStrip(selection):
	global slideNames
	global slideCounter
	global thumbSize
	global thumbnail
	global thumb
	global selector
	global selectorImage
	global selectionImage
	if 2 <= slideCounter <= 12:
		question = slideNames[slideCounter]
		question = question[:len(question)-4]
		thumbSize[slideCounter-2] = Image.open('slides/thumbnails/'+question+'/'+selection+'.png')
		thumbSize[slideCounter-2] = thumbSize[slideCounter-2].resize((30, 50), Image.ANTIALIAS)
		thumbnail[slideCounter-2] = ImageTk.PhotoImage(thumbSize[slideCounter-2])
		thumb[slideCounter-2] = Label(root, image = thumbnail[slideCounter-2])
		thumb[slideCounter-2].place(x = 60 + (slideCounter - 2)*33, y = 604)
	
	xpos , ypos = getPos( selection )
	'''
	selectionImage = Image.open('slides/selector.png')
	selectionImage = selectionImage.resize((150, 150), Image.ANTIALIAS)
	selectorImage = ImageTk.PhotoImage(selectionImage)
	selector = Label(root, image = selectorImage)
	selector.place(x = xpos, y = ypos)
	'''
	drawBox( xpos, ypos )
	

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
	playFilename = 'recordings/'+(slideNames[slideCounter])[:len(slideNames[slideCounter])-3]+'wav'
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
	buttons[9].config(background = 'yellow')
	currentSelection = 3
	if slideCounter == 14:
		buttons[9].config(background = 'red')
		recordReport()

def R2():
	updateStrip('r2')
	global currentSelection
	global buttons
	buttons[9].config(background = 'yellow')
	currentSelection = 4

def R3():
	updateStrip('r3')
	global currentSelection
	global buttons
	buttons[9].config(background = 'yellow')
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
	buttons[9].config(background = 'white')
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
	buttons[9].config(background = 'yellow')
	currentSelection = 0

def L2():
	updateStrip('l2')
	global currentSelection
	global buttons
	buttons[9].config(background = 'yellow')
	currentSelection = 1

def L3():
	updateStrip('l3')
	global currentSelection
	global buttons
	buttons[9].config(background = 'yellow')
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
	root.geometry('485x850')
	root.title('Reporting Panel Prototype v1.2')
	root.configure(background = 'white')
	# Initialize Labels:
	loadImage()
	createButtons()
	audioInstruct()
	root.mainloop()

if __name__=='__main__':
	initButtonFunctions()
	recordingsDirectory()
	windowSetup()	
