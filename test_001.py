import sys, os
from new_chip_class import *
cm,mm,um,nm = 10**4,10**3,1,10**-3
name = os.path.basename(__file__[:-3])

PIC = PIC(1*cm, 1*cm)
PIC.set_wg_width(300*nm)
PIC.edge_mask(3*mm,3*mm,3*mm,3*mm)
PIC.markers([(5*mm-100*um,5*mm+100*um)],200*um, 10*um)

for i in range(20):
	PIC.set_origin([5*mm,5*mm-i*10*um])
	PIC.set_write_layer(i+10)
	PIC.tp([3*um,0*um],100*nm,300*nm)
	for n in range(20):
		PIC.bragg([370*nm*1,0],370*nm,0,85*nm,100*nm)
	PIC.tp([3*um,0*um],300*nm,100*nm)


PIC.build(name)