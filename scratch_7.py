import pygame, sys

pygame.init()

WIDTH = 600
HEIGHT = 600
LINE_COLOR = (25, 135, 145)
LINE_WIDTH = 15
BACKGROUND = (20, 170, 156)
BLACK = (0, 0, 0)
BOARD_COLS = 3
BOARD_ROWS = 3
ROW = 0
COL = 1
DIAG_A = 2
DIAG_B = 3

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('tic tac toe')
screen.fill(BACKGROUND)

board = [[0, 0, 0].copy() for i in range(3)]


def draw_lines():
    # 1 -
    pygame.draw.line(screen, LINE_COLOR, (0, 200), (600, 200), LINE_WIDTH)
    # 2 -
    pygame.draw.line(screen, LINE_COLOR, (0, 400), (600, 400), LINE_WIDTH)
    # 1 |
    pygame.draw.line(screen, LINE_COLOR, (200, 0), (200, 600), LINE_WIDTH)
    # 2 |
    pygame.draw.line(screen, LINE_COLOR, (400, 0), (400, 600), LINE_WIDTH)


def draw_XO():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, BLACK, (int(col * 200 + 100), int(row * 200 + 100)), 60, 15)
            if board[row][col] == 2:
                pygame.draw.line(screen, BLACK, (col * 200 + 50, row * 200 + 150), (col * 200 + 150, row * 200 + 50),
                                 23)
                pygame.draw.line(screen, BLACK, (col * 200 + 50, row * 200 + 50), (col * 200 + 150, row * 200 + 150),
                                 23)


def set_sqr(row, col, player):
    board[row][col] = player


def can_set_sqr(row, col):
    if board[row][col] == 0:
        return True
    else:
        return False


def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True


class TermsOfWin:
    def __init__(self, kind, index):
        self.kind = kind
        self.index = index


def terms_of_win(player):
    for col in range(BOARD_COLS):
        count = 0
        for row in range(BOARD_ROWS):
            if board[row][col] == player:
                count += 1
        if count == BOARD_ROWS:
            return TermsOfWin(COL, col)
    for row in range(BOARD_ROWS):
        count = 0
        for col in range(BOARD_COLS):
            if board[row][col] == player:
                count += 1
        if count == BOARD_COLS:
            return TermsOfWin(ROW, row)
    count = 0
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS):
            if board[row][col] == player and row == col:
                count += 1
    if count == BOARD_COLS:
        return TermsOfWin(DIAG_A, 0)
    count = 0
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS):
            if board[row][col] == player and row + col == BOARD_COLS - 1:
                count += 1
    if count == BOARD_COLS:
        return TermsOfWin(DIAG_B, 0)
    return None


def draw_v_w_line(col, player):
    posX = col * 200 + 100
    pygame.draw.line(screen, BLACK, (posX, 15), (posX, HEIGHT - 15), 15)


def draw_h_w_line(row, player):
    posY = row * 200 + 100
    pygame.draw.line(screen, BLACK, (15, posY), (WIDTH - 15, posY), 15)


def draw_a_d_line(player):
    pygame.draw.line(screen, BLACK, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)


def draw_d_d_line(player):
    pygame.draw.line(screen, BLACK, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)


def restart():
    screen.fill(BACKGROUND)
    draw_lines()
    player = 1
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0


draw_lines()

player = 1
gameover = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not gameover:
            X = event.pos[0]
            Y = event.pos[1]

            clicked_col = int(X // 200)
            clicked_row = int(Y // 200)

            if can_set_sqr(clicked_row, clicked_col):

                set_sqr(clicked_row, clicked_col, player)
                terms = terms_of_win(player)
                if terms:
                    gameover = True
                    if terms.kind == COL:
                        draw_v_w_line(terms.index, player)
                    elif terms.kind == ROW:
                        draw_h_w_line(terms.index, player)
                    elif terms.kind == DIAG_A:
                        draw_d_d_line(player)
                    elif terms.kind == DIAG_B:
                        draw_a_d_line(player)

                player = 2 if player == 1 else 1

                draw_XO()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
    pygame.display.update()
