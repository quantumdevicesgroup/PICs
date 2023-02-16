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
wg_len = 50*um
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





# ### left side ###
# # the set of waveguide should be an even number, each set contains two waveguide
# # 14 straight waveguides
# coord1 = []
# for i in range(7):
# 	for j in range(2):
# 		PIC.set_write_layer(40+i*2+(j+1))
# 		PIC.x, PIC.y = 2.5*mm+x_extra, 4.2*mm+i*y_sep_i+j*y_sep_j
# 		PIC.tp(50*um,130*nm,300*nm)
# 		PIC.wg(wg_extra)
# 		PIC.wg(wg_len)	
# 		for n in range(20):
# 			PIC.bragg([370*nm*1,0],370*nm,0,75*nm,100*nm)
# 	start = tuple([2.5*mm+x_extra+50*um+wg_extra, 4.2*mm+i*y_sep_i+j*y_sep_j/2])
# 	stop = tuple([PIC.x+feedline_extra, 4.2*mm+i*y_sep_i+j*y_sep_j/2])
# 	PIC.get_coordinate(coord1, i, start, stop)



# #4 PCC#
# coord4 = []
# for i in range(2):
#     for j in range(2):
#         PIC.set_write_layer(30+i*2+(j+1))
#         PIC.x, PIC.y = 2.5*mm+x_extra,4*mm+i*y_sep_i+j*y_sep_j
#         PIC.tp(50*um,130*nm,300*nm)
#         PIC.wg(wg_extra+100*um) #put all PCC region under CPW
#         PIC.pcc(0,1,(295)*nm,(245)*nm,4,7,7,15,0.64,(i-1)*10.0*nm)
#     start = tuple([2.5*mm+x_extra+50*um+wg_extra, 4*mm+i*y_sep_i+j*y_sep_j/2])
#     stop = tuple([PIC.x+feedline_extra, 4*mm+i*y_sep_i+j*y_sep_j/2])
#     PIC.get_coordinate(coord4, i, start, stop)


# # 14 diagonal waveguides
# y_sep_j = 30*np.sqrt(2)*um
# coord2 = []
# for i in range(11):
# 	for j in range(2):
# 		PIC.set_write_layer(60+i*2+(j+1))
# 		PIC.x, PIC.y = 2.5*mm+x_extra, 4.9*mm+i*y_sep_i+j*y_sep_j
# 		PIC.tp(50*um,130*nm,300*nm)
# 		PIC.wg(wg_extra)
# 		PIC.wg([(10*um,0),(wg_len/np.sqrt(2), wg_len/np.sqrt(2)), (10*um,0)])
# 		temp = tuple([PIC.x, PIC.y])
# 		for n in range(20):
# 			PIC.bragg([370*nm*1,0],370*nm,0,75*nm,100*nm)
# 	start = tuple([2.5*mm+x_extra+50*um+wg_extra+10*um, 4.9*mm+i*y_sep_i+j*y_sep_j/2])
# 	stop = tuple([temp[0]-10*um+feedline_extra, temp[1]-y_sep_j/2+feedline_extra])
# 	PIC.get_coordinate(coord2, i, start, stop, 7)

# #4 ring resonator#
# y_sep_i = 100*um 
# y_sep_j = 40.5*um
# coord3 = []
# gaps = [150*nm, 250*nm]
# for i in range (2):
#     for j in range (2):
#         PIC.set_write_layer(20+i*2+(j+1))
#         PIC.x, PIC.y = 2.5*mm+x_extra, 3.75*mm+i*y_sep_i+j*y_sep_j
#         gap = gaps[i]
#         PIC.tp(50*um,130*nm,300*nm)
#         PIC.wg(wg_extra+50*um)
#         x,y = PIC.get_position()
#         dy = 2*300*nm + 2*gap + 2*5*um
#         PIC.wg([(10*um,0),(30*um,-dy/2),(10*um,0)])
#         PIC.ring(5*um, gap)
#         PIC.tp(50*um,300*nm,50*nm)
#         PIC.wg([(10*um,0),(30*um,dy/2),(20*um,0)], origin=[x,y])
#         PIC.tp(50*um,300*nm,50*nm)
#     start = tuple([2.5*mm+x_extra+50*um+wg_extra, 3.75*mm+i*y_sep_i+j*y_sep_j/2])
#     stop = tuple([PIC.x+feedline_extra, 3.75*mm+i*y_sep_i+j*y_sep_j/2])
#     PIC.get_coordinate(coord3, i, start, stop)


