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

    def rotate_right():
        rotationArray=self.blockArray[:]
        for i in range(len(rotationArray)):
            #turns rows 1 to 3 into coordinates -1 to 1
            y=i-2
            for j in range(len(rotationArray[i])):
                #turns cols 1 to 3 into coordinates -1 to 1
                x=j-2
                #rotates the point (x,y) to new point (a,b)
                a=y
                b=-x
                #stores 
                self.blockArray[b+2][a+2]=rotationArray[i][j]
        
    def rotate_left():
        rotationArray=self.blockArray[:]
        for i in range(len(rotationArray)):
            #turns rows 1 to 3 into coordinates -1 to 1
            y=i-2
            for j in range(len(rotationArray[i])):
                #turns cols 1 to 3 into coordinates -1 to 1
                x=j-2
                #rotates the point (x,y) to new point (a,b)
                a=-y
                b=x
                #stores 
                self.blockArray[b+2][a+2]=rotationArray[i][j]

    def draw_piece(x,y):
        

    def fall():
        pass

class PieceI (Pieces):
    def __init__(self):
        self.color=cyan
        self.blockArray=[[False,False,False,False],
                         [True,True,True,True],
                         [False,False,False,False],
                         [False,False,False,False]]

class PieceJ (Pieces):
    def __init__(self):
        self.color=blue
        self.blockArray=[[True,False,False],
                         [True,True,True],
                         [False,False,False]]

class PieceL (Pieces):
    def __init__(self):
        self.color=orange
        self.blockArray=[[False,False,True],
                         [True,True,True],
                         [False,False,False]]

class PieceO (Pieces):
    def __init__(self):
        self.color=yellow
        self.blockArray=[[False,True,True,False],
                         [False,True,True,False],
                         [False,False,False,False]]

class PieceS (Pieces):
    def __init__(self):
        self.color=green
        self.blockArray=[[False,True,True],
                         [True,True,False],
                         [False,False,False]]

class PieceT (Pieces):
    def __init__(self):
        self.color=purple
        self.blockArray=[[False,True,False],
                         [True,True,True],
                         [False,False,False]]

class PieceZ (Pieces):
    def __init__(self):
        self.color=red
        self.blockArray=[[True,True,False],
                         [False,True,True],
                         [False,False,False]]
   
