#!/usr/bin/env python

import wx
import math

import multiprocessing as mp
import time
import random
import math
"""
def sensor(sensex, sensey):
	while True:
		time.sleep(0.75)
		sensex.value = random.uniform(180,221)
		sensey.value = random.uniform(180,221)
"""

class PPMenu(wx.Menu):
	def __init__(self, parent):
		super(PPMenu, self).__init__()

		self.parent = parent


		cmi = wx.MenuItem(self, wx.NewId(), 'Close')
		self.AppendItem(cmi)
		self.Bind(wx.EVT_MENU, self.onClose, cmi)

	def onClose(self, e):
		self.parent.Close()

	def onNew(self, e):
		self.parent.Change(None)

class Marker(object):

	def __init__(self, x=0,y=1):
		self._x = x
		self._y = y

	def x(self):
		return self._x

	def y(self):
		return self._y

	def set_x(self, x):
		self._x = x

	def set_y(self, y):
		self._y = y

	def set(self,x,y):
		self._x = x
		self._y = y

class radarGraph(wx.Panel):

	Speed = 100
	ID_TIMER = 1


	def __init__(self, parent, maxscale, minscale):
		self.maxscale = maxscale #signal which will show contact (at "1" on the graph)
		self.minscale = minscale #signal which will show at the limit of the graph (10)
		self.alpha = 1.0/9*(self.maxscale - self.minscale)
		self.p = self.maxscale+self.alpha
		self.rot = math.cos(math.pi/4.0)

		wx.Panel.__init__(self, parent)

		self.sensex = parent.sensex
		self.sensey = parent.sensey

		self.SetBackgroundColour('WHITE')
		self.Bind(wx.EVT_PAINT, self.OnPaint)

		self.timer = wx.Timer(self, radarGraph.ID_TIMER)

		self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(wx.EVT_TIMER, self.Change, id=radarGraph.ID_TIMER)

		self.marker=Marker()

		self.timer.Start(radarGraph.Speed)

	def OnRightDown(self, e):
		self.PopupMenu(PPMenu(self), e.GetPosition())

	def OnPaint(self, event):
		dc = wx.PaintDC(self)
		self.size_x, self.size_y = self.GetClientSizeTuple()
		self.radar_radius = min(self.size_y*0.85/(self.rot*2), self.size_x / 2)
		dc.SetDeviceOrigin(self.size_x/2, self.size_y*0.9)
		dc.SetAxisOrientation(True, True)

		region = wx.Region(0,self.size_y*0.005,self.size_x,self.size_y*0.9)
		dc.SetClippingRegionAsRegion(region)


		self.DrawAxis(dc)
		self.DrawGrid(dc)
		self.DrawMarker(dc)
		#self.DrawCoords(dc)

		dc.DestroyClippingRegion()

	def DrawAxis(self, dc):
		dc.SetPen(wx.Pen('#1ac500',2, wx.SOLID))
		dc.DrawLine(0,0,-self.radar_radius*self.rot*2*self.rot,self.radar_radius*self.rot*2*self.rot)
		dc.DrawLine(0,0,self.radar_radius*self.rot*2*self.rot,self.radar_radius*self.rot*2*self.rot)

		for i in range(0,21,1):
			dc.DrawLine(-self.radar_radius,0,self.radar_radius,0)

			dc.DrawLine(self.rot * self.radar_radius * (0.05*i+0.01), 
				self.rot * self.radar_radius * (0.05*i-0.01),
				self.rot * self.radar_radius * (0.05*i-0.01), 
				self.rot * self.radar_radius * (0.05*i+0.01))
		
			dc.DrawLine(self.rot * self.radar_radius * (-0.01-0.05*i), self.rot * self.radar_radius * (0.05*i-0.01),
				self.rot * self.radar_radius * (-0.05*i+0.01), self.rot * self.radar_radius * (0.05*i+0.01))

	def DrawGrid(self, dc):
		dc.SetBrush(wx.Brush('#4c4c4c', wx.TRANSPARENT))
		dc.SetPen(wx.Pen('#bbbbbb', 2, wx.SOLID))
		
		for i in range(1,11,1):
			dc.DrawCircle(0,0,self.radar_radius*0.1*i)

			dc.DrawPolygon(((0,0),
				(self.rot*self.radar_radius*0.1*i,self.rot*self.radar_radius*0.1*i),
				(0,2*self.rot*self.radar_radius*0.1*i),
				(-self.rot*self.radar_radius*0.1*i,self.rot*self.radar_radius*0.1*i)))

		dc.SetPen(wx.Pen('#555555', 3, wx.SOLID))
		dc.DrawCircle(0,0,self.radar_radius/2)
		dc.DrawCircle(0,0,self.radar_radius)

		dc.DrawCircle(0,0,self.radar_radius*2*self.rot)



	def DrawMarker(self, dc):
		x = self.marker.x()
		y = self.marker.y()
		dist = math.sqrt(x*x + y*y)
		if (dist > 1):
			dc.SetPen(wx.Pen('#ee2222', 15, wx.SOLID))

			dc.DrawLine(0,0,
				(x-y)*self.radar_radius/10.0*self.rot,
				(x+y)*self.radar_radius/10.0*self.rot)

			dc.SetPen(wx.Pen('#ff9999', 4, wx.SOLID))
			dc.DrawLine(0,0,
				(x-y)*self.radar_radius*self.rot*2/dist*self.rot,
				(x+y)*self.radar_radius*self.rot*2/dist*self.rot)

		else:
			dc.SetPen(wx.Pen('#ff0000', 4, wx.SOLID))
			dc.SetBrush(wx.Brush('#ff0000', wx.CROSSDIAG_HATCH))
			dc.DrawCircle(0,0,self.radar_radius)

	def Change(self,event):

		newXcoord, newYcoord = self.getNewData()
		if (newXcoord != self.marker.x() or newYcoord != self.marker.y()):
			self.marker.set(newXcoord, newYcoord)

			dc = wx.PaintDC(self)
			dc.Clear()

			dc.SetDeviceOrigin(self.size_x/2, self.size_y*0.9)
			dc.SetAxisOrientation(True, True)

			region = wx.Region(0,self.size_y*0.005,self.size_x,self.size_y*0.9)
			dc.SetClippingRegionAsRegion(region)

			self.DrawAxis(dc)
			self.DrawGrid(dc)
			self.DrawMarker(dc)
			#self.DrawCoords(dc)

			dc.DestroyClippingRegion()

	def getNewData(self):

		newXcoord = (self.p-self.sensex.value) / self.alpha
		newYcoord = (self.p-self.sensey.value) / self.alpha

		return newXcoord, newYcoord

	def onClose(self, event):
		self.Destroy()

class ArvaFrame(wx.Frame):
	def __init__(self, parent,sensex,sensey,maxscale,minscale):
		super(ArvaFrame, self).__init__(parent, style=wx.CLOSE_BOX |  wx.CAPTION)
		self.sensex = sensex
		self.sensey = sensey		
		self.SetSize((800,800))
		self.SetTitle('ArPi')
	
		radar = radarGraph(self,maxscale, minscale)

		self.Centre()
		self.Show(True)
		self.ShowFullScreen(True)

	def OnQuit(self, e):
		self.Close()

def initgraph(sensex,sensey,maxscale, minscale):
	arpi = wx.PySimpleApp()
	ArvaFrame(None,sensex,sensey,maxscale, minscale)
	arpi.MainLoop()