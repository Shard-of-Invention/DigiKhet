'''                                                                     
88888888ba,    88               88  88      a8P   88                                
88      `"8b   ""               ""  88    ,88'    88                         ,d     
88        `8b                       88  ,88"      88                         88     
88         88  88   ,adPPYb,d8  88  88,d88'       88,dPPYba,    ,adPPYba,  MM88MMM  
88         88  88  a8"    `Y88  88  8888"88,      88P'    "8a  a8P_____88    88     
88         8P  88  8b       88  88  88P   Y8b     88       88  8PP"""""""    88     
88      .a8P   88  "8a,   ,d88  88  88     "88,   88       88  "8b,   ,aa    88,    
88888888Y"'    88   `"YbbdP"Y8  88  88       Y8b  88       88   `"Ybbd8"'    "Y888  
                    aa,    ,88                                                      
                     "YbbbdP"                                                       

A digital representation of one of my favorite childhood board games: Khet - the Laser Board Game!

By:  Blake McGill

Goals:
Make grid string generator that generates an X by Y size board with each cell being able to hold a single character
Make functional game that two players could play via text I/O.
Big O notation docstrings for all methods

Stretch Goals:
Make GUI
Make into game can play via HTTP PUT and GET requests
Make both Deflexion, Khet, and Khet 2 variants
Make basic AI (IDEA: use __ge__, __le__, etc. methods for evaluation of pieces/board)
Make error wrapper and handler class, named Maat (after Egyptian god of order)
Make Khet-specific error types

Sprints:
03/01/2021-03/14/2021: Set up all Gamepiece classes
03/15/2021-03/28/2021: Set up Board and Laser classes
03/29/2021-04/10/2021: Set up Gamemaster and Player classes
04/11/2021-04/25/2021: Set up Curator classes
Log:
-03/01/2021//Set up classes and brief explanation for some. Added rules dump and goals. Started Gamepiece class.
-03/07/2021//Created PieceSide dataclass as the value for each gamepiece's side. Created debug interface to test classes.

'''
from collections import deque
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass, field

class Board:
    #10x8
    #holds state of board, including piece position, player piece count, tile type
    def __init__():
        print('REPLACE')

class Laser:
    #calculates laser path, determine if hits gamepiece, use queue for laser (using beam offsets to draw beam)
    def __init__(self):
        print('REPLACE')
    
    def __repr__(self):
        return 'I am a LASER!'

@dataclass
class PieceSide:
    reflects: bool = field(default=False)
    def __post_init__(self, reflects=False, shared=None):
        if shared != None:
            if reflects == True:
                self.reflects = shared

class Gamepiece(ABC):
    '''
    Abstract Base Class for Khet gamepieces. Holds gamepiece's body, board location, if its in play or not, and has methods for movement/rotation/deletion
    TODO: make __str__ and __repr__ functions for each gamepiece (make abstract method in base class) to return string for full characteristics dump, __repr__ for Board display
    '''
    _SIDES = ['Top','Right','Bottom','Left'] # sides of gamepiece
    _DIRECTIONS = ['Up','Down','Left','Right'] # directions of movement

    #set body, alive status, and location [x,y] to initial values (location received as argument), abstract method
    @abstractmethod
    def __init__(self, location):
        self.body = {}
        self.isAlive = True
        if location:
            self.location = location
        else: raise ValueError
        for side in self._SIDES:
            self.body[side] = None
        pass

    @property
    def name(self):
        return self.__class__.__name__

    def beam(self, side: PieceSide):
        if self.body[side]:
            if self.body[side].reflects:
                return self.body[side].reflects
        return False

    def rotate(self, cw: bool = True):
        try: 
            old_body = deque(self.body.values())
            old_body.rotate(1) if cw == True else old_body.rotate(-1)
            self.body = dict(zip(self.body.keys(), old_body))
            return self.body
        except TypeError:
            print('Not valid rotation')
            return 
    
    def move(self, direction: str):
        previous_location = self.location
        try:
            i = self._DIRECTIONS.index(direction)
            if i == 0 or i == 1:
                self.location[1] = self.location[1] + 1 if i == 0 else self.location[1] - 1
            elif i == 2 or i == 3:
                self.location[0] = self.location[0] + 1 if i == 2 else self.location[0] - 1
            else:
                raise ValueError()
        except ValueError:
            self.location = previous_location
            return None
        return self.location

    def to_Duat(self):
        self.isAlive = False

class Pharaoh(Gamepiece):
    def __init__():
        print('REPLACE')

class Scarab(Gamepiece):
    def __init__():
        print('REPLACE')   
 
class Pyramid(Gamepiece):
    def __init__():
        print('REPLACE') 

class Obelisk(Gamepiece):
    def __init__():
        print('REPLACE')

class Anubis(Gamepiece):
    def __init__():
        print('REPLACE')

