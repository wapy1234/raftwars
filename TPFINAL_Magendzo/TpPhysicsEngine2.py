#This is supposed to be the physics engine of version 3
import random
import math
import time
from PIL import ImageTk,Image

# dot product got from https://stackoverflow.com/questions/32669855/dot-product-of-two-lists-in-python
# quadratic got from https://stackoverflow.com/questions/15398427/solving-quadratic-equation
''' Followed physics tutorial from 
https://gamedevelopment.tutsplus.com/tutorials/how-to-create-a-custom-2d-physics-engine-the-basics-and-impulse-resolution--gamedev-6331
https://yal.cc/rectangle-circle-intersection-test/
https://learnopengl.com/In-Practice/2D-Game/Collisions/Collision-Detection
'''
def quadratic(a,b,c):
	d = b**2-4*a*c # discriminant
	if d < 0:
		print('a')
		return
	elif d == 0:
		print('b')
		x = (-b+math.sqrt(b**2-4*a*c))/2*a
		return x
	else:
		print('c')
		x1 = (-b+math.sqrt((b**2)-(4*(a*c))))/(2*a)
		x2 = (-b-math.sqrt((b**2)-(4*(a*c))))/(2*a)
		return(x1, x2)

def dotProduct(v1, v2):
    if len(v1) != len(v2):
      return 0
    return sum(i[0] * i[1] for i in zip(v1, v2))

def pythagoreanSolver(a,b):
	c = a**2 +b**2
	c = math.sqrt(c)
	return c

def worldToScreen(wX, wY, offset = 0):
	sW = 800
	sH = 800
	wW = 20
	wH = 20
	sX = ((wX + wW/2)/wW)*sW - offset
	sY = ((-wY + wH/2)/wH)*sH
	return (sX, sY)

def screenToWrold(sX, sY):
	sW = 800
	sH = 800
	wW = 20
	wH = 20
	wX = ((sX/sW)*wW)-(wW/2)
	wY = ((sY/sH)*-wH)+(wH/2)
	return (wX, wY)


