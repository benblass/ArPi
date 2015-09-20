#!/usr/bin/env python

import multiprocessing as mp
from threading import Thread
import time
import threading

import sys, select, os

import radargui as r
import sensor457 as s

class RadarGui(Thread):
	def __init__(self, sensex,sensey,maxscale, minscale):
		Thread.__init__(self)
		self.sensex = sensex
		self.sensey = sensey
		self.maxscale = maxscale
		self.minscale = minscale

	def run(self):
		r.initgraph(self.sensex,self.sensey,self.maxscale, self.minscale)


def sensor(sensex, sensey):
	tb = s.top_block(sensex)
	tb.start()
	tb.wait()

if __name__ == '__main__':
	sensex = mp.Value('f',0)
	sensey = mp.Value('f',0)
	
	maxscale = 200
	minscale = 0.05	

	sensorproc = mp.Process(name='daemon', target=sensor, args=(sensex, sensey))
	sensorproc.daemon = True
	sensorproc.start()

	guithread = RadarGui(sensex, sensey, maxscale, minscale)
	guithread.daemon = True
	guithread.start()

	while True:
		if not sensorproc.is_alive():
			exit_status = "Sensing process died - ExitCode : " + str(sensorproc.exitcode)
			break
		if not guithread.is_alive():
			exit_status = "Radar closed -  ExitCode : " + str(guithread.exitcode)
			break

	print "Exiting : " + exit_status