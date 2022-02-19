"""
Lukasz Komza
lkomza@berkeley.edu
"""
import gdspy, time
import numpy as np
from picwriter import toolkit as tk
import picwriter.components as pc

def calculate_bragg_rads(wg_w,u_cell,ff):
	h = np.sqrt(ff * u_cell**2 / np.pi)
	v = h * (wg_w/u_cell)
	return h,v

class Chip:

	def __init__(self, x, y, field, dx=0,dy=0):
		self.x,self.y = x,y
		self.chip = gdspy.Cell("chip")
		self.chip.add(gdspy.Rectangle((0+dx,0+dy),(x+dx,y+dy),layer=0,datatype=0))
		self.write_layer = 1
		#for i in range(int(self.x/field)): # field size stitching from e-beam
			#for j in range(int(self.y/field)):
				#self.chip.add(gdspy.Rectangle((i*field,j*field),((i+1)*field,(j+1)*field),layer=17,datatype=0))

	def build(self,name):
		tk.build_mask(self.chip, self.wgt, final_layer=3, final_datatype=0)
		gdspy.write_gds(name+'.gds', unit=1.0e-6, precision=1.0e-9)

	def change_write_layer(self, layer):
		self.wgt = pc.WaveguideTemplate(wg_width=self.wg_width,clad_width=self.clad_width,bend_radius=self.bend_rad,resist='-', fab='ETCH',wg_layer=layer,wg_datatype=0,clad_layer=2,clad_datatype=0)
		self.write_layer = layer

	def create_wgt(self,wgw,cw,br):
		self.wgt = pc.WaveguideTemplate(wg_width=wgw,clad_width=cw,bend_radius=br,resist='-', fab='ETCH',wg_layer=1,wg_datatype=0,clad_layer=2,clad_datatype=0)
		self.wg_width,self.clad_width,self.bend_rad = wgw,cw,br

	def etch_label(self,s,h,text):
		self.chip.add(gdspy.Text(text, h, s,layer=self.write_layer))

	def deep_etch(self,d_e_l):
		self.deep_etch_len = d_e_l
		self.chip.add(gdspy.Rectangle((0,0),(self.deep_etch_len,self.y),layer=5,datatype=0))
		self.chip.add(gdspy.Rectangle((self.x-self.deep_etch_len,0),(self.x,self.y),layer=5,datatype=0))

	def etch_wg(self,path,w=False):
		if(w):
			store_wgt = self.wgt
			self.wgt = pc.WaveguideTemplate(wg_width=w,clad_width=self.clad_width,bend_radius=self.bend_rad,resist='-', fab='ETCH',wg_layer=self.write_layer,wg_datatype=0,clad_layer=2,clad_datatype=0)
			wg = pc.Waveguide(path,self.wgt)
			tk.add(self.chip, wg)
			self.wgt = store_wgt
			return path[-1]
		else:
			wg = pc.Waveguide(path,self.wgt)
			tk.add(self.chip, wg)
			return path[-1]

	def etch_uturn(self,s,d,parity=1):
		if(d == 'WEST'):
			self.etch_wg([	(s[0],s[1]),
							(s[0]+self.bend_rad,s[1]),
							(s[0]+self.bend_rad,s[1]+2*self.bend_rad*parity),
							(s[0],s[1]+2*self.bend_rad*parity)])
			return s[0],s[1]+2*self.bend_rad*parity
		if(d == 'EAST'):
			self.etch_wg([	(s[0],s[1]),
							(s[0]-self.bend_rad,s[1]),
							(s[0]-self.bend_rad,s[1]+2*self.bend_rad),
							(s[0],s[1]+2*self.bend_rad)])
			return s[0],s[1]+2*self.bend_rad

	def etch_scurve(self,s,y,d):
		if(d == 'EAST'):
			self.etch_wg([	(s[0],s[1]),
							(s[0]+self.bend_rad,s[1]),
							(s[0]+self.bend_rad,s[1]+2*self.bend_rad+y),
							(s[0]+2*self.bend_rad,s[1]+2*self.bend_rad+y)])
			return s[0]+2*self.bend_rad,s[1]+2*self.bend_rad+y
		if(d == 'WEST'):
			self.etch_wg([	(s[0],s[1]),
							(s[0]-self.bend_rad,s[1]),
							(s[0]-self.bend_rad,s[1]+2*self.bend_rad+y),
							(s[0]-2*self.bend_rad,s[1]+2*self.bend_rad+y)])
			return s[0]-2*self.bend_rad,s[1]+2*self.bend_rad+y

	def etch_tight_uturn(self,s,g,d):
		rad_1 = self.bend_rad + g
		if(d == 'WEST'):
			self.etch_wg([	(s[0],s[1]),
							(s[0]+rad_1,s[1]),
							(s[0]+rad_1,s[1]+2*rad_1),
							(s[0]-self.bend_rad,s[1]+2*rad_1),
							(s[0]-self.bend_rad,s[1]+g),
							(s[0]-2*self.bend_rad,s[1]+g)])
			return s[0]-2*self.bend_rad,s[1]+g
		if(d == 'EAST'):
			self.etch_wg([	(s[0],s[1]),
							(s[0]-rad_1,s[1]),
							(s[0]-rad_1,s[1]+2*rad_1),
							(s[0]+self.bend_rad,s[1]+2*rad_1),
							(s[0]+self.bend_rad,s[1]+g),
							(s[0]+2*self.bend_rad,s[1]+g)])
			return s[0]+2*self.bend_rad,s[1]+g

	def etch_tp(self,s,l,s_w,e_w):
		s = (s[0],s[1])
		if(s_w<e_w):
			tp = pc.Taper(self.wgt,l,port=(s[0]+l,s[1]),start_width=e_w,end_width=s_w,direction='WEST')
		if(s_w>=e_w):
			tp = pc.Taper(self.wgt,l,port=s,start_width=s_w,end_width=e_w,direction='EAST')
		tk.add(self.chip, tp)
		return s[0]+l,s[1]

	def etch_saw_bragg_ref(self,s,l,tp,p,dc,wid,w=False):
		if(w):
			store_wgt = self.wgt
			self.wgt = pc.WaveguideTemplate(wg_width=w,clad_width=self.clad_width,bend_radius=self.bend_rad,resist='-', fab='ETCH',wg_layer=self.write_layer,wg_datatype=0,clad_layer=2,clad_datatype=0)
			br = pc.DBR(self.wgt,l,p,dc,wid,taper_length=tp,port=s)
			tk.add(self.chip, br)
			return s[0]+l+2*tp,s[1]
		else:
			br = pc.DBR(self.wgt,l,p,dc,wid,taper_length=tp,port=s)
			tk.add(self.chip, br)
			return s[0]+l+2*tp,s[1]

	def etch_circ_bragg_ref(self,s,n1,n2,sp,h_r,v_r):
		for i in range(n2+1):
			self.chip.add(gdspy.Round((s[0]+i*sp,s[1]),[h_r*(i+1)/(n2+1),v_r*(i+1)/(n2+1)],tolerance=1e-4,layer=8,datatype=0))
		for i in range(n1):
			self.chip.add(gdspy.Round((s[0]+(i+n2)*sp,s[1]),[h_r,v_r],tolerance=1e-4,layer=8,datatype=0))

	def etch_circ_bragg_ref_left(self,s,n1,n2,sp,h_r,v_r):
		for i in range(n2+1):
			self.chip.add(gdspy.Round((s[0]-i*sp,s[1]),[h_r*(i+1)/(n2+1),v_r*(i+1)/(n2+1)],tolerance=1e-4,layer=3,datatype=0))
		for i in range(n1):
			self.chip.add(gdspy.Round((s[0]-(i+n2)*sp,s[1]),[h_r,v_r],tolerance=1e-4,layer=3,datatype=0))

	def etch_circ_bragg_tp(self,s,n,sp,h_r,v_r):
		for i in range(n):
			frac = (i+1)/n
			v = v_r*frac
			h = h_r*frac
			self.chip.add(gdspy.Round((s[0]+i*sp,s[1]),[h,v],tolerance=1e-4,layer=4,datatype=0))

	def etch_directional_coupler(self,s,l,g): # doesnt work, old args
		cp = pc.DirectionalCoupler(self.wgt,l,g,port=s,parity=-1)
		tk.add(self.chip, cp)
		return cp.portlist['output_bot']['port'],cp.portlist['output_top']['port'],cp.portlist['input_top']['port']

	def etch_ring(self,s,r,g,p):
		rg = pc.Ring(self.wgt,r,g,port=s,parity=p)
		tk.add(self.chip, rg)
		return s[0]+2*r,s[1]

	def etch_markers(self, coords, m_l, m_w):
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
		    self.chip.add(m12)
		    m_1=gdspy.Path(marker_w,(marker_x+marker_l/2+marker_w/2,marker_y+marker_w/2))
		    m_1.segment(marker_l/2+marker_w/2, "-x",**ld_markers)
		    m_2=gdspy.Path(marker_w,(marker_x+marker_w/2,marker_y+marker_l/2+marker_w/2))
		    m_2.segment(marker_l/2+marker_w/2,"-y",**ld_markers)
		    m12=gdspy.boolean(m_1, m_2, "or",**ld_markers)
		    self.chip.add(m12)

	def bool_layer(self,l1,l2,op,lt):
		layer1 = self.chip.get_polygons(by_spec = (l1,0))
		layer2 = self.chip.get_polygons(by_spec = (l2,0))
		print("Performing "+op+" on layers "+str(l1)+" and "+str(l2)+"...")
		start = time.time()
		layer = gdspy.boolean(layer1,layer2,op,layer=lt)
		end = time.time()
		print("Time elapsed: "+str(end-start))
		self.chip.add(layer)