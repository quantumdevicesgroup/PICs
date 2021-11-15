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
#chip.deep_etch(1*mm)

chip.etch_markers([(5*mm-25*um,5*mm+25*um)],50*um, 3*um)
chip.etch_markers([(5*mm-175*um,5*mm+175*um)],250*um, 10*um)

chip.etch_markers([(6*mm-240*um,5*mm-35*um)],50*um, 3*um)
chip.etch_markers([(6*mm-90*um,5*mm-175*um)],250*um, 10*um)

write_layer = 30
for i in range(30):
	chip.change_write_layer(write_layer)
	x_s, y_s = 5*mm,5*mm
	chip.etch_wg([(x_s+i*25*um,y_s),(x_s+i*25*um+10*um,y_s)])
	chip.etch_wg([(x_s+i*25*um,y_s-5*um),(x_s+i*25*um+10*um,y_s-5*um)])
	chip.etch_saw_bragg_ref((x_s+i*25*um,y_s-10*um),(480*nm*10),480*nm*5,480*nm,0.5,100*nm,w=300*nm)
	#chip.etch_label((x_s+i*25*um,y_s-20*um),5*um,str(50+i*50))
	write_layer += 1

chip.build('HSiQ_dose_calib')