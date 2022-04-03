import sys, os
from new_chip_class import *
cm,mm,um,nm = 10**4,10**3,1,10**-3
name = os.path.basename(__file__[:-3])

PIC = PIC(1*cm, 1*cm)
PIC.set_wg_width(300*nm)
PIC.edge_mask(2*mm,2*mm,2*mm,2*mm)
PIC.markers([(2.5*mm,7.5*mm),(7.5*mm,7.5*mm),(7.5*mm,2.5*mm)],200*um, 10*um)

wg_len = 100*um
i_var = 20*um
j_var = 100*um

for i in range(11):
	for j in range(3):
		PIC.set_origin([2*mm+(j-1)*j_var+(i-5)*i_var-100*um,4*mm+i*125*um+j*25*um])
		PIC.set_wg_width(130*nm)
		PIC.wg([(100*um,0)])
		PIC.set_wg_width(300*nm)
		PIC.tp([50*um,0*um],130*nm,300*nm)
		PIC.wg([(wg_len,0)])
		for n in range(20):
			PIC.bragg([370*nm*1,0],370*nm,0,85*nm,100*nm)

for i in range(11):
	for j in range(3):
		PIC.set_origin([10*mm-2*mm+(j-1)*j_var+(i-5)*i_var+100*um,4*mm+i*125*um+j*25*um])
		PIC.set_wg_width(130*nm)
		PIC.wg([(-100*um,0)])
		PIC.set_wg_width(300*nm)
		PIC.tp([-50*um,0*um],130*nm,300*nm)
		PIC.wg([(-wg_len,0)])
		for n in range(20):
			PIC.bragg([-370*nm*1,0],370*nm,0,85*nm,100*nm)

gaps = (150*nm, 250*nm)
for i in range(len(gaps)):
	for j in range(3):
		PIC.set_origin([2*mm+(j-1)*j_var-100*um,5.5*mm+50*um*j+150*um*i])
		PIC.set_wg_width(130*nm)
		PIC.wg([(100*um,0)])
		PIC.set_wg_width(300*nm)
		PIC.tp([50*um,0*um],130*nm,300*nm)
		PIC.wg([(wg_len-100*um,0)])
		x,y = PIC.get_position()
		dy = 2*300*nm + 2*gaps[i] + 2*5*um
		PIC.wg([(10*um,0),(30*um,-dy/2),(10*um,0)])
		PIC.ring(5*um, gaps[i])
		PIC.tp([50*um,0*um],300*nm,50*nm)
		PIC.set_origin([x,y])
		PIC.wg([(10*um,0),(30*um,dy/2),(20*um,0)])
		PIC.tp([50*um,0*um],300*nm,50*nm)

gaps = (150*nm, 250*nm)
for i in range(len(gaps)):
	for j in range(3):
		PIC.set_origin([10*mm-2*mm+(j-1)*j_var+100*um,5.5*mm+50*um*j+150*um*i])
		PIC.set_wg_width(130*nm)
		PIC.wg([(-100*um,0)])
		PIC.set_wg_width(300*nm)
		PIC.tp([-50*um,0*um],130*nm,300*nm)
		PIC.wg([(-wg_len+100*um,0)])
		x,y = PIC.get_position()
		dy = 2*300*nm + 2*gaps[i] + 2*5*um
		PIC.wg([(-10*um,0),(-30*um,-dy/2),(-10*um,0)])
		PIC.set_origin([PIC.x-10*um,PIC.y])
		PIC.ring(5*um, gaps[i])
		PIC.set_origin([PIC.x-10*um,PIC.y])
		PIC.tp([-50*um,0*um],300*nm,50*nm)
		PIC.set_origin([x,y])
		PIC.wg([(-10*um,0),(-30*um,dy/2),(-20*um,0)])
		PIC.tp([-50*um,0*um],300*nm,50*nm)

PIC.build(name)