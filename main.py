import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from vectorUtils import getColumnInMatrix
from intersection import *

xOffset = 0
yOffset = 0
zOffset = 0
axes = plt.axes(projection='3d')

def configAxes():
	global axes
	axes.set_yticklabels([])
	axes.set_xticklabels([])
	axes.set_zticklabels([])
	plt.xlim(-5, 15)
	plt.ylim(-15, 15)

def draw(geometry):
	[quad1, quad2, intersection] = geometry

	axes.clear()
	configAxes()

	axes.plot3D(getColumnInMatrix(quad1,0), getColumnInMatrix(quad1,1), getColumnInMatrix(quad1,2), 'red')
	axes.plot3D(getColumnInMatrix(quad2,0), getColumnInMatrix(quad2,1), getColumnInMatrix(quad2,2), 'green')
	if intersection != []:
		plotIntersection = axes.plot3D(getColumnInMatrix(intersection,0), getColumnInMatrix(intersection,1), getColumnInMatrix(intersection,2), 'blue')

	axes.figure.canvas.draw()
	
def calculateGeometry(xOffset, yOffset, zOffset):
	#Green quad
	quad1 = [
		[-5, 4, 15],
		[-5, 4, -15],
		[15, 0, -15],
		[15, 0, 15],
		[-5, 4, 15]]

	#Red quad
	quad2 = [
			[-5+xOffset,  5+yOffset, 0+zOffset],
			[ 5+xOffset,  5+yOffset, 0+zOffset],
			[ 5+xOffset, -5+yOffset, 0+zOffset],
			[-5+xOffset, -5+yOffset, 0+zOffset],
			[-5+xOffset,  5+yOffset, 0+zOffset]]

	#Blue line
	intersection = quadsIntersection(quad1[0],quad1[1],quad1[2],quad1[3],quad2[0],quad2[1],quad2[2],quad2[3])

	return [quad1, quad2, intersection]

def processInput(event):
	global xOffset, yOffset,zOffset
	if event.key=="right":
		xOffset += 1
	if event.key=="left":
		xOffset -= 1
	if event.key=="up":
		yOffset += 1
	if event.key=="down":
		yOffset -= 1
	if event.key=="z":
		zOffset += 1
	if event.key=="x":
		zOffset -= 1

def on_press(event):
	processInput(event)
	geometry = calculateGeometry(xOffset, yOffset, zOffset)
	draw(geometry)


axes.figure.canvas.mpl_connect('key_press_event', on_press)
configAxes()
geometry = calculateGeometry(xOffset, yOffset, zOffset)
draw(geometry)

plt.show()
