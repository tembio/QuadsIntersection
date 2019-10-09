import math
from vectorUtils import *

#https://www.youtube.com/watch?v=ELQG5OvmAE8
def lineSegmentIntersection(l0, l1, s0, s1):
	r = vectorFromPoints(l0,l1)
	s = vectorFromPoints(s0,s1)
	q = vectorFromPoints(s0,l0)

	dotqr = dotProduct(q,r)
	dotqs = dotProduct(q,s)
	dotrs = dotProduct(r,s)
	dotrr = dotProduct(r,r)
	dotss = dotProduct(s,s)

	denom = dotrr*dotss - dotrs*dotrs
	numer  = dotqs*dotrs - dotqr*dotss

	if denom == 0:
		return False

	t = (numer*1.0) / (denom*1.0) # param for line
	u = (dotqs + t*dotrs) / dotss # param for segment

	p0 = [l0[0] + t*r[0], l0[1] + t*r[1], l0[2] + t*r[2]] 
	p1 = [s0[0] + u*s[0], s0[1] + u*s[1], s0[2] + u*s[2]] 


	if u>=0.0 and u<=1.0 and norm(vectorFromPoints(p0,p1))<0.0001:
		return p0
	else:
		return False


# http://geomalgorithms.com/a05-_intersect-1.html
def planePlaneIntersection(n0, p0, n1, p1):
	u = crossProduct(n0, n1);

	ax = u[0] if u[0] >= 0 else -u[0]
	ay = u[1] if u[1] >= 0 else -u[1]
	az = u[2] if u[2] >= 0 else -u[2]

    # Test if the two planes are parallel
	if ax+ay+az < 0.0001:
		v = vectorFromPoints(p0, p1)
		if dotProduct(p1, v) == 0:      #p1 lies in Plane 0
			return 1                    #Planes coincide
		else:
			return 0                    #Planes are parallel


	# 3 plane intersection method to find point in line
	d0 = -dotProduct(n0, p0)
	d1 = -dotProduct(n1, p1)
	aux = substract(scalarProduct(n0,d1), scalarProduct(n1,d0))
	intersectPoint = divideByScalar(crossProduct(aux, u), (norm(u)*norm(u)));


	return [intersectPoint, [u[0]+intersectPoint[0], u[1]+intersectPoint[1], u[2]+intersectPoint[2]] ]


def PointBetweenPointsInLine(p, s0, s1):
	tx=0
	ty=0
	tz=0

	if vectorFromPoints(s0,s1)[0] != 0:
		tx = (p[0] - s0[0]) / vectorFromPoints(s0,s1)[0]
	if vectorFromPoints(s0,s1)[1] != 0:
		ty = (p[1] - s0[1]) / vectorFromPoints(s0,s1)[1]
	if vectorFromPoints(s0,s1)[2] != 0:
		tz = (p[2] - s0[2]) / vectorFromPoints(s0,s1)[2]

	return  tx>=0 and tx<=1 and ty>=0 and ty<=1 and tz>=0 and tz<=1; 


# quads defined in contiguous positions
def quadsIntersection(h0, h1, h2, h3, f0, f1, f2, f3):
	quad1Sides = []
	quad1Sides.append([h0, h1])
	quad1Sides.append([h1, h2])
	quad1Sides.append([h2, h3])
	quad1Sides.append([h3, h0])

	quad2Sides = []
	quad2Sides.append([f0, f1])
	quad2Sides.append([f1, f2])
	quad2Sides.append([f2, f3])
	quad2Sides.append([f3, f0])

	quad1PlaneNormal = crossProduct(substract(h1, h0), substract(h3, h0))
	quad1PlanePoint = h0

	quad2PlaneNormal = crossProduct(substract(f1, f0), substract(f3, f0))
	quad2Point = f0

	intersectionLine = planePlaneIntersection(quad1PlaneNormal, quad1PlanePoint, quad2PlaneNormal, quad2Point)

	if intersectionLine == 0:
		print("Parallel: No intersection")
		return []

	if intersectionLine == 1:
		print("Quads aligned")
		return []

	quad1Intersections = []
	for side in quad1Sides:
		intersectionPoint = lineSegmentIntersection(intersectionLine[0], intersectionLine[1], side[0], side[1])
		if intersectionPoint != False:
			quad1Intersections.append(intersectionPoint)

	quad2Intersections = []
	for side in quad2Sides:
		intersectionPoint = lineSegmentIntersection(intersectionLine[0], intersectionLine[1], side[0], side[1])
		if intersectionPoint != False:
			quad2Intersections.append(intersectionPoint)

	if len(quad1Intersections)<2 or len(quad2Intersections)<2:
		return []

	quad1Point1InBetween = PointBetweenPointsInLine(quad1Intersections[0], quad2Intersections[0], quad2Intersections[1])
	quad1Point2InBetween = PointBetweenPointsInLine(quad1Intersections[1], quad2Intersections[0], quad2Intersections[1])
	quad2Point1InBetween = PointBetweenPointsInLine(quad2Intersections[0], quad1Intersections[0], quad1Intersections[1])
	quad2Point2InBetween = PointBetweenPointsInLine(quad2Intersections[1], quad1Intersections[0], quad1Intersections[1])

	#Quad1 larger than Quad2
	if not quad1Point1InBetween and not quad1Point2InBetween and quad2Point1InBetween and quad2Point2InBetween: 
		return quad2Intersections

	#Quad2 larger than Quad1	
	if quad1Point1InBetween and quad1Point2InBetween:
		return quad1Intersections

	#Partial collision
	solution = []

	if quad1Point1InBetween:
		solution.append(quad1Intersections[0])
		if quad2Point1InBetween:
			solution.append(quad2Intersections[0])
		else:
			solution.append(quad2Intersections[1])

	if quad1Point2InBetween:
		solution.append(quad1Intersections[1])
		if quad2Point1InBetween:
			solution.append(quad2Intersections[0])
		else:
			solution.append(quad2Intersections[1])

	return solution