class Physics(object):
	def __init__(self):
		self.gravity = 9.81
		self.norm = ()
		self.penetration = 0

	def collisionResolution(self, objectA, objectB):
		relativeVelocity = (objectB.velocity[0] - objectA.velocity[0], objectB.velocity[1] - objectA.velocity[1])
		velocityNorm = dotProduct(relativeVelocity, self.norm)
		if(velocityNorm > 0):
			return
		e = min(objectA.restitution, objectB.restitution)
		j = -(1 + e) * velocityNorm
		j /= objectA.invMass + objectB.invMass
		impulse = (j*self.norm[0], j*self.norm[1])
		#print(impulse)
		objAVelocityX = objectA.velocity[0] - objectA.invMass*impulse[0]
		objAVelocityY = objectA.velocity[1] - objectA.invMass*impulse[1]
		objBVelocityX = objectB.velocity[0] + objectB.invMass*impulse[0]
		objBVelocityY = objectB.velocity[1] + objectB.invMass*impulse[1]
		#print(objectA.velocity)
		objectA.velocity = (objAVelocityX, objAVelocityY)
		#print(objectA.velocity)
		objectB.velocity = (objBVelocityX, objBVelocityY)
		#Calculate Friction
		tangent = (relativeVelocity[0] - dotProduct(relativeVelocity, self.norm)*self.norm[0], relativeVelocity[1] - dotProduct(relativeVelocity, self.norm)*self.norm[1])
		tnorm = (math.sqrt(tangent[0]**2 + tangent[1]**2))
		if(tnorm != 0):
			t = (tangent[0]/tnorm, tangent[1]/tnorm)
			jt = -dotProduct(relativeVelocity, t)
			jt = jt/(objectA.invMass + objectB.invMass)
			mu = pythagoreanSolver(objectA.sf, objectB.sf)
			if(abs(jt) < j*mu):
				frictionImpulse = (jt * t[0], jt * t[1])
			else:
				df = pythagoreanSolver(objectA.df, objectB.df)
				frictionImpulse = (-j * t[0] * df, -j * t[1] * df)
			objAVelocityX = objectA.velocity[0] - objectA.invMass*frictionImpulse[0]
			objAVelocityY = objectA.velocity[1] - objectA.invMass*frictionImpulse[1]
			objBVelocityX = objectB.velocity[0] + objectB.invMass*frictionImpulse[0]
			objBVelocityY = objectB.velocity[1] + objectB.invMass*frictionImpulse[1]
			objectA.velocity = (objAVelocityX, objAVelocityY)
			objectB.velocity = (objBVelocityX, objBVelocityY)

	def poisitonCorrection(self, objectA, objectB):
		percent = 0.2
		leeway = 0.06
		correction = max(self.penetrationDepth - leeway, 0) /(objectA.invMass + objectB.invMass) * percent
		objectA.position = (objectA.position[0], objectA.position[1] + (objectA.invMass * correction))
		objectB.position = (objectB.position[0] + (objectB.invMass * correction), objectB.position[1] + (objectB.invMass * correction))

	def circleVsCircleCollision(self, objectA, objectB):
		vector = (objectB.position[0] - objectA.position[0], objectB.position[1] - objectA.position[1])
		r = objectB.radius + objectA.radius
		rad = r**2
		if(vector[0]**2 + vector[1]**2 > rad):
			return False
		distance = math.sqrt(vector[0]**2 + vector[1]**2)
		if(distance != 0):
			self.penetration = rad - distance
			self.norm = [vector[0]/distance, vector[1]/distance]
			return True 
		else:
			self.penetration = objectA.radius
			self.norm = [1,0]
			return True

	def nonCircleVsNonCircle(self, objectA, objectB):
		vector = (objectB.position[0] - objectA.position[0], objectB.position[1] - objectA.position[1])
		objectAExtentX = (objectA.maxX - objectA.minX)/2
		objectBExtentX = (objectB.maxX - objectB.minX)/2
		xOverlap = objectAExtentX + objectBExtentX - abs(vector[0])
		if(xOverlap > 0):
				objectAExtentY = (objectA.maxY - objectA.minY)/2
				objectBExtentY = (objectB.maxY - objectB.minY)/2
				yOverlap = objectAExtentY + objectBExtentY - abs(vector[1])
				if(yOverlap > 0):
					if(xOverlap > yOverlap):
						if(vector[0] < 0):
							self.norm = (-1, 0)
						else:
							self.norm = (1, 0)
						self.penetrationDepth = xOverlap
						return True
					else:
						if(vector[1] < 0):
							self.norm = (0, -1)
						else:
							self.norm = (0, 1)
						self.penetrationDepth = yOverlap
						return True
		return False

	def circleVsNonCircle(self, objectA, objectB):
		#DON"T FUCK WITH THIS!!!!
		extentX = (objectA.maxX - objectA.minX)/2
		extentY = (objectA.maxY - objectA.minY)/2
		closestPointX = max(objectA.position[0] - extentX, min(objectB.position[0], objectA.position[0] + extentX))
		closestPointY = max(objectA.position[1] + extentY, min(objectB.position[1], objectA.position[1] - extentY))
		vector = (objectB.position[0] - closestPointX, objectB.position[1] - closestPointY)
		closestPoint = [closestPointX, closestPointY]
		inside = False
		distance = (vector[0])**2 + (vector[1])**2 
		if(distance > objectB.radius**2 and inside == False):
			# if(isinstance(objectB, Person)):
			# 	print("not")
			# 	objectB.force = (0, -.000005981*objectB.mass)
			return False
		d = math.sqrt(distance)
		if(inside):
			self.normal = [-vector[0], vector[1]]
			self.penetration = objectB.radius - d
		else:
			maxi = 0
			best = (0,0)
			posDirection = [(0,1), (1,0), (0,-1), (-1,0)]
			for direction in posDirection:
				dot = dotProduct(direction, vector)
				if(dot > maxi):
					maxi = dot
					best = direction 
			self.norm = (-best[0], -best[1])
			self.penetrationDepth = objectB.radius - distance
		# if(isinstance(objectB, Person)):
		# 	print("tot")
		# 	objectB.force = (0, 0)
		return True


	def movement(self, objectA, dt):
		objectA.velocity = (objectA.velocity[0] + (objectA.invMass*objectA.force[0])*dt, objectA.velocity[1] + (objectA.invMass*objectA.force[1])*dt)
		velocity = objectA.velocity
		objectA.position = (objectA.position[0] + velocity[0]*dt, objectA.position[1] + velocity[1]*dt)

