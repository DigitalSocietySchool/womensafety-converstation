from Tkinter import *
from os import system, path
from tkFileDialog import askopenfilename
import threading
import playing
import time

filepath = ''

def play():
   if filepath == '':
       return 
   details = path.split(filepath) 
   system('cd '+details[0])
   system('./arplay '+details[1])

def playRRA():
   #print 'Playing...'
   playThread = threading.Thread(target = play)
   playThread.start()
   #print threading.enumerate()
   
def pauseRRA():
   pass

def openRRA():
   global filepath
   filepath = askopenfilename(filetypes=[("RRA Files","*.rra"),])
   
def windowSetup():
   top = Tk()
   global filepath
   filepath = None
   top.geometry('250x100')
   top.title('RRA Player')
   frameWork = Frame(top)
   play = Button(frameWork, text = 'Play', command = playRRA)
   play.pack(side=LEFT)
   stop = Button(frameWork, text = 'Pause', command = pauseRRA)
   stop.pack(side=LEFT)
   openFile = Button(top, text = 'Open', command = openRRA)
   openFile.pack(side = RIGHT)
   frameWork.pack(side = BOTTOM)
   top.mainloop()

if __name__ == '__main__':
   windowSetup()
