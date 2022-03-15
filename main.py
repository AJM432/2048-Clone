#! /Users/alvin/opt/anaconda3/bin/python3
import pygame
import random
import time
import math

# Constants
# ________________________________________
GREY = (125, 125, 125)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SILVER = (192,192,192)
FPS = 60
# always one less than actual size since arrays start at index 0
BOARD_ARRAY_DIMENSION = 4-1
BOTTOM_BAR_HEIGHT = 100
LINE_THICKNESS = 10
WIDTH = HEIGHT = 500
BOARD_NUMBER_START = 0 # starting values of all cells
LINE_COLOR = BLACK
game_score = 0
pygame.init()


# pygame.font.init()

py_font = pygame.font.SysFont('Calibri', 25)

WIN = pygame.display.set_mode((WIDTH, HEIGHT+BOTTOM_BAR_HEIGHT))
pygame.display.set_caption("2048")
pygame.display.update()

# ________________________________________


# Functions
# ________________________________________
# switch matrix rows with columns
def transpose_matrix(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


def reverse_matrix_rows(matrix):  # [::-1] each row
    return [row[::-1] for row in matrix]


def display_matrix(list_of_lists):
    for row in list_of_lists:
        print(row)


def new_block_value():
    return random.choice([2, 4])


def find_open_position(board):
    # find all possible cell positions in board
    open_cells = []
    for row_index, row in enumerate(board):
        for col_index, col in enumerate(row):
            if col == 0:
                open_cells.append([row_index, col_index])
    if open_cells == []:
        return False
    else:
        return random.choice(open_cells)


# always assuming your input is "a" direction and transforming matrix back to original layout
def perform_board_motion(board):
    global game_score
    for row_index, row in enumerate(board):
        addition_performed = False
        for col_index, value in enumerate(row):
            if value != 0:
                if 0 in row[0:col_index]:
                    if row.index(0)-1 >= 0:
                        if row[row.index(0)-1] == value and not addition_performed:
                            board[row_index][row.index(
                                0)-1] = value + row[row.index(0)-1]
                            game_score += value + row[row.index(0)-1]
                            board[row_index][col_index] = 0
                            addition_performed = True
                        else:
                            # getting first 0
                            board[row_index][row.index(0)] = value
                            board[row_index][col_index] = 0
                    else:
                        # getting first 0
                        board[row_index][row.index(0)] = value
                        board[row_index][col_index] = 0
                elif col_index-1 >= 0:
                    if row[col_index-1] == value and not addition_performed:
                        board[row_index][col_index-1] = value + \
                            row[col_index-1]
                        game_score += value + row[col_index-1]
                        board[row_index][col_index] = 0
                        addition_performed = True
    return board


def check_is_move_possible(board):
    for row in range(len(board)):
        if 0 in board[row]:
            return True
        for col in range(len(board[row])-1):
            if board[row][col] == board[row][col+1] and board[row][col+1] != 0: # if value is 0 user can still move
                return True

    tran_matrix = transpose_matrix(board)
    for row in range(len(tran_matrix)):
        for col in range(len(tran_matrix[row])-1):
            if tran_matrix[row][col] == tran_matrix[row][col+1] and tran_matrix[row][col+1] != 0:
                return True
    return False

# ________________________________________


def draw_grid(thickness, line_color, dimensions):
    for row in range(1, dimensions+1):
        pygame.draw.line(WIN, line_color, (row*(WIDTH/dimensions), 0),
                         (row*(WIDTH / dimensions), HEIGHT), thickness)

    for column in range(1, dimensions+1):
        pygame.draw.line(WIN, line_color, (0, column*(HEIGHT/dimensions)),
                         (WIDTH, column*(HEIGHT / dimensions)), thickness)


# random color scheme
def get_rgb_value(number):
    if number ==  0:
        return SILVER
    elif number in (2, 4):
        return (255, 255, 204)
    elif number == 8:
        return (255, 204, 153)
    elif number == 16:
        return (255, 153, 51)
    elif number == 32:
        return (255, 128, 0)
    elif number == 64:
        return (255, 102, 102)
    elif number == 128:
        return (255, 255, 102)
    elif number == 256:
        return (255, 255, 75)
    elif number == 512:
        return (255, 255, 51)
    elif number == 1024:
        return (255, 255, 0)
    elif number == 2048:
        return (255, 215, 0)
    else:
        return (50, 50, 27)
    # return (255-math.log2(number)*20, 200-math.log2(number)*5, 0)

def update_game_grid(board):
    dimensions = BOARD_ARRAY_DIMENSION + 1
    for row in range(dimensions):
        for col in range(dimensions):
            # center_point_x = WIDTH/dimensions*col + (WIDTH/dimensions)/2
            center_point_x = WIDTH/dimensions*col
            # center_point_y = HEIGHT/dimensions*row + (HEIGHT/dimensions)/2
            center_point_y = HEIGHT/dimensions*row
            number = board[row][col]

            box_color = get_rgb_value(number)  # random color algo
            pygame.draw.rect(WIN, box_color, (center_point_x,
                             center_point_y, WIDTH/dimensions, HEIGHT/dimensions))
            if number != 0:
                text_surface = py_font.render(str(number), False, BLACK)
                WIN.blit(text_surface, (center_point_x + (WIDTH/dimensions) /
                        2, center_point_y+(HEIGHT/dimensions)/2))


def main_game_loop(board, previous_board_tracker):
    global game_score
    clock = pygame.time.Clock()
    running = True
    WIN.fill(WHITE)
    draw_grid(LINE_THICKNESS, LINE_COLOR, BOARD_ARRAY_DIMENSION+1)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                previous_board_tracker = board
                if event.key == pygame.K_UP:
                    board = transpose_matrix(board)
                    board = perform_board_motion(board)
                    board = transpose_matrix(board)

                elif event.key == pygame.K_RIGHT:
                    board = reverse_matrix_rows(board)
                    board = perform_board_motion(board)
                    board = reverse_matrix_rows(board)

                elif event.key == pygame.K_LEFT:
                    # function already assumes motion is in "a" direction
                    board = perform_board_motion(board)

                elif event.key == pygame.K_DOWN:
                    board = transpose_matrix(board)
                    board = reverse_matrix_rows(board)
                    board = perform_board_motion(board)
                    board = reverse_matrix_rows(board)
                    board = transpose_matrix(board)

                open_pos = find_open_position(board)
                if open_pos != False and previous_board_tracker != board: # check if board changed
                    board[open_pos[0]][open_pos[1]] = new_block_value()
                else:
                    if check_is_move_possible(board) == False:
                        print("You ran out of cells!, GAME OVER")
                        text_surface = py_font.render('GAME OVER', False, BLUE)
                        WIN.fill(WHITE)
                        WIN.blit(text_surface, (WIDTH/3, HEIGHT/3))
                        pygame.display.update()
                        time.sleep(4)
                        running = False

                display_matrix(board)
                print("________________________________________")

        WIN.fill(WHITE)
        update_game_grid(board)
        draw_grid(LINE_THICKNESS, LINE_COLOR, BOARD_ARRAY_DIMENSION+1)
        text_surface = py_font.render(
            'Score: ' + str(game_score), False, BLACK)
        WIN.blit(text_surface, (WIDTH/3, HEIGHT + BOTTOM_BAR_HEIGHT/2))
        clock.tick(FPS)
        pygame.display.update()
    pygame.quit()


# create 2d matrix of board
board = [[BOARD_NUMBER_START for x in range(0, BOARD_ARRAY_DIMENSION+1)]
         for y in range(0, BOARD_ARRAY_DIMENSION+1)]
previous_board_tracker = []
# board = [[0, 0, 0, 0],
        #  [4, 8, 16, 0],
        #  [2, 16, 64, 0],
        #  [8, 128, 256, 1024]]


# game starts spawning two blocks
if BOARD_NUMBER_START == 0:
    open_pos = find_open_position(board)
    board[open_pos[0]][open_pos[1]] = new_block_value()

    open_pos = find_open_position(board)
    board[open_pos[0]][open_pos[1]] = new_block_value()

display_matrix(board)


if __name__ == "__main__":
    print("Use the wasd keys to move up, left, down and right. Enter \"quit\" to quit")
    main_game_loop(board, previous_board_tracker)

    display_matrix(board)
