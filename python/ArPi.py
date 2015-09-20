#!/usr/bin/env python

import multiprocessing as mp
from threading import Thread
import time
import threading

import sys, select, os

import radargui as r
import sensor457 as s



"""
class Sensor(mp.Process):
	def __init__(self, sensex, sensey):
		mp.Process.__init__(self)
		self.tb = s.top_block(sensex)

	def run(self):
		self.tb.start()
		self.tb.wait()
		
	def stop (self):
		self.tb.stop()
"""

def Sensor(sensex, sensey):
	tb = s.top_block(sensex)
	tb.start()
	tb.wait()

if __name__ == '__main__':
	sensex = mp.Value('f',0)
	sensey = mp.Value('f',0)
	
	maxscale = 1000
	minscale = 0.05	

	sensorproc = mp.Process(target=Sensor, args=(sensex, sensey))
	sensorproc.daemon = True
	sensorproc.start()

	guithread = r.RadarGui(sensex, sensey, maxscale, minscale)
	guithread.daemon = True
	guithread.start()

	while True:
		time.sleep(1)
		if not sensorproc.is_alive():
			exit_status = "Sensing process died - ExitCode : " + str(sensorproc.exitcode)
			break
		if not guithread.is_alive():			
			exit_status = "Radar closed"
			sensorproc.stop()
			sensorproc.terminate()
			break

	print "Exiting : " + exit_status