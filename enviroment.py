import numpy as np

class SnakeGame:

    def __init__(self, w=80, h=80, tile_dim=8):
        self.w = w
        self.h = h
        self.tile_dim = tile_dim
        self.possible_moves = [[0, tile_dim], [0, -tile_dim], [tile_dim, 0], [-tile_dim, 0]]

        self.snake = [[3 * self.tile_dim, 4 * self.tile_dim], 
                      [2 * self.tile_dim, 4 * self.tile_dim], 
                      [self.tile_dim, 4 * self.tile_dim]]
        self.direction = [self.tile_dim, 0]
        self.apple = []
        self.__spawn_apple()
        self.apple_eaten = False
        self.end_game = False
    
    def restart(self):
        self.snake = [[3 * self.tile_dim, 4 * self.tile_dim], 
                      [2 * self.tile_dim, 4 * self.tile_dim], 
                      [self.tile_dim, 4 * self.tile_dim]]
        self.direction = [self.tile_dim, 0]
        self.apple = []
        self.__spawn_apple()
        self.apple_eaten = False
        self.end_game = False
        return self.__get_state()

    def __spawn_apple(self):
        overlap = True
        while overlap:
            self.apple = [np.random.randint(0, self.w // self.tile_dim) * self.tile_dim,
                    np.random.randint(0, self.h // self.tile_dim) * self.tile_dim]
            for i in range(len(self.snake)):
                overlap = self.snake[i][0] == self.apple[0] and self.snake[i][1] == self.apple[1]
                if overlap:
                    break

    def __eat_apple(self):
        if self.snake[0][0] == self.apple[0] and self.snake[0][1] == self.apple[1]:
            self.apple_eaten = True
            self.snake.append(self.snake[-1].copy())

    def __snake_move(self):
        for i in range(len(self.snake) - 1, 0, -1):
            self.snake[i] = self.snake[i - 1].copy()
        self.snake[0] = [self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1]]


    def check_collision(self):
        if self.snake[0][0] < 0 or self.snake[0][0] >= self.w or self.snake[0][1] < 0 or self.snake[0][1] >= self.h:
            return True
        for i in range(1, len(self.snake)):
            if self.snake[0][0] == self.snake[i][0] and self.snake[0][1] == self.snake[i][1]:
                return True
        return False
    
    def __get_state(self):
        state = np.zeros((self.h, self.w))
        state[self.apple[1]:self.apple[1]+self.tile_dim, self.apple[0]:self.apple[0]+self.tile_dim,] = 1
        state[self.snake[0][1]:min(self.snake[0][1]+self.tile_dim, self.h), self.snake[0][0]:min(self.snake[0][0]+self.tile_dim, self.w)] = 0.75
        for snake_part in self.snake[1:]:
            state[snake_part[1]:snake_part[1]+self.tile_dim, snake_part[0]:snake_part[0]+self.tile_dim] = 0.4
        return state


    def step(self, action):
        proposed_direction = self.possible_moves[action].copy()
        if self.direction[0]*proposed_direction[0] + self.direction[1]*proposed_direction[1] >= 0:
            self.direction = proposed_direction
        self.__snake_move()
        self.__eat_apple()
        if self.apple_eaten:
            self.__spawn_apple()
            reward = 3
            self.apple_eaten = False
        else:
            reward = -0.1
        self.end_game = self.check_collision()
        if self.end_game:
            reward = -5
        return self.__get_state(), reward, self.end_game
        
