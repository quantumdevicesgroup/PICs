import sys, os
from PIC_class import *
cm,mm,um,nm = 10**4,10**3,1,10**-3
name = os.path.basename(__file__[:-3])

PIC = PIC(1*cm, 1*cm, (0.5*cm, 0.5*cm))
PIC.edge_mask(2*mm,2*mm,0,0)
PIC.markers([(2.5*mm,7.5*mm),(2.5*mm,2.5*mm),(7.5*mm,2.5*mm)],200*um, 10*um)

wg_len = 100*um
i_var = 15*um
j_var = 100*um

for i in range(16):
	for j in range(3):
		PIC.set_write_layer(20+i)
		PIC.wg(25*um, origin=[2*mm+(j-1)*j_var+(i-5)*i_var-50*um,4*mm+i*125*um+j*25*um], width=130*nm)
		PIC.tp(50*um,130*nm,300*nm)
		PIC.wg(wg_len)
		for n in range(20):
			PIC.bragg([370*nm*1,0],370*nm,0,85*nm,100*nm)

for i in range(16):
	for j in range(3):
		PIC.set_write_layer(40+i)
		PIC.wg(-25*um, origin=[10*mm-2*mm+(j-1)*j_var+(i-5)*i_var-50*um,4*mm+i*125*um+j*25*um], width=130*nm)
		PIC.tp(-50*um,130*nm,300*nm)
		PIC.wg(-wg_len)
		for n in range(20):
			PIC.bragg([-370*nm*1,0],370*nm,0,85*nm,100*nm)

PIC.build(name)