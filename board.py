import pygame, sys
import random

WIDTH = 25
HEIGHT = 25

black = (0, 0, 0)
gray = (100, 100, 100)
white = (255, 255, 255)
cyan = (0, 255, 255)
yellow = (255, 255, 0)
purple = (255, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
orange = (255, 125, 0)

colors = {"cyan":cyan,
            "yellow":yellow,
            "purple":purple,
            "green":green,
            "red":red,
            "blue":blue,
            "orange":orange}

def get_row_top_loc(rowNum, height = HEIGHT):
    return rowNum * height + 10
    
def get_col_left_loc(colNum, width = WIDTH):
    return colNum * width + 10

def update_text(screen, message, width = 10, messageNum = 1):
    textSize = 20
    font = pygame.font.Font(None, 20)
    textY = 0 + textSize * messageNum
    text = font.render(message, True, white, black)
    textRect = text.get_rect()
    textRect.x = (width + 1) * WIDTH + 10
    textRect.centery = textY
    screen.blit(text, textRect)

def new_board(width = 10, height = 22, speed = 1):
    pygame.init()

    window_size = [width * WIDTH + 200, height * HEIGHT + 20]
    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption("Tetris")

    board = Board(width, height)

    moveCount = 0

    clock = pygame.time.Clock()

    main_loop(screen, board, moveCount, clock, False, False, speed)

def draw_grid(screen, width, height):

    for i in range(width + 1):
        pygame.draw.line(screen, red, (i * WIDTH + 10, 10), (i * WIDTH + 10, HEIGHT * height + 10))
    for i in range(height + 1):
        pygame.draw.line(screen, red, (10, i * HEIGHT + 10), (WIDTH * width + 10, i * HEIGHT + 10))

def main_loop(screen, board, moveCount, clock, stop, pause, speed):
    board.squares.draw(screen)
    draw_grid(screen, board.width, board.height)
    pygame.display.flip()

    reset = False
    while stop == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = 1 - pause
        if stop == False and pause == False:
            board.squares.draw(screen)
            draw_grid(screen, board.width, board.height)

            update_text(screen, " Tetris ", board.width, 1)

            pygame.display.flip()
            clock.tick(10 * speed)

            list = random_list(board.width, board.height)
            for keys in list.keys():
                s = board.get_square(keys[1], keys[0])
                i = list[keys]
                k = colors.keys()[i]
                s.set_color(colors[k])
                
            board.squares.draw(screen)
            draw_grid(screen, board.width, board.height)
            pygame.display.flip()
            clock.tick(5 * speed)

    if reset:
        new_game()
    pygame.quit()

def random_list(width, height):
    list = {}
    for i in range(10):
        c = random.randint(0, width - 1)
        r = random.randint(0, height - 1)
        i = random.randint(0, len(colors.values()) - 1)
        list[(c, r)] = i
    return list


class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.rect.x = get_col_left_loc(col)
        self.rect.y = get_row_top_loc(row)

    def get_rect_from_square(self):
        return pygame.Rect(get_col_left_loc(self.col), get_rect_from_square(self.row), WIDTH, HEIGHT)

    def set_color(self, color):
        self.color = color;
        self.image.fill(self.color)

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.squares = pygame.sprite.RenderPlain()
        self.boardSquares = {}

        for i in range(width):
            for j in range(height):
                s = Square(j, i, gray)
                self.boardSquares[(j, i)] = s
                self.squares.add(s)

    def get_square(self, x, y):
        return self.boardSquares[(x, y)]

if __name__ == "__main__":
    new_board()
    time.sleep(10)
