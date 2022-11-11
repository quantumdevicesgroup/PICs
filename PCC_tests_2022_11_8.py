import sys, os
from PIC_class import *
cm,mm,um,nm = 10**4,10**3,1,10**-3
name = os.path.basename(__file__[:-3])

PIC = PIC(1*cm, 1*cm, (0.5*cm, 0.5*cm))
PIC.edge_mask(3*mm,3*mm,0,0)
PIC.markers([(3.5*mm,6.5*mm),(3.5*mm,3.5*mm),(6.5*mm,3.5*mm)],200*um, 10*um)

wg_len = 5*um

# gaps = [150*nm, 250*nm]
# for j in range(2):
# 	for i in range(3):
# 		PIC.x, PIC.y = 3*mm+1*um,5.65*mm+i*50*um+j*200*um
# 		gap = gaps[j]
# 		PIC.tp(50*um,130*nm,300*nm)
# 		PIC.wg(10*um)
# 		x,y = PIC.get_position()
# 		dy = 2*300*nm + 2*gap + 2*5*um
# 		PIC.wg([(10*um,0),(30*um,-dy/2),(10*um,0)])
# 		PIC.ring(5*um, gap)
# 		PIC.tp(50*um,300*nm,50*nm)
# 		PIC.wg([(10*um,0),(30*um,dy/2),(20*um,0)], origin=[x,y])
# 		PIC.tp(50*um,300*nm,50*nm)

PIC.set_write_layer(20)
for k in range(3):
	for j in range(5):
		for i in range(5):
			PIC.set_write_layer(PIC.write_layer+1)
			PIC.x, PIC.y = 3*mm+2*um,4*mm+i*25*um+j*150*um+k*800*um
			PIC.tp(50*um,130*nm,300*nm)
			PIC.wg(wg_len)
			PIC.pcc(0,1,(295)*nm+(j-2)*15*nm,(245)*nm+(j-2)*15*nm,4+k,7,7,15,0.64,(i-2)*10.0*nm)

for k in range(3):
	for j in range(5):
		for i in range(5):
			PIC.set_write_layer(PIC.write_layer+1)
			PIC.x, PIC.y = 10*mm-3*mm-2*um,4*mm+i*25*um+j*150*um+k*800*um
			PIC.tp(-50*um,130*nm,300*nm)
			PIC.wg(-wg_len)
			PIC.pcc(0,-1,(295)*nm+(j-2)*15*nm,(245)*nm+(j-2)*15*nm,7+k,7,7,15,0.64,(i-2)*10.0*nm)

# gaps = [150*nm, 250*nm]
# # 3 x 2 ring resonators 
# for j in range(2):
# 	for i in range(3):
# 		PIC.set_write_layer(80+i)
# 		gap = gaps[j]
# 		PIC.wg(-x_extra, origin=[10*mm-2*mm+x_extra-(i-1)*5*um, 6.25*mm+i*50*um+j*200*um], width=130*nm)
# 		PIC.tp(-50*um,130*nm,300*nm)
# 		PIC.wg(-10*um)
# 		x,y = PIC.get_position()
# 		dy = 2*300*nm + 2*gap + 2*5*um
# 		PIC.wg([(-10*um,0),(-30*um,-dy/2),(-10*um,0)])
# 		PIC.x = PIC.x-10*um
# 		PIC.ring(5*um, gap)
# 		PIC.x = PIC.x-10*um
# 		PIC.tp(-50*um,300*nm,50*nm)
# 		PIC.wg([(-10*um,0),(-30*um,dy/2),(-20*um,0)], origin=[x,y])
# 		PIC.tp(-50*um,300*nm,50*nm)

PIC.build(name)