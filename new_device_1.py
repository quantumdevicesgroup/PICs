import sys, os
from new_chip_class import *
cm,mm,um,nm = 10**4,10**3,1,10**-3
name = os.path.basename(__file__[:-3])

PIC = PIC(1*cm, 1*cm)
PIC.set_wg_width(300*nm)
PIC.edge_mask(3*mm,3*mm,3*mm,3*mm)
PIC.markers([(3.25*mm,6.75*mm),(6.75*mm,6.75*mm),(6.75*mm,3.25*mm)],200*um, 10*um)

for i in range(11):
	for j in range(3):
		PIC.set_origin([3*mm+2*um+(j-1)*1*um,4*mm+i*125*um+j*25*um])
		PIC.tp([50*um,0*um],130*nm,300*nm)
		PIC.wg([(400*um,0)])
		PIC.bragg([370*nm*30,0],370*nm,0,85*nm,100*nm)

gaps = (150*nm, 250*nm)
for i in range(len(gaps)):
	for j in range(3):
		PIC.set_origin([3*mm+2*um+(j-1)*1*um,5.5*mm+i*150*um+50*um*j])
		PIC.tp([50*um,0*um],130*nm,300*nm)
		PIC.wg([(300*um,0)])
		x,y = PIC.get_position()
		dy = 2*300*nm + 2*gaps[i] + 2*5*um
		PIC.wg([(10*um,0),(30*um,-dy/2),(10*um,0)])
		PIC.ring(5*um, gaps[i])
		PIC.tp([50*um,0*um],300*nm,50*nm)
		PIC.set_origin([x,y])
		PIC.wg([(10*um,0),(30*um,dy/2),(20*um,0)])
		PIC.tp([50*um,0*um],300*nm,50*nm)

x = 3.15*mm - 50*um
y = 6.65*mm
gap = 5*um
for i in range(10):
	PIC.design.add(gdspy.Rectangle((x,y),(x+(i+1)*1*um,y+1*um),layer=1,datatype=0))
	PIC.design.add(gdspy.Rectangle((x,y+gap),(x+(i+1)*1*um,y+ gap +(i+1)*1*um),layer=1,datatype=0))
	x += (i+1)*1*um + gap

PIC.build(name)