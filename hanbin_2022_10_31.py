import sys, os
from PIC_class import *
cm,mm,um,nm = 10**4,10**3,1,10**-3
name = os.path.basename(__file__[:-3])

PIC = PIC(1*cm, 1*cm, (0.5*cm, 0.5*cm))
PIC.edge_mask(2*mm,2*mm,0,0)
PIC.markers([(2.5*mm,7.5*mm),(2.5*mm,2.5*mm),(7.5*mm,2.5*mm)],200*um, 10*um)

wg_len = 200*um
x_extra = 25*um
y_sep_i = 250*um
y_sep_j = 50*um
x_sep_i = -10*um
x_sep_j = 20*um

# 5 x 3 diagonal waveguides
for i in range(5):
	for j in range(3):
		PIC.set_write_layer(20+i)
		PIC.wg(x_extra, origin=[2*mm-x_extra+j*x_sep_j+i*x_sep_i,3.5*mm+i*y_sep_i+j*y_sep_j], width=130*nm)
		PIC.tp(50*um,130*nm,300*nm)
		PIC.wg([(10*um,0),(wg_len/np.sqrt(2), wg_len/np.sqrt(2)), (10*um,0)])
		for n in range(20):
			PIC.bragg([370*nm*1,0],370*nm,0,85*nm,100*nm)

# 5 x 3 straight waveguides
for i in range(5):
	for j in range(3):
		PIC.set_write_layer(30+i)
		PIC.wg(x_extra, origin=[2*mm-x_extra+j*x_sep_j+i*x_sep_i,5*mm+i*y_sep_i+j*y_sep_j], width=130*nm)
		PIC.tp(50*um,130*nm,300*nm)
		PIC.wg(wg_len)
		for n in range(20):
			PIC.bragg([370*nm*1,0],370*nm,0,85*nm,100*nm)

gaps = [150*nm, 250*nm]
# 3 x 2 ring resonators 
for j in range(2):
	for i in range(3):
		PIC.set_write_layer(40+i)
		gap = gaps[j]
		PIC.wg(x_extra, origin=[2*mm-x_extra+(i-1)*5*um, 6.25*mm+i*50*um+j*200*um], width=130*nm)
		PIC.tp(50*um,130*nm,300*nm)
		PIC.wg(10*um)
		x,y = PIC.get_position()
		dy = 2*300*nm + 2*gap + 2*5*um
		PIC.wg([(10*um,0),(30*um,-dy/2),(10*um,0)])
		PIC.ring(5*um, gap)
		PIC.tp(50*um,300*nm,50*nm)
		PIC.wg([(10*um,0),(30*um,dy/2),(20*um,0)], origin=[x,y])
		PIC.tp(50*um,300*nm,50*nm)

# 1 x 3 PCCs
for i in range(3):
	PIC.set_write_layer(50+i)
	PIC.wg(x_extra, origin=[2*mm-x_extra+(i-1)*10*um, 6.75*mm+i*50*um], width=130*nm)
	PIC.tp(50*um,130*nm,300*nm)
	PIC.wg(10*um)
	PIC.pcc(0,1,(295)*nm,(245)*nm,4,7,7,15,0.64,(i-1)*10.0*nm)


### left side ###

# 5 x 3 diagonal waveguides
for i in range(5):
	for j in range(3):
		PIC.set_write_layer(60+i)
		PIC.wg(-x_extra, origin=[10*mm - 2*mm + x_extra - j*x_sep_j - i*x_sep_i,3.5*mm+i*y_sep_i+j*y_sep_j], width=130*nm)
		PIC.tp(-50*um,130*nm,300*nm)
		PIC.wg([(-10*um,0),(-wg_len/np.sqrt(2), wg_len/np.sqrt(2)), (-10*um,0)])
		for n in range(20):
			PIC.bragg([-370*nm*1,0],370*nm,0,85*nm,100*nm)

# 5 x 3 straight waveguides
for i in range(5):
	for j in range(3):
		PIC.set_write_layer(70+i)
		PIC.wg(-x_extra, origin=[10*mm - 2*mm+x_extra-j*x_sep_j-i*x_sep_i,5*mm+i*y_sep_i+j*y_sep_j], width=130*nm)
		PIC.tp(-50*um,130*nm,300*nm)
		PIC.wg(-wg_len)
		for n in range(20):
			PIC.bragg([-370*nm*1,0],370*nm,0,85*nm,100*nm)

gaps = [150*nm, 250*nm]
# 3 x 2 ring resonators 
for j in range(2):
	for i in range(3):
		PIC.set_write_layer(80+i)
		gap = gaps[j]
		PIC.wg(-x_extra, origin=[10*mm-2*mm+x_extra-(i-1)*5*um, 6.25*mm+i*50*um+j*200*um], width=130*nm)
		PIC.tp(-50*um,130*nm,300*nm)
		PIC.wg(-10*um)
		x,y = PIC.get_position()
		dy = 2*300*nm + 2*gap + 2*5*um
		PIC.wg([(-10*um,0),(-30*um,-dy/2),(-10*um,0)])
		PIC.x = PIC.x-10*um
		PIC.ring(5*um, gap)
		PIC.x = PIC.x-10*um
		PIC.tp(-50*um,300*nm,50*nm)
		PIC.wg([(-10*um,0),(-30*um,dy/2),(-20*um,0)], origin=[x,y])
		PIC.tp(-50*um,300*nm,50*nm)

PIC.build(name)