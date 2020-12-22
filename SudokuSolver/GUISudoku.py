import pygame
import time
import random

pygame.font.init()

class Grid:
    boards = {
        1 : [
        [3,0,0,8,0,1,0,0,2],
        [2,0,1,0,3,0,6,0,4],
        [0,0,0,2,0,4,0,0,0],
        [8,0,9,0,0,0,1,0,6],
        [0,6,0,0,0,0,0,5,0],
        [7,0,2,0,0,0,4,0,9],
        [0,0,0,5,0,9,0,0,0],
        [9,0,4,0,8,0,7,0,5],
        [6,0,0,1,0,7,0,0,3]
        ],
        2 : [
            [0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,3,0,8,5],
            [0,0,1,0,2,0,0,0,0],
            [0,0,0,5,0,7,0,0,0],
            [0,0,4,0,0,0,1,0,0],
            [0,9,0,0,0,0,0,0,0],
            [5,0,0,0,0,0,0,7,3],
            [0,0,2,0,1,0,0,0,0],
            [0,0,0,0,4,0,0,0,9]
        ],
        3 : [
            [5,3,0,0,7,0,0,0,0],
            [6,0,0,1,9,5,0,0,0],
            [0,9,8,0,0,0,0,6,0],
            [8,0,0,0,6,0,0,0,3],
            [4,0,0,8,0,3,0,0,1],
            [7,0,0,0,2,0,0,0,6],
            [0,6,0,0,0,0,2,8,0],
            [0,0,0,4,1,9,0,0,5],
            [0,0,0,0,8,0,0,7,9]
        ],
        4 : [
            [0,0,6,4,8,1,3,0,0],
            [0,2,0,0,0,0,0,4,0],
            [7,0,0,0,0,0,0,0,9],
            [8,0,0,0,9,0,0,0,4],
            [6,0,0,3,4,2,0,0,1],
            [5,0,0,0,6,0,0,0,2],
            [3,0,0,0,0,0,0,0,5],
            [0,9,0,0,0,0,0,7,0],
            [0,0,5,7,1,6,2,0,0]
        ],
        5: [
            [0,3,0,0,1,0,0,6,0],
            [7,5,0,0,3,0,0,4,8],
            [0,0,6,9,8,4,3,0,0],
            [0,0,3,0,0,0,8,0,0],
            [9,1,2,0,0,0,6,7,4],
            [0,0,4,0,0,0,5,0,0],
            [0,0,1,6,7,5,2,0,0],
            [6,8,0,0,9,0,0,1,5],
            [0,9,0,0,4,0,0,3,0]
        ]
    }
    board = boards[random.randint(1,5)]
    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if checker(self.model, (row,col), val) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (0, int(i*gap)), (self.width, int(i*gap)), thick)
            pygame.draw.line(self.win, (0, 0, 0), (int(i * gap), 0), (int(i * gap), self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if checker(self.model, (row, col), i):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    def solve_gui(self):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if checker(self.model, (row, col), i):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (int(x+5), int(y+5)))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (int(x) + (int(gap/2 - text.get_width()/2)), int(y) + (int(gap/2 - text.get_height()/2))))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (int(x),int(y), int(gap), int(gap)), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = int(self.width / 9)
        x = int(self.col * gap)
        y = int(self.row * gap)

        pygame.draw.rect(win, (255, 255, 255), (int(x), int(y), gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (int(x) + int(gap / 2 - text.get_width() / 2), int(y) + int(gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
            time.sleep(0.1)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)
            time.sleep(0.1)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col

    return None

def checker(board, location, num):
    row,col = location

    #Check row
    for i in range(0,len(board)):
        if board[row][i] == num and col !=i:
            return False
    #Check col
    for i in range(0,len(board)):    
        if board[i][col] == num and col !=i:
            return False
    #Check box
    box_col = col//3
    box_row = row//3

    for i in range(box_row*3, box_row*3 + 3):
        for j in range(box_col*3, box_col*3 + 3):
            if board[i][j] == num and (i,j) != location:
                return False
    return True


def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw()


def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + "." + str(sec)
    return mat


def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku Solver")
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)
        possible_keys = {pygame.K_1 : 1, pygame.K_2 : 2, pygame.K_3 : 3, pygame.K_4 : 4, pygame.K_5 : 5, 
                        pygame.K_6 : 6, pygame.K_7 : 7, pygame.K_8 : 8, pygame.K_9 : 9, pygame.K_KP1: 1, 
                        pygame.K_KP2 : 2, pygame.K_KP3 : 3, pygame.K_KP4 : 4, pygame.K_KP5 : 5, 
                        pygame.K_KP6 : 6, pygame.K_KP7 : 7, pygame.K_KP8 : 8, pygame.K_KP9 : 9}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key in possible_keys:
                    key = possible_keys[event.key]

                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    board.solve_gui()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()