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
-03/08/2021//Updated comments, docstrings, added them where possible, continuing gamepiece class development.
'''
from collections import deque
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from msilib.schema import Error
from tempfile import TemporaryFile

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

class Board:
    #10x8
    #holds state of board, including piece position, player piece count, tile type
    def __init__(self):
        pass

class Laser:
    '''
    Class for laser operation. Uses Doubly-Linked List to 'build' laser.
    '''
    def __init__(self):
        pass
    
    def __repr__(self):
        pass

class ReflectMatrix:
    '''
    Class for handling reflection of the laser for each gamepiece.\n
    init_matrix, list of reflection values for each side of the game piece \n
        valid values: -1, 0, 1 \n
        value at each index in array corresponds with direction laser will reflect to on opposite axis \n
        if 0, no reflection \n
        format: [NORTH, EAST, SOUTH, WEST] \n
        example: [-1,0,0,1] would mean laser reflects north when from west, and west from north \n
    '''
    # attributes declaration
    def __init__(self, init_matrix):
        if len(init_matrix) is not 4:   
            raise ValueError('Invalid matrix.')
        for i in range(4):
            if type(init_matrix[i]) is not int:
                raise ValueError('Invalid matrix.')
            if init_matrix[i] > 1 or init_matrix[i] < -1:
                raise ValueError('Invalid matrix.')
        self._matrix = init_matrix

    def reflect(self, side):
        if self.matrix[side] is not 0:
            return (self.matrix[side], 0) if side % 2 is 0 else (0, self.matrix[side], 0)
        else: return None

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, new_matrix : list):
        if len(list) is not 4:
            raise ValueError('Invalid matrix.')
        self._matrix = new_matrix
        
            
        


# @dataclass
# class ReflectMatrix:
#     '''
#     Data class storing properties of a given gamepiece's side.\n
#     '''
#     def __
#     reflects: bool = field(default=False)
#     def __post_init__(self):

class Gamepiece(ABC):
    '''
    Abstract Base Class for Khet gamepieces. Holds gamepiece's body, board location, if its in play or not, and has methods for movement/rotation/deletion
    TODO: make __str__ and __repr__ functions for each gamepiece (make abstract method in base class) to return string for full characteristics dump, __repr__ for Board display
    '''
    
    @abstractmethod
    def __init__(self, location: list, faction):
        '''
        Abstract method for initializing gamepiece
        Big O: O(1)
        Gamepiece properties:
        Location: location (X,Y) (TODO: may need to be moved to Board?)
        Type: name of gamepiece type (ex. Scarab)
        Faction: Imhotep (Silver) or Osiris (Red)
        Reflection Matrix: matrix for when laser hits gamepiece
        is_alive: Boolean for status
        '''
        try:
            self.location = location
            self.faction = faction
            self._is_alive = True
            self._type = None
            self._reflection = None
            pass
        except:
            print(f'Error in initialization of gamepiece.')
            pass

    @property
    def name(self):
        '''
        Property returning name of Gamepiece using built-in class/name methods
        Big O: O(1)
        '''
        return self.__class__.__name__

    @property
    def reflection(self):
        return self._reflection
    
    @reflection.setter
    def reflection(self, matrix: list):
        self.reflection = ReflectMatrix(matrix)
    # def beam(self, side: PieceSide):
    #     '''
    #     Simulates laser hitting gamepiece's side.
    #     Returns next laser location if side is reflective, else returns False
    #     Big O: O(1)
    #     '''
    #     try:
    #         if self.body[side]: #if side isn't empty (non-initialized),
    #             if self.body[side].reflects: #if it is reflective,
    #                 return self.body[side].reflects #return direction of next laser location
    #         return False #else return false
    #     except:
    #         print('Error in beam function!')

    def rotate(self, cw: bool = True):
        '''
        Rotate gamepiece 1/4 turn (90°) clockwise or counterclockwise using a deque.
        Returns new body state.
        Big O: O(1)
        '''
        try: 
            old_matrix = deque(self._reflection) #store old state's values in deque
            old_body.rotate(1) if cw is True else old_body.rotate(-1) #shift values by 1 based on clockwise param
            self.body = dict(zip(self.body.keys(), old_body)) #new body pairs old key with shifted value
            return self.body #returns new body
        except:
            print('Error in rotate function!')
    
    def move(self, direction: str):
        '''
        Move gamepiece one space away (no diagonal).
        Returns new location.
        Big O: O(1)
        '''
        try:
            i = self._DIRECTIONS.index(direction) #get index for direction in _DIRECTIONS
            if i == 0 or i == 1: #if move up or down
                self.location[1] = self.location[1] + 1 if i is 0 else self.location[1] - 1 #set new y position based on direction
            elif i == 2 or i == 3: #else if move left or right
                self.location[0] = self.location[0] + 1 if i is 2 else self.location[0] - 1 #set new x position based on direction
            else: #else invalid movement, return None (keep current location)
                return None
            return self.location
        except:
            print('Error in move function!')

    def to_Duat(self):
        '''
        Activate gamepiece death (to Duat, Egyptian underworld)
        '''
        self.isAlive = False #set alive status to false
        self.location = None #set location to none

class Sphinx(Gamepiece):
    '''
    Gamepiece child class for Sphinx Gamepiece.
    Sphinx is stationary, and has limited rotation capabilities.
    '''
    default_location = dict({'Red': [9,0], 'Black': [0,7]}) #default locations for each player's sphinx

    def __init__(self, *location, faction='Red'):
        '''
        Initialize gamepiece for Sphinx. Ignores location parameter, but doesn't throw error.
        Sphinx placed based on faction.
        '''
        try:
            if len(location) != 0: #if location isn't empty
                print(f'{location} ignored. Sphinx placed based on faction.') #notify users
            super().__init__(self.default_location[faction], faction) #run gamepiece class init with location and faction
            for side in self._SIDES: #for each side of gamepiece
                self.body[side] = PieceSide() #set to nonreflective
            if self.faction == 'Red': #if faction is red
                self.body['Top'] = Laser() #face up
            else: self.body['Bottom'] = Laser() #else face down
        except:
            print('Error in Sphinx initialization!')

    
    def move(self, *direction):
        '''
        Overwrites Gamepiece move method to indicate Sphinxes can't move.
        '''
        print(f'Can\'t move {direction}; Reason: {self.name} gamepieces can\'t move.')

    def rotate(self):
        '''
        Overwritten rotate class that restricts movement of Sphinx to never aim laser at board edge.
        '''
        if isinstance(self.body['Top'], Laser) or isinstance(self.body['Bottom'], Laser): #if laser is facing up or down
            super().rotate(False) #call Gamepiece method for counterclockwise rotation
        else: super().rotate(True) #else call for clockwise rotation
        for side in self._SIDES: #for each side in lookup list
            if isinstance(self.body[side], Laser): #if side has laser
                return self.body[side] #return side with laser on it
    
    def to_Duat(self):
        print('Sphinxes never die.')

class Pharaoh(Gamepiece):
    def __init__(self):
        pass

class Scarab(Gamepiece):
    def __init__(self):
        pass

class Pyramid(Gamepiece):
    def __init__(self):
        pass

class Obelisk(Gamepiece):
    def __init__(self):
        pass

class Anubis(Gamepiece):
    def __init__(self):
        pass

class Gamemaster():
    # rulemaster, checks for wins
    def __init__(self):
        pass

class Player():
    # player of game (requires 2)
    def __init__(self):
        pass

class Curator():
    # 'plays' game, asking players for input, displaying board, moves pieces, manages turns and time, checks with gamemaster for rules
    def __init__(pass):
        pass

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
