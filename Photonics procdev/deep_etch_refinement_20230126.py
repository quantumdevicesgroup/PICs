import sys, os
sys.path.append("..")
from PIC_class import *
cm,mm,um,nm = 10**4,10**3,1,10**-3
name = os.path.basename(__file__[:-3])

PIC = PIC(1*cm, 1*cm, (0.5*cm, 0.5*cm))
PIC.wg(10*um) # I'm lazy


PIC.Rectangle(((0*mm), (0*mm)), 10) # deep etch mask
PIC.Rectangle(((0*mm), (0*mm)), 10) # edge removal mask


PIC.build(name)