class Body(object):
	def __init__(self, shape, volume, material, position):
		self.shape = shape
		self.position = position
		self.rotation = 0
		self.transformation = (self.position, self.rotation)
		self.density = material[0]
		self.restitution = material[1]
		self.volume = volume
		self.mass = self.density*self.volume
		if(self.mass == 0):
			self.invMass = 0
		else:
			self.invMass = 1/self.mass
		self.force = (0,0)

	def sumForces(forces):
		for force in forces:
			forceX = force[0] + self.force[0]
			forceY = force[1] + self.force[1]
			self.force = (forceX, forceY)

class Person(Body):
	def __init__(self, volume, material, position):
		self.position = position #World
		self.rotation = 0
		self.transformation = (self.position, self.rotation)
		self.density = material[0]
		self.restitution = material[1]
		self.volume = volume
		self.mass = self.density*self.volume
		if(self.mass == 0):
			self.invMass = 0
		else:
			self.invMass = 1/self.mass
		self.force = (0,0)
		self.dradius = 35
		self.radius = self.dradius*(20/800)
		self.velocity = (0,0)
		self.df = 0.75
		self.sf = 0.9
		self.health = 10

	def drawPerson(self, canvas, data, img):
		center = worldToScreen(self.position[0], self.position[1])
		canvas.create_text(center[0] - data.cameraX, center[1] - 75, text= "Health:" + str(self.health), anchor="center", fill = "red" )
		#canvas.create_oval(center[0] - self.dradius - data.cameraX, center[1] - self.dradius, center[0] + self.dradius - data.cameraX, center[1] + self.dradius, fill = "yellow")
		canvas.create_image(center[0] - data.cameraX, center[1] + 2, anchor="center", image = img)

	def inTurn(self, inPosition):
		position = screenToWrold(inPosition[0], inPosition[1])
		return Gun(position, self.position)

	def hit(self):
		damage = random.randint(20,60)//10
		self.health -= damage

	def originalPosReturn(self, originalPos):
		if(self.health > 0):
			self.position = (originalPos)

	def resetVelocity(self):
		self.velocity = (0,0)

	def isOffScreen(self):
		position = worldToScreen(self.position[0], self.position[1])
		return (position[1] + self.dradius >= 800)

class Enemy(Person):

	def inTurn(self, data):
		v = 12
		g = 9.81
		x = self.position[0] + 3.84
		h = self.position[0] + 7.18
		alpha = (g*x**2)/(2*v**2)
		phi = math.atan(x/h)
		num = (alpha - h)/(math.sqrt(h**2 + x**2))
		n = math.acos(num)
		perfAngle = (phi + n)/2
		if(data.level < 3):
			angle = random.uniform((perfAngle - (math.pi/3)), (perfAngle + (math.pi/3)))
		elif(data.level <6):
			angle = random.uniform(perfAngle - (math.pi/4), perfAngle + (math.pi/4))
		else:
			angle = random.uniform(perfAngle - (math.pi/6), perfAngle + (math.pi/6))
		position = (v*math.cos(angle), v*math.sin(angle))
		return EnemyGun(position, self.position)


