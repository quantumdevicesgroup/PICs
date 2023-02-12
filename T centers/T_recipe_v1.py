import sys, os
sys.path.append("..")
from PIC_class import *
import numpy as np

cm,mm,um,nm = 10**4,10**3,1,10**-3
name = os.path.basename(__file__[:-3])

#gdspy.current_library = gdspy.GdsLibrary()
PIC = PIC(1*cm, 1*cm, (0.5*cm, 0.5*cm))
PIC.edge_mask(2*mm,2*mm,0,0)
#PIC.markers([(1*mm,3*mm),(3*mm,3*mm),(9*mm,3*mm)],100*um, 4*um)

wg_len = 300*um
wg_extra = 120*um
y_sep_i = 100*um 
y_sep_j = 50*um

### left cleave ###
for i in range(1):
	for j in range(2):
		PIC.set_write_layer(10+i*2+(j+1))
		PIC.x, PIC.y = 1.1*mm, 4.7*mm+i*y_sep_i+j*y_sep_j
		PIC.tp(50*um,130*nm,300*nm)
		PIC.wg(wg_extra)
		PIC.wg(wg_len)	
		for n in range(20):
			PIC.bragg([370*nm*1,0],370*nm,0,75*nm,100*nm)
### micropuck ###
radius_sel = [300*nm, 305*nm, 520*nm, 527*nm, 754*nm, 812*nm]
radius_sweep = []
for i in range (6):
    radius_sweep= np.arange(250+i*100, 250+(i+1)*100, 10)
    PIC.micropucks(([1.1*mm, 4.25*mm-i*6*um]), radius_sweep*nm, 13, 5, 10*um)
PIC.micropucks(([1.1*mm, 4.25*mm-50*um]), radius_sel, 13, 10, 10*um)
### block ###
for i in range(2):
    for j in range(1):
        PIC.Rectangle([(1.1*mm+j*50*um, 4.35*mm+i*30*um),(1.1*mm+(i+1)*10*um+j*50*um, 4.35*mm+(i+1)*10*um+i*30*um)], 15)

### middle cleave ###
coord1 = []
for i in range(1):
	for j in range(2):
		PIC.set_write_layer(20+i*2+(j+1))
		PIC.x, PIC.y = 2.5*mm, 4.7*mm+i*y_sep_i+j*y_sep_j
		PIC.tp(50*um,130*nm,300*nm)
		PIC.wg(wg_extra)
		PIC.wg(wg_len)	
		for n in range(20):
			PIC.bragg([370*nm*1,0],370*nm,0,75*nm,100*nm)
### micropuck ###
radius_sel = [300*nm, 305*nm, 520*nm, 527*nm, 754*nm, 812*nm]
radius_sweep = []
for i in range (6):
    radius_sweep= np.arange(250+i*100, 250+(i+1)*100, 10)
    PIC.micropucks(([2.5*mm, 4.25*mm-i*6*um]), radius_sweep*nm, 23, 5, 10*um)
PIC.micropucks(([2.5*mm, 4.25*mm-50*um]), radius_sel, 23, 10, 10*um)
### block ###
for i in range(2):
    for j in range(1):
        PIC.Rectangle([(2.5*mm+j*50*um, 4.35*mm+i*30*um),(2.5*mm+(i+1)*10*um+j*50*um, 4.35*mm+(i+1)*10*um+i*30*um)], 25)

### right cleave ###
coord1 = []
for i in range(1):
	for j in range(3):
		PIC.set_write_layer(30+i*2+(j+1))
		PIC.x, PIC.y = 8.5*mm, 4.7*mm+i*y_sep_i+j*y_sep_j
		PIC.tp(50*um,130*nm,300*nm)
		PIC.wg(wg_extra)
		PIC.wg(wg_len)	
		for n in range(20):
			PIC.bragg([370*nm*1,0],370*nm,0,75*nm,100*nm)
### micropuck ###
radius_sel = [300*nm, 305*nm, 520*nm, 527*nm, 754*nm, 812*nm]
radius_sweep = []
for i in range (6):
    radius_sweep= np.arange(250+i*100, 250+(i+1)*100, 10)
    PIC.micropucks(([8.5*mm, 4.25*mm-i*6*um]), radius_sweep*nm, 34, 5, 10*um)
PIC.micropucks(([8.5*mm, 4.25*mm-50*um]), radius_sel, 34, 10, 10*um)
### block ###
for i in range(2):
    for j in range(1):
        PIC.Rectangle([(8.5*mm+j*50*um, 4.35*mm+i*30*um),(8.5*mm+(i+1)*10*um+j*50*um, 4.35*mm+(i+1)*10*um+i*30*um)], 35)


PIC.build(name)