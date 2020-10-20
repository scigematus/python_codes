from bokeh.layouts import column, layout
from bokeh.models import ColumnDataSource, Slider
from bokeh.models.widgets import Button, TextInput, PreText
from bokeh.plotting import figure
from bokeh.server.server import Server
from bokeh.document import without_document_lock
import numpy as np
from tornado import gen
from tornado.queues import Queue
from functools import partial
import time
import pandas as pd

pd.set_option('display.max_colwidth', 100)

import sys
import asyncio

if int(sys.version[2]) > 7:
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def bkapp(doc):
	class status():
		def __init__(self):
			self.on = False
			self.ready = 0

		@gen.coroutine
		@without_document_lock
		def turn_on(self):
			self.on = True

		@gen.coroutine
		@without_document_lock
		def turn_off(self):
			self.on = False

	class graph():
		def __init__(self, q, stat):
			self.q = q
			self.stat = stat
			self.source = ColumnDataSource(data=dict(x=[], y=[]))
			self.plot = figure(y_axis_label='Voltage (Volt)', title='Live Data', output_backend='webgl')
			self.plot.circle(x='x', y='y', source=self.source)

		@gen.coroutine
		@without_document_lock
		def update(self, x, y):
			self.source.stream(dict(x=x,y=y))
	
		@gen.coroutine
		@without_document_lock
		def excute(self, txt):
			while True:
				if not self.stat.on:
					break
				yield gen.sleep(0.5)
				x = []
				y = []
				while True:
					try:
						xy = self.q.get_nowait()
						x.append(xy[0])
						y.append(xy[1])
					except:
						break
				doc.add_next_tick_callback(partial(self.update, x=x, y=y))
			print('task_finish')
			stat.ready += 1

	class measure():
		def __init__(self, q, stat):
			self.q = q
			self.stat = stat
			self.div = PreText(text = 'recipe file:\n')
			
		@gen.coroutine
		@without_document_lock
		def excute(self, txt):
			try:
				recipe_df = pd.read_csv(txt.value, delimiter=',', header=None)
				self.div.text = 'recipe file:\n' + str(recipe_df)
				print(str(recipe_df))
				i = 0
				y0 = time.time()
				while True:
					if not self.stat.on:
						break
					yield gen.sleep(0.05)
					i += 1
					y = time.time()
					xy = [i, y-y0]
					y0 = y
					self.q.put(xy)
				stat.turn_off
				stat.ready += 1
				print('measure_finish')
			except Exception as exception:
				print(exception)

	class starter():
		def __init__(self, stat, *args):
			self.num = len(args)
			stat.ready = self.num
			self.args = args
			self.stat = stat
		def ignite(self, txt):
			if (not self.stat.on) and (stat.ready > self.num - 1):
				stat.ready = 0
				self.stat.turn_on()
				for arg in self.args:
					arg.excute(txt1)

	stat = status()
	q1 = Queue()
	btn1 = Button(label='START', button_type='success')
	btn2 = Button(label='STOP', button_type='danger')
	txt1 = TextInput(title='Folder:', value='recipe_example.csv')
	grp1 = graph(q1, stat)
	msr1 = measure(q1, stat)
	strtr = starter(stat, grp1, msr1)
	btn1.on_click(strtr.ignite)
	btn2.on_click(stat.turn_off)	
	doc.add_root(layout([[txt1], [btn1], [msr1.div], [grp1.plot], [btn2]]))

server = Server({'/': bkapp}, num_procs=1)
server.start()

if __name__ == '__main__':
	print('Opening Bokeh application on http://localhost:5006/')
	server.io_loop.add_callback(server.show, '/')
	server.io_loop.start()