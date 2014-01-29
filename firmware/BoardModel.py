import pieces, board, random, copy


gray = (100, 100, 100)

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

class BoardModel:

    class CollisionTypeEnum:
        wall = 0
        pieceSide = 0
        floor = 1
        pieceBelow = 2

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pieceBag = PieceBag()

        self.boardSquares = []

        for i in range(height):
            self.boardSquares.append([])
            for j in range(width):
                self.boardSquares[i].append(board.Square(i, j, gray))

        print self.boardSquares

        self.activePiece = False
        self.currentPiece = None
        self.pieceRow = 0
        self.pieceCol = 0

    def get_square(self, x, y):
        return self.boardSquares[y][x]

    def new_piece(self):
        if not self.pieceBag.remaining:
            self.pieceBag.refill_bag()
        self.currentPiece = pieces.get_piece(self.pieceBag.get_next_piece())
        self.activePiece = True
        self.pieceCol = 3
        self.pieceRow = 0

    def check_rotate(self):
        #makes a copy of self.currentPiece so that changing rotatedPiece doesn't mess up self.currentPiece
        rotatedPiece = copy.deepcopy(self.currentPiece)
        #rotates rotatedPiece so that we have a copy of what spaces self.currentPiece will rotate into
        rotatedPiece.blockArray = self.currentPiece.rotate()
        #returns True if a block from the rotate piece will rotate into an existing colored block below it
        for i in range(rotatedPiece.height):
            for j in range(rotatedPiece.width):
                if rotatedPiece.blockArray[i][j] and self.boardSquares[i + self.pieceRow][j + self.pieceCol].color != gray and not self.currentPiece.blockArray[i][j]:
                    return True
        #returns False if there are only gray squares below the rotating piece
        return False

    def rotate_piece(self):
        #checks if rotating the piece will cause it to overlap with an existing colored square
        #if rotation will cause an overlap, then the piece does not rotate
        if not self.check_rotate():
            self.clear_piece() #Try a different way to do this
            self.currentPiece.blockArray = self.currentPiece.rotate()
            self.draw_piece()
            

    def _will_collide(self, dx, dy):
        for i in range(self.currentPiece.height):
            for j in range(self.currentPiece.width):
                if self.currentPiece.blockArray[i][j]:
                    if i + dy < self.currentPiece.height and i + dy > -1 and j + dx < self.currentPiece.width and j + dx >= -1 and not self.currentPiece.blockArray[i + dy][j + dx]:
                        #print "i: " + str(i) + " j: " + str(j) + " dy: " + str(dy) + " dx: " + str(dx)
                        if j + self.pieceCol + dx < 0 or j + self.pieceCol + dx > self.width - 1:  #should be 'or', not 'and'?
                            return True, self.CollisionTypeEnum.wall
                        elif i + self.pieceRow + dy > self.height - 1:
                            return True, self.CollisionTypeEnum.floor
                        elif self.boardSquares[i + self.pieceRow + dy][j + self.pieceCol + dx].color != gray and dy == 1:
                            return True, self.CollisionTypeEnum.pieceBelow
                        elif self.boardSquares[i + self.pieceRow][j + self.pieceCol + dx].color != gray and abs(dx) == 1:
                            return True, self.CollisionTypeEnum.pieceSide
                    #These additional elif statements are used for the case in which there is a colored square on the edge
                    #piece's 3x3 or 4x4
                    elif i + dy == self.currentPiece.height and i + dy > -1:
                        if i + self.pieceRow + dy > self.height - 1:
                            return True, self.CollisionTypeEnum.floor
                        elif self.boardSquares[i + self.pieceRow + dy][j + self.pieceCol + dx].color != gray:
                            return True, self.CollisionTypeEnum.pieceBelow
                    # This elif statement checks for collisions on the leftmost and rightmost columns of blocks in a piece
                    elif j + dx == self.currentPiece.width or j + dx == -1:
                        if j + self.pieceCol + dx < 0 or j + self.pieceCol + dx > self.width - 1:  #should be 'or', not 'and'?
                            return True, self.CollisionTypeEnum.wall
                        elif self.boardSquares[i + self.pieceRow + dy][j + self.pieceCol + dx].color != gray:
                            return True, self.CollisionTypeEnum.pieceSide
                    
                        
        return False, None

    def act_on_piece(self, dx, dy):
        if self.activePiece:
            willCollide, collisionType = self._will_collide(dx, dy)
            if willCollide:
                if collisionType != self.CollisionTypeEnum.wall:
                    self.activePiece = False
                    lines=self.check_lines()
                    self.drop_lines(lines)
            else:
                self.clear_piece()
                self.pieceRow += dy
                self.pieceCol += dx
                self.draw_piece()


    def draw_piece(self):
        for i in range(self.currentPiece.height):
            for j in range(self.currentPiece.width):
                if self.currentPiece.blockArray[i][j]:
                    try:
                        self.boardSquares[i + self.pieceRow][j + self.pieceCol].set_color(self.currentPiece.color)
                    except IndexError:
                        print "X: " + str(j + self.pieceCol) + " Y: " + str(i + self.pieceRow)

    def clear_piece(self):
        for i in range(self.currentPiece.height):
            for j in range(self.currentPiece.width):
                if self.currentPiece.blockArray[i][j]:
                    self.boardSquares[i + self.pieceRow][j + self.pieceCol].set_color(gray)

    def check_lines(self):
        lines = []
        for i in range(self.height-1,0,-1):
            line = [i]
            colors = []
            for j in range(self.width):
                line.append(self.boardSquares[i][j])
                colors.append(self.boardSquares[i][j].color)
            if gray not in colors:
                lines.append(line)
            else:
                pass
            
        return lines

    def clear_line(self,line):
        for square in line[1:]:
            square.set_color(gray)

    def drop_lines(self,lines):
        for line in lines:
            self.clear_line(line)
            Row = line.pop(0) - 1
            if Row >= self.height - 1:
                pass
            else:
                for i in range(Row,0,-1):
                    for j in range(self.width):
                        self.boardSquares[i+1][j].set_color(self.boardSquares[i][j].color)
                        self.boardSquares[i][j].set_color(gray)
                    
            
            
            
                


