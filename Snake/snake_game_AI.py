import pygame
import random
import numpy as np
from enum import Enum

# Cores
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

pygame.init()

class Directions(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class Apple:
    def __init__(self, windowWidth, windowHeight, size):
        self.width = windowWidth
        self.height = windowHeight
        self.size = size

        self.change_location()
    
    def change_location(self):
        #Garante que está dentro da GRID do jogo
        self.x = random.randint(0, (self.width - self.size) // self.size ) * self.size
        self.y = random.randint(0, (self.height - self.size) // self.size ) * self.size
    
    def draw_apple(self, screen):
        pygame.draw.rect(screen, red, [self.x, self.y, self.size, self.size])

class Player:
    def __init__(self, length, x, y):
        self.snake_block = 15
        self.snake_speed = 8
        self.length = length
        self.x = (x // self.snake_block) * self.snake_block
        self.y = (y // self.snake_block) * self.snake_block
        self.x_change = self.snake_block
        self.y_change = 0
        self.direction = Directions.RIGHT
        self.snake_list = []

        for i in range(length):
            self.snake_list.insert(0, [self.x - i * self.snake_block, self.y])

    
    def draw_snake(self, screen):
        for x in self.snake_list:
            pygame.draw.rect(screen, green, [x[0], x[1], self.snake_block, self.snake_block])
    
    def change_direction(self, action):
        # [reto, direita, esquerda]

        clock_wise = [Directions.RIGHT, Directions.DOWN, Directions.LEFT, Directions.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0,1,0]):
            new_idx = (idx + 1) % len(clock_wise) #vira a direita r -> d -> l -> u
            new_dir = clock_wise[new_idx]
        else:# Action == [0, 0, 1]
            new_idx = (idx - 1) % len(clock_wise) #vira a esquerda r -> u -> l -> d
            new_dir = clock_wise[new_idx]

        self.direction = new_dir

        if self.direction == Directions.LEFT:
            self.x_change = -self.snake_block
            self.y_change = 0
        elif self.direction == Directions.RIGHT:
            self.x_change = self.snake_block
            self.y_change = 0
        elif self.direction == Directions.UP:
            self.y_change = -self.snake_block
            self.x_change = 0
        elif self.direction == Directions.DOWN:
            self.y_change = self.snake_block
            self.x_change = 0

    def move_snake(self, action, width, height):
        self.change_direction(action)
        
        self.x += self.x_change
        self.y += self.y_change

        if self.x >= width:
            self.x = 0
        elif self.x < 0:
            self.x = width - self.snake_block
        
        if self.y >= height:
            self.y = 0
        elif self.y < 0:
            self.y = height - self.snake_block

        snake_Head = []
        snake_Head.append(self.x)
        snake_Head.append(self.y)
        self.snake_list.append(snake_Head)
        if len(self.snake_list) > self.length:
            del self.snake_list[0]
        
    
    def check_food_be_eaten(self, apple: Apple) -> int:
        
        if [apple.x, apple.y] in self.snake_list:
            self.length += 1
            apple.change_location()
            return 1
        
        return 0
    
    def on_collision(self, app):
        for i in range(0, len(self.snake_list) - 1):
            if self.snake_list[-1] == self.snake_list[i]:
                return True
        
        return False

    def return_length_snake(self) -> list:
        return len(self.snake_list)

class SnakeGameAI:
    #Tamanho da tela
    windowWidth = 900
    windowHeight = 600

    def __init__(self):
        self.running = True
        self.screen = None
        self.score = 0
        self.clock = None
        self.player = Player(3, self.windowWidth/2, self.windowHeight/2)
        self.food = Apple(self.windowWidth, self.windowHeight, self.player.snake_block)
        self.frame_iteration = 0

    def on_init(self):
        self.screen = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.running = True
        

    def game_over(self):
        self.screen.fill("black")
        font_style = pygame.font.SysFont("bahnschrift", 25)
        message = font_style.render("Game Over! Press Q-Quit or C-Play Again", True, red)
        text_rect = message.get_rect(center=(self.windowWidth // 2, self.windowHeight // 2))
        self.screen.blit(message, text_rect)
        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                        waiting = False
                    elif event.key == pygame.K_c:
                        self.__init__()   # Reinicia o jogo
                        self.on_execute()
                        waiting = False

    def draw_game(self):
        # Preenche a tela para não ter nada do frame anterior
        self.screen.fill("black")
        self.player.draw_snake(self.screen)
        self.food.draw_apple(self.screen)
        self.draw_score()
        pygame.display.flip()

    def draw_score(self):
        font_style = pygame.font.SysFont("bahnschrift", 25)
        text = font_style.render("Score: " + str(self.score), True, white)
        self.screen.blit(text, (0, 0))

    def play_step(self, action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
        reward = 0
        self.player.move_snake(action, self.windowWidth, self.windowHeight)
            
        if(self.player.check_food_be_eaten(self.food)):
            self.score += 1
            reward = 10
            
        done = False
        if self.player.on_collision(self) or self.frame_iteration > 100*self.player.return_length_snake():
            done = True
            reward = -10
            return reward, done, self.score
            
        self.draw_game()
        #Descomente essa linha caso queira visualizar o agente jogando o jogo, para treinar deixe ela comentada
        #self.clock.tick(self.player.snake_speed) 

        return reward, done, self.score

    def get_display_size(self) -> tuple:
        return (self.windowWidth, self.windowHeight)
