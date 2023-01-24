import sys, os
sys.path.append("..")
from PIC_class import *
cm,mm,um,nm = 10**4,10**3,1,10**-3
name = os.path.basename(__file__[:-3])

PIC = PIC(1*cm, 1*cm, (0.5*cm, 0.5*cm))
PIC.markers([(4*mm,4*mm)],100*um, 4*um)





gap_wid = 2*um + PIC.width/2 # air gap between waveguides and silicon

# sweep width of rectangles (6um - 15um)
for i in range(4):
	num_tether = 3
	rect_wid = 6*um + i*3*um
	taper_len = 10*um

	PIC.x, PIC.y = 4*mm+50*um, 4*mm+50*um+60*um*i # set starting coords close to alignment marker
	PIC.tp(taper_len,100*nm,300*nm)
	x_s, y_s = PIC.x, PIC.y # record pos for drawing rects later
	PIC.wg(10*um)
	for i in range(10):
		PIC.bragg([370*nm*1,0],370*nm,0,85*nm,100*nm)
	PIC.wg(1*um)

	num_tether = 3
	for j in range(num_tether):
		dx = (PIC.x - x_s) / num_tether
		PIC.Rectangle(((x_s+j*dx, y_s-gap_wid), (x_s+400*nm+j*dx, y_s+gap_wid)), 10) # tether

	PIC.Rectangle(((x_s, y_s-gap_wid), (PIC.x, y_s-gap_wid-rect_wid)), 10) # bottom rectangle
	PIC.Rectangle(((x_s, y_s+gap_wid), (PIC.x, y_s+gap_wid+rect_wid)), 10) # top rectangle
	PIC.Rectangle(((PIC.x, PIC.y-gap_wid-rect_wid), (PIC.x+rect_wid, PIC.y+gap_wid+rect_wid)), 10) # right rectangle


# sweep number of tethers (1 - 4)
for i in range(4):
	num_tether = i+1
	rect_wid = 15*um
	taper_len = 10*um

	PIC.x, PIC.y = 4*mm+150*um, 4*mm+50*um+60*um*i # set starting coords close to alignment marker
	PIC.tp(taper_len,100*nm,300*nm)
	x_s, y_s = PIC.x, PIC.y # record pos for drawing rects later
	PIC.wg(10*um)
	for i in range(10):
		PIC.bragg([370*nm*1,0],370*nm,0,85*nm,100*nm)
	PIC.wg(1*um)

	for j in range(num_tether):
		dx = (PIC.x - x_s) / num_tether
		PIC.Rectangle(((x_s+j*dx, y_s-gap_wid), (x_s+400*nm+j*dx, y_s+gap_wid)), 10) # tether

	PIC.Rectangle(((x_s, y_s-gap_wid), (PIC.x, y_s-gap_wid-rect_wid)), 10) # bottom rectangle
	PIC.Rectangle(((x_s, y_s+gap_wid), (PIC.x, y_s+gap_wid+rect_wid)), 10) # top rectangle
	PIC.Rectangle(((PIC.x, PIC.y-gap_wid-rect_wid), (PIC.x+rect_wid, PIC.y+gap_wid+rect_wid)), 10) # right rectangle


# sweep length of taper (10*um - 25*um)
for i in range(4):
	num_tether = 3
	rect_wid = 15*um
	taper_len = 10*um + 5*um*i

	PIC.x, PIC.y = 4*mm+250*um, 4*mm+50*um+60*um*i # set starting coords close to alignment marker
	PIC.tp(taper_len,100*nm,300*nm)
	x_s, y_s = PIC.x, PIC.y # record pos for drawing rects later
	PIC.wg(10*um)
	for i in range(10):
		PIC.bragg([370*nm*1,0],370*nm,0,85*nm,100*nm)
	PIC.wg(1*um)

	for j in range(num_tether):
		dx = (PIC.x - x_s) / num_tether
		PIC.Rectangle(((x_s+j*dx, y_s-gap_wid), (x_s+400*nm+j*dx, y_s+gap_wid)), 10) # tether

	PIC.Rectangle(((x_s, y_s-gap_wid), (PIC.x, y_s-gap_wid-rect_wid)), 10) # bottom rectangle
	PIC.Rectangle(((x_s, y_s+gap_wid), (PIC.x, y_s+gap_wid+rect_wid)), 10) # top rectangle
	PIC.Rectangle(((PIC.x, PIC.y-gap_wid-rect_wid), (PIC.x+rect_wid, PIC.y+gap_wid+rect_wid)), 10) # right rectangle


# sweep width of tethers (100nm - 400nm)
for i in range(4):
	num_tether = 3
	rect_wid = 15*um
	taper_len = 10*um
	tether_wid = 100*nm + i*100*nm

	PIC.x, PIC.y = 4*mm+350*um, 4*mm+50*um+60*um*i # set starting coords close to alignment marker
	PIC.tp(taper_len,100*nm,300*nm)
	x_s, y_s = PIC.x, PIC.y # record pos for drawing rects later
	PIC.wg(10*um)
	for i in range(10):
		PIC.bragg([370*nm*1,0],370*nm,0,85*nm,100*nm)
	PIC.wg(1*um)

	for j in range(num_tether):
		dx = (PIC.x - x_s) / num_tether
		PIC.Rectangle(((x_s+j*dx, y_s-gap_wid), (x_s+tether_wid+j*dx, y_s+gap_wid)), 10) # tether

	PIC.Rectangle(((x_s, y_s-gap_wid), (PIC.x, y_s-gap_wid-rect_wid)), 10) # bottom rectangle
	PIC.Rectangle(((x_s, y_s+gap_wid), (PIC.x, y_s+gap_wid+rect_wid)), 10) # top rectangle
	PIC.Rectangle(((PIC.x, PIC.y-gap_wid-rect_wid), (PIC.x+rect_wid, PIC.y+gap_wid+rect_wid)), 10) # right rectangle

# sweep lengths of air gap (2um - 8um)
for i in range(4):
	gap_wid = 2*um + PIC.width/2 + i*2*um
	num_tether = 2
	rect_wid = 15*um
	taper_len = 10*um
	tether_wid = 400*nm

	PIC.x, PIC.y = 4*mm+450*um, 4*mm+50*um+70*um*i # set starting coords close to alignment marker
	PIC.tp(taper_len,100*nm,300*nm)
	x_s, y_s = PIC.x, PIC.y # record pos for drawing rects later
	PIC.wg(10*um)
	for i in range(10):
		PIC.bragg([370*nm*1,0],370*nm,0,85*nm,100*nm)
	PIC.wg(1*um)

	for j in range(num_tether):
		dx = (PIC.x - x_s) / num_tether
		PIC.Rectangle(((x_s+j*dx, y_s-gap_wid), (x_s+tether_wid+j*dx, y_s+gap_wid)), 10) # tether

	PIC.Rectangle(((x_s, y_s-gap_wid), (PIC.x, y_s-gap_wid-rect_wid)), 10) # bottom rectangle
	PIC.Rectangle(((x_s, y_s+gap_wid), (PIC.x, y_s+gap_wid+rect_wid)), 10) # top rectangle
	PIC.Rectangle(((PIC.x, PIC.y-gap_wid-rect_wid), (PIC.x+rect_wid, PIC.y+gap_wid+rect_wid)), 10) # right rectangle


PIC.build(name)