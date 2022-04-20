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
    -equal spacing characters required
Make GUI using tkinter
Make into game can play via HTTP PUT and GET requests
Make both Deflexion, Khet, and Khet 2 variants
Make basic AI (IDEA: use __ge__, __le__, etc. methods for evaluation of pieces/board state)
Make error wrapper and handler class
Make Khet-specific error types
Log:
-03/01/2021//Set up classes and brief explanation for some. Added rules dump and goals. Started Gamepiece class.
-03/07/2021//Created PieceSide dataclass as the value for each gamepiece's side. Created debug interface to test classes.
-03/08/2021//Updated comments, docstrings, added them where possible, continuing gamepiece class development.
-02/20/2022//Replaced method for reflection of laser when it interacts with gamepiece (new-> ReflectMatrix)
'''
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from urllib.parse import ParseResultBytes

def rotate(self, cw: bool = True):
    '''
    Rotate gamepiece 1/4 turn (90°) clockwise or counterclockwise using a deque.
    Returns new body state.
    Big O: O(1)
    '''
    try: 
        new_matrix = deque(self.reflection.matrix)
        new_matrix.rotate(1) if cw is True else new_matrix.rotate(-1) 
        self.reflection = ReflectMatrix(new_matrix)
        return list(new_matrix) 
    except:
        print('Error in rotate function!')

def move(self, direction):
    '''
    Move gamepiece one space away (no diagonal).
    Returns new location.
    Big O: O(1)
    '''
    try:
        assert(direction in DIRECTIONS)
        self.location = [loc + offset for loc, offset in zip(self.location, MOVE_MATRIX(direction))]
        return self.location
    except:
        print('Error in move function!')
class Board:
    #10x8
    #holds state of board, including piece position, player piece count, tile type
    def __init__(self, rank = 8, file = 10):
        self._MAX_RANK = max(rank)
        self._MAX_FILE = max(file)
        self._board_state = dict()
        for rank in range(rank):
            for file in range(file):
                self._board_state[(rank, file)] = None

class Gamepiece(ABC):
    '''
    Abstract base dataclass for gamepieces. Stores player affiliation, movement 
    ruleset, and reflection data.
    '''
    @abstractmethod
    def __init__(self, player : str):
        self.player = player
        self._can_move = True
        self._can_rotate = True
        self._reflect_state = None
        pass

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def player(self):
        return self.player

    @property
    def can_move(self):
        return self._can_move
    
    @property
    def can_rotate(self):
        return self._can_rotate

    @property
    def reflect_state(self):
        return self._reflect_state

    @reflect_state.setter
    def reflect_state(self, state: list):
        assert(len(state)==4)
        self._reflect_state = state

    def __call__(self, rank: int, file: int) -> str:
        '''
        Object can be called while providing a location to store it internally within the Gamepiece.
        Will be useful in AI features.
        '''
        self.location = (rank, file)
        return f'Location: rank {rank}, file {file} stored in {self.name} data.'

    def __str__(self) -> str:
        return self.__class__.__name__

class Sphinx(Gamepiece):
    '''
    Gamepiece child class for Sphinx Gamepiece.
    Sphinx is stationary, and has limited rotation capabilities.
    '''
    class Laser:
        '''
        Class for laser operation.
        '''
        #Matrix to use in beam calculations: Direction : Sphinx Location, Offset to Next Beam Location
        LOCATION_DIRECTION_MATRIX = {
            'N':((7, 9), (-1, 0)),
            'E':((0, 0), (0,  1)),
            'S':((0, 0), (1,  0)),
            'W':((7, 9), (0, -1))
            }

        def __init__(self, direction):
            self._initial_direction = direction
        
        def beam(self, board_state : dict):
            '''
            Uses board_state and initial direction to generate laserbeam path on board.
            Returns location of hit gamepiece, or wall indication
            '''
            for rank in range()
            pass

    VALID_STATE = ('Block','Block','Block','Block') #Only valid reflect state for Sphinx
    VALID_FACES_FOR = {'Red': ('S','E'), 'Silver': ('N','W')}
    def __init__(self, player : str, face = None):
        '''
        Initialize gamepiece for Sphinx. Ignores location parameter.
        Sphinx placed based on faction.
        '''
        super.__init__(player)
        default_face = self.VALID_FACES_FOR[player][0] #default face for direction of laser
        self._face = face if face in self.VALID_FACES_FOR[player] else default_face
        self._laser = self.Laser(self._face)
        self._can_move = False
        self._reflect_state = self.VALID_STATE

    @property
    def laser(self):
        return self._laser

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
    def __init__(self):
        self.players = Player(), Player()
        self.board = Board()
        pass

'''
Debug Interface: uncomment if __name__ statement to activate debug interface
'''
def debug():
    test_gamepiece = Sphinx('Red',[7,7])
    print(f'Beam() return with Argument: \'Right\':\n     {test_gamepiece.beam("Top")}')
    print(f'Rotate() return with Argument: \'None (default=clockwise)\':\n     {test_gamepiece.rotate()}')
    print(f'Move() return with Argument: \'Down\':\n     {test_gamepiece.move("Down")}')

if __name__ == '__main__': 
    print()


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