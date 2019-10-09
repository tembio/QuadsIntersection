import math

def getColumnInMatrix(matrix, i):
    return [row[i] for row in matrix]

def  vectorFromPoints(p0, p1):
	return [p1[0]-p0[0], p1[1]-p0[1], p1[2]-p0[2]]

def dotProduct(v0, v1):
	return v0[0]*v1[0] + v0[1]*v1[1] + v0[2]*v1[2] 

def norm(v):
	return math.sqrt(v[0]*v[0]+v[1]*v[1]+v[2]*v[2])

def scalarProduct(v, s):
	return [v[0]*s, v[1]*s, v[2]*s]

def substract(v0, v1):
	return [v0[0]-v1[0], v0[1]-v1[1], v0[2]-v1[2]]

def divideByScalar(v, s):
	return [v[0]/s, v[1]/s, v[2]/s]

def crossProduct(u, v):  
    dim = len(u)
    s = []
    for i in range(dim):
        if i == 0:
            j,k = 1,2
            s.append(u[j]*v[k] - u[k]*v[j])
        elif i == 1:
            j,k = 2,0
            s.append(u[j]*v[k] - u[k]*v[j])
        else:
            j,k = 0,1
            s.append(u[j]*v[k] - u[k]*v[j])
    return s
