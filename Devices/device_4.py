import sys
try:
	sys.path.append("C:\\Users\\lukas\\Desktop\\QDG_PICs")
	from chip_class import *
except:
	sys.path.append("C:\\Users\\Lukasz\\Desktop\\QDG_PICs")
	from chip_class import *
import numpy as np
cm,mm,um,nm = 10**4,10**3,1,10**-3

chip = Chip(1*cm, 1*cm, 600*um)
chip.create_wgt(300*nm,0*um,20*um)
chip.deep_etch(2*mm)
chip.etch_markers([	(2.6*mm,7.2*mm),(7.9*mm,7.15*mm),(7.4*mm,1.9*mm)],200*um, 10*um)

# this time, I'm trying to avoid propogation at 100nm as much as possible
# I'm sweeping the distance between the cleave and the start of the adiabatic taper

write_layer = 30
for i in range(21):
	for j in range(3):
		x,y = chip.etch_tp((1.95*mm+(j-1)*100*um+(i-10)*25*um,2*mm+j*25*um+i*250*um),100*um,100*nm,300*nm)
		x,y = chip.etch_wg([(x,y),(x+10*um,y)],300*nm)
		x,y = chip.etch_saw_bragg_ref((x,y),(480*nm*30),480*nm*10,480*nm,0.5,100*nm,w=300*nm)

for i in range(21):
	for j in range(3):
		x,y = chip.etch_tp((10*mm-1.95*mm+(j-1)*100*um+(i-10)*25*um-100*um,2*mm+j*25*um+i*250*um),100*um,300*nm,100*nm)
		x,y = chip.etch_wg([(x-100*um,y),(x-100*um-10*um,y)],300*nm)
		x,y = chip.etch_saw_bragg_ref((x-(480*nm*50),y),(480*nm*30),480*nm*10,480*nm,0.5,100*nm,w=300*nm)

	#chip.etch_label((x+4*um,y-2.5*um),5*um,"+"+str(2*i))
	#for j in range(7):
	#	chip.etch_markers([(2*mm-30*um+(j*10*um),4*mm+i*125*um-1*um)],1*um,100*nm) # spaced 10um apart
chip.build('device_4')