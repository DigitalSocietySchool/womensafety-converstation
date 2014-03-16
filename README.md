<center>Conver<i>[s]</i>tation<br>
<strong>Project NextWave</strong><br>
MediaLAB Amsterdam</center>

README
======

Authors
-------
	Bauke Bakker
	Daksh Varshneya
	Marissa Memelink
	Yashvanth Kondi


What is it?
-----------
This repository contains the code/software backend for the 'Conver[s]tation'
reporting panel prototype, made as part of the Women's Safety Project, a
joint effort by MediaLAB Amsterdam, Fields of View and IIIT Bangalore.
Comissioned by Cisco System.


Project Description
-------------------
Can be found at:
http://medialab.hva.nl/blog/project/womens-safety-india/


Usage
-----
The files present in this directory correspond to the physical prototype.
They are to be run on the Raspberry Pi that powers the actual panel.

Most of the dependencies for this program can be built by executing the
'dependencies' script in the softProto/ folder.
In addition to the script, the RPi.GPIO Python Module can be installed as
follows:

	sudo apt-get install python-rpi.gpio

Execution (on the Raspberry Pi, configured according to the schematics,
provided as another component of the deliverables):

	sudo python rasproto.py <report output folder>

(execution has to be done as root in order to access the GPIO ports).


For the Soft Prototype, the following steps are to be followed:

1. Download and extract the entire package.
2. Copy the softProto folder to the appropriate directory.
3. Open terminal (Ctrl+Alt+T), navigate to the softProto folder, and type the following commands:

		chmod a+x dependencies
     	chmod a+x runProto
     	sudo su
     	#	Installation of the dependencies requires administrator priviledges.
     	./dependencies
     	#      That should build all the required dependencies for the prototype, so to exit from administrator mode, type:
		exit

4. To run the prototype:

     	./runProto

This should ideally get the prototype running. Not being our primary product, its
not very robust, and in case pressing the 'Stop' button doesn't kill the panel,
the only sureshot way of stopping it is closing the terminal (Alt+tab if required).
But it is unlikely that such a situation would arise.
To run the prototype again, open up another Terminal (Ctrl+Alt+T), then type:

    	cd softProto
    	./runProto
