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

PIC.set_write_layer(20)

taper1_len = 50*um
taper2_len = 50*um
tapered_len = 10*um
start_x = 2.5*mm+2*um
start_y = 4.5*mm
for j in range(5):
	for i in range(5):
		# wg parameters
		tapered_wid = 900*nm + (i-2)*300*nm
		wg_spacing = 10*um
		# wg drawing
		PIC.x, PIC.y = start_x, start_y+i*wg_spacing+j*wg_spacing*10 # start
		PIC.tp(taper1_len,130*nm,300*nm)
		PIC.wg(5*um)
		PIC.tp(taper2_len,300*nm,tapered_wid)
		x_s, y_s = PIC.x + tapered_len/2, PIC.y
		PIC.wg(tapered_len, width=tapered_wid)
		PIC.tp(taper2_len,tapered_wid,300*nm)
		PIC.wg(5*um)
		for n in range(20):
			PIC.bragg([370*nm*1,0],370*nm,0,85*nm,100*nm)
		# contact parameters
		contact_wid = 1*um + (j-2)*250*nm
		contact_overlap = 300*nm
		via_len_1 = 10*um
		via_wid_1 = 1*um
		# contact drawing
		PIC.Rectangle(((x_s - contact_wid/2, y_s - contact_overlap + tapered_wid/2), (x_s + contact_wid/2, y_s + wg_spacing/2)), 10)
		PIC.Rectangle(((x_s - contact_wid/2, y_s + wg_spacing/2), (PIC.x + via_len_1, y_s + wg_spacing/2 + via_wid_1)), 10)
via_wid_2 = 10*um
PIC.Rectangle(((PIC.x + via_len_1, y_s + wg_spacing/2 + via_wid_1), (PIC.x + via_len_1 + via_wid_2, start_y + wg_spacing/2)), 10)
y_mid = (PIC.y + start_y)/2
via_wid_3 = 10*um
via_len_3 = 100*um
PIC.Rectangle(((PIC.x + via_len_1 + via_wid_2, y_mid + via_wid_3/2 + via_wid_1), (PIC.x + via_len_1 + via_wid_2 + via_len_3, y_mid - via_wid_3/2)), 10)
bond_pad_dim = 100*um
PIC.Rectangle(((PIC.x + via_len_1 + via_wid_2 + via_len_3, y_mid - bond_pad_dim/2),(PIC.x + via_len_1 + via_wid_2 + via_len_3 + bond_pad_dim, y_mid + bond_pad_dim/2)), 10)

PIC.build(name)