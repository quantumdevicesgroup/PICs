import sys, os
from PIC_class import *
cm,mm,um,nm = 10**4,10**3,1,10**-3
name = os.path.basename(__file__[:-3])

PIC = PIC(1*cm, 1*cm, (0.5*cm, 0.5*cm))
PIC.edge_mask(2*mm,2*mm,0,0)
PIC.markers([(2.5*mm,2.5*mm)],200*um, 10*um)

wg_len = 20*um
x_extra = 10*um
y_sep_i = 25*um
y_sep_j = 600*um
x_sep_i = -10*um
x_sep_j = 20*um

# # the first run:
# for i in range(10):
# 	for j in range(3):
# 		PIC.set_write_layer(10*(j+2)+i)
# 		PIC.wg(x_extra, origin=[2.6*mm,2.6*mm + i*y_sep_i + j*y_sep_j], width=130*nm)
# 		PIC.tp(20*um,130*nm,300*nm)
# 		PIC.wg([(10*um,0),(wg_len/np.sqrt(2), wg_len/np.sqrt(2)), (10*um,0)])
# 		for n in range(20):
# 			PIC.bragg([370*nm*1,0],370*nm,0,85*nm,100*nm)

# the second run:
for i in range(20):
	for j in range(2):
		PIC.set_write_layer(20*(j+1)+i)
		PIC.wg(x_extra, origin=[2.6*mm,2.6*mm + i*y_sep_i + j*y_sep_j], width=130*nm)
		PIC.tp(20*um,130*nm,300*nm)
		PIC.wg([(10*um,0),(wg_len/np.sqrt(2), wg_len/np.sqrt(2)), (10*um,0)])
		for n in range(20):
			PIC.bragg([370*nm*1,0],370*nm,0,85*nm,100*nm)


PIC.build(name)