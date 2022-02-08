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
chip.create_wgt(300*nm,0*um,20*um)
chip.deep_etch(2*mm)
chip.etch_markers([(0.8*mm,4.825*mm),(4.8*mm,4.825*mm),(8.8*mm,4.825*mm)],200*um, 10*um)

for i in range(10):
	chip.etch_wg([(1*mm-100*um,4.5*mm+i*25*um),(1*mm+200*um,4.5*mm+i*25*um)])
	chip.etch_wg([(5*mm-100*um,4.5*mm+i*25*um),(5*mm+200*um,4.5*mm+i*25*um)])
	chip.etch_wg([(9*mm-100*um,4.5*mm+i*25*um),(9*mm+200*um,4.5*mm+i*25*um)])


chip.build('HF_HSQ_test_1')