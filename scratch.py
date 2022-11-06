from enum import Enum
import random
import curses
from curses import wrapper
from time import sleep
import time


class StateOfSnake(Enum):
    ALIVE = 0
    HIT_BY_WALL = 1
    EATEN_BY_ITSELF = 2


class Direction(Enum):
    UNKWOWN = 0
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


# .ooooo0
# нарисовать окно
class Snake:
    def __init__(self):
        self.direction = Direction.UNKWOWN
        # (x, y) (0 - head) (2 - tail)
        self.body = [(10, 10), (9, 10), (8, 10)]
        self.state = StateOfSnake.ALIVE

    def move(self):
        if self.direction == Direction.RIGHT:
            body_head = self.body[0]
            x = body_head[0]
            y = body_head[1]
            self.body.insert(0, (x + 1, y))
            self.body.pop()
        if self.direction == Direction.LEFT:
            self.body.insert(0, (self.body[0][0] - 1, self.body[0][1]))
            self.body.pop()
        if self.direction == Direction.UP:
            self.body.insert(0, (self.body[0][0], self.body[0][1] - 1))
            self.body.pop()
        if self.direction == Direction.DOWN:
            self.body.insert(0, (self.body[0][0], self.body[0][1] + 1))
            self.body.pop()

    def set_direction(self, direction):
        self.direction = direction

    def eat(self):
        self.body.append(self.body[-1])

    def is_head(self, x, y):
        if x == self.body[0][0] and y == self.body[0][1]:
            return True
        else:
            return False

    def is_tail(self, x, y):
        if x == self.body[-1][0] and y == self.body[-1][1]:
            return True
        else:
            return False

    def is_body(self, x, y):
        for x1, y1 in self.body[1: -1]:
            if x == x1 and y == y1:
                return True
        return False

    def death_of_snake(self, settings):
        if self.is_snake_dead():
            return self.state
        if self.body[0] in self.body[1:]:
            self.state = StateOfSnake.EATEN_BY_ITSELF
        if self.body[0][0] in (-1, settings.width) or self.body[0][1] in (-1, settings.height - 1):
            self.state = StateOfSnake.HIT_BY_WALL
        else:
            pass
        return self.state

    def is_snake_dead(self):
        return not self.state == StateOfSnake.ALIVE


class Settings:
    def __init__(self):
        self.speed = 0.5
        self.width = 20
        self.height = 20
        self.apple_count = 1


def create_apple(snake, height, width, apples):
    y = random.randint(0, height)
    x = random.randint(0, width)
    if (x, y) in snake.body or (x, y) in apples:
        return create_apple(snake, height, width, apples)
    return (x, y)


def try_eating_apple(snake, apples, height, width):
    new_apples = []
    for apple in apples:
        if apple == snake.body[0]:
            snake.eat()
            new_apples.append(create_apple(snake, height, width, apples))
        else:
            new_apples.append(apple)
    return new_apples


def draw_walls(screen, settings):
    screen.addstr(0, 0, '█' * (settings.width + 2))
    screen.addstr(settings.height, 0, '█' * (settings.width + 2))
    for y in range(1, settings.height):
        screen.addstr(y, 0, '█' + ' ' * settings.width + '█')


def main(stdscr):
    global snake
    curses.curs_set(False)
    curses.cbreak()
    stdscr.keypad(True)
    curses.noecho()
    stdscr.nodelay(True)
    prev_time = time.time()
    last_key = -1
    settings = Settings()
    settings.width = 40
    settings.speed = 0.25
    settings.apple_count = 3

    apples = [create_apple(snake, settings.height - 2, settings.width - 2, []) for _ in range(0, settings.apple_count)]
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    shifts = (1, 1)
    while True:
        curr_time = time.time()
        if curr_time - prev_time >= settings.speed:
            snake.move()
            snake.death_of_snake(settings)
            if snake.is_snake_dead():
                break
            apples = try_eating_apple(snake, apples, settings.height - 2, settings.width - 2)
            prev_time = curr_time
        # отрисовка
        stdscr.clear()
        draw_walls(stdscr, settings)
        stdscr.addstr(snake.body[0][1] + shifts[0], snake.body[0][0] + shifts[1], '0')
        for cell in snake.body[1:-1]:
            stdscr.addstr(cell[1] + shifts[0], cell[0] + shifts[1], 'o')
        stdscr.addstr(snake.body[-1][1] + shifts[0], snake.body[-1][0] + shifts[1], '.')

        for apple in apples:
            stdscr.addstr(apple[1] + shifts[0], apple[0] + shifts[1], 'Q', curses.color_pair(2))

        key = stdscr.getch()
        if key != -1:
            last_key = key

        # stdscr.addstr(0, 0, f'{last_key}')
        if last_key == 10:
            break
        elif last_key == 454:
            snake.set_direction(Direction.RIGHT)
        elif last_key == 456:
            snake.set_direction(Direction.DOWN)
        elif last_key == 452:
            snake.set_direction(Direction.LEFT)
        elif last_key == 450:
            snake.set_direction(Direction.UP)

        stdscr.refresh()

    # stdscr.addstr(0, 0, 'A')
    # x = 0
    # x2 = 0
    # count = 0
    # curses.curs_set(False)
    # while True:
    #     count = count + 1
    #     if count % 2 == 0:
    #         x = x + 1
    #     stdscr.clear()
    #     stdscr.addstr(0, x, 'A')
    #     x2 = x2 + 1
    #     stdscr.addstr(1, x2, 'B')
    #     stdscr.refresh()
    #     sleep(0.5)
    stdscr.clear()
    gameover = 'GAME OVER'
    if snake.state == StateOfSnake.HIT_BY_WALL:
        gameover = 'GAME OVER BY WALLS'
    elif snake.state == StateOfSnake.EATEN_BY_ITSELF:
        gameover = 'YOU SHOULD EAT YOURSELF NOW'
    stdscr.addstr(settings.height // 2, settings.width // 2 - len(gameover) // 2, gameover, curses.color_pair(1))
    while True:
        if stdscr.getch() == 10:
            break


if __name__ == '__main__':
    global snake
    snake = Snake()
    snake.set_direction(Direction.DOWN)
    # apple = create_apple(snake, 20, 20)
    # for y in range(0 , 20):
    #     for x in range(0, 20):
    #         if x == apple[0] and y == apple[1]:
    #             print('Q', end = '')
    #         elif snake.is_head(x, y):
    #             print('0', end = '')
    #         elif snake.is_tail(x, y):
    #             print('.', end = '')
    #         elif snake.is_body(x, y):
    #             print('o', end = '')
    #         else:
    #             print(' ', end = '')
    #     print()
    # stdscr = curses.initscr()
    # begin_x = 0
    # begin_y = 0
    # weight_field = 20
    # height_field = 20
    # win = curses.newwin(weight_field, height_field, begin_y, begin_x)
    # win.getkey()
    # wrapper

    wrapper(main)
