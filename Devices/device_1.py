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
chip.etch_markers([(2.325*mm,5.005*mm),(10*mm-2.325*mm,5.005*mm)],250*um, 15*um)

write_layer = 30

for i in range(8):
	chip.change_write_layer(write_layer)
	x,y = chip.etch_wg([(1.9*mm,4*mm+i*125*um),(2.1*mm,4*mm+i*125*um)],100*nm)
	x,y = chip.etch_tp((x,y),50*um,100*nm,300*nm)
	x,y = chip.etch_wg([(x,y),(x+25*um,y)],300*nm)
	x,y = chip.etch_saw_bragg_ref((x,y),(480*nm*30),480*nm*10,480*nm,0.5,100*nm,w=300*nm)
	write_layer += 1
for i in range(8):
	chip.change_write_layer(write_layer)
	x,y = chip.etch_wg([(10*mm-1.9*mm,4*mm+i*125*um),(10*mm-2.1*mm,4*mm+i*125*um)],100*nm)
	x,y = chip.etch_tp((x-50*um,y),50*um,300*nm,100*nm)
	x,y = chip.etch_wg([(x-50*um,y),(x-75*um,y)],300*nm)
	x,y = chip.etch_saw_bragg_ref((x-(480*nm*50),y),(480*nm*30),480*nm*10,480*nm,0.5,100*nm,w=300*nm)
	write_layer += 1
chip.build('device1')