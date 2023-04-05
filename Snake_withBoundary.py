import numpy
import pygame as pyg
import random
import time
from enum import Enum

black = (0,0,0)
green = (124,176,107)

class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4

win_width = 500
win_height = 500

pyg.init()
pyg.display.set_caption('Snake')
window = pyg.display.set_mode((win_width,win_height))
refresh = pyg.time.Clock()

snake_pos = [win_width // 2,win_height // 2]
snake_body = [[snake_pos[0],snake_pos[1]],[snake_pos[0] - 10,snake_pos[1]],[snake_pos[0] - 20,snake_pos[1]]]
global food_pos
food_pos = [win_width // 10, win_height // 10]
global score
score = 0

def keyhandling(direction):
    newDirection = direction
    for event in [e for e in pyg.event.get() if e.type == pyg.KEYDOWN]:
        if event.key == pyg.K_UP and direction != Direction.DOWN:
            newDirection = Direction.UP
        if event.key == pyg.K_DOWN and direction != Direction.UP:
            newDirection = Direction.DOWN
        if event.key == pyg.K_LEFT and direction != Direction.RIGHT:
            newDirection = Direction.LEFT
        if event.key == pyg.K_RIGHT and direction != Direction.LEFT:
            newDirection = Direction.RIGHT
    return newDirection

def movesnake(direction):
    if direction == Direction.UP:
        snake_pos[1] -= 10
    if direction == Direction.DOWN:
        snake_pos[1] += 10
    if direction == Direction.RIGHT:
        snake_pos[0] += 10
    if direction == Direction.LEFT:
        snake_pos[0] -= 10
    snake_body.insert(0,list(snake_pos))


def food():
    global score
    if snake_pos == food_pos:
        score += 10
        newfood()
    else:
        snake_body.pop()
    

def newfood():
    global food_pos
    food_pos = [random.randrange(1, (win_width//10))*10,
                random.randrange(1, (win_height//10))*10]
    

def repaint():
    window.fill(green)
    for body in snake_body:
        pyg.draw.rect(window, black, pyg.Rect(body[0], body[1], 10, 10))
    pyg.draw.rect(window, black, pyg.Rect(food_pos[0], food_pos[1], 10, 10))

    return

def gameover():
    if snake_pos[0] < 0 or snake_pos[0] > win_width - 10:
        gameovermsg()
    if snake_pos[1] < 0 or snake_pos [1] > win_width - 10:
        gameovermsg()
    for part in snake_body [1:]:
        if part == snake_pos:
            gameovermsg()

def gameovermsg():
    font = pyg.font.SysFont('Arial', 62)
    render = font.render(f"Score:{score}", True, black)
    rect = render.get_rect()
    rect.midtop = (win_width // 2, win_height // 2)
    window.blit(render,rect)
    pyg.display.flip()
    time.sleep(2)
    pyg.quit()

    return

def detspeed():
    global score
    speed = 10
    if score > 50:
        speed += score // 10
    return speed
        

def hud():
    return

def gamefun():
    direction = Direction.RIGHT
    while True:
        speed = detspeed()
        direction = keyhandling(direction)
        movesnake(direction)
        food()
        repaint()
        gameover()
        hud()
        pyg.display.update()
        refresh.tick(speed)




    

if __name__ == "__main__":
    gamefun()

