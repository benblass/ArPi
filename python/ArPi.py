#!/usr/bin/env python

import multiprocessing as mp
import time
import threading
import sensor457 as s

def daemon(val):
	tb = dummysensor(val)
	time.sleep(5)

class dummysensor():
	def __init__(self, val):
		def _measure_(val):
			val.value = 7
		_measure_thread = threading.Thread(target=_measure_, args=(val,))
		_measure_thread.daemon = True
		_measure_thread.start()

if __name__ == '__main__':
	v = mp.Value('f',0)
	d = mp.Process(name='daemon', target=daemon, args=(v,))

	d.start()
	time.sleep(2)
	d.terminate()
	print v.value

