
#This is version 3's run function
#All images are inspired from the original game Raft Wars
import math
import time
from TpPhysicsEngine2 import *
from tkinter import *
from PIL import ImageTk,Image  

def moveCameraInitial(data, objectA):
	if(objectA.position[0] >= 10):
		data.cameraX = data.width
	if(objectA.position[0] >= 30):
		data.cameraX += data.width
	if(objectA.position[0] >= 50):
		data.cameraX += data.width

def moveCameraFinal(data, objectA):
	if(objectA.position[0] <= 50):
		data.cameraX = data.width*2
	if(objectA.position[0] <= 30):
		data.cameraX = data.width
	if(objectA.position[0] <= 10):
		data.cameraX = 0

def init(data):
	data.startTime = time.time()
	data.level = 1
	data.menu = True
	data.menuIMG = ImageTk.PhotoImage(Image.open("menu.png"))
	data.semiMenu = False
	data.cameraX = 0
	data.enemyTurn = False
	data.physics = Physics()
	data.inTurn = True 
	data.bullet = None
	data.gun = None 
	data.playColor = "light blue"
	data.background = ImageTk.PhotoImage(Image.open("background.png"))
	data.mainChar = PhotoImage(file = "main_char.gif")
	data.baby = ImageTk.PhotoImage(Image.open("baby.png"))
	data.count = 0
	data.enemyShoot = False
	if(data.level == 1): 
		#Pirates
		data.playerRafts = [Raft(0, (0.3,0.2), (-5.67, -8.425), (-2.64, -7.85), (-8.70, -9))]
		data.enemyRafts = [
					  Raft(0, (0.3,0.2), (55,-8.0625), (52.5, -7.125), (57.5, -9)), 
					  Raft(0, (0.3,0.2), (60.75,-7), (60.5, -6), (61, -8)),
					  Raft(0, (0.3,0.2), (63,-7.5), (61, -6.75), (66, -8)), 
					  Raft(0, (0.3,0.2), (66.25,-5), (65.5, -2), (67, -8))] 
		data.player = Person(2*math.pi*50**2, (0.5,0.5), (-3.64,-7.18))
		data.players = [(data.player, (-3.64,-7.18), data.mainChar), (Person(2*math.pi*50**2, (0.5,0.5), (-6.64,-7.18)), (-6.64,-7.18), data.baby)]
		data.enemies = [[Enemy(2*math.pi*50**2, (0.5,0.5), (55,-6.25)), (55,-6.25)], [Enemy(2*math.pi*50**2, (0.5,0.5), (63,-6)), (63,-6)]]
		data.shootingEnemy = data.enemies[0][0]
		data.playerRaft = ImageTk.PhotoImage(Image.open("playerRaft.png"))
		data.babyRaft = ImageTk.PhotoImage(Image.open("charRaft 2.png"))
		data.enemyChar = ImageTk.PhotoImage(Image.open("pirate.png"))
		data.pirateShip = ImageTk.PhotoImage(Image.open("pirateShip.png"))
		data.pirateBar = ImageTk.PhotoImage(Image.open("pirateBar.png"))
		data.raftImg = [[data.playerRaft, 250, 735], [data.pirateShip, 3000, 575], [data.pirateBar, 2600, 715], [data.babyRaft, 150, 725]]

