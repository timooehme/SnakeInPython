import pygame as pyg
import random
import time
from enum import Enum

#Configure the Colors for the game
black = (0,0,0)
green = (124,176,107)

#Setup for the Controls
class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4
#Size of the Gameboard
win_width = 500
win_height = 500

#General initialisation
pyg.init()
pyg.display.set_caption('Snake')
window = pyg.display.set_mode((win_width,win_height))
refresh = pyg.time.Clock()
#Initalposition of snake might be randomized in the future
snake_pos = [win_width // 2,win_height // 2]

#Snake is a list of tuples that will be modified
snake_body = [[snake_pos[0],snake_pos[1]],[snake_pos[0] - 10,snake_pos[1]],[snake_pos[0] - 20,snake_pos[1]]]

#Initalposition of food might be randomized in the future
global food_pos
food_pos = [win_width // 10, win_height // 10]
#keeping track of score
global score
score = 0

#Managing the keyboard inputs playable with WASD and Arrows.
#letting keyboard inputs through if no inverse direction and snake is outside of window
def keyhandling(direction):
    newDirection = direction
    for event in [e for e in pyg.event.get() if e.type == pyg.KEYDOWN]:
        if (event.key == pyg.K_UP or event.key == pyg.K_w) and direction != Direction.DOWN and snake_pos[0] > 0 and snake_pos[0] < win_width:
            newDirection = Direction.UP
        if (event.key == pyg.K_DOWN or event.key == pyg.K_s) and direction != Direction.UP and snake_pos[0] > 0 and snake_pos[0] < win_width:
            newDirection = Direction.DOWN
        if (event.key == pyg.K_LEFT or event.key == pyg.K_a) and direction != Direction.RIGHT and snake_pos[1] > 0 and snake_pos[1] < win_height:
            newDirection = Direction.LEFT
        if (event.key == pyg.K_RIGHT or event.key == pyg.K_d) and direction != Direction.LEFT and snake_pos[1] > 0 and snake_pos[1] < win_height:
            newDirection = Direction.RIGHT
    return newDirection

#Checking for boundary and move the snake and add ne part which is poped in food function
def movesnake(direction):
    if snake_pos[0] < 0:
        snake_pos [0] = win_width
    if snake_pos[1] < 0:
        snake_pos [1] = win_height
    if snake_pos[0] > win_width:
        snake_pos [0] = -10
    if snake_pos[1] > win_height:
        snake_pos [1] = -10 

    if direction == Direction.UP:
        snake_pos[1] -= 10
    if direction == Direction.DOWN:
        snake_pos[1] += 10
    if direction == Direction.RIGHT:
        snake_pos[0] += 10
    if direction == Direction.LEFT:
        snake_pos[0] -= 10
    snake_body.insert(0,list(snake_pos))

#handling the eating of the snake and remove tail if nothing was eaten
def food():
    global score
    if snake_pos == food_pos:
        score += 10
        newfood()
    else:
        snake_body.pop()
    
#generating new food position. might end up on top of snake -> update it in the future
def newfood():
    global food_pos
    food_pos = [random.randrange(1, (win_width//10))*10,
                random.randrange(1, (win_height//10))*10]
    
#Drawing of the Game is happening here:
def repaint():
    window.fill(green)
    for body in snake_body:
        pyg.draw.rect(window, black, pyg.Rect(body[0], body[1], 10, 10))
    pyg.draw.rect(window, black, pyg.Rect(food_pos[0], food_pos[1], 10, 10))
    return

#collisonhandling of the snake
def gameover():
    for part in snake_body [1:]:
        if part == snake_pos:
            font = pyg.font.SysFont('Arial', 60)
            render = font.render(f"Score:{score}", True, black)
            rect = render.get_rect()
            rect.midtop = (win_width // 2, win_height // 2)
            window.blit(render,rect)
            pyg.display.flip()
            time.sleep(2)
            pyg.quit()

#increase speed with score -> increase of difficulty 
def detspeed():
    global score
    speed = 10
    if score > 50:
        speed += score // 10
    return speed

#Main functions call
def gamefun():
    direction = Direction.RIGHT
    while True:
        speed = detspeed()
        direction = keyhandling(direction)
        movesnake(direction)
        food()
        repaint()
        gameover()
        pyg.display.update()
        refresh.tick(speed)


if __name__ == "__main__":
    gamefun()

