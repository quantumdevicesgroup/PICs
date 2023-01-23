# Lukasz Komza
# lkomza@berkeley.edu

import gdspy, time
import numpy as np
from picwriter import toolkit as tk
import picwriter.components as pc
from transmission_line import transmission_line as tl, cpw

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
		gdspy.write_gds(name+'.gds', unit=1.0e-6, precision=1e-9)

	def get_position(self):
		return self.x,self.y

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

		if((type(path) is float) or (type(path) is int)): # if path is a single number, x
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
			self.design.add(gdspy.Round((self.x+xm*(i*period+period/2),self.y+ym*(i*period+period/2)),[abs(xm*para_rad+ym*perp_rad), abs(xm*perp_rad+ym*para_rad)],number_of_points=50,layer=8,datatype=0))
		self.design.add(gdspy.Rectangle((self.x,self.y-self.width/2),(self.x + path[0], self.y+self.width/2),layer=9,datatype=0))
		self.x = self.x+path[0]
		self.bool_layer(8,9,"xor",self.write_layer)
		self.design.remove_polygons(lambda pts, layer, datatype: layer==8)
		self.design.remove_polygons(lambda pts, layer, datatype: layer==9)

	def bragg_tp(self, path, period, taper_num, para_rad, perp_rad):
		xm,ym = 1,0
		if(path[0]<0): xm,ym = -1,0
		elif(path[1]>0): xm,ym = 0,1
		elif(path[1]<0): xm,ym = 0,-1
		for i in range(taper_num):
			self.design.add(gdspy.Round((self.x+xm*(i*period+period/2),self.y+ym*(i*period+period/2)),[abs(xm*para_rad+ym*perp_rad)*(i+1)/(taper_num+1), abs(xm*perp_rad+ym*para_rad)*(i+1)/(taper_num+1)],number_of_points=50,layer=8,datatype=0))
		self.design.add(gdspy.Rectangle((self.x-ym*self.width/2,self.y-xm*self.width/2),(self.x + xm*taper_num*period+ym*self.width/2, self.y+ ym*taper_num*period+xm*self.width/2),layer=9,datatype=0))
		self.x = self.x+xm*taper_num*period
		self.y = self.y+ym*taper_num*period
		self.bool_layer(8,9,"xor",self.write_layer)
		self.design.remove_polygons(lambda pts, layer, datatype: layer==8)
		self.design.remove_polygons(lambda pts, layer, datatype: layer==9)

	def ring(self, radius, gap, p=1):
		ring = pc.Ring(self.wgt, radius, gap, port=[self.x,self.y], parity = p)
		tk.add(self.design, ring)
		self.x,self.y = ring.portlist['output']['port']

	def pcc(self, direct, inverse, a_m, a_d, N_trans, N_front, N_taper, N_back, ff, sweep): 
		xm,ym=inverse,0
		if (direct):
			xm,ym=0,inverse

		path1=[xm*N_trans*a_m,ym*N_trans*a_m]
		self.bragg_tp(path1,a_m,N_trans,a_m*ff/2+sweep,a_m*ff/2+sweep)
		
		path2=[xm*N_front*a_m,ym*N_front*a_m]
		self.bragg(path2,a_m,0,a_m*ff/2+sweep,a_m*ff/2+sweep)

		d=(a_m-a_d)*2/(N_taper+1)
		x0=self.x
		y0=self.y
		for i in range(1, N_taper+1):
			index=abs(i-(N_taper+1)/2)
			self.design.add(gdspy.Round((self.x+xm*(a_d+index*d)/2,self.y+ym*(a_d+index*d)/2),[ff*(a_d+index*d)/2+sweep, ff*(a_d+index*d)/2+sweep],tolerance=1e-4,layer=8,datatype=0))
			self.x= self.x+xm*(a_d+index*d)
			self.y= self.y+ym*(a_d+index*d)
		self.design.add(gdspy.Rectangle((x0-ym*self.width/2,y0-xm*self.width/2),(self.x+ym*self.width/2, self.y+xm*self.width/2),layer=9,datatype=0))
		self.bool_layer(8,9,"xor",self.write_layer)
		self.design.remove_polygons(lambda pts, layer, datatype: layer==8)
		self.design.remove_polygons(lambda pts, layer, datatype: layer==9)
		path3=[xm*N_back*a_m,ym*N_back*a_m]
		self.bragg(path3,a_m,0,a_m*ff/2+sweep,a_m*ff/2+sweep)

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

	def Rectangle(self, coords, layer): 
		r = gdspy.Rectangle(coords[0], coords[1], layer=layer)
		self.design.add(r)
	
    
	def markers_protect(self, coords, layer, size): 
		for i in range(len(coords)):
			lb = (coords[i][0]-size*um, coords[i][1]-size*um)
			rt = (coords[i][0]+size*um, coords[i][1]+size*um)
			self.Rectangle([lb, rt], layer=layer)
	
	def get_coordinate(self, coord, n, start, stop, pair=None): #record the position of each set of wg and connect
		if pair is None or pair%2 == 0:
			if n%2 == 1:
				coord.append(start)
				coord.append(stop)
			else:
				coord.append(stop)
				coord.append(start)
		else:
			if n%2 == 0:
				coord.append(start)
				coord.append(stop)
			else:
				coord.append(stop)
				coord.append(start)
	
	def add_pt(self, coord, turn_bt, turn_tp): #smoonth the end of CPW on wg
		bottom_port = coord[0]
		top_port = coord[-1]
		bottom_add = tuple([bottom_port[0]+turn_bt,bottom_port[1]])
		top_add = tuple([top_port[0]+turn_tp,top_port[1]])
		coord.append(top_add)
		coord.insert(0, bottom_add)

	# Positive: written in regions where metal should be deposited. 
	# Negative: written only gap regions (where metal shouldn't be deposited)

	def feedline(self, coord, trace, gap, ground, lay, radius=None, positive=True):
		feedline_cpw = cpw.CPW(outline=coord, trace=trace, gap=gap, ground=ground, radius=None)
		if positive:
			feedline_cpw.draw(cell=self.design, origin=(0,0), layer=lay, draw_trace=True, draw_gap=False, draw_ground=True)
		else:
			feedline_cpw.draw(cell=self.design, origin=(0,0), layer=lay, draw_trace=False, draw_gap=True, draw_ground=False)
	
	def get_vertices(self, endpt, trace, gap, ground, radius=None):
		coord = [(0,0), (endpt, 0)]
		vertices = cpw.CPW(outline=coord, trace=trace, gap=gap, ground=ground, radius=None)
		return vertices
	
	def get_transition_vertices(self, trace1, trace2, gap1, gap2, ground1, ground2, trans_len):
		transition = cpw.CPWTransition(start_point=(0, 0), end_point=np.array([trans_len,0]), start_trace=trace1, end_trace=trace2, start_gap=gap1, end_gap=gap2, start_ground=ground1, end_ground=ground2)
		return transition


	def draw_connect_launch(self, connect, launch, border1, transition, startpt, layer, border2=None, positive=True):
		if positive:
			feedline = tl.SegmentList([connect, transition, launch, border1, border2])
			feedline.draw(cell=self.design, origin=startpt, layer=layer, draw_trace=True, draw_gap=False, draw_ground=True, individual_keywords={3:dict(draw_trace=False), 4:dict(draw_gap=True)})
		else:
			feedline = tl.SegmentList([connect, transition, launch, border1])
			feedline.draw(cell=self.design, origin=startpt, layer=layer, draw_trace=False, draw_gap=True, draw_ground=False, individual_keywords={3:dict(draw_trace=True, draw_gap=True)})

	def draw_transition(self, vertices, startpt, layer, positive=True):
		if positive:
			vertices.draw(cell=self.design, origin=startpt, layer=layer, draw_trace=True, draw_gap=False, draw_ground=True)
		else:
			vertices.draw(cell=self.design, origin=startpt, layer=layer, draw_trace=False, draw_gap=True, draw_ground=False)


	def connect_two_seg(self, coord1, a, coord2, b, trace, gap, ground, layer, radius=None, positive=True):
		path = []
		pt1 = coord1[-1]
		pt2 = coord2[0]
		for i in range(a):
			addpt = tuple([pt1[0]+i*10*um, pt1[1]])
			path.append(addpt)
		for i in range(b):
			addpt = tuple([pt2[0]+(b-1-i)*10*um, pt2[1]])
			path.append(addpt)
		line = cpw.CPW(outline=path, trace=trace, gap=gap, ground=ground, radius=None)
		if positive:
			line.draw(cell=self.design, origin=(0,0), layer=layer, draw_trace=True, draw_gap=False, draw_ground=True)
		else:
			line.draw(cell=self.design, origin=(0,0), layer=layer, draw_trace=False, draw_gap=True, draw_ground=False)
	
	def micropucks(self, start, radius, layer, repeat, interval=None):
		if (type(radius) is int):
			r = gdspy.Round(start, radius, tolerance=1E-4, layer=layer)
			self.design.add(r)
			if (repeat > 1):
				for j in range(repeat - 1):
					#start[0] += radius + interval + radius
					start[0] += interval
					r = gdspy.Round(start, radius, tolerance=1E-4, layer=layer)
					self.design.add(r)
		else:
			for i in range (len(radius)):
				if i == 0:
					r = gdspy.Round(start, radius[i], tolerance=1E-4, layer=layer)
					self.design.add(r)
					if (repeat > 1):
						for j in range (repeat - 1):
							#start[0] += radius[0] + interval + radius[0]
							start[0] += interval
							r = gdspy.Round(start, radius[i], tolerance=1E-4, layer=layer)
							self.design.add(r)
				else:
					#start[0] += radius[i-1] + interval + radius[i]
					start[0] += 2*interval
					r = gdspy.Round(start, radius[i], tolerance=1E-4, layer=layer)
					self.design.add(r)
					if (repeat > 1):
						for j in range (repeat - 1):
							#start [0] += radius[i] + interval + radius[i]
							start [0] += interval
							r = gdspy.Round(start, radius[i], tolerance=1E-4, layer=layer)
							self.design.add(r)
