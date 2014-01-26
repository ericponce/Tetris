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
    def update_dimensions(self):
        height=0
        width=0
        for i in range(len(self.blockArray)):
            if True in self.blockArray[i]:
                height+=1
        for i in range(len(self.blockArray)):
            x=sum(self.blockArray[i])
            if x>width:
                width=x
        self.height,self.width=height,width
            
    def rotate(self):
        rotationArray=[]
        for i in range(len(self.blockArray)):
            rotationArray.append([])
        for i in range(len(self.blockArray)):
            for j in range(len(self.blockArray[i])):
                rotationArray[i].append(self.blockArray[len(self.blockArray)-1-j][i])
        self.height, self.width = self.width, self.height
        return rotationArray
        

class PieceI (Pieces):
    def __init__(self):
        self.height=1
        self.width=4
        self.color=cyan
        self.blockArray=[[False,False,False,False],
                         [True,True,True,True],
                         [False,False,False,False],
                         [False,False,False,False]]
    
            

class PieceJ (Pieces):
    def __init__(self):
        self.height=2
        self.width=3
        self.color=blue
        self.blockArray=[[True,False,False],
                         [True,True,True],
                         [False,False,False]]

class PieceL (Pieces):
    def __init__(self):
        self.height=2
        self.width=3
        self.color=orange
        self.blockArray=[[False,False,True],
                         [True,True,True],
                         [False,False,False]]

class PieceO (Pieces):
    def __init__(self):
        self.width=2
        self.height=2
        self.color=yellow
        self.blockArray=[[False,True,True,False],
                         [False,True,True,False],
                         [False,False,False,False]]

    def rotate(self):
        return self.blockArray

class PieceS (Pieces):
    def __init__(self):
        self.height=2
        self.width=3
        self.color=green
        self.blockArray=[[False,True,True],
                         [True,True,False],
                         [False,False,False]]

class PieceT (Pieces):
    def __init__(self):
        self.color=purple
        self.height=2
        self.width=3
        self.blockArray=[[False,True,False],
                         [True,True,True],
                         [False,False,False]]

class PieceZ (Pieces):
    def __init__(self):
        self.height=2
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

