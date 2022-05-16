
from domain import SimFile, Space
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph import functions as fn
from pyqtgraph.Qt import QtCore


class App:
	def __init__(self, space):
		self.space:Space = space
		self.app = pg.mkQApp("GLScatterPlotItem Example")

		self.w = gl.GLViewWidget()
		self.g = gl.GLGridItem()
		self.sp = gl.GLScatterPlotItem(pxMode=False)

	
	def setup(self):
		self.w.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
		self.w.setCameraPosition(distance=20)
		self.sp.translate(5,5,0)

		self.w.addItem(self.g)
		self.w.addItem(self.sp)

	def show(self):
			self.w.show()
			self.t = QtCore.QTimer()
			self.t.timeout.connect(self.update)
			self.t.start(50)

	def update(self):
		self.space.nextIteration(50/1000)
		pos = []
		size = []
		color= []
		for p in self.space.particles:
			pos.append(p.loc.array())
			size.append(p.r)
			color.append(p.color)

		self.sp.setData(pos=pos, size=size, color=np.array(color))
			

if __name__ == '__main__':
	simFile = SimFile('inputs/intermediate_04.txt')
	space = simFile.import_space()
	app = App(space)
	app.setup()
	app.show()
	pg.exec()