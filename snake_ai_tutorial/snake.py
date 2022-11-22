import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont('arial', 25)


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

class SnakeGame:
    def __init__(self, w=640,h=480):
        self.w = w
        self.h = h       
        #init display
        self.display = pygame.display.set_mode(size=(self.w, self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        #init game state
        self.dir = Dir.RIGHT
        self.head = Point(self.w/2, self.h/2)
        self.snake= [self.head, 
                    Point(self.head.x - BLOCK_SIZE, self.head.y), 
                    Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()


    def play_step(self):
        #colelct user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.dir = Dir.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.dir = Dir.RIGHT
                elif event.key == pygame.K_UP:
                    self.dir = Dir.UP
                elif event.key == pygame.K_DOWN:
                    self.dir = Dir.DOWN
                
                
        #move snake
        self._move(self.dir)
        self.snake.insert(0,self.head)

        #game over?
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
        #place new food/move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        #update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        #return game over and score
        return game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display,BLUE1, pygame.Rect(pt.x,pt.y,BLOCK_SIZE, BLOCK_SIZE ))
            pygame.draw.rect(self.display,BLUE2, pygame.Rect(pt.x+4,pt.y+4,12, 12 ))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x,self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()

    def _move(self, dir):
        x = self.head.x
        y = self.head.y

        if dir  == Dir.RIGHT:
            x += BLOCK_SIZE
        elif dir  == Dir.LEFT:
            x -= BLOCK_SIZE
        elif dir  == Dir.UP:
            y -= BLOCK_SIZE
        elif dir  == Dir.DOWN:
            y += BLOCK_SIZE
        self.head = Point(x,y)

    def _is_collision(self):
        if self.head.x > self.w - BLOCK_SIZE \
            or self.head.x < 0 \
            or self.head.y > self.h - BLOCK_SIZE \
            or self.head.y < 0:
                return True
        if self.head in self.snake[1:]:
            return True
        return False


if __name__ == "__main__":
    game = SnakeGame()

    #game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break
    print('Final Score: ', score)
        #break when game over
    pygame.quit()