def initLevel(data):
	if(data.level == 2):
		#Neighbors
		data.playerRafts = [Raft(0, (0.3,0.2), (-5.67, -8.425), (-2.64, -7.85), (-8.70, -9))]
		data.enemyRafts = [Raft(0, (0.3,0.2), (64.5,-8), (55.5, -7.5), (64.5, -8.5))] 
		data.player = Person(2*math.pi*50**2, (0.5,0.5), (-3.64,-7.18))
		data.players = [(data.player, (-3.64,-7.18), data.mainChar), (Person(2*math.pi*50**2, (0.5,0.5), (-6.64,-7.18)), (-6.64,-7.18), data.baby)]
		data.enemies = [[Enemy(2*math.pi*50**2, (0.5,0.5), (58,-6.75)), (58,-6.75)], [Enemy(2*math.pi*50**2, (0.5,0.5), (61.5,-6.75)), (61.5,-6.75)]]
		data.shootingEnemy = data.enemies[0][0]
		data.playerRaft = ImageTk.PhotoImage(Image.open("playerRaft.png"))
		data.babyRaft = ImageTk.PhotoImage(Image.open("charRaft 2.png"))
		data.enemyChar = ImageTk.PhotoImage(Image.open("neighborChar.png"))
		data.neighborRaft = ImageTk.PhotoImage(Image.open("neighborRaft.png"))
		data.raftImg = [[data.playerRaft, 250, 735], [data.neighborRaft, 2800, 750], [data.babyRaft, 150, 725]]
	if(data.level == 3):
		#Police
		data.playerRafts = [Raft(0, (0.3,0.2), (-5.67, -8.425), (-2.64, -7.85), (-8.70, -9))]
		data.enemyRafts = [Raft(0, (0.3,0.2), (64.5,-8), (55.5, -7.5), (64.5, -8.5))] 
		data.player = Person(2*math.pi*50**2, (0.5,0.5), (-3.64,-7.18))
		data.players = [(data.player, (-3.64,-7.18), data.mainChar), (Person(2*math.pi*50**2, (0.5,0.5), (-6.64,-7.18)), (-6.64,-7.18), data.baby)]
		data.enemies = [[Enemy(2*math.pi*50**2, (0.5,0.5), (58,-6.75)), (58,-6.75)], [Enemy(2*math.pi*50**2, (0.5,0.5), (61.5,-6.75)), (61.5,-6.75)]]
		data.shootingEnemy = data.enemies[0][0]
		data.playerRaft = ImageTk.PhotoImage(Image.open("playerRaft.png"))
		data.babyRaft = ImageTk.PhotoImage(Image.open("charRaft 2.png"))
		data.enemyChar = ImageTk.PhotoImage(Image.open("cop.png"))
		data.policeRaft = ImageTk.PhotoImage(Image.open("policeRaft.png"))
		data.raftImg = [[data.playerRaft, 250, 735], [data.policeRaft, 2800, 725], [data.babyRaft, 150, 725]]
	if(data.level == 4):
		#Thug
		data.playerRafts = [Raft(0, (0.3,0.2), (-5.67, -8.425), (-2.64, -7.85), (-8.70, -9))]
		data.enemyRafts = [Raft(0, (0.3,0.2), (64.5,-8), (55.5, -7.5), (64.5, -8.5))] 
		data.player = Person(2*math.pi*50**2, (0.5,0.5), (-3.64,-7.18))
		data.players = [(data.player, (-3.64,-7.18), data.mainChar), (Person(2*math.pi*50**2, (0.5,0.5), (-6.64,-7.18)), (-6.64,-7.18), data.baby)]
		data.enemies = [[Enemy(2*math.pi*50**2, (0.5,0.5), (58,-6.75)), (58,-6.75)], [Enemy(2*math.pi*50**2, (0.5,0.5), (61.5,-6.75)), (61.5,-6.75)]]
		data.shootingEnemy = data.enemies[0][0]
		data.playerRaft = ImageTk.PhotoImage(Image.open("playerRaft.png"))
		data.babyRaft = ImageTk.PhotoImage(Image.open("charRaft 2.png"))
		data.enemyChar = ImageTk.PhotoImage(Image.open("thug.png"))
		data.thugRaft = ImageTk.PhotoImage(Image.open("thugRaft.png"))
		data.raftImg = [[data.playerRaft, 250, 735], [data.thugRaft, 2800, 725], [data.babyRaft, 150, 725]]


def mousePressed(event, data):
	if(data.menu == True):
		if((event.x >= 350 and event.x <= 450) and (event.y >= 375 and event.y <= 425)):
			data.menu = False
	elif(data.semiMenu == True):
		if((event.x >= 500 and event.x <= 700) and (event.y >= 75 and event.y <= 125)):
			data.semiMenu = False
	else:
		if(data.inTurn == True):
			data.bullet = data.gun.shoot()
			data.inTurn = False
   
def mouseMotion(event, data):
	if(data.menu == True):
		if((event.x >= 350 and event.x <= 450) and (event.y >= 375 and event.y <= 425)):
			data.playColor = "yellow"
		else:
			data.playColor = "light blue"
	elif(data.semiMenu == True):
		if((event.x >= 500 and event.x <= 700) and (event.y >= 75 and event.y <= 125)):
			data.playColor = "yellow"
		else:
			data.playColor = "light blue"
	else:
		data.gun = data.player.inTurn((event.x, event.y))
	