# ### CPW ###
# feedline_trace = 24.5*um
# feedline_gap = 5.5*um
# feedline_ground = 100*um


# ### CPW on ring resonator ###
# ring_gap = 16*um
# ring_trace = 24.5*um
# ring_ground = 100*um
# shrink_len = 50*um
# PIC.feedline(coord3, ring_trace, ring_gap, ring_ground, 98, 30, positive=False)
# shrink = PIC.get_transition_vertices(ring_trace, feedline_trace, ring_gap, feedline_gap, ring_ground, feedline_ground, shrink_len)
# PIC.draw_transition(shrink, coord3[0], 98, positive=False)
# PIC.draw_transition(shrink, coord3[-1], 98, positive=False )
# PIC.add_pt(coord3, shrink_len, shrink_len)

# ### CPW on top of wg
# turn = 20*um
# turnn = -20*um

# PIC.add_pt(coord1, 1*turn, 2*turnn)
# PIC.add_pt(coord2, 2*turnn-10*um, turn)
# connect_path = [coord3[-2], coord3[-1]]
# PIC.add_pt(connect_path, 0, turn)
# PIC.add_pt(connect_path, 0, turn)
# PIC.add_pt(coord4, connect_path[-1][0]-coord4[0][0], coord1[0][0]-coord4[-1][0])


# coord_path = []
# coord_path.extend(connect_path)
# coord_path.extend(coord4)
# coord_path.extend(coord1)
# coord_path.extend(coord2)
# PIC.feedline(coord_path, feedline_trace, feedline_gap, feedline_ground, 98, 30, positive=False)



# ### Launch pad and connection ###
# launch_trace = 390*um
# launch_gap = 112*um
# launch_ground = 800*um
# launch_border1 = 100*um
# launch_length = 600*um
# transition_length = 300*um
# #connect_len1 = 8.1*mm - coord_path[0][0]
# connect_len2 = 8.15*mm - coord_path[-1][0]
# connect_len1 = 8.15*mm - coord3[0][0]

# connect1 = PIC.get_vertices(connect_len1, feedline_trace, feedline_gap, feedline_ground, 10)
# launch = PIC.get_vertices(launch_length, launch_trace, launch_gap, launch_ground)
# border1 = PIC.get_vertices(launch_border1, launch_trace, launch_gap, launch_ground)
# transition = PIC.get_transition_vertices(feedline_trace, launch_trace, feedline_gap, launch_gap, feedline_ground, launch_ground, transition_length)

# PIC.draw_connect_launch(connect1, launch, border1, transition, coord3[0], 98, positive=False)

# connect2 = PIC.get_vertices(connect_len2, feedline_trace, feedline_gap, feedline_ground, 10)
# PIC.draw_connect_launch(connect2, launch, border1, transition, coord_path[-1], 98, positive=False)

# ### Inverse design ###
# PIC.Rectangle([(2.5*mm+x_extra+50*um+10*um, 3.1*mm), (9.7*mm, 6.9*mm)],99)
# PIC.Rectangle([(7.5*mm, 2*mm), (9.7*mm, 8*mm)],99)
# PIC.bool_layer(98, 99, "xor", 97) 
# PIC.Rectangle([(2.5*mm+x_extra+50*um+10*um, 3.1*mm), (2.5*mm+0.5*mm, 3.4*mm)],96)   
# PIC.Rectangle([(2.5*mm+x_extra+50*um+10*um, 6.6*mm), (2.5*mm+0.5*mm, 6.9*mm)],96) 
# PIC.bool_layer(96, 97, "xor", 100) 

# ### Nb marker ###
# for i in range (3):
#     PIC.micropucks(([2.5*mm+3*um, 3.25*mm-i*5*um]), 1*um, 100, 2, 5*um)
#     PIC.micropucks(([2.5*mm+3*um, 6.76*mm+i*5*um]), 1*um, 100, 2, 5*um)

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