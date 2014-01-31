import pygame, sys
import random
import pieces, BoardModel

WIDTH = 25
HEIGHT = 25

try:
    infile = open('HighScore', 'r')
    BEST_SCORE = infile.read()
    if BEST_SCORE == '':
        BEST_SCORE = 0
    infile.close()
except:
    outfile = open('HighScore', 'w')
    outfile.close()
    BEST_SCORE = 0

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



# Used for positional data
def get_row_top_loc(rowNum, height = HEIGHT):
    return rowNum * height + 10
    
# Used for position data
def get_col_left_loc(colNum, width = WIDTH):
    return colNum * width + 10

# Print out a line of text on the right corner
def update_line(screen, message, width = 10, height = 1, messageNum = 1):
    textSize = 20
    font = pygame.font.Font(None, 20)
    textY = 10 + height + textSize * messageNum
    text = font.render(message, True, white, black)
    textRect = text.get_rect()
    textRect.x = (width + 1) * WIDTH + 10
    textRect.centery = textY
    screen.blit(text, textRect)

# Print out multiple lines of text
def update_text(screen, messages, width = 10, height = 1):
    for i in range(len(messages)):
        update_line(screen, messages[i], width, height, i + 1)

# Create new board and thereofre a new game
def new_board(width = 10, height = 22, speed = 0.4):
    pygame.init()

    window_size = [width * WIDTH + 200, height * HEIGHT + 20]
    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption("Tetris")

    pygame.mouse.set_visible(False)

    board = Board(width, height)

    moveCount = 0

    clock = pygame.time.Clock()

    main_loop(screen, board, moveCount, clock, False, False, speed)

# Draw grids for the board
def draw_grid(screen, width, height):

    for i in range(width + 1):
        pygame.draw.line(screen, red, (i * WIDTH + 10, 10), (i * WIDTH + 10, HEIGHT * height + 10))
    for i in range(height + 1):
        pygame.draw.line(screen, red, (10, i * HEIGHT + 10), (WIDTH * width + 10, i * HEIGHT + 10))

# Main logic and drawing loop
def main_loop(screen, board, moveCount, clock, stop, pause, speed, bestScore=BEST_SCORE):
    board.squares.draw(screen)
    draw_grid(screen, board.width, board.height)
    pygame.display.flip()
    q = QueueViewer(board.width, 120, 120);

    reset = False
    while stop == False:
        stop, pause, reset = event_check(board, stop, pause, reset)
        if stop == False and pause == False:

            if not board.boardModel.activePiece:
                board.boardModel.new_piece()
                q.set_next_piece(board.boardModel.nextPiece)
                q.draw(screen)

            stop, pause, reset = event_check(board, stop, pause, reset)

            #endGame will remain false until one or more of the top three rows contain a colored square(s)
            endGame = board.boardModel.act_on_piece(0, 1)

            board.squares.draw(screen)
            draw_grid(screen, board.width, board.height)

            #displays Game Over message and pauses game is endGame is true
            if endGame:
                update_text(screen, [" Tetris ", " LEFT/RIGHT to move ", " UP to rotate ", " Q to quit ", " Press 'R' to Try Again ", " Score: " + str(board.boardModel.score) + " ", " Best Score: " + str(bestScore) + " ", " GAME OVER "], board.width, 120)
                pause = True
            else:
                update_text(screen, [" Tetris ", " LEFT/RIGHT to move ", " UP to rotate ", " Q to quit ", " Press 'R' to Reset ", " Score: " + str(board.boardModel.score) + " ", " Best Score: " + str(bestScore) + " "], board.width, 120)
                pass
            
            pygame.display.flip()
            clock.tick(board.boardModel.score / 20.0 + 4)

        #creates new game when reset is true by making all squares on board gray, and then calling new_board() to start a new game
        if reset:
            board.boardModel.clear_board(board.height, board.width)
            new_board()
    if board.boardModel.score > int(bestScore):
        bestScore = board.boardModel.score
    outfile = open('HighScore', 'w')
    outfile.write(str(bestScore))
    outfile.close()
    pygame.quit()

