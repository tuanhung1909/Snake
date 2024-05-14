import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial', 25)

dau = pygame.image.load('meo.png')
dau1 = pygame.transform.scale(dau, (30,30))

vang1 = pygame.image.load('pngegg.png')
vang = pygame.transform.scale(vang1,(30,30))

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')
def khoangcach(dau,dich):
    return ((dau.x-dich.x)**2+(dau.y - dich.y)**2)**(1/2)
# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
ORRANGE = (255,128,0)
PINK = (255,153,255)

BLOCK_SIZE = 20
SPEED = 1000

class SnakeGameAI:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Khối nguu")
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        # khởi tạo trạng thái
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.cnv = Point(100,200)
        self.frame_iteration = 0


    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        #if self.food.x <= self.cnv.x+10 and self.food.x >= self.cnv.x  and self.food.y >= self.cnv.y  and self.food.y <= self.cnv.y + 50 :
            #self._place_food()


    def play_step(self, action):
        self.frame_iteration += 1
        # 1. người chơi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. chuyển động
        self._move(action) 
        #cập nhật toạn độ điểm đầu
        self.snake.insert(0, self.head)
        
        # 3. kiểm tra nếu thua
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 10000*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. vị trí đồ ăn mới
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
            self.snake.pop()
        else:
            #d=khoangcach(self.food, self. head)
            #reward -=
            self.snake.pop()
        
        # 5. cập nhật màn hình và tốc độ
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. trả điểm 
        return reward, game_over, self.score


    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # chạm tường
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # tự chạm vào nó
        if pt in self.snake[1:]:
            return True
        #if self.head.x <= self.cnv.x+10 and self.head.x >= self.cnv.x  and self.head.y >= self.cnv.y  and self.head.y <= self.cnv.y + 50 :
        #    return True

        return False

    def _update_ui(self):
        self.display.fill(WHITE)

        #self.display.blit(dau1,(self.snake[0].x - 20,self.snake[0].y - 20))
        for pt in self.snake[0:]:
            pygame.draw.rect(self.display, BLACK, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, PINK, pygame.Rect(pt.x+9, pt.y+9, 12, 12))
        #pygame.draw.rect(self.display, BLACK, (self.cnv.x,self.cnv.y,10,50)) 
        #pygame.draw.rect(self.display, BLUE1, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        #self.display.blit(vang,self.food)
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        

        text = font.render("Score: " + str(self.score), True, ORRANGE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)