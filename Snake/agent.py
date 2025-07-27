import torch
import random
from collections import deque
import numpy as np
from snake_game_AI import SnakeGameAI, Player, Apple, Directions
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0 #Parâmetro que serve para controlar a aletoriedade
        self.gamma = 0.9 #Valor que encoraja o agente a recompensas a longo ou a curto prazo dependendo do seu valor
        self.memory = deque(maxlen=MAX_MEMORY) #double-ended queue
        self.model = Linear_QNet(11, 256, 3) #Qtd de estados / hidden states / Qtd de saidas (reto, vira direita, vira esquerda)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    
    def get_state(self, game):
        head = game.player.snake_list[-1]
        point_l = [head[0] - game.player.snake_block, head[1]]
        point_r = [head[0] + game.player.snake_block, head[1]]
        point_u = [head[0], head[1] - game.player.snake_block]
        point_d = [head[0], head[1] + game.player.snake_block]

        dir_l = game.player.direction == Directions.LEFT
        dir_r = game.player.direction == Directions.RIGHT
        dir_u = game.player.direction == Directions.UP
        dir_d = game.player.direction == Directions.DOWN

        # Perigo (se há colisão ao virar naquela direção)
        danger_straight = (
            (dir_r and point_r in game.player.snake_list) or
            (dir_l and point_l in game.player.snake_list) or
            (dir_u and point_u in game.player.snake_list) or
            (dir_d and point_d in game.player.snake_list)
        )

        danger_right = (
            (dir_u and point_r in game.player.snake_list) or
            (dir_r and point_d in game.player.snake_list) or
            (dir_d and point_l in game.player.snake_list) or
            (dir_l and point_u in game.player.snake_list)
        )

        danger_left = (
            (dir_u and point_l in game.player.snake_list) or
            (dir_r and point_u in game.player.snake_list) or
            (dir_d and point_r in game.player.snake_list) or
            (dir_l and point_d in game.player.snake_list)
        )

        state = [
            #Importante ter o risco de colisão para treinar eficientemente nosso agente, verificando se a cabeça da cobra irá bater no corpo
            danger_straight,
            danger_right,
            danger_left,

            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Localização da comida
            game.food.x < head[0],  # food left head[0] == x
            game.food.x > head[0],  # food right head[0] == x
            game.food.y < head[1],  # food up head[1] == y
            game.food.y > head[1]  # food down head[1] == y
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) #popleft se MAX_MEMORY eh alcançado

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 80 - self.number_of_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0,2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0) 
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        
        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    game.on_init()
    while True:
        # Obter estador antigo
        old_state = agent.get_state(game)

        #Obter movimento
        final_move = agent.get_action(old_state)

        #Movimentar
        reward, done, score = game.play_step(final_move)
        new_state = agent.get_state(game)

        #Train short memory
        agent.train_short_memory(old_state, final_move, reward, new_state, done)

        #remember
        agent.remember(old_state, final_move, reward, new_state, done)

        if done:
            #treinar memória longa
            game = SnakeGameAI()
            game.on_init()
            agent.number_of_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()
            
            print('Game', agent.number_of_games, 'Score', score, 'Record', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.number_of_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == "__main__":
    train()