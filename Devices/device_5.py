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
chip.create_wgt(300*nm,0*um,10*um)
chip.deep_etch(2*mm)
chip.etch_markers([	(2.25*mm,5*mm),(7.75*mm,5*mm),(7.75*mm,2.75*mm)],200*um, 10*um)

# this time, I'm trying to avoid propogation at 100nm as much as possible
# I'm sweeping the distance between the cleave and the start of the adiabatic taper

# just 300nm

x,y = 0,0
for i in range(11):
	for j in range(3):
		x,y = chip.etch_wg([(1.95*mm+(j-1)*10*um+(i-5)*2*um,3*mm+i*125*um+j*25*um),(2*mm+(j-1)*10*um+(i-5)*2*um,3*mm+i*125*um+j*25*um)],130*nm)
		x,y = chip.etch_tp((x,y),50*um,130*nm,300*nm)
		x,y = chip.etch_wg([(x,y),(2.11*mm + 370*nm*34,y)])
		chip.etch_circ_bragg_ref([x-370*nm*34,y],30,4,370*nm,85*nm,100*nm)

for i in range(3):
	x,y = chip.etch_wg([(1.95*mm+(i-1)*5*um,4.5*mm+50*um*i),(2*mm+(i-1)*5*um,4.5*mm+50*um*i)],130*nm)
	xb,yb = chip.etch_tp((x,y),50*um,130*nm,300*nm)
	x,y = xb,yb
	dy = 300*nm*(0.5+0.5+1) + 2*150*nm + 5*um*2
	x,y = chip.etch_wg(([x,y],[x+100*um,y]))
	x,y = chip.etch_wg(([x,y],[x+10*um,y],[x+20*um,y-dy/2],[x+30*um,y-dy/2]))
	x,y = chip.etch_ring([x,y],5*um,150*nm,1)
	x,y = chip.etch_wg([(x,y),(x+5*um,y)])
	x,y = chip.etch_tp((x,y),50*um,300*nm,130*nm)
	x,y = chip.etch_wg([(x,y),(x+10*um,y)],130*nm)
	x,y = xb,yb
	x,y = chip.etch_wg(([x,y],[x+100*um,y]))
	x,y = chip.etch_wg(([x,y],[x+10*um,y],[x+20*um,y+dy/2],[x+40*um,y+dy/2]))
	x,y = chip.etch_wg([(x,y),(x+5*um,y)])
	x,y = chip.etch_tp((x,y),50*um,300*nm,130*nm)
	x,y = chip.etch_wg([(x,y),(x+10*um,y)],130*nm)

for i in range(3):
	x,y = chip.etch_wg([(1.95*mm+(i-1)*5*um,4.7*mm+50*um*i),(2*mm+(i-1)*5*um,4.7*mm+50*um*i)],130*nm)
	xb,yb = chip.etch_tp((x,y),50*um,130*nm,300*nm)
	x,y = xb,yb
	dy = 300*nm*(0.5+0.5+1) + 2*250*nm + 5*um*2
	x,y = chip.etch_wg(([x,y],[x+100*um,y]))
	x,y = chip.etch_wg(([x,y],[x+10*um,y],[x+20*um,y-dy/2],[x+30*um,y-dy/2]))
	x,y = chip.etch_ring([x,y],5*um,250*nm,1)
	x,y = chip.etch_wg([(x,y),(x+5*um,y)])
	x,y = chip.etch_tp((x,y),50*um,300*nm,130*nm)
	x,y = chip.etch_wg([(x,y),(x+10*um,y)],130*nm)
	x,y = xb,yb
	x,y = chip.etch_wg(([x,y],[x+100*um,y]))
	x,y = chip.etch_wg(([x,y],[x+10*um,y],[x+20*um,y+dy/2],[x+40*um,y+dy/2]))
	x,y = chip.etch_wg([(x,y),(x+5*um,y)])
	x,y = chip.etch_tp((x,y),50*um,300*nm,130*nm)
	x,y = chip.etch_wg([(x,y),(x+10*um,y)],130*nm)

