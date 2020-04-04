import turtle
import math
import random
import matplotlib.pyplot as plt

wn = turtle.Screen()
wn.title("Coronavirus Simulator")
wn.bgcolor("White")
wn.tracer(0)

start = False
socialDistancing = False
def space():
	global start
	start = not(start)

def s():
	global socialDistancing
	socialDistancing = True

wn.onkey(s, "s")
wn.onkey(space, "space")


leon = turtle.Turtle()
leon.speed(0)
leon.shape("square")
leon.color("black")
leon.penup()
leon.hideturtle()
leon.goto(250, 0)
leon.write("Press Space to Begin the Simulation",align = "left",font=("Courier", 12, "normal"))

madeline = turtle.Turtle()
madeline.speed(0)
madeline.shape("square")
madeline.color("black")
madeline.penup()
madeline.hideturtle()
madeline.goto(-250,0)
madeline.write("Press s to initiate social distancing!", align="right", font=("Courier", 12, "normal"))

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 300)

canvas_width = 300
canvas_height = 300

data = []
balls = []
colors = []
timeInfected = []
ball_radius = 10
infected = 1

for i in range(100):
	balls.append(turtle.Turtle())
	colors.append("green")
	timeInfected.append(0)

for ball in balls:
	ball.shape("circle")
	ball.color("green")
	ball.penup()
	#ball.shapesize(radius,radius,0)
	ball.speed(0)
	x = random.randint(-200, 200)
	y = random.randint(-200,200)
	ball.goto(x,y)
	if socialDistancing:
		if balls.index(ball) % 2 == 0:
			ball.dy = 0
			ball.dx = 0
		else:
			ball.dy = 8*random.random() - 4
			ball.dx = 8*random.random() - 4
	else:
		ball.dy = 8*random.random() - 4
		ball.dx = 8*random.random() - 4


time = 0

balls[0].color("red")
colors[0] = "red"
timeInfected[0] = 1

recovered = 0

def moveObjects():
	for ball in balls:
		ball.sety(ball.ycor() + ball.dy)
		ball.setx(ball.xcor() + ball.dx)

def ballCollision():
	global infected
	global recovered
	for i in range(len(balls)-1):
		ball = balls[i]
		if not(timeInfected[balls.index(ball)] == 0) and time == timeInfected[balls.index(ball)] + 300:
			ball.color("grey")
			colors[balls.index(ball)] = "grey"
			infected -= 1
			recovered += 1
			

		for index in range(i+1,len(balls),1):
			ball1 = balls[index]
			d = math.sqrt(math.pow(ball.xcor()-ball1.xcor(),2) + math.pow(ball.ycor()-ball1.ycor(),2))
			if d <= 2 * ball_radius:

				

				theta1 = math.atan2(ball.dy , ball.dx)
				theta2 = math.atan2(ball1.dy , ball1.dx)
				phi = math.atan2( (ball1.ycor() - ball.ycor()),  (ball1.xcor() - ball.xcor()) )
				v1 = math.sqrt(ball.dx * ball.dx + ball.dy * ball.dy)
				v2 = math.sqrt(ball1.dx * ball1.dx + ball1.dy * ball1.dy)

				dx1F = (2*v2*math.cos(theta2 - phi)) / 2 * math.cos(phi)+ v1*math.sin(theta1-phi) * math.cos(phi + math.pi / 2)
				dy1F = (2*v2*math.cos(theta2 - phi))/ 2 * math.sin(phi)+ v1*math.sin(theta1-phi) * math.sin(phi + math.pi / 2)
				dx2F = (2*v1*math.cos(theta1 - phi)) / 2 * math.cos(phi) + v2*math.sin(theta2-phi) * math.cos(phi+math.pi/2)
				dy2F = (2*v1*math.cos(theta1 - phi)) / 2 * math.sin(phi) + v2*math.sin(theta2-phi) * math.sin(phi+math.pi/2)

				

				if socialDistancing and balls.index(ball) % 2 == 0:
					ball.dx = 0
					ball.dy = 0
					ball1.dx *= -1
					ball1.dy *= -1
				elif socialDistancing and balls.index(ball1) % 2 == 0:
					ball1.dx = 0
					ball1.dy = 0
					ball.dx *= -1
					ball.dy *= -1
				else:
					ball.dx = dx1F
					ball.dy = dy1F
					ball1.dx = dx2F
					ball1.dy = dy2F
				

				if random.randint(1,2) == 2 and colors[balls.index(ball)] == "red" and colors[balls.index(ball1)] == "green":
					#ball1 is getting infected
					timeInfected[balls.index(ball1)] = time
					infected += 1
					ball1.color("red")
					colors[balls.index(ball1)] = "red"
					pen.clear()
				if random.randint(1,2) == 2 and colors[balls.index(ball)] == "green" and colors[balls.index(ball1)] == "red":
					#ball is getting infected
					timeInfected[balls.index(ball)] = time
					infected += 1
					ball.color("red")
					colors[balls.index(ball)] = "red"
					pen.clear()
				
				
				staticCollision(ball, ball1, False)

		wallCollision(balls[i])
	wallCollision(balls[len(balls)-1])

def wallCollision(ball):
	if(ball.xcor() - ball_radius + ball.dx < -canvas_width or \
		ball.xcor() + ball_radius + ball.dx > canvas_width ):
		ball.dx *= -1

	if(ball.ycor() - ball_radius + ball.dy < -canvas_height or \
		ball.ycor() + ball_radius + ball.dy > canvas_height ):
		ball.dy *= -1

	if(ball.ycor() + ball_radius > canvas_height):
		ball.sety(canvas_height - ball_radius)

	if(ball.ycor() - ball_radius < -canvas_height):
		ball.sety(-canvas_height + ball_radius)

	if(ball.xcor() + ball_radius > canvas_width):
		ball.setx(canvas_width - ball_radius)

	if(ball.xcor() - ball_radius < -canvas_width):
		ball.setx(-canvas_width + ball_radius)

def staticCollision(ball, ball1, emergency = False):
	distance = math.sqrt(math.pow(ball.xcor()-ball1.xcor(),2) + math.pow(ball.ycor()-ball1.ycor(),2))
	overlap = ball_radius * 2 - distance

	theta = math.atan2(ball.ycor() - ball1.ycor(), (ball.xcor() - ball1.xcor()))

	if (emergency):
		(ball, ball1) = (ball1, ball)

	ball.setx(ball.xcor() - overlap * math.cos(theta))
	ball.sety(ball.ycor() - overlap * math.sin(theta))

	if distance < 2 * ball_radius:
		if not emergency:
			staticCollision(ball, ball1, True)

time = 0
data1=[]
recoveredArr = []

while time <= 1000:
	wn.update()
	turtle.listen()

	if(start):
		moveObjects()
		ballCollision()
		pen.clear()
		pen.write("Infected: " + str(infected) + "       " + "Susceptible: " + str(100-infected-recovered), align="center", font=("Courier", 14, "normal"))

		time += 1
		if(time % 10 == 0):
			data.append(infected)
			data1.append(100- infected + recovered)
			recoveredArr.append(recovered)


plt.plot(data, color = "red")
plt.xlabel("time")
plt.ylabel("number of people")
plt.axis([0, 100, 0, 100])
plt.show()
turtle.done()
