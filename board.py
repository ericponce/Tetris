import pygame, sys
import random
import pieces

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
    piece_on_board=False

    reset = False
    while stop == False:
        if stop == False and pause == False:
            if piece_on_board:
                stop,pause,row,col,piece=event_check(board,piece,row,col,stop,pause)
            board.squares.draw(screen)
            draw_grid(screen, board.width, board.height)

            update_text(screen, " Tetris ", board.width, 1)
            update_text(screen, " Press q to quit", board.width, 2)

            pygame.display.flip()
            clock.tick(10 * speed)

            if piece_on_board:
                stop,pause,row,col,piece=event_check(board,piece,row,col,stop,pause)
            #falling pieces
            if piece_on_board:
                row,col=board.move_piece(piece,row,col,0,1)
                board.squares.draw(screen)
                draw_grid(screen, board.width, board.height)

            #Inserting piece into board
            if not piece_on_board:
                if len(board.pieceBag.bag)==0:
                    board.pieceBag.refill_bag()
                piece=board.retrieve_piece()
                row,col=0,3
                board.insert_piece(piece,row,col)
                piece_on_board=True
            
            #Eric's cool display#
            #list = random_list(board.width, board.height)
            #for key in list:
            #    s = board.get_square(key[1], key[0])
            #    i = list[key]
            #    s.set_color(colors[i])
            piece_on_board=board.check_piece(piece,row,col)

            stop,pause,row,col,piece=event_check(board,piece,row,col,stop,pause)
            board.squares.draw(screen)
            draw_grid(screen, board.width, board.height)
            pygame.display.flip()
            clock.tick(5 * speed)

    if reset:
        new_game()
    pygame.quit()

#made it a separate time so events can be checked more than once for fall
def event_check(board,piece,row,col,stop,pause):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop = True
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = 1 - pause
                elif event.key == pygame.K_q:
                    stop = True
                elif event.key == pygame.K_RIGHT:
                    row,col=board.move_piece(piece,row,col,1,0)
                elif event.key == pygame.K_LEFT:
                    row,col=board.move_piece(piece,row,col,-1,0)
                elif event.key == pygame.K_a:
                    """board.clear_piece(piece,row,col)
                    piece.blockArray=piece.rotate_left()
                    board.insert_piece(piece,row,col)"""
                    pass
                elif event.key == pygame.K_UP:
                    board.clear_piece(piece,row,col)
                    piece.blockArray=piece.rotate()
                    piece.update_dimensions()
                    board.insert_piece(piece,row,col)
    return stop, pause, row, col, piece

def random_list(width, height):
    list = {}
    for i in range(10):
        c = random.randint(0, width - 1)
        r = random.randint(0, height - 1)
        i = random.randint(0, len(colors) - 1)
        list[(c, r)] = i
    return list

class PieceBag:
    def __init__(self):
        self.bag=[]
        self.refill_bag()

    def refill_bag(self):
        for x in range(7):
            self.bag.append(random.randint(0, 6))

        self.remaining = 7
        pass

    def get_next_piece(self):
        self.remaining -= 1;
        nextPiece=self.bag.pop(0)
        return nextPiece

    def remaining_pieces(self):
        return self.remaining


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
        self.pieceBag=PieceBag()

        self.squares = pygame.sprite.RenderPlain()
        self.boardSquares = {}

        for i in range(width):
            for j in range(height):
                s = Square(j, i, gray)
                self.boardSquares[(j, i)] = s
                self.squares.add(s)

    def retrieve_piece(self):
        piece=pieces.get_piece(self.pieceBag.get_next_piece())
        return piece

    def get_square(self, x, y):
        return self.boardSquares[(x, y)]

    def insert_piece(self, piece, row, col):
        j=row
        for row_position in piece.blockArray:
            i=col
            for col_position in row_position:
                if col_position==True:
                    s=self.boardSquares[(j,i)]
                    s.set_color(piece.color)
                else:
                    pass
                i+=1
            j+=1

    def clear_piece(self,piece,row,col):
        j=row
        for row_position in piece.blockArray:
            i=col
            for col_position in row_position:
                if col_position==True:
                    s=self.boardSquares[(j,i)]
                    s.set_color(gray)
                else:
                    pass
                i+=1
            j+=1

    def move_piece(self, piece, row, col, dx, dy):
        self.clear_piece(piece,row,col)
        row+=dy
        col+=dx
        if col<=0:
            col=0
        elif col>=self.width-piece.width:
            col=self.width-piece.width
        self.insert_piece(piece,row,col)
        print row,col
        return row,col

    # Checks to see if piece has hit bottom of the board 
    def check_piece(self, piece, row, col):
        if row==self.height-piece.height:
            return False
        else:
            return True

if __name__ == "__main__":
    new_board()
