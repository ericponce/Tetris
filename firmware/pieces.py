import pygame

black = (0, 0, 0)
white = (255, 255, 255)
cyan = (0, 255, 255)
yellow = (255, 255, 0)
purple = (255, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
orange = (255, 125, 0)

class Pieces:
    def rotate(self):
        rotationArray=[]
        n=len(self.blockArray);
        for i in range(n):
            rotationArray.append([])
            for j in range(n):
                rotationArray[i].append(self.blockArray[n - 1 - j][i])
        self.height, self.width = self.width, self.height
        return rotationArray
        

class PieceI (Pieces):
    def __init__(self):
        self.height = 4
        self.width = 4
        self.color = cyan
        self.blockArray = [[False,False,False,False],
                         [True,True,True,True],
                         [False,False,False,False],
                         [False,False,False,False]]
    
            

class PieceJ (Pieces):
    def __init__(self):
        self.height=3
        self.width=3
        self.color=blue
        self.blockArray=[[True,False,False],
                         [True,True,True],
                         [False,False,False]]

class PieceL (Pieces):
    def __init__(self):
        self.height=3
        self.width=3
        self.color=orange
        self.blockArray=[[False,False,True],
                         [True,True,True],
                         [False,False,False]]

class PieceO (Pieces):
    def __init__(self):
        self.width=4
        self.height=3
        self.color=yellow
        self.blockArray=[[False,True,True,False],
                         [False,True,True,False],
                         [False,False,False,False]]

    def rotate(self):
        return self.blockArray

class PieceS (Pieces):
    def __init__(self):
        self.height=3
        self.width=3
        self.color=green
        self.blockArray=[[False,True,True],
                         [True,True,False],
                         [False,False,False]]

class PieceT (Pieces):
    def __init__(self):
        self.color=purple
        self.height=3
        self.width=3
        self.blockArray=[[False,True,False],
                         [True,True,True],
                         [False,False,False]]

class PieceZ (Pieces):
    def __init__(self):
        self.height=3
        self.width=3
        self.color=red
        self.blockArray=[[True,True,False],
                         [False,True,True],
                         [False,False,False]]

#Pieces put into tuple to be called by index number
PIECES = ('PieceJ', 'PieceI', 'PieceL', 'PieceO', 'PieceS', 'PieceT', 'PieceZ')

def get_piece(index):
    piece=eval(PIECES[index])()
    return piece

