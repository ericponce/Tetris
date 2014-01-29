import pygame, sys
import random
import pieces, BoardModel

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

colors = (  cyan,
            yellow,
            purple,
            green,
            red,
            blue,
            orange)

def get_row_top_loc(rowNum, height = HEIGHT):
    return rowNum * height + 10
    
def get_col_left_loc(colNum, width = WIDTH):
    return colNum * width + 10

def update_line(screen, message, width = 10, messageNum = 1):
    textSize = 20
    font = pygame.font.Font(None, 20)
    textY = 0 + textSize * messageNum
    text = font.render(message, True, white, black)
    textRect = text.get_rect()
    textRect.x = (width + 1) * WIDTH + 10
    textRect.centery = textY
    screen.blit(text, textRect)

def update_text(screen, messages, width = 10):
    for i in range(len(messages)):
        update_line(screen, messages[i], width, i + 1)

def new_board(width = 10, height = 22, speed = 0.5):
    pygame.init()

    window_size = [width * WIDTH + 200, height * HEIGHT + 20]
    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption("Tetris")

    pygame.mouse.set_visible(False)

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
        if stop == False and pause == False:

            if not board.boardModel.activePiece:
                print "Getting new piece"
                board.boardModel.new_piece()

            stop,pause = event_check(board, stop, pause)

            board.boardModel.act_on_piece(0, 1)

            board.squares.draw(screen)
            draw_grid(screen, board.width, board.height)

            update_text(screen, [" Tetris ", " LEFT/RIGHT to move ", " UP to rotate ", "Q to quit"], board.width)

            pygame.display.flip()
            clock.tick(10 * speed)

    if reset:
        new_game()
    pygame.quit()

#made it a separate time so events can be checked more than once for fall
def event_check(board, stop, pause):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = 1 - pause
                elif event.key == pygame.K_q:
                    stop = True
                    pygame.quit()
                elif event.key == pygame.K_UP:
                    board.boardModel.rotate_piece()
                elif event.key == pygame.K_RIGHT:
                    board.boardModel.act_on_piece(1, 0)
                elif event.key == pygame.K_LEFT:
                    board.boardModel.act_on_piece(-1, 0)
    return stop, pause

def random_list(width, height):
    list = {}
    for i in range(10):
        c = random.randint(0, width - 1)
        r = random.randint(0, height - 1)
        i = random.randint(0, len(colors) - 1)
        list[(c, r)] = i
    return list

class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(color)
        self.color = color
        self.rect = self.image.get_rect()

        self.rect.x = get_col_left_loc(col)
        self.rect.y = get_row_top_loc(row)

    def get_rect_from_square(self):
        return pygame.Rect(get_col_left_loc(self.col), get_row_top_loc(self.row), WIDTH, HEIGHT)

    def set_color(self, color):
        self.color = color;
        self.image.fill(self.color)
    def is_empty(self):
        return self.color == gray

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.boardModel = BoardModel.BoardModel(width, height)

        self.squares = pygame.sprite.RenderPlain()

        for i in range(width):
            for j in range(height):
                self.squares.add(self.boardModel.get_square(i, j))

    def get_square(self, x, y):
        return self.boardModel.get_square(x, y)

    def update_sprites(self):
        self.squares = pygame.sprite.RenderPlain()

        for i in range(width):
            for j in range(height):
                self.squares.add(self.boardModel.get_square(i, j))

        

if __name__ == "__main__":
    new_board()