x,y = 0,0
for i in range(11):
	for j in range(3):
		x,y = chip.etch_wg([(10*mm-1.95*mm-(j-1)*10*um-(i-5)*2*um,3*mm+i*125*um+j*25*um),(10*mm-2*mm-(j-1)*10*um-(i-5)*2*um,3*mm+i*125*um+j*25*um)],130*nm)
		x,y = chip.etch_tp((x-50*um,y),50*um,300*nm,130*nm)
		x,y = chip.etch_wg([(x-50*um,y),(10*mm-2.11*mm - 370*nm*34,y)])
		chip.etch_circ_bragg_ref_left([x+370*nm*34,y],30,4,370*nm,85*nm,100*nm)

for i in range(3):
	x,y = chip.etch_wg([(10*mm-1.95*mm-(i-1)*5*um,4.5*mm+50*um*i),(10*mm-2*mm-(i-1)*5*um,4.5*mm+50*um*i)],130*nm)
	xb,yb = chip.etch_tp((x-50*um,y),50*um,300*nm,130*nm)
	x,y = xb-50*um,yb
	dy = 300*nm*(0.5+0.5+1) + 2*150*nm + 5*um*2
	x,y = chip.etch_wg(([x,y],[x-100*um,y]))
	x,y = chip.etch_wg(([x,y],[x-10*um,y],[x-20*um,y-dy/2],[x-30*um,y-dy/2]))
	x,y = chip.etch_ring([x-10*um,y],5*um,150*nm,1)
	x=x-10*um
	x,y = chip.etch_wg([(x,y),(x-5*um,y)])
	x,y = chip.etch_tp((x-50*um,y),50*um,130*nm,300*nm)
	x=x-50*um
	x,y = chip.etch_wg([(x,y),(x-10*um,y)],130*nm)
	x,y = xb,yb
	x,y = xb-50*um,yb
	x,y = chip.etch_wg(([x,y],[x-100*um,y]))
	x,y = chip.etch_wg(([x,y],[x-10*um,y],[x-20*um,y+dy/2],[x-40*um,y+dy/2]))
	x,y = chip.etch_wg([(x,y),(x-5*um,y)])
	x,y = chip.etch_tp((x-50*um,y),50*um,130*nm,300*nm)
	x=x-50*um
	x,y = chip.etch_wg([(x,y),(x-10*um,y)],130*nm)

for i in range(3):
	x,y = chip.etch_wg([(10*mm-1.95*mm-(i-1)*5*um,4.7*mm+50*um*i),(10*mm-2*mm-(i-1)*5*um,4.7*mm+50*um*i)],130*nm)
	xb,yb = chip.etch_tp((x-50*um,y),50*um,300*nm,130*nm)
	x,y = xb-50*um,yb
	dy = 300*nm*(0.5+0.5+1) + 2*250*nm + 5*um*2
	x,y = chip.etch_wg(([x,y],[x-100*um,y]))
	x,y = chip.etch_wg(([x,y],[x-10*um,y],[x-20*um,y-dy/2],[x-30*um,y-dy/2]))
	x,y = chip.etch_ring([x-10*um,y],5*um,250*nm,1)
	x=x-10*um
	x,y = chip.etch_wg([(x,y),(x-5*um,y)])
	x,y = chip.etch_tp((x-50*um,y),50*um,130*nm,300*nm)
	x=x-50*um
	x,y = chip.etch_wg([(x,y),(x-10*um,y)],130*nm)
	x,y = xb,yb
	x,y = xb-50*um,yb
	x,y = chip.etch_wg(([x,y],[x-100*um,y]))
	x,y = chip.etch_wg(([x,y],[x-10*um,y],[x-20*um,y+dy/2],[x-40*um,y+dy/2]))
	x,y = chip.etch_wg([(x,y),(x-5*um,y)])
	x,y = chip.etch_tp((x-50*um,y),50*um,130*nm,300*nm)
	x=x-50*um
	x,y = chip.etch_wg([(x,y),(x-10*um,y)],130*nm)

#chip.bool_layer(3,8,"xor",3)

chip.build('device_5')