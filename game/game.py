import numpy as np
import time
import random
import pygame

class Game(object):
    def __init__(self, width=600, height=600):
        self.width = width
        self.height = height

        pygame.init()
        self.display = pygame.display.set_mode((self.width, self.height))

        self.cell_size = 4
        self.sleep_time = 0.01
        self.board_size = (self.width/self.cell_size,
                self.height/self.cell_size)
        self.random_new_board()

    def __game_loop(self):
        while (True):
            for event in pygame.event.get():
                print event
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == 114: # 'r'
                        self.random_new_board()

            self.__calculate_next_board()
            self.__draw_board()
            pygame.display.update()
            time.sleep(self.sleep_time)
        pass

    def random_new_board(self):
        self.board = np.random.random_integers(0, 1, self.board_size)
        self.board[0, ] = 0
        self.board[-1, ] = 0
        self.board[:, 0] = 0
        self.board[:, -1] = 0

    def __calculate_next_board(self):
        new_board = np.zeros(self.board_size)
        new_board[1:-1, 1:-1] += self.board[:-2, :-2] + self.board[:-2, 1:-1] \
            + self.board[:-2, 2:] + self.board[1:-1, :-2] \
            + self.board[1:-1, 2:] + self.board[2:, :-2] \
            + self.board[2:, 1:-1] + self.board[2:, 2:]

        new_board = np.where(new_board > 3, 0, new_board)
        new_board = np.where(new_board < 2, 0, new_board)

        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                if new_board[i][j] == 2:
                    new_board[i][j] = self.board[i][j]

        new_board = np.where(new_board == 3, 1, new_board)
        self.board = new_board

    def __draw_cell(self, x, y, alive):
        color = (255, 255, 255) if alive == 1 else (0, 0, 0)
        pygame.draw.rect(self.display, color,
            [x * self.cell_size, y * self.cell_size,
                self.cell_size, self.cell_size])

    def __draw_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.__draw_cell(i, j, self.board[i][j])

    def run(self):
        # start game loop
        self.__game_loop()

        # end game
        pygame.quit()

