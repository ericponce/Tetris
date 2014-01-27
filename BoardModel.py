
gray = (100, 100, 100)

class BoardModel:
    def __init(self, width, height):
        self.width = width
        self.height = height
        self.PieceBag = PieceBag()

        self.boardSquares = []

        for i in range(height):
            self.boardSquares.append([])
            for j in range(width):
                s = Square
                self.boardSquares[i].append(Square(j, i, gray))

        self.currentPiece = None;
        self.pieceRow = 0;
        self.pieceCol = 0;

    def get_square(self, x, y):
        return self.boardSquares[y][x]

    def new_piece(self):
        if not self.pieceBag.remaining:
            self.pieceBag.refill_bag()
        currentPiece = pieces.get_piece(self.pieceBag.get_next_piece())

    def act_on_piece(self, dx, dy):
        if not _will_collide():
            self.pieceRow += dy
            self.pieceCol += dx

        
    #private, returns true if the piece will collide on the next move, edges count as collision
    def _will_collide(self, dx, dy):
        bool willNot = True
        for i in range(height):
            for j in range(width):
                willNot = willNot and (boardSquares[i + self.pieceRow + dy][j + self.pieceCol + dx].color == gray if self.currentPiece.blockArray[j][i])
        return not willNot


    def insert_piece(self):
        for i in range(len(piece.blockArray)):
            for j in range(len(piece.blockArray[0])):
                if self.currentPiece.blockArray[j][i]:
                    self.boardSquares[i + self.peiceRow][j + self.pieceCol].set_color(piece.color)

    def clear_piece(self):
        for i in range(len(piece.blockArray)):
            for j in range(len(piece.blockArray[0])):
                if self.currentPiece.blockArray[j][i]:
                    self.boardSquares[i + self.peiceRow][j + self.pieceCol].set_color(gray)

    def move_piece(self, piece, row, col, dx, dy):
        self.clear_piece(piece,row,col)
        row += dy
        col += dx
        if col <= 0:
            col = 0
        elif col >= self.width - piece.width:
            col = self.width - piece.width
        self.insert_piece(piece, row, col)
        return row, col