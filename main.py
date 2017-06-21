import kivy
kivy.require('1.10.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from random import randint

def printCellStatus(status):
    return{
        CELL_STATUS.SHIP  : 'x',
        CELL_STATUS.NO_SHIP  : 'n',
        CELL_STATUS.NEAR_SHIP: '@'
    }[status]


class CELL_STATUS:
    SHIP = 0
    NO_SHIP = 1
    NEAR_SHIP = 2

class DIRECTION:
    UP = 0
    DOWN= 1
    LEFT= 2
    RIGHT =3

class Position:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class Ship:
       def __init__(self, lives):
           self.lives=lives

class Cell:
    def __init__(self,pos):
        self.pos=pos
        self.status=CELL_STATUS.NO_SHIP
        self.ship=None

    def setShip(self,ship):
        self.ship=ship
        self.setStatus(CELL_STATUS.SHIP)

    def setStatus(self,status):
            self.status=status
    def __str__(self):
        return self.pos.x
    def __repr__(self):
        return str(self.pos.x)+':'+str(self.pos.y)


class Board:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.cells=[[Cell(Position(j,i)) for j in range(self.width)] for i in range(self.height)]

    def setShips(self,listOfShips):
        counter=0
        for ship in listOfShips:
            shipPlaced = False
            while shipPlaced is False:
                prime_x=randint(0,self.width-1)
                prime_y=randint(0,self.height-1)
                currentCell=self.cells[prime_x][prime_y]


                direction=randint(0,2)

                if direction is DIRECTION.UP and prime_x-(ship.lives-1) < 0:
                    continue

                elif direction is DIRECTION.DOWN and prime_x+(ship.lives-1) >= self.width:
                    continue

                elif direction is DIRECTION.LEFT and prime_y-(ship.lives-1) < 0:
                    continue

                #elif direction is DIRECTION.RIGHT and prime_y-ship.lives > self.height:



                if currentCell.status is CELL_STATUS.NEAR_SHIP or CELL_STATUS.SHIP:
                    continue
                isOccupied = False
                for lives in range(ship.lives):
                    if direction is DIRECTION.DOWN:
                       if self.cells[prime_x+lives][prime_y].status is (CELL_STATUS.NEAR_SHIP or CELL_STATUS.SHIP):
                           isOccupied=True
                           break
                    elif direction is DIRECTION.UP:
                       if self.cells[ prime_x-lives][prime_y].status is (CELL_STATUS.NEAR_SHIP or CELL_STATUS.SHIP):
                           isOccupied=True
                           break
                    elif direction is DIRECTION.LEFT:
                       if self.cells[prime_x][prime_y-lives].status is (CELL_STATUS.NEAR_SHIP or CELL_STATUS.SHIP):
                           isOccupied=True
                           break
                    elif direction is DIRECTION.RIGHT:
                        if self.cells[prime_x][prime_y+lives].status is (CELL_STATUS.NEAR_SHIP or CELL_STATUS.SHIP):
                            isOccupied=True
                            break

                if isOccupied == True:
                    continue

                for lives in range(ship.lives):
                    if direction is DIRECTION.DOWN:
                        if prime_y+1 < self.width:
                            self.cells[prime_x][prime_y+1].setStatus(CELL_STATUS.NEAR_SHIP)
                            if prime_x+1 < self.height:
                                self.cells[prime_x+1][prime_y+1].setStatus(CELL_STATUS.NEAR_SHIP)
                            if prime_x!=0:
                                self.cells[prime_x-1][prime_y+1].setStatus(CELL_STATUS.NEAR_SHIP)
                        if prime_y >= 1 :
                            if prime_x+1 < self.height:
                                self.cells[prime_x+1][prime_y-1].setStatus(CELL_STATUS.NEAR_SHIP)
                            if prime_x !=0:
                                self.cells[prime_x-1][prime_y-1].setStatus(CELL_STATUS.NEAR_SHIP)
                            self.cells[prime_x][prime_y-1].setStatus(CELL_STATUS.NEAR_SHIP)
                        if prime_x+1 != self.height or prime_x == 0:
                            self.cells[prime_x+1][prime_y].setStatus(CELL_STATUS.NEAR_SHIP)
                        if self.cells[prime_x-1][prime_y].status is not CELL_STATUS.SHIP and prime_x != 0:
                            self.cells[prime_x-1][prime_y].setStatus(CELL_STATUS.NEAR_SHIP)

                        self.cells[prime_x][prime_y].setShip(ship)
                        prime_x+=1
                    elif direction is DIRECTION.UP:
                        if prime_y+1 < self.width:
                            self.cells[prime_x][prime_y+1].setStatus(CELL_STATUS.NEAR_SHIP)
                            if prime_x+1 < self.height:
                                self.cells[prime_x+1][prime_y+1].setStatus(CELL_STATUS.NEAR_SHIP)
                            if prime_x!=0:
                                self.cells[prime_x-1][prime_y+1].setStatus(CELL_STATUS.NEAR_SHIP)
                        if prime_y >= 1 :
                            if prime_x+1 < self.height:
                                self.cells[prime_x+1][prime_y-1].setStatus(CELL_STATUS.NEAR_SHIP)
                            if prime_x !=0:
                                self.cells[prime_x-1][prime_y-1].setStatus(CELL_STATUS.NEAR_SHIP)
                            self.cells[prime_x][prime_y-1].setStatus(CELL_STATUS.NEAR_SHIP)
                        if prime_x != 0:
                            self.cells[prime_x-1][prime_y].setStatus(CELL_STATUS.NEAR_SHIP)

                        if prime_x+1!=self.height and self.cells[prime_x+1][prime_y].status is not CELL_STATUS.SHIP and prime_x != 0:
                            self.cells[prime_x+1][prime_y].setStatus(CELL_STATUS.NEAR_SHIP)

                        self.cells[prime_x][prime_y].setShip(ship)
                        prime_x-=1




                    elif direction is DIRECTION.LEFT:
                        if prime_x>0:
                            self.cells[prime_x-1][prime_y].setStatus(CELL_STATUS.NEAR_SHIP)
                            if prime_y>0:
                                self.cells[prime_x-1][prime_y-1].setStatus(CELL_STATUS.NEAR_SHIP)
                            if prime_y+1<self.width:
                                self.cells[prime_x-1][prime_y+1].setStatus(CELL_STATUS.NEAR_SHIP)
                        if prime_x+1<self.height:
                            self.cells[prime_x+1][prime_y].setStatus(CELL_STATUS.NEAR_SHIP)
                            if prime_y+1<self.width:
                                self.cells[prime_x+1][prime_y+1].setStatus(CELL_STATUS.NEAR_SHIP)
                            if prime_y>=1:
                                self.cells[prime_x+1][prime_y-1].setStatus(CELL_STATUS.NEAR_SHIP)

                        if prime_y!=0:
                            self.cells[prime_x][prime_y-1].setStatus(CELL_STATUS.NEAR_SHIP)
                        if prime_y>self.width and self.cells[prime_x][prime_y+1].status is not CELL_STATUS.SHIP:
                            self.cells[prime_x][prime_y+1].setStatus(CELL_STATUS.NEAR_SHIP)

                        self.cells[prime_x][prime_y].setShip(ship)
                        prime_y-=1
                    elif direction is DIRECTION.RIGHT:
                        self.cells[prime_x-1][prime_y].setStatus(CELL_STATUS.NEAR_SHIP)
                        self.cells[prime_x-1][prime_y-1].setStatus(CELL_STATUS.NEAR_SHIP)
                        self.cells[prime_x+1][prime_y+1].setStatus(CELL_STATUS.NEAR_SHIP)
                        self.cells[prime_x+1][prime_y-1].setStatus(CELL_STATUS.NEAR_SHIP)
                        self.cells[prime_x-1][prime_y+1].setStatus(CELL_STATUS.NEAR_SHIP)
                        self.cells[prime_x][prime_y+1].setStatus(CELL_STATUS.NEAR_SHIP)
                        self.cells[prime_x+1][prime_y].setStatus(CELL_STATUS.NEAR_SHIP)
                        if self.cells[prime_x][prime_y-1].status is not CELL_STATUS.SHIP:
                            self.cells[prime_x][prime_y-1].setStatus(CELL_STATUS.NEAR_SHIP)
                        self.cells[prime_x][prime_y].setShip(ship)
                        prime_y+=1

                shipPlaced=True
                counter+=1
                print "ShipPlaced"+str(counter)





    def printBoard(self):
        for x in range(self.width):
            for y in range(self.height):
                #print self.cells[x][y].pos.x,
                #print self.cells[x][y].pos.y,
                print printCellStatus(self.cells[x][y].status),
            print " "






class MyApp(App):

    def build(self):
        return Label(text='Hello world')


if __name__ == '__main__':
    b=Board(10,10)
    b.setShips([Ship(4),Ship(4),Ship(3),Ship(2)])
    b.printBoard()

    #MyApp().run()
