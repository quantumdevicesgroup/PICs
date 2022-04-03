import sys, os
import gdspy
from picwriter import toolkit as tk
import picwriter.components as pc
cm,mm,um,nm = 10**4,10**3,1,10**-3
name = os.path.basename(__file__[:-3])

design = gdspy.Cell("device_layer")
design.add(gdspy.Round((0,0),6*2.54*cm/2,tolerance=1e-1,layer=3,datatype=0))

# for i in range(10):
# 	r = 
# 	PIC.design.add(gdspy.Rectangle((1,1),(2,2)))

# PIC.design.add(gdspy.Rectangle((1,1),(2,2)))



#tk.build_mask(design, self.wgt, final_layer=2, final_datatype=0)
gdspy.write_gds(name+'.gds', unit=1.0e-6, precision=1.0e-9)