# Check for keyboard events
def event_check(board, stop, pause, reset):
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
                elif event.key == pygame.K_r:
                    pause = False
                    reset = True
                elif event.key == pygame.K_UP:
                    board.boardModel.rotate_piece()
                elif event.key == pygame.K_RIGHT:
                    board.boardModel.act_on_piece(1, 0)
                elif event.key == pygame.K_LEFT:
                    board.boardModel.act_on_piece(-1, 0)
                elif event.key == pygame.K_DOWN:
                    board.boardModel.hard_drop()
                
    return stop, pause, reset

# Used for next piece display. A sprite containing a grid.
class QueueViewer(pygame.sprite.Sprite):
    def __init__(self, boardWidth, viewerWidth, viewerHeight):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([viewerWidth, viewerHeight])
        self.image.fill(blue)
        self.piece = None

        self.rect = self.image.get_rect()
        self.rect.x = get_col_left_loc(boardWidth + 1)
        self.rect.y = 10

        self.width = viewerWidth
        self.height = viewerHeight

        self.queueSprite = pygame.sprite.RenderPlain()
        self.queueSprite.add(self)

    def draw(self, screen):
        self.queueSprite.draw(screen)
        self.squares.draw(screen)
        self.__draw_outline(screen)

    def set_next_piece(self, piece):
        self.piece = piece
        self.__create_grid()

    def __draw_outline(self, screen):
        pygame.draw.line(screen, gray, (self.rect.x, self.rect.y), (self.rect.x + self.width, self.rect.y)) #Top
        pygame.draw.line(screen, gray, (self.rect.x, self.rect.y + self.width), (self.rect.x + self.width, self.rect.y + self.height)) #Bottom
        pygame.draw.line(screen, gray, (self.rect.x, self.rect.y), (self.rect.x, self.rect.y + self.height)) #Left
        pygame.draw.line(screen, gray, (self.rect.x + self.width, self.rect.y), (self.rect.x + self.width, self.rect.y + self.height)) #Right

    def __create_grid(self):
        self.squares = pygame.sprite.RenderPlain()
        if (self.piece.height == self.piece.width):
            for i in range(self.piece.height):
                for j in range(self.piece.width):
                    s = Square(i, j, (self.piece.color if self.piece.blockArray[i][j] else black), self.width/self.piece.width, self.height/self.piece.height)
                    s.rect.x = self.rect.x + self.width/self.piece.width * j;
                    s.rect.y = self.rect.y + self.height/self.piece.height * i;
                    self.squares.add(s)
        else:
            size = (self.piece.width if self.piece.width > self.piece.height else self.piece.height)

            for i in range(size):
                for j in range(size):
                    s = Square(i, j, (self.piece.color if i < self.piece.height and j < self.piece.width and self.piece.blockArray[i][j] else black), self.width/self.piece.width, self.height/self.piece.height)
                    s.rect.x = self.rect.x + self.width/self.piece.width * j;
                    s.rect.y = self.rect.y + self.height/self.piece.height * i;
                    self.squares.add(s)

# Used for display block type objects
class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, color, width = WIDTH, height = HEIGHT):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.color = color
        self.rect = self.image.get_rect()

        self.rect.x = get_col_left_loc(col)
        self.rect.y = get_row_top_loc(row)

    def get_rect_from_square(self):
        return pygame.Rect(get_col_left_loc(self.col), get_row_top_loc(self.row), self.width, self.height)

    def set_color(self, color):
        self.color = color;
        self.image.fill(self.color)
    def is_empty(self):
        return self.color == gray

# Stores square sprites and handles communication to BoardModel. Controller in MVC
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

        
# Main
if __name__ == "__main__":
    new_board()





