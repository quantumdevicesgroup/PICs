import sys
sys.path.append("C:\\Users\\lukas\\Desktop\\QDG_PICs")
from chip_class import *
import numpy as np
cm,mm,um,nm = 10**4,10**3,1,10**-3

chip = Chip(1*cm, 1*cm, 600*um)
chip.create_wgt(300*nm,0*um,20*um)
#chip.deep_etch(1*mm)


chip.etch_markers([(6*mm,6*mm)],200*um, 10*um)

write_layer = 30
for i in range(20):
	chip.change_write_layer(write_layer)
	x_s, y_s = 5*mm,5*mm
	x,y=chip.etch_wg([(x_s+i*10*um,y_s),(x_s+i*10*um,y_s-10*um)])
	#x,y=chip.etch_wg((x_s+i*10*um,y_s),(310*nm*15),0,310*nm,0.5,220*nm)
	write_layer += 1

# write_layer = 30
# for i in range(19):
# 	x_i = x_s+(i-9.25)*30*um
# 	for j in range(5):
# 		chip.change_write_layer(write_layer)
# 		x,y=chip.etch_saw_bragg_ref((x_i,y_s+(j-2)*2*um),(310*nm*50),0,310*nm,0.5,220*nm)
# 	chip.etch_label((x+1*um,y-0.5*um),1*um,str(500+i*250))
# 	write_layer += 1

chip.build('HSiQ_dose_calib')