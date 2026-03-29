import pygame
import sys
import random
import tkinter as tk

from pygame import display

pygame.init()
pygame.display.set_caption("Sidescrolling Shooter")
clock = pygame.time.Clock()
#ration 4:3
width = 600
height = 450

#Colours
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)

#Screen creation
screen = pygame.display.set_mode((width, height))


#Create Classes
class Player():

  def __init__(self):
    self.x = 0
    self.y = 0
    self.dx = 0
    self.dy = 0
    self.surface = pygame.image.load("sprites/player.png").convert()
    self.maxhealth = 20
    self.health = self.maxhealth
    self.kills = 0
    self.score = 0

  def up(self):
    self.dy = -5

  def down(self):
    self.dy = 5

  def left(self):
    self.dx = -5

  def right(self):
    self.dx = 5

  def move(self):
    self.y = self.y + self.dy
    self.x = self.x + self.dx

    #Border Collisions
    if self.y < 0:
      self.y = 0
      self.dy = 0

    elif self.y > 550:
      self.y = 550
      self.dy = 0

    if self.x < 0:
      self.x = 0
      self.dx = 0

    elif self.x > 700:
      self.x = 700
      self.dx = 0

  def distance(self, other):  #exponention
    return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

  def render(self):
    screen.blit(self.surface, (int(self.x), int(self.y)))
    #HP Bar
    pygame.draw.line(
        screen, green, (int(self.x), int(self.y)),
        (int(self.x + (40 * (self.health / self.maxhealth))), int(self.y)), 2)


class Missle():

  def __init__(self):
    self.x = 0
    self.y = 1000
    self.dx = 0
    self.dy = 0
    self.surface = pygame.image.load("sprites/missile.png").convert()
    self.state = "ready"

  #When the missle appears
  def fire(self):
    self.state = "firing"
    self.x = player.x + 25
    self.y = player.y + 16
    self.dx = 10

  #As logn as we're firing , it moves forword. Going in update loops
  def move(self):
    if self.state == "firing":
      self.x = self.x + self.dx
    if self.x > width:
      self.state = "ready"
      self.y = 1000

  def distance(self, other):
    return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

  def render(self):
    screen.blit(self.surface, (int(self.x), int(self.y)))


class Enemy():

  def __init__(self):
    self.x = 600
    self.y = random.randint(0, 550)
    self.dx = random.randint(10, 50) / -10  #to make it go left
    self.dy = 0
    self.surface = pygame.image.load("sprites/enemy.png").convert()
    self.max_health = random.randint(5, 15)
    self.health = self.max_health
    self.type = "enemy"

  def move(self):
    self.x = self.x + self.dx
    self.y = self.y + self.dy

    #Border check
    if self.x < -30:
      self.x = random.randint(800, 900)
      self.y = random.randint(0, 550)
      self.health = self.max_health

    if self.y < 0:
      self.y = 0
      self.dy *= -1

    elif self.y > 550:
      self.y = 550
      self.dy *= -1

  def distance(self, other):
    return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

  def render(self):
    screen.blit(self.surface, (int(self.x), int(self.y)))
    pygame.draw.line(
        screen, green, (int(self.x), int(self.y)),
        (int(self.x + (40 * (self.health / self.max_health))), int(self.y)), 2)


class Star():

  def __init__(self):
    self.x = random.randint(0, 1000)
    self.y = random.randint(0, 550)
    self.dx = random.randint(10, 50) / -30
    images = ["sprites/yellow_star.png", "sprites/red_star.png", "sprites/white_star.png"]
    self.surface = pygame.image.load(random.choice(images)).convert()

  def move(self):
    self.x = self.x + self.dx
    if self.x < 0:
      self.x = random.randint(800, 900)
      self.y = random.randint(0, 550)

  def distance(self, other):  #exponention
    return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

  def render(self):
    screen.blit(self.surface, (int(self.x), int(self.y)))


