import turtle
import random
import time

win = turtle.Screen()
win.title("Space Invaders - CiccioBro")
win.bgcolor("black")
win.setup(width=600, height=600)
win.tracer(0)

score = 0
powerups = []

def generate_powerup():
    powerup = turtle.Turtle()
    powerup.shape("square")
    powerup.color("blue")
    powerup.penup()
    powerup.speed(0)
    x = random.randint(-290, 290)
    y = random.randint(100, 250)
    powerup.goto(x, y)
    return powerup

def move_powerup(powerup):
    y = powerup.ycor()
    y -= invader_speed + 10
    powerup.sety(y)

def move_alien_ship(alien_ship):
    x = alien_ship.xcor()
    x += alien_ship.direction * 5
    alien_ship.setx(x)

    # Change direction and move down when touching screen edges
    if x > 290 or x < -290:
        alien_ship.direction *= -1
        y = alien_ship.ycor()
        y -= 40
        alien_ship.sety(y)

def update_score():
    score_display.clear()
    score_display.write("SCORE : {}".format(score), align="left", font=("Courier", 12, "normal"))

def update_health_bar(health_bar, health):
    health_bar.clear()
    health_bar.write("HEALTH : {}".format(health), align="right", font=("Courier", 12, "normal"))

score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(-290, 260)
update_score()

# Health bar of the alien ship
health_bar = turtle.Turtle()
health_bar.speed(0)
health_bar.color("white")
health_bar.penup()
health_bar.hideturtle()
health_bar.goto(280, 260)
alien_health = 100
update_health_bar(health_bar, alien_health)

player = turtle.Turtle()
player.shape("turtle")
player.color("white")
player.penup()
player.speed(0)
player.goto(0, -250)
player.setheading(90)

player_speed = 30
bullet_speed = 3

def move_left():
    x = player.xcor()
    x -= player_speed
    if x < -290:
        x = -290
    player.setx(x)

def move_right():
    x = player.xcor()
    x += player_speed
    if x > 290:
        x = 290
    player.setx(x)

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

win.listen()
win.onkey(move_left, "Left")
win.onkey(move_right, "Right")
win.onkey(fire_bullet, "space")

num_invaders = 7
invaders = []

for _ in range(num_invaders):
    invader = turtle.Turtle()
    invader.shape("circle")
    invader.color("red")
    invader.penup()
    invader.speed(0)
    x = random.randint(-290, 290)
    y = random.randint(100, 250)
    invader.goto(x, y)
    invaders.append(invader)

alien_ship = turtle.Turtle()
alien_ship.shape("square")
alien_ship.color("green")
alien_ship.penup()
alien_ship.speed(0)
alien_ship.goto(0, 200)
alien_ship.direction = 1

invader_speed = 2
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("yellow")
bullet.penup()
bullet.speed(10)
bullet.shapesize(stretch_wid=0.5, stretch_len=0.5)  # Make the alien ship's bullet thinner
bullet.hideturtle()
bullet_state = "ready"

def move_invaders():
    for invader in invaders:
        y = invader.ycor()
        y -= invader_speed
        invader.sety(y)

        if player.distance(invader) < 20:
            player.hideturtle()
            invader.hideturtle()
            print("GAME OVER!!!")
            win.bye()

        if y < -290:
            player.hideturtle()
            invader.hideturtle()
            print("GAME OVER!!!")
            win.bye()
    
    move_alien_ship(alien_ship)

    for powerup in powerups:
        move_powerup(powerup)

    win.update()
    win.ontimer(move_invaders, 100)

move_invaders()

start_time = time.time()
while True:
    if random.randint(1, 10000) == 1:
        powerup = generate_powerup()
        powerups.append(powerup)

    for powerup in powerups:
        if player.distance(powerup) < 20:
            powerup.hideturtle()
            powerups.remove(powerup)
            player_speed = 60
            invader_speed = 1

    if bullet_state == "fire":
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)

        for invader in invaders:
            if bullet.distance(invader) < 15:
                bullet.hideturtle()
                bullet_state = "ready"
                invader.hideturtle()
                score += 10
                update_score()

        if y > 290:
            bullet.hideturtle()
            bullet_state = "ready"

    if time.time() - start_time > 1000000:
        if alien_ship.isvisible():
            move_alien_ship(alien_ship)

    # Check if player's bullet hits the alien ship
    if bullet_state == "fire" and bullet.distance(alien_ship) < 15:
        bullet.hideturtle()
        bullet_state = "ready"
        alien_health -= 10
        update_health_bar(health_bar, alien_health)

        if alien_health <= 0:
            alien_ship.hideturtle()
            print("YOU WIN!!!")
            win.bye()

    win.update()
