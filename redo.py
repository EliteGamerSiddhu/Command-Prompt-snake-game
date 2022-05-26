from copy import deepcopy
import string
from time import time, sleep
from msvcrt import kbhit, getch
from random import randint
import os

#CONTROLS ARE ARROW KEYS

UP, DOWN, LEFT, RIGHT = 'up', 'down', 'left', 'right' #Declaring all constant variables
Win = 224
Console = 0
Mode = Win #When running in Console change to console and when using command prompt change to Win, this changes input of keycode

#Making game functions

def initialize_food(size:list, food_no:int, food_pos_list:list): #selects random food positions to start game with
    f = deepcopy(food_pos_list)
    for i in range(food_no):
        x = randint(2, (size[0]-1))
        y = randint(2, (size[1]-1))
        f.append([x,y])
    return f

def get_input(): #takes the keyboard input
    if kbhit():
        key = getch()
        key = int.from_bytes(key, 'little')
        if key == Mode:
            if kbhit():
                arrow = getch()
                arrow = int.from_bytes(arrow, 'little')
                if arrow == 72:
                    key = UP
                elif arrow == 75:
                    key = LEFT
                elif arrow == 80:
                    key = DOWN
                elif arrow == 77:
                    key = RIGHT

                return key

        else:

            return None

def draw_frame(size: list, snake_pos_list:list, food_pos_list:list, wall:string, snake_head:string, snake_body:string, food_char:string): #Draws each frame with the given parameters
    for j in range(1, size[1]+1):
        for i in range(1, size[0]+1):
            pos = [i, j]
            if j == 1 or j == size[1] or i == 1 or i == size[0]:
                print(wall, end='')
            elif pos in food_pos_list:
                print(food_char, end='')
            elif pos == snake_pos_list[0]:
                print(snake_head, end='')
            elif pos in snake_pos_list:
                print(snake_body, end='')
            else:
                print(' ', end='')
        print()

def check_collision(size: list, snake_pos_list:list, food_pos_list:list, direction:string): #Checks if the snake will collide with something in the next frame
    s = deepcopy(snake_pos_list)
    collide = False
    eat = False
    food_pos = None
    snake_head = s[0]
    if direction == DOWN:
        snake_head[1] += 1
        if snake_head[1] >= size[1]:
            collide = True
    elif direction == UP:
        snake_head[1] -= 1
        if snake_head[1] <= 1:
            collide = True
    elif direction == RIGHT:
        snake_head[0] += 1
        if snake_head[0] >= size[0]:
            collide = True
    elif direction == LEFT:
        snake_head[0] -= 1
        if snake_head[0] <= 1:
            collide = True
    
    if snake_head in food_pos_list:
        collide = True
        eat = True
        food_pos = snake_head

    if snake_head in snake_pos_list:
        collide = True
    
    return collide, eat, food_pos

def update_snake(snake_pos_list:list, direction:string, grow:bool): #Moves the snake positions in a particular direction for next frame
    s = deepcopy(snake_pos_list)

    if grow == True:
        s.append([0,0])

    for x in range(len(s)-1, 0, -1):
        s[x] = list(s[x-1])

    if direction == DOWN:
        s[0][1] += 1
    elif direction == UP:
        s[0][1] -= 1
    elif direction == RIGHT:
        s[0][0] += 1
    elif direction == LEFT:
        s[0][0] -= 1

    return s

def update_food(size:list, snake_pos_list:list, food_pos_list:list, food_pos:list): #updates the food positions
    f = deepcopy(food_pos_list)
    x,y = 0,0
    while [x,y] in snake_pos_list or [x,y] == [0,0]:
        x = randint(2, (size[0]-1))
        y = randint(2, (size[1]-1))

    index = f.index(food_pos)
    f[index] = [x,y]
    return f

def change_direct(key:string, direction:string): #changes direction of the snake
    d = direction
    if key == UP:
        if d != DOWN:
            d = key
    elif key == DOWN:
        if d != UP:
            d = key
    elif key == LEFT:
        if d != RIGHT:
            d = key
    elif key == RIGHT:
        if d != LEFT:
            d = key

    return d

#main (driver program)

#Inputting all character to print frame
#Can take input any character supported by command prompt/console

WALL = input('Enter character to represent wall: ') 
SNAKE_HEAD = input('Enter character to represent snake head: ')
SNAKE_BODY = input('Enter charater to represent snake body: ')
FOOD_CHAR = input('Enter character to represent food: ')

#Determining map properties

SIZE = [0,0]
SIZE[1] = int(input('Enter height of map: '))
SIZE[0] = int(input('Enter width of map: '))

#Inputting game settings like speed of snake and number of food on screen in one frame

FOOD_NO = int(input('Enter number of food: '))
SPEED = float(input('Enter snake speed: '))
SPEED = 1/SPEED
SNAKE = [[int(SIZE[0]/2), int(SIZE[1]/2)]]
FOOD = []
FOOD = initialize_food(SIZE, FOOD_NO, FOOD)
DIRECT = RIGHT
game_over = False

os.system(f"mode con cols={SIZE[0]} lines={SIZE[1]+1}") #Opens resized window of command prompt to hide printing mess

input("PRESS ANY KEY TO START..........") #Statement before starting the main game

while not game_over:
    draw_frame(SIZE, SNAKE, FOOD, WALL, SNAKE_HEAD, SNAKE_BODY, FOOD_CHAR)
    key = get_input()
    DIRECT = change_direct(key, DIRECT)
    collide, eat, food_pos = check_collision(SIZE, SNAKE, FOOD, DIRECT)
    if collide is True and eat is False:
        game_over = True
    else:
        SNAKE = update_snake(SNAKE, DIRECT, eat)
        if food_pos is not None:
            FOOD = update_food(SIZE, SNAKE, FOOD, food_pos)
    sleep(SPEED) #Determines the frame rate, frame rate is directly related to speed of snake

print(f'GAME OVER        SNAKE LENGTH = {len(SNAKE)}') #Game over message and final snake length as score

input('Press any key to quit....')

quit() #ends the program in the command prompt, just a neat way