import sys, os
sys.path.append("..")
from PIC_class import *
cm,mm,um,nm = 10**4,10**3,1,10**-3
name = os.path.basename(__file__[:-3])

PIC = PIC(1*cm, 1*cm, (0.5*cm, 0.5*cm))
PIC.edge_mask(1.5*mm,1.5*mm,0,0, layer=11)
PIC.edge_mask(2.5*mm,2.5*mm,0,0, layer=12)
in_dim = 3*mm
PIC.markers([(in_dim, 10*mm-in_dim),(in_dim,in_dim),(10*mm-in_dim,in_dim)],75*um, 4*um)

gap_wid = 2*um + PIC.width/2
pillar_rad = 4*um
tether_wid = 200*nm

PIC.set_write_layer(20)
for k in range(3):
	for j in range(3):
		for i in range(3):
			PIC.set_write_layer(PIC.write_layer+1)
			PIC.x, PIC.y = 2.5*mm+2*um, 4.5*mm+i*2*(gap_wid + pillar_rad)+j*65*um+k*250*um
			PIC.tp(10*um,130*nm,300*nm)
			PIC.wg(1*um)
			x_s, y_s = PIC.x, PIC.y
			PIC.wg(1*um)
			PIC.pcc(0,1,(295)*nm+(j-1)*15*nm,(245)*nm+(j-1)*15*nm,4+k,7,7,15,0.64,(i-1)*10.0*nm)
			PIC.wg(1*um)
			
			dx = (PIC.x - x_s)
			PIC.Rectangle(((x_s, y_s-gap_wid), (x_s+tether_wid, y_s+gap_wid)), 10) # tether
			PIC.Circle(((x_s, PIC.y+gap_wid+pillar_rad)), pillar_rad+0.5*um, 10) # top circle
			PIC.Circle(((x_s, PIC.y-gap_wid-pillar_rad)), pillar_rad+0.5*um, 10) # bottom circle
			PIC.Circle((PIC.x+pillar_rad, PIC.y), pillar_rad+0.5*um, 10) # right circle

# for k in range(3):
# 	for j in range(5):
# 		for i in range(5):
# 			PIC.set_write_layer(PIC.write_layer+1)
# 			PIC.x, PIC.y = 10*mm-3*mm-2*um,4*mm+i*25*um+j*150*um+k*800*um
# 			PIC.tp(-50*um,130*nm,300*nm)
# 			PIC.wg(-wg_len)
# 			PIC.pcc(0,-1,(295)*nm+(j-2)*15*nm,(245)*nm+(j-2)*15*nm,7+k,7,7,15,0.64,(i-2)*10.0*nm)

PIC.build(name)