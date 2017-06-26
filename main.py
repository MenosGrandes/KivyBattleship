import kivy
kivy.require('1.10.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from random import randint
from termcolor import colored

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


class Cell():
    def __init__(self,pos):
        self.pos=pos
        self.status=CELL_STATUS.NO_SHIP
        self.ship=None
        self.nighbours = []

    def setShip(self,ship):
        self.ship=ship
        self.setStatus(CELL_STATUS.SHIP)

    def setStatus(self,status):
            self.status=status
    def __str__(self):
        return self.pos.x
    def __repr__(self):
        return str(self.pos.x)+':'+str(self.pos.y)

    def removeNeight(self):
        for cell in self.nighbours:
            cell.setStatus(CELL_STATUS.NO_SHIP)

class Board:
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.cells=[[Cell(Position(j,i)) for j in range(self.width)] for i in range(self.height)]

    def setShipsRandom(self, listOfShips):
        counter=0
        for ship in listOfShips:
            shipPlaced = False
            while shipPlaced is False:
                prime_x=randint(0,self.width-1)
                prime_y=randint(0,self.height-1)
                currentCell=self.cells[prime_x][prime_y]

                direction = 1  # randint(0,3)

                if direction is DIRECTION.UP and prime_x-(ship.lives-1) < 0:
                    continue

                elif direction is DIRECTION.DOWN and prime_x+(ship.lives-1) >= self.width:
                    continue

                elif direction is DIRECTION.LEFT and prime_y-(ship.lives-1) < 0:
                    continue

                elif direction is DIRECTION.RIGHT and prime_y + (ship.lives - 1) >= self.height:
                    continue



                if currentCell.status is CELL_STATUS.NEAR_SHIP or CELL_STATUS.SHIP:
                    continue

                isOccupied = False
                for lives in range(ship.lives):
                    if direction is DIRECTION.DOWN:
                        if self.cells[prime_x + lives][prime_y].status is CELL_STATUS.NEAR_SHIP or \
                                        self.cells[prime_x + lives][prime_y].status is CELL_STATUS.SHIP:
                           isOccupied=True
                           break
                    elif direction is DIRECTION.UP:
                        if self.cells[prime_x - lives][prime_y].status is CELL_STATUS.NEAR_SHIP or \
                                        self.cells[prime_x - lives][prime_y].status is CELL_STATUS.SHIP:
                           isOccupied=True
                           break
                    elif direction is DIRECTION.LEFT:
                        if self.cells[prime_x][prime_y - lives].status is CELL_STATUS.NEAR_SHIP or self.cells[prime_x][
                                    prime_y - lives].status is CELL_STATUS.SHIP:
                           isOccupied=True
                           break
                    elif direction is DIRECTION.RIGHT:
                        if self.cells[prime_x][prime_y + lives].status is CELL_STATUS.NEAR_SHIP or self.cells[prime_x][
                                    prime_y + lives].status is CELL_STATUS.SHIP:
                            isOccupied=True
                            break

                if isOccupied == True:
                    continue

                for lives in range(ship.lives):
                    if direction is DIRECTION.DOWN:
                        if prime_y+1 < self.width:
                            self.cells[prime_x][prime_y+1].setStatus(CELL_STATUS.NEAR_SHIP)
                            currentCell.nighbours.append(self.cells[prime_x][prime_y + 1]);
                            if prime_x+1 < self.height:
                                self.cells[prime_x+1][prime_y+1].setStatus(CELL_STATUS.NEAR_SHIP)
                                currentCell.nighbours.append(self.cells[prime_x + 1][prime_y + 1]);
                            if prime_x!=0:
                                self.cells[prime_x-1][prime_y+1].setStatus(CELL_STATUS.NEAR_SHIP)
                                currentCell.nighbours.append(self.cells[prime_x - 1][prime_y + 1]);
                        if prime_y >= 1 :
                            if prime_x+1 < self.height:
                                self.cells[prime_x+1][prime_y-1].setStatus(CELL_STATUS.NEAR_SHIP)
                                currentCell.nighbours.append(self.cells[prime_x + 1][prime_y - 1]);
                            if prime_x !=0:
                                self.cells[prime_x-1][prime_y-1].setStatus(CELL_STATUS.NEAR_SHIP)
                                currentCell.nighbours.append(self.cells[prime_x - 1][prime_y - 1]);

                            self.cells[prime_x][prime_y-1].setStatus(CELL_STATUS.NEAR_SHIP)
                            currentCell.nighbours.append(self.cells[prime_x][prime_y - 1]);

                        if prime_x+1 != self.height or prime_x == 0:
                            self.cells[prime_x+1][prime_y].setStatus(CELL_STATUS.NEAR_SHIP)
                            currentCell.nighbours.append(self.cells[prime_x + 1][prime_y]);
                        if self.cells[prime_x-1][prime_y].status is not CELL_STATUS.SHIP and prime_x != 0:
                            self.cells[prime_x-1][prime_y].setStatus(CELL_STATUS.NEAR_SHIP)
                            currentCell.nighbours.append(self.cells[prime_x - 1][prime_y]);

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
                        if (prime_y + 1) < self.width and self.cells[prime_x][
                                    prime_y + 1].status is not CELL_STATUS.SHIP:
                            self.cells[prime_x][prime_y+1].setStatus(CELL_STATUS.NEAR_SHIP)

                        self.cells[prime_x][prime_y].setShip(ship)
                        prime_y-=1
                    elif direction is DIRECTION.RIGHT:
                        if prime_x > 0:
                            self.cells[prime_x - 1][prime_y].setStatus(CELL_STATUS.NEAR_SHIP)
                            if prime_y > 0:
                                self.cells[prime_x - 1][prime_y - 1].setStatus(CELL_STATUS.NEAR_SHIP)
                            if prime_y + 1 < self.width:
                                self.cells[prime_x - 1][prime_y + 1].setStatus(CELL_STATUS.NEAR_SHIP)
                        if prime_x + 1 < self.height:
                            self.cells[prime_x + 1][prime_y].setStatus(CELL_STATUS.NEAR_SHIP)
                            if prime_y + 1 < self.width:
                                self.cells[prime_x + 1][prime_y + 1].setStatus(CELL_STATUS.NEAR_SHIP)
                            if prime_y >= 1:
                                self.cells[prime_x + 1][prime_y - 1].setStatus(CELL_STATUS.NEAR_SHIP)

                        if prime_y + 1 < self.width:
                            self.cells[prime_x][prime_y + 1].setStatus(CELL_STATUS.NEAR_SHIP)
                        if (prime_y) > 0 and self.cells[prime_x][prime_y - 1].status is not CELL_STATUS.SHIP:
                            self.cells[prime_x][prime_y-1].setStatus(CELL_STATUS.NEAR_SHIP)

                        self.cells[prime_x][prime_y].setShip(ship)
                        prime_y+=1

                shipPlaced=True
                counter+= 1
                print "ShipPlaced" + str(counter) + "at " + str(prime_x) + ":" + str(prime_y)

    def move(self, pos):
        ship = self.cells[pos.x][pos.y].ship
        if ship is not None:
            ship.lives -= 1
            print ship
            print "TRAFIONY lives" + str(ship.lives)
            self.cells[pos.x][pos.y].setStatus(CELL_STATUS.NO_SHIP)
            if ship.lives <= 0:
                print "ZABITY"
                self.cells[pos.x][pos.y].removeNeight()
                print ship
                return True

        return False
    def printBoard(self):
        for x in range(self.width):
            for y in range(self.height):
                option = printCellStatus(self.cells[x][y].status)
                if option is 'x':
                    print colored('x', 'red'),
                elif option is '@':
                    print colored('@', 'green'),
                else:
                    print colored('n', 'grey'),
            print " "






class MyApp(App):

    def build(self):
        return Label(text='Hello world')


if __name__ == '__main__':
    b=Board(10, 10)
    b.setShipsRandom([Ship(1), Ship(2), Ship(3)])
    b.printBoard()
    print " "
    dead = False
    while dead is False:
        dead = b.move(Position(randint(0, 9), randint(0, 9)))
    b.printBoard()


    #MyApp().run()