class Sphinx(Gamepiece):

    default_location = dict({'Red': [9,0], 'Black': [0,7]})

    def __init__(self, faction='Red', *location):
        if len(location) != 0:
            print(f'{location} ignored. Sphinx placed based on faction.')
        if (faction == 'Red' or faction == 'Silver'):
            super().__init__(self.default_location[faction])
            self.faction = faction
            for side in self._SIDES:
                self.body[side] = PieceSide()
            if self.faction == 'Red':
                self.body['Top'] = Laser()
            else: self.body['Bottom'] = Laser()
        else: raise ValueError

    
    def move(self, *direction):
        print(f'Can\'t move {direction}; Reason: {self.name} gamepieces can\'t move.')

    def rotate(self):
        if isinstance(self.body['Top'], Laser) or isinstance(self.body['Bottom'], Laser):
            super().rotate(False)
        else: super().rotate(True)
        for side in self._SIDES:
            if isinstance(self.body[side], Laser):
                return self.body[side]


class Gamemaster():
    # rulemaster, checks for wins
    def __init__(self):
        print('REPLACE')

class Player():
    # player of game (requires 2)
    def __init__():
        print('REPLACE')

class Curator():
    # 'plays' game, asking players for input, displaying board, moves pieces, manages turns and time, checks with gamemaster for rules
    def __init__():
        print('REPLACE') 

'''
Debug Interface: uncomment if __name__ statement to activate debug interface
'''
def debug():
    test_gamepiece = Sphinx('Red',[7,7])
    print(f'Beam() return with Argument: \'Right\':\n     {test_gamepiece.beam("Top")}')
    print(f'Rotate() return with Argument: \'None (default=clockwise)\':\n     {test_gamepiece.rotate()}')
    print(f'Move() return with Argument: \'Down\':\n     {test_gamepiece.move("Down")}')

if __name__ == '__main__': debug()










'''
    Rules Dump from wikipedia:
    Each player starts the game with 14 playing pieces (12 in Deflexion) on a 10x8 board, arranged in one of several predefined configurations, and a laser. The board has some squares (right file, left corners) that are restricted to pieces of one side or the other, preventing the creation of impenetrable fortress positions. In the original game, the lasers were built into the gameboard; in the "Khet 2.0" version, the lasers are instead built into two extra Sphinx playing pieces, which can be rotated as a player's turn even though they cannot be moved from their starting positions. Scarab (formerly "Djed") and Pyramid pieces have mirrors (one on the Pyramid, and two on the Scarab) positioned such that when the laser beam strikes a reflective side, it reflects at a 90° angle. Players try to position pieces in a fashion that allows the laser beam to reflect into the opponent's Pharaoh, thus winning the game; however, they must also try to protect their own Pharaoh from being struck by the laser beam at the same time. On each turn, a player either moves a piece one square in any direction, or rotates a piece 90 degrees clockwise or counterclockwise. After moving, the player must fire his or her laser, and any piece of either color hit on a non-reflecting side is removed from play.

    The pieces in the game are:

    Pharaoh (1 of each color)
        The Pharaoh is the most important piece for each side. If hit with a laser, it is destroyed and its owner loses the game. Similar to a king in chess, the Pharaoh pieces are comparatively weak, and so are often not moved unless under duress.
    Scarab/Djed (2 of each color)
        Scarabs (formerly called Djeds) consist primarily of large, dual-sided mirrors. They reflect a laser coming in from any direction, and thus cannot be eliminated from the board. Also, unlike other pieces, Scarabs may move into an adjacent square even if it is already occupied, by switching places with the piece found there (whichever color it may be). Thus, they are the most powerful pieces on the board, but must be used with care, as a move that puts one side of the mirror in a favorable position may expose the player to attack using the opposite side of the same mirror.
    Pyramid (7 of each color)
        Pyramids have a single diagonal mirror, and form the primary mechanism for directing the path of the laser. They are vulnerable to a hit from two of the four sides, and must be defended lest the player lose their ability to build paths of any size.
    Obelisk (2 in Deflexion, 4 in Khet 1, not in Khet 2)
        Large pillars with no mirrored sides, these are vulnerable to attack from any direction, and therefore useful mostly as an emergency sacrifice to protect another piece (such as the Pharaoh). In Khet 1, each player starts the game with four obelisks each; a laser hit always removes an obelisk.
    Anubis (2 in Khet 2 only)
        Anubis replaced Obelisks in Khet 2.0; they have the advantage that, despite still being unmirrored, they are not affected by a laser strike on the front; they must be hit on the sides or rear in order to be eliminated.
    Sphinx (1 of each color)
        In Khet 2.0, the Sphinxes hold the lasers. They may not move (each player's is located at their closest right-hand corner) but may be rotated in place so as to fire down the rank instead of the file. A Sphinx is unaffected by laser fire, whether the opponent's or its own reflected back upon itself.

    Three opening setups are most commonly used: Classic, which is the standard starting configuration, and is the best setup for one's first time playing; Imhotep, which is a variation on the Classic setup that introduces new defensive possibilities; and Dynasty, which has a fairly even mix of offense and defense, and moves quickly. However, any configuration agreed upon by both players can be used. In Deflexion, half the pieces were gold, and half were silver. When the company changed the name to Khet, the gold pieces were changed to red. In Deflexion, gold always goes first, and in Khet, silver always goes first.
'''