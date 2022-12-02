import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np


pygame.init()
font = pygame.font.SysFont('arial', 25)

#reset 
#reward
#play(action)
#game iteration
#is collision 
class Dir(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', ['x', 'y'])

#rgb
WHITE = (255,255,255)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 5

class SnakeGameAI:
    def __init__(self, w=640,h=480):
        self.w = w
        self.h = h       
        #init display
        self.display = pygame.display.set_mode(size=(self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        #init game state
        self.dir = Dir.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake= [self.head, 
                    Point(self.head.x - BLOCK_SIZE, self.head.y), 
                    Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iter = 0


    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()


    def play_step(self, action):
        #colelct user input
        self.frame_iter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        #move snake
        reward = 0
        self._move(action)
        self.snake.insert(0,self.head)

        #game over?
        game_over = False
        if self._is_collision() or self.frame_iter > 100*len(self.snake):
            game_over = True
            reward -= 10
            return reward, game_over, self.score
        #place new food/move
        if self.head == self.food:
            self.score += 1
            reward += 10
            self._place_food()
        else:
            self.snake.pop()
        #update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        #return game over and score
        return reward. game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display,BLUE1, pygame.Rect(pt.x,pt.y,BLOCK_SIZE, BLOCK_SIZE ))
            pygame.draw.rect(self.display,BLUE2, pygame.Rect(pt.x+4,pt.y+4,12, 12 ))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x,self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()

    def _move(self, action):
        #[straight, right, left]
        clock_wise = [Dir.RIGHT, Dir.DOWN, Dir.LEFT, Dir.UP]
        idx = clock_wise.index(self.dir)

        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx] #no change
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] #right
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] #right

        self.dir = new_dir
        x = self.head.x
        y = self.head.y

        if self.dir  == Dir.RIGHT:
            x += BLOCK_SIZE
        elif self.dir  == Dir.LEFT:
            x -= BLOCK_SIZE
        elif self.dir  == Dir.UP:
            y -= BLOCK_SIZE
        elif self.dir  == Dir.DOWN:
            y += BLOCK_SIZE
        self.head = Point(x,y)

    def _is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt.x > self.w - BLOCK_SIZE \
            or pt.x < 0 \
            or pt.y > self.h - BLOCK_SIZE \
            or pt.y < 0:
                return True
        if pt in self.snake[1:]:
            return True
        return False