def timerFired(data):
	data.count += 1
	if(data.menu == False and data.semiMenu == False):
		#Gameplay
		if(data.inTurn == False):
			if(data.enemyTurn == False):
				data.physics.movement(data.bullet, data.timerDelay)
				moveCameraInitial(data, data.bullet)
				for enemy in data.enemies:
					data.physics.movement(enemy[0], data.timerDelay)
					for raft in data.enemyRafts:
						if(data.physics.circleVsNonCircle(raft, enemy[0])):
							data.physics.collisionResolution(enemy[0], raft)
							data.physics.poisitonCorrection(enemy[0], raft)
						if(data.physics.circleVsCircleCollision(data.bullet, enemy[0])):
							data.physics.collisionResolution(data.bullet, enemy[0])
							enemy[0].hit()
						if(data.physics.circleVsNonCircle(raft, data.bullet)):
							data.physics.collisionResolution(data.bullet, raft)
						if(enemy[0].health <= 0 or enemy[0].isOffScreen()):
							if(enemy in data.enemies):
								data.enemies.remove(enemy)
							if(len(data.enemies) == 0):
								data.level += 1
								initLevel(data)
								data.cameraX = 0
								data.semiMenu = True
								data.inTurn = True
								data.bullet = None
								return
							else:
								data.shootingEnemy = data.enemies[0][0]
				ftime = time.time()
				if(data.bullet.isOffScreen() or (ftime - data.startTime)%25 == 0):
					data.enemyTurn = True
					data.gun = None
					data.bullet = None
					for enemy in data.enemies:
						enemy[0].originalPosReturn(enemy[1])
					data.cameraX = 2400
			elif(data.enemyTurn == True):
				if(data.enemyShoot == False):
					data.gun = data.shootingEnemy.inTurn(data)
					data.bullet = data.gun.shoot(data)
					data.enemyShoot = True
				data.physics.movement(data.bullet, data.timerDelay)
				moveCameraFinal(data, data.bullet)
				if(data.enemyShoot == True):
					for player in data.players:
						data.physics.movement(player[0], data.timerDelay)
						for raft in data.playerRafts:
							if(data.physics.circleVsNonCircle(raft, player[0])):
								data.physics.collisionResolution(player[0], raft)
								data.physics.poisitonCorrection(player[0], raft)
							if(data.physics.circleVsCircleCollision(data.bullet, player[0])):
								data.physics.collisionResolution(data.bullet, player[0])
								player[0].hit()
							if(data.physics.circleVsNonCircle(raft, data.bullet)):
								data.physics.collisionResolution(data.bullet, raft)
							if(player[0].health <= 0 or player[0].isOffScreen()):
								if(player in data.players):
									data.players.remove(player)
								if(len(data.players) == 0 ):
									data.cameraX = 0
									data.semiMenu = True
									data.inTurn = True
									data.bullet = None
									return
								else:
									data.player = data.players[0][0]
				ftime = time.time()
				if(data.bullet.isOffScreen() or (ftime - data.startTime)%25 == 0):
					data.enemyTurn = False
					data.enemyShoot = False
					data.inTurn = True
					for enemy in data.enemies:
						enemy[0].resetVelocity()
					for player in data.players:
						player[0].resetVelocity()
						player[0].originalPosReturn(player[1])
					data.cameraX = 0

def redrawAll(canvas, data):
	if(data.menu == True):
		canvas.create_image(400, 400, anchor = "center", image= data.menuIMG)
		canvas.create_rectangle(350, 375, 450, 425, fill = data.playColor)
		canvas.create_text(400, 400, anchor = "center", text = "PLAY", font = "Arial 24 bold")
	elif(data.semiMenu == True):
		canvas.create_image(1600 - data.cameraX, 325, anchor = "center", image= data.background)
		canvas.create_rectangle(0,715,1500,850, fill = "light blue")
		for player in data.players:
			player[0].drawPerson(canvas, data, player[2])
		for raft in data.raftImg:
			canvas.create_image(raft[1] - data.cameraX, raft[2], anchor = "center", image = raft[0])
		canvas.create_rectangle(500,75,700,125, fill = data.playColor)
		canvas.create_text(600, 100, anchor = "center", text = "NEXT", font = "Arial 24 bold")
	else:
		canvas.create_image(1600 - data.cameraX, 325, anchor = "center", image= data.background)
		# for r in data.enemyRafts:
		# 	r.drawRaft(canvas, data)
		# for l in data.playerRafts:
		# 	l.drawRaft(canvas, data)
		if(data.gun != None):    
			data.gun.drawGun(canvas, data)
		for enemy in data.enemies:
			enemy[0].drawPerson(canvas, data, data.enemyChar)
		if(data.bullet != None):    
			data.bullet.drawBullet(canvas, data)
		canvas.create_rectangle(0,715,1500,850, fill = "light blue")
		for player in data.players:
			player[0].drawPerson(canvas, data, player[2])
		for raft in data.raftImg:
			canvas.create_image(raft[1] - data.cameraX, raft[2], anchor = "center", image = raft[0])

	



###################################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    def mouseMotionWrapper(event, canvas, data):
        if(data.inTurn):
            mouseMotion(event, data)
            redrawAllWrapper(canvas, data)
        else: 
            pass

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 3 #40 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<Motion>", lambda event:
                            mouseMotionWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 800)