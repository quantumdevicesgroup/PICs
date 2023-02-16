import sys, os
sys.path.append("..")
from PIC_class import *
import numpy as np

cm,mm,um,nm = 10**4,10**3,1,10**-3
name = os.path.basename(__file__[:-3])

#gdspy.current_library = gdspy.GdsLibrary()
PIC = PIC(1*cm, 1*cm, (0.5*cm, 0.5*cm))
PIC.edge_mask(1.5*mm,1.5*mm,0,0, layer=11)
PIC.edge_mask(2.5*mm,2.5*mm,0,0, layer=12)
PIC.markers([(3*mm,7*mm),(3*mm,3*mm),(7*mm,3*mm)],100*um, 4*um)

x_extra = 2*um # facet protection
wg_len = 10*um
tether_len = 1.8*um
tether_extra = 1*um
pillar_rad = 4.5*um
tether_pillar_overlap = 0.3*um
y_sep_i = 1.5*um*2+9*um+400*nm
for i in range(5):
    PIC.set_write_layer(20+i)
    PIC.x, PIC.y = 2.5*mm+x_extra, 4.5*mm+i*y_sep_i
    PIC.tp(20*um, 160*nm, 230*nm)
    PIC.tp(5*um, 230*nm, 400*nm)
    temp_x, temp_y = PIC.x, PIC.y
    PIC.set_wg_width(400*nm)
    PIC.set_write_layer(20+i)
    PIC.wg(wg_len)
    for n in range(20):
        PIC.bragg([300*nm*1,0],300*nm,0,52.5*nm,70*nm)
    PIC.wg(1*um)
    PIC.Circle((PIC.x+pillar_rad-0.5*um, PIC.y), pillar_rad, 10)
    for n in range(2): 
        # if want to overlap tether with wg, should add some vertical rectangle here
        #PIC.set_write_layer(50)
        start = tuple([0, (-1)**n*tether_len])
        PIC.x = temp_x+tether_extra
        PIC.y = temp_y+(-1)**n*PIC.width/2
        PIC.tp(start, 100*nm, 200*nm)
        PIC.Circle((PIC.x, PIC.y+(-1)**n*(-tether_pillar_overlap+4.5*um)), pillar_rad,10)


for i in range(2):
    for j in range(1):
        PIC.Rectangle([(2.6*mm+j*50*um, 4.35*mm+i*30*um),(2.6*mm+(i+1)*10*um+j*50*um, 4.35*mm+(i+1)*10*um+i*30*um)], 45)


# ### micropuck ###
# radius_sel = [300*nm, 305*nm, 520*nm, 527*nm, 754*nm, 812*nm]
# radius_sweep = []
# for i in range (6):
#     radius_sweep= np.arange(250+i*100, 250+(i+1)*100, 10)
#     PIC.micropucks(([2.5*mm+50*um, 3.25*mm-i*6*um]), radius_sweep*nm, 91, 5, 5*um)
#     PIC.micropucks(([2.5*mm+50*um, 6.76*mm+i*6*um]), radius_sweep*nm, 91, 5, 5*um)
# PIC.micropucks(([2.5*mm+50*um, 3.25*mm-50*um]), radius_sel, 91, 10, 5*um)
# PIC.micropucks(([2.5*mm+50*um, 6.76*mm+50*um]), radius_sel, 91, 10, 5*um)

# PIC.Rectangle([(0,0), (1.5*mm, 1*cm)], 10)


PIC.build(name)