from enum import Enum
import random
import curses
from curses import wrapper
from time import sleep
import time


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
        pass

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
        for x1, y1 in self.body[1 : -1]:
            if x == x1 and y == y1:
                return True
        return False



def create_apple(snake, hight, width):
    y = random.randint(0, hight)
    x = random.randint(0, width)
    for x1, y1 in snake.body:
        if x1 == x and y1 == y:
            return create_apple(snake, hight, width)
    return (x, y)

def eat_apple(snake, apple):
    x = apple[0]
    y = apple[1]
    for x1, y1 in snake.body:
        if x == x1 and y == y1:
            apple = None



# дано: y=9, x=10; x1=10, y1=10


# snake = None


def main(stdscr):
    global snake
    curses.curs_set(False)
    curses.cbreak()
    stdscr.keypad(True)
    curses.noecho()
    stdscr.nodelay(True)
    prev_time = time.time()
    last_key = -1
    while True:
        curr_time = time.time()
        if curr_time - prev_time >= 0.5:
            snake.move()
            prev_time = curr_time
        stdscr.clear()
        stdscr.addstr(snake.body[0][1], snake.body[0][0], '0')
        stdscr.addstr(snake.body[-1][1], snake.body[-1][0], '.')
        for cell in snake.body[1:-1]:
            stdscr.addstr(cell[1], cell[0], 'o')


        key = stdscr.getch()
        if key != -1:
            last_key = key


        stdscr.addstr(0, 0, f'{last_key}')
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





    stdscr.getkey()




# создать яблоко -> съесть его -> создать новое яблоко





if __name__ == '__main__':

    global snake
    snake = Snake()
    snake.set_direction(Direction.DOWN)
    # apple = create_apple(snake, 20, 20)
    # for y in range(0 , 20):
    #    for x in range(0, 20):
    #        if x == apple[0] and y == apple[1]:
    #            print('Q', end = '')
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

