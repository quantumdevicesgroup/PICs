import numpy as np
import gdspy
from picwriter import toolkit as tk
import picwriter.components as pc
cm,mm,um,nm = 10**4,10**3,1,10**-3

def etch_markers(coords, m_l, m_w):
	marker_l = m_l
	marker_w = m_w
	ld_markers= {"layer": 6, "datatype": 0}
	for i in range(len(coords)):
	    marker_x=coords[i][0]
	    marker_y=coords[i][1]
	    m_1=gdspy.Path(marker_w,(marker_x-marker_l/2-marker_w/2,marker_y-marker_w/2))
	    m_1.segment(marker_l/2+marker_w/2,"+x",**ld_markers)
	    m_2=gdspy.Path(marker_w,(marker_x-marker_w/2,marker_y-marker_l/2-marker_w/2))
	    m_2.segment(marker_l/2+marker_w/2,"+y",**ld_markers)
	    m12=gdspy.boolean(m_1, m_2, "or",**ld_markers)
	    chip.add(m12)
	    m_1=gdspy.Path(marker_w,(marker_x+marker_l/2+marker_w/2,marker_y+marker_w/2))
	    m_1.segment(marker_l/2+marker_w/2, "-x",**ld_markers)
	    m_2=gdspy.Path(marker_w,(marker_x+marker_w/2,marker_y+marker_l/2+marker_w/2))
	    m_2.segment(marker_l/2+marker_w/2,"-y",**ld_markers)
	    m12=gdspy.boolean(m_1, m_2, "or",**ld_markers)
	    chip.add(m12)


chip = gdspy.Cell("chip")
chip.add(gdspy.Rectangle((0,0),(1*cm,1*cm),layer=0,datatype=0))

x,y = 4*mm,5*mm
for i in range(25):
	for j in range(25):
		chip.add(gdspy.Round((x+i*2*um,y+j*2*um),50*nm/2,tolerance=1e-4))

x,y = 5*mm,5*mm
for i in range(25):
	for j in range(25):
		chip.add(gdspy.Round((x+i*2*um,y+j*2*um),75*nm/2,tolerance=1e-4))

x,y = 6*mm,5*mm
for i in range(25):
	for j in range(25):
		chip.add(gdspy.Round((x+i*2*um,y+j*2*um),125*nm/2,tolerance=1e-4))


etch_markers([(3.95*mm,4.95*mm),(4.95*mm,4.95*mm),(5.95*mm,4.95*mm)],200*um, 15*um)
etch_markers([(3.995*mm,4.995*mm),(4.995*mm,4.995*mm),(5.995*mm,4.995*mm)],9*um, 1*um)


# build
#tk.build_mask(chip, wgt, final_layer=3, final_datatype=0)
gdspy.write_gds('implant_mask.gds', unit=1.0e-6, precision=1.0e-9)