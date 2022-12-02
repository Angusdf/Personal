import torch
import random
import numpy as np
from collections import deque 
from snake_with_ai import SnakeGameAI, Dir, Point

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = .001

class Agent:

    def __int__(self):
        self.n_game = 0
        self.epsilon = 0
        self.gamma = 0
        self.mem = deque(maxlen = MAX_MEMORY)


    def get_state(self, game):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_mem(self):
        pass

    def train_short_mem(self):
        pass

    def get_action(self, state):
        pass

def train():
    plot_score = []
    plot_mean = []
    total_score =0
    record = 0
    agent = Agent()
    game = SnakeGameAI()

    while True:
        state_old = agent.get_state(game)

        final_move = agent.get_action(state_old)

        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        agent.train_short_mem

if __name__ == "__main__":
    train()