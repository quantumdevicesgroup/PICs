import gdspy, time
import numpy as np
from picwriter import toolkit as tk
import picwriter.components as pc
cm,mm,um,nm = 10**4,10**3,1,10**-3

class PIC:

	def __init__(self, x_domain, y_domain, x_zero=0, y_zero=0):
		self.x_domain, self.y_domain = x_domain,y_domain
		self.x, self.y = 0,0
		self.write_layer = 1
		self.design = gdspy.Cell("device_layer")
		self.design.add(gdspy.Rectangle((0+x_zero,0+y_zero),(x_domain+x_zero, y_domain+y_zero),layer=0,datatype=0))

	def set_write_layer(self, layer):
		self.write_layer = layer
		self.set_wg_width(self.width, self.bend_rad, wg_layer=layer)

	def set_wg_width(self, width, bend_radius=10*um, wg_layer=1, clad_layer=2):
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

	def build(self, name):
		tk.build_mask(self.design, self.wgt, final_layer=2, final_datatype=0)
		gdspy.write_gds(name+'.gds', unit=1.0e-6, precision=1.0e-9)

	def set_origin(self, origin):
		self.x,self.y = origin

	def get_position(self):
		return self.x,self.y

	def wg(self, path):
		origin = self.x, self.y
		coords = []
		for i in range(len(path)):
				self.x,self.y = self.x+path[i][0], self.y+path[i][1]
				coords.append((self.x,self.y))
		wg = pc.Waveguide([origin]+coords,self.wgt)
		self.x,self.y = wg.portlist['output']['port']
		tk.add(self.design, wg)

	def tp(self, path, w1, w2):
		direction = 'EAST'
		if(path[0]<0): direction = 'WEST'
		elif(path[1]>0): direction = 'NORTH'
		elif(path[1]<0): direction = 'SOUTH'
		tp = pc.Taper(self.wgt, max(abs(path[0]),abs(path[1])), port=(self.x,self.y), start_width = w1, end_width = w2, direction=direction)
		self.x,self.y = tp.portlist['output']['port']
		tk.add(self.design, tp)

	def bragg(self, path, period, taper_num, para_rad, perp_rad):
		xm,ym = 1,0
		if(path[0]<0): xm,ym = -1,0
		elif(path[1]>0): xm,ym = 0,1
		elif(path[1]<0): xm,ym = 0,-1
		period_num = int(max(abs(path[0]),abs(path[1]))/period)
		for i in range(period_num):
			self.design.add(gdspy.Round((self.x+xm*(i*period+period/2),self.y+ym*(i*period+period/2)),[abs(xm*para_rad+ym*perp_rad), abs(xm*perp_rad+ym*para_rad)],tolerance=1e-4,layer=3,datatype=0))
		self.design.add(gdspy.Rectangle((self.x,self.y-self.width/2),(self.x + path[0], self.y+self.width/2),layer=4,datatype=0))
		self.x = self.x+path[0]
		self.bool_layer(3,4,"xor",self.write_layer)
		self.design.remove_polygons(lambda pts, layer, datatype: layer==3)
		self.design.remove_polygons(lambda pts, layer, datatype: layer==4)

	def bragg_tp(self, path, period, taper_num, para_rad, perp_rad):
		xm,ym = 1,0
		if(path[0]<0): xm,ym = -1,0
		elif(path[1]>0): xm,ym = 0,1
		elif(path[1]<0): xm,ym = 0,-1
		for i in range(taper_num):
			self.design.add(gdspy.Round((self.x+xm*(i*period+period/2),self.y+ym*(i*period+period/2)),[abs(xm*para_rad+ym*perp_rad)*(i+1)/(taper_num+1), abs(xm*perp_rad+ym*para_rad)*(i+1)/(taper_num+1)],tolerance=1e-4,layer=3,datatype=0))
		self.design.add(gdspy.Rectangle((self.x,self.y-self.width/2),(self.x + xm*taper_num*period, self.y+self.width/2),layer=4,datatype=0))
		self.x = self.x+xm*taper_num*period
		self.bool_layer(3,4,"xor",self.write_layer)
		self.design.remove_polygons(lambda pts, layer, datatype: layer==3)
		self.design.remove_polygons(lambda pts, layer, datatype: layer==4)

	def ring(self, radius, gap, p=1):
		ring = pc.Ring(self.wgt, radius, gap, port=[self.x,self.y], parity = p)
		tk.add(self.design, ring)
		self.x,self.y = ring.portlist['output']['port']

	def edge_mask(self, left, right, top, bottom):
		r_1 = gdspy.Rectangle((0,0),(left,self.y_domain),layer=5,datatype=0)
		r_2 = gdspy.Rectangle((self.x_domain-right,0),(self.x_domain,self.y_domain),layer=5,datatype=0)
		r_11 = gdspy.boolean(r_1, r_2, "or", layer=5)
		r_1 = gdspy.Rectangle((left,self.y_domain-top),(self.x_domain-right,self.y_domain),layer=5,datatype=0)
		r_2 = gdspy.Rectangle((left,bottom),(self.x_domain-right,0),layer=5,datatype=0)
		r_22 = gdspy.boolean(r_1, r_2, "or", layer=5)
		r = gdspy.boolean(r_11, r_22, "or", layer=5)
		self.design.add(r)

	def bool_layer(self,layer_1,layer_2,operation,final_layer):
		layer1 = self.design.get_polygons(by_spec = (layer_1,0))
		layer2 = self.design.get_polygons(by_spec = (layer_2,0))
		#print("Performing "+operation+" on layers "+str(layer_1)+" and "+str(layer_2)+"...")
		#start = time.time()
		layer = gdspy.boolean(layer1,layer2,operation,layer=final_layer)
		#end = time.time()
		#print("Time elapsed: "+str(end-start))
		self.design.add(layer)

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