class Gun(object):
	def __init__(self, position, center):
		#position = mousePosition
		self.positionX = position[0] #World
		self.positionY = position[1] #World
		self.cx = center[0] #World
		self.cy = center[1] - 0.25 #World
		self.lengthAim = min(350*20/800, math.sqrt((self.positionY - self.cy)**2 +(self.positionX - self.cx)**2)) #World
		self.length = 100*20/800
		if(self.positionX == self.cx):
			self.angle = math.pi/2
		else:
			self.angle = math.atan((self.positionY - self.cy)/(self.positionX - self.cx)) #World
		self.gunPosX = self.cx + self.length*math.cos(self.angle) #World
		self.gunPosY = self.cy + self.length*math.sin(self.angle) #World
		self.aimPosX = self.cx + self.lengthAim*math.cos(self.angle) #World
		self.aimPosY = self.cy + self.lengthAim*math.sin(self.angle) #world
		self.power = min(0.12,((math.sqrt((self.positionY - self.cy)**2 +(self.positionX - self.cx)**2))-3.115*10**-15)/60)

	def drawGun(self, canvas, data):
		center = worldToScreen(self.cx, self.cy) #Screen
		gunPos = worldToScreen(self.gunPosX, self.gunPosY) #Screen
		aimPos = worldToScreen(self.aimPosX, self.aimPosY) #Screen
		#angle = math.degrees(self.angle)
		canvas.create_line(center[0] + data.cameraX, center[1], aimPos[0] + data.cameraX, aimPos[1], fill = "red", width = 5, dash = (1,1))
		canvas.create_line(center[0] + data.cameraX, center[1], gunPos[0] + data.cameraX, gunPos[1], fill = "chocolate1", width = 10)
		#canvas.create_image(center[0] + data.cameraX, center[1] + data.cameraX, anchor="center", image = img)

	def rotate(self, newPositionX, newPositionY):
		self.positionX = newPositionX
		self.positionY = newPositionY
		self.angle = math.atan((self.cy - self.positionY)/(self.positionX - self.cx))
		self.gunPosX = self.cx + self.length*math.cos(self.angle)
		self.gunPosY = self.cy - self.length*math.sin(self.angle)

	def shoot(self):
		velocity = (self.power*math.cos(self.angle), self.power*math.sin(self.angle))
		return Bullet("circle", math.pi*100, (0.3,0.8), (self.gunPosX, self.gunPosY), self.angle, velocity)

class EnemyGun(Gun):
	def shoot(self, data):
		if(data.level < 3):
			angle = random.uniform(3*math.pi/4 - math.pi/4, 3*math.pi/4 + math.pi/4)
		elif(data.level <6):
			angle = random.uniform(3*math.pi/4 - (math.pi/5), 3*math.pi/4 + (math.pi/5))
		else:
			angle = random.uniform(3*math.pi/4 - (math.pi/6), 3*math.pi/4 + (math.pi/6))
		power = random.uniform(0.08, 0.12)
		velocity = (power*math.cos(angle), power*math.sin(angle))
		gunPosX = self.cx - self.length*math.cos(angle) #World
		gunPosY = self.cy - self.length*math.sin(angle)
		return Bullet("circle", math.pi*100, (0.3,0.8), (gunPosX, gunPosY), angle, velocity)


class Bullet(Body):
	def __init__(self, shape, volume, material, position, angle, velocity):
		self.shape = shape
		self.position = position #World
		self.rotation = 0
		self.transformation = (self.position, self.rotation)
		self.density = material[0]
		self.restitution = material[1]
		self.volume = volume
		self.mass = self.density*self.volume
		if(self.mass == 0):
			self.invMass = 0
		else:
			self.invMass = 1/self.mass
		self.force = (0,-.00015981*self.mass)
		self.dradius = 15 #Screen
		self.radius = self.dradius*(20/800) #World
		self.angle = angle
		self.velocity = velocity
		self.sf = 0.9
		self.df = 0.6

	def isOffScreen(self):
		position = worldToScreen(self.position[0], self.position[1])
		return (position[1] + self.dradius >= 800)

	def drawBullet(self, canvas, data):
		position = worldToScreen(self.position[0], self.position[1], data.cameraX)
		canvas.create_oval(position[0] - self.dradius, position[1] - self.dradius,\
	position[0] + self.dradius, position[1] + self.dradius, fill = "yellow")

class Raft(Body):
	def __init__(self, volume, material, position, mini, maxi):
		self.position = position #World
		self.rotation = 0
		self.transformation = (self.position, self.rotation)
		self.density = material[0]
		self.restitution = material[1]
		self.volume = volume
		self.mass = self.density*self.volume
		if(self.mass == 0):
			self.invMass = 0
		else:
			self.invMass = 1/self.mass
		self.force = (0,0)
		self.radius = 50
		self.minX = mini[0] #World
		self.minY = mini[1] #World
		self.maxX = maxi[0] #World
		self.maxY = maxi[1] #World
		self.velocity = (0,0)
		self.df = 0.05
		self.sf = 0.2

	def drawRaft(self, canvas, data):
		mini = worldToScreen(self.minX, self.minY)
		maxi = worldToScreen(self.maxX, self.maxY)
		center = worldToScreen(self.position[0], self.position[1])
		canvas.create_rectangle(mini[0] - data.cameraX, mini[1], maxi[0] - data.cameraX, maxi[1], fill = "brown")
	



