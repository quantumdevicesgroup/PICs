# Lukasz Komza
# lkomza@berkeley.edu

import gdspy, time
import numpy as np
from picwriter import toolkit as tk
import picwriter.components as pc
cm,mm,um,nm = 10**4,10**3,1,10**-3

class PIC:

	def __init__(self, x_domain, y_domain, origin, layername='device_layer'): # initialize the cell with a rectangle
		self.x_domain, self.y_domain = x_domain, y_domain
		self.x, self.y = origin[0], origin[1]
		self.design = gdspy.Cell(layername)
		self.design.add(gdspy.Rectangle((self.x-self.x_domain/2, self.y-self.y_domain/2),(self.x+self.x_domain/2, self.y+self.y_domain/2),layer=0,datatype=0))
		self.write_layer = 10
		self.width = 300*nm
		self.set_wg_width(width = self.width, wg_layer = 10)

	def set_wg_width(self, width=300*nm, bend_radius=10*um, wg_layer=10, clad_layer=2):
		self.width, self.bend_rad = width, bend_radius
		self.wgt = pc.WaveguideTemplate(wg_width = width,
										clad_width = 0,
										bend_radius = bend_radius,
										resist='-',
										fab='ETCH',
										wg_layer=wg_layer,
										wg_datatype=0,
										clad_layer=clad_layer,
										clad_datatype=0)

	def set_write_layer(self, layer):
		self.write_layer = layer
		self.set_wg_width(width = self.width, wg_layer=layer)

	def build(self, name):
		tk.build_mask(self.design, self.wgt, final_layer=3, final_datatype=0)
		gdspy.write_gds(name+'.gds', unit=1.0e-6, precision=1.0e-9)

	def wg(self, path, origin=None, width=None):

		if(origin): # if an override exists, use it
			self.x, self.y = origin
		start = self.x, self.y

		if(width):
			width_holder = self.width
			self.set_wg_width(width=width, wg_layer=self.write_layer)

		if(type(path) is list): # if path is a list of coordinates, [(x1,y1), (x2,y2), ...]
			coords = []
			for i in range(len(path)):
				self.x, self.y = self.x + path[i][0], self.y + path[i][1]
				coords.append((self.x, self.y))
			wg = pc.Waveguide([start] + coords, self.wgt)

		if(type(path) is tuple): # if path is a single coordinate, (x,y)
			self.x, self.y = self.x + path[0], self.y + path[1]
			wg = pc.Waveguide([start] + [[self.x, self.y]], self.wgt)

		if(type(path) is float or int): # if path is a single number, x
			self.x += path
			wg = pc.Waveguide([start] + [[self.x, self.y]], self.wgt)

		self.x, self.y = wg.portlist['output']['port']
		tk.add(self.design, wg)

		if(width):
			self.set_wg_width(width=width_holder, wg_layer=self.write_layer)

	def tp(self, path, w1, w2):

		direction = 'EAST'
		if(type(path) is tuple): # if path is a single coordinate, (x,y)
			if(path[0] < 0): direction = 'WEST'
			elif(path[1] > 0): direction = 'NORTH'
			elif(path[1] < 0): direction = 'SOUTH'
			tp = pc.Taper(self.wgt, max(abs(path[0]),abs(path[1])), port=(self.x, self.y), start_width = w1, end_width = w2, direction = direction)

		if(type(path) is float or int): # if path is a single number, x
			if(path < 0): direction = 'WEST'
			tp = pc.Taper(self.wgt, abs(path), port=(self.x, self.y), start_width = w1, end_width = w2, direction = direction)

		self.x, self.y = tp.portlist['output']['port']
		tk.add(self.design, tp)

	def bragg(self, path, period, taper_num, para_rad, perp_rad):
		xm,ym = 1,0
		if(path[0]<0): xm,ym = -1,0
		elif(path[1]>0): xm,ym = 0,1
		elif(path[1]<0): xm,ym = 0,-1
		period_num = int(max(abs(path[0]),abs(path[1]))/period + 0.5)
		for i in range(period_num):
			self.design.add(gdspy.Round((self.x+xm*(i*period+period/2),self.y+ym*(i*period+period/2)),[abs(xm*para_rad+ym*perp_rad), abs(xm*perp_rad+ym*para_rad)],tolerance=1e-4,layer=8,datatype=0))
		self.design.add(gdspy.Rectangle((self.x,self.y-self.width/2),(self.x + path[0], self.y+self.width/2),layer=9,datatype=0))
		self.x = self.x+path[0]
		self.bool_layer(8,9,"xor",self.write_layer)
		self.design.remove_polygons(lambda pts, layer, datatype: layer==8)
		self.design.remove_polygons(lambda pts, layer, datatype: layer==9)

	def bool_layer(self, layer_1, layer_2, operation, final_layer, debug=False):
		layer1 = self.design.get_polygons(by_spec = (layer_1,0))
		layer2 = self.design.get_polygons(by_spec = (layer_2,0))
		if(debug):
			print("Performing "+operation+" on layers "+str(layer_1)+" and "+str(layer_2)+"...")
			start = time.time()
		layer = gdspy.boolean(layer1,layer2,operation,layer=final_layer)
		if(debug):
			end = time.time()
			print("Time elapsed: "+str(end-start))
		self.design.add(layer)

	def edge_mask(self, left, right, top, bottom):
		r_1 = gdspy.Rectangle((0,0),(left,self.y_domain),layer=5,datatype=0)
		r_2 = gdspy.Rectangle((self.x_domain-right,0),(self.x_domain,self.y_domain),layer=5,datatype=0)
		r_11 = gdspy.boolean(r_1, r_2, "or", layer=5)
		r_1 = gdspy.Rectangle((left,self.y_domain-top),(self.x_domain-right,self.y_domain),layer=5,datatype=0)
		r_2 = gdspy.Rectangle((left,bottom),(self.x_domain-right,0),layer=5,datatype=0)
		r_22 = gdspy.boolean(r_1, r_2, "or", layer=5)
		r = gdspy.boolean(r_11, r_22, "or", layer=5)
		self.design.add(r)

	def markers(self, coords, m_l, m_w):
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
		    self.design.add(m12)
		    m_1=gdspy.Path(marker_w,(marker_x+marker_l/2+marker_w/2,marker_y+marker_w/2))
		    m_1.segment(marker_l/2+marker_w/2, "-x",**ld_markers)
		    m_2=gdspy.Path(marker_w,(marker_x+marker_w/2,marker_y+marker_l/2+marker_w/2))
		    m_2.segment(marker_l/2+marker_w/2,"-y",**ld_markers)
		    m12=gdspy.boolean(m_1, m_2, "or",**ld_markers)
		    self.design.add(m12)