class Highscores():
  def __init__(self , filename):
    self. filename = filename
    self.scores = []
    self.load()

  def load(self):
    try:
      with open(self.filename, "r") as file:
        for line in file:
          name , score = line.strip().split(",")
          self.scores.append((name , int(score)))
    except FileNotFoundError:
      pass

  def add_score(self , name , score):
    self.scores.append((name , score))
    self.scores.sort(key = lambda x: x[1] , reverse = True)#start with the highest and go down
    self.scores = self.scores[:10]#only show the top 10 scores
    self.save()

  def save(self):
    with open(self.filename , "w") as file:
      for name , score in self.scores:
        file.write(f"{name},{score}\n")

  def render(self):
    y = 40
    screen.fill(black)
    for i , (name , score) in enumerate(self.scores):
      text = font.render(f"{i+1}. {name} - {score}" , True , white)
      text_rect = text.get_rect(center = (width/2 , y))
      print(f"{i+1}. {name} - {score}")
      screen.blit(text , text_rect)
      y += 30

class InputBox:
  def __init__(self , master):
    self.master = master
    master.title("Input Printer")

    self.input_label = tk.Label(master , text = "Enter your name for the highscore:")
    self.input_label.pack()
    self.input_entry = tk.Entry(master)
    self.input_entry.pack()

    self.submit_button = tk.Button(master , text = "Submit" , command = self.submit)
    self.submit_button.pack()


  def submit(self):
    highscores.add_score(self.input_entry.get() , player.score)
    root.destroy()

    
#Create sounds
missile_sound = pygame.mixer.Sound("sprites/missile.wav")
explosion_sound = pygame.mixer.Sound("sprites/explosion.wav")
missile_sound.set_volume(0.2)
explosion_sound.set_volume(0.2)

#Create fonts
font = pygame.font.SysFont("arial", 24)

#Highscore Object
highscores = Highscores("highscores.txt")

#Create object
player = Player()
missiles = [Missle(), Missle(), Missle()]
enemies = []

for i in range(5):
  enemies.append(Enemy())

stars = []
for i in range(30):
  stars.append(Star())


def fire_missles():
  # if missler eady
  for missile in missiles:
    if missile.state == "ready":
      missile.fire()
      break


#Main Game Loop / UpdateLoop
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        player.up()
      if event.key == pygame.K_DOWN:
        player.down()
      if event.key == pygame.K_LEFT:
        player.left()
      if event.key == pygame.K_RIGHT:
        player.right()
      if event.key == pygame.K_SPACE:
        fire_missles()
        missile_sound.play()

  #Update Objects
  player.move()

  for missile in missiles:
    missile.move()
   
  for star in stars:
    star.move()

  for enemy in enemies:
    enemy.move()
    for missile in missiles:
      if enemy.distance(missile) < 30:
        explosion_sound.play()
        enemy.health -= 4
        if enemy.health <= 0:
          enemy.x = random.randint(800, 900)
          enemy.y = random.randint(0, 550)
          if enemy.type == "boss":
            player.score += 50

          player.kills += 1
          if player.kills % 2 == 0:
            enemy.surface = pygame.image.load("sprites/boss.png").convert()
            enemy.health = enemy.max_health
            enemy.dy = random.randint(-5, 5)
            enemy.type = "boss"
          else:
            enemy.type = "enemy"
            enemy.dy = 0
            enemy.surface = pygame.image.load("sprites/enemy.png").convert()
            enemy.max_health = random.randint(5, 15)
            enemy.health = enemy.max_health
        else:
          enemy.x += 20
        #reset Missle
        missile.dx = 0
        missile.x = 0
        missile.y = 1000
        missile.state = "ready"

        #Score
        player.score += 10

      #Chech for player collision
      if player.distance(enemy) < 30:
        explosion_sound.play()
        player.health -= random.randint(5, 10)
        enemy.health -= random.randint(5, 10)
        enemy.x = random.randint(800, 900)
        enemy.y = random.randint(0, 550)

        if player.health <= 0:
          root = tk.Tk()
          #root.eval('tk::PlaceWindow . center')
          gui = InputBox(root)
          root.mainloop()
          screen.fill(black)
          highscores.render()
          pygame.display.flip()
      
          while True:
            for event in pygame.event.get():
              if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

  #Rendering
  screen.fill(black)
  player.render()

  for star in stars:
    star.render()

  for missile in missiles:
    missile.render()

  for enemy in enemies:
    enemy.render()

  #Ammo counter
  ammo = 0
  for missile in missiles:
    if missile.state == "ready":
      ammo = ammo + 1
    for x in range(ammo):
      screen.blit(missile.surface, (400 + 30 * x, 20))

  #Render Score
  score_surface = font.render(f"Score: {player.score} Kills: {player.kills}",
                              True, white)
  screen.blit(score_surface, (300, 200))

  pygame.display.flip()
  clock.tick(30)
