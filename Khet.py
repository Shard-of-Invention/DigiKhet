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

A digital version of one of my favorite childhood board games: Khet - the Laser Board Game!
By:  Blake McGill
Last Revision: 04/24/2022

Goals:
    Make into game played over tkinter GUI
    Make into game can play via HTTP PUT and GET requests
    Make both Deflexion, Khet, and Khet 2.0 variants
    Make basic AI (IDEA: use __ge__, __le__, etc. methods for evaluation of pieces/board state)
    Make error wrapper and handler class
    Make Khet-specific error types

Log:
    -03/01/2021//Set up classes and brief explanation for some. Added rules dump and goals. Started Gamepiece class.
    -03/07/2021//Created PieceSide dataclass as the value for each gamepiece's side. Created debug interface to test classes.
    -03/08/2021//Updated comments, docstrings, added them where possible, continuing gamepiece class development.
    -02/20/2022//Replaced method for reflection of laser when it interacts with gamepiece (new-> ReflectMatrix)
    -04/03/2022//Worked on outline for better OOP understanding (Located on GDrive: DigiKhet Program Design)
    -04/11/2022//Entire redesign based on outline
        -Gamepieces will only hold internal information for standard play (may hold external location info when AI implemented)
            -No more complex reflection matrices, simple cardinal direction dictionary
        -Board holds all Gamepiece information for pieces present
        -Laser attached to Sphinx class (attribute of Sphinx in Khet 2.0)
            -Will return location of wall or hit gamepiece
        -Player class simple dataclass containing name and color
        -Curator manages all turn-based states and actions
    -04/13/2022//Completed initial abstract base class for Gamepieces
    -04/16/2022//Completed Sphinx Gamepiece child class
    -04/17/2022//Started initial Laser class development, sidelining beam() method until Board development
    -04/21/2022//Started Board development
    -04/23/2022//Continued Board development, made Player dataclass
        - Completed init method (aside from loading default state file)
        - Completed structure for get_state method TODO: complete method
        - Completed set_state method
    -04/24/2022//Completed board development and Gamepieces development, continued Laser development
'''

from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Player:
    '''Retains player metadata'''
    name: str
    color: str

    def __str__(self):
        return self.name

class Gamepiece(ABC):
    '''
    Abstract base dataclass for gamepieces. Stores player affiliation, movement 
    ruleset, and reflection data.
    '''
    @abstractmethod
    def __init__(self, player : Player):
        self.player = player
        self._can_move = True
        self._can_rotate = True
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
    VALID_STATES = ('Block','Block','Block','Block') #Only valid reflect state for Sphinx
    VALID_FACES_FOR = {'Red': ('S','E'), 'Silver': ('N','W')}

    def __init__(self, player : Player, face = None):
        '''
        Initialize gamepiece for Sphinx. Ignores location parameter.
        Sphinx placed based on faction.
        '''
        super.__init__(player)
        default_face = self.VALID_FACES_FOR[player][0] #default face for direction of laser
        self._face = face if face in self.VALID_FACES_FOR[player] else default_face
        self._laser = Laser(self._face)
        self._can_move = False
        self._reflect_state = self.VALID_STATES

    @property
    def laser(self):
        return self._laser

class Pharaoh(Gamepiece):
    VALID_STATES = ('Hit','Hit','Hit','Hit')
    def __init__(self, player : Player):
        super.__init__(player)
        self._can_rotate = False
        self._reflect_state = self.VALID_STATES
        pass

class Scarab(Gamepiece):
    VALID_STATES = (('E','N','W','S'),('W','S','E','N'))
    def __init__(self, player : Player, state = None):
        super.__init__(player)
        if state:
            assert(state in self.VALID_STATES)
            self._reflect_state = state
        else:
            self._reflect_state = self.VALID_STATES[0]

class Pyramid(Gamepiece):
    VALID_STATES = (('E','N','Hit','Hit'),('Hit','S','E','Hit'),('Hit','Hit','W','S'),('W','Hit','Hit','N'))
    def __init__(self, player : Player, state = None):
        super.__init__(player)
        if state:
            assert(state in self.VALID_STATES)
            self._reflect_state = state
        else:
            self._reflect_state = self.VALID_STATES[0]

class Anubis(Gamepiece):
    VALID_STATES = (('Block','Hit','Hit','Hit'),('Hit','Block','Hit','Hit'),('Hit','Hit','Block','Hit'),('Hit','Hit','Hit','Block'))
    def __init__(self, player : Player, state = None):
        super.__init__(player)
        if state:
            assert(state in self.VALID_STATES)
            self._reflect_state = state
        else:
            self._reflect_state = self.VALID_STATES[0]

class Board:
    '''
        Game board. Initialized with number of ranks (rows) and files (columns).
        If exclusive_zones is True, maintains list of locations exclusive to each player
        If default_state_file is passed, loads 
    '''
    def __init__(self, ranks = 8, files = 10, exclusive_zones = True, default_state_file = None):
        self.MAX_RANK = max(range(ranks))
        self.MAX_FILE = max(range(files))
        self.board_state = dict()
        self.exc_zones = dict()
        if exclusive_zones:
            #exclusive files (on own side of board)
            home_files = {
                'Red'    : [(rank,0) for rank in range(ranks)],
                'Silver' : [(rank,self.MAX_FILE) for rank in range(ranks)]
            }
            #exclusive cells (on enemy side of board)
            away_cells = {
                'Red'    : [(self.MAX_RANK,self.MAX_FILE-1),(0,self.MAX_FILE-1)],
                'Silver' : [(0+1,self.MAX_RANK),(0+1,0)]
            }
            for player in home_files:
                if player in away_cells:
                    self.exc_zones[player] = home_files[player] + away_cells[player]
                else:
                    pass
        if default_state_file:
            self.board_state = default_state_file #TODO: load dict from csv
        for rank in range(ranks):
            for file in range(files):
                self.board_state[(rank, file)] = None

    def get_state(self, location = None, gamepiece_type = None, player = None):
        '''
        Get state of Board based on supplied parameters. If a location is supplied, return value will be Gamepiece or None.
        If location isn't supplied, return value will be list of tuples (rank,file) or None
        TODO: Find a way to make more elegant than if-elif-else (and sort more logically)
        '''
        gamepiece_match = self.board_state[location].name == gamepiece_type if location else False
        player_match = self.board_state[location].player == player if location else False
        if gamepiece_type and player and location:
            #return Gamepiece if same type, of player, and at location
            return self.board_state[location] if gamepiece_match and player_match else None
        elif gamepiece_type and location:
            #return Gamepiece if at type at location
            return self.board_state[location] if gamepiece_match else None
        elif player and location:
            #return Gamepiece if owned by player at location
            return self.board_state[location] if player_match else None
        elif location:
            #returns Gamepiece or None if location empty
            return self.board_state[location]
        elif gamepiece_type and player:
            #return locations of gamepieces owned by player
            return [loc for loc in self.board_state.keys() if (self.board_state[loc].player == player) and (self.board_state[loc].name == gamepiece_type)]
        elif gamepiece_type:
            #return locations of gamepieces of that type
            return [loc for loc in self.board_state.keys() if self.board_state[loc].name == gamepiece_type]
        elif player:
            #return locations of gamepieces owned by player
            return [loc for loc in self.board_state.keys() if self.board_state[loc].player == player]
        else:
            #returns board state
            return self.board_state

    def set_state(self, location : tuple, gamepiece : Gamepiece):
        self.board_state[location] = gamepiece

class Laser:
    '''
    Class for laser operation.
    '''
    #Matrix to use in beam calculations: Direction : Sphinx Location, Offset to Next Beam Location
    #implies standard board size, TODO: make agnostic of board size

    #(Sphinx direction: (Sphinx location, movement offset, end of rank/file in direction, opposite direction index)
    LOCATION_DIRECTION_MATRIX = {
        'N': ((7, 9), (-1, 0), (0, 10), 2),
        'E': ((0, 0), (0,  1), (0, 10), 3),
        'S': ((0, 0), (1,  0), (8, 0), 0),
        'W': ((7, 9), (0, -1), (8, 0), 1)
        }
    def __init__(self, direction):
        self._initial_direction = direction
        self._last_beam = None
    
    def beam(self, board : Board):
        '''
        Uses board_state and initial direction to generate laserbeam path on board.
        Returns location of hit gamepiece, or wall indication
        ''' 
        direction = self._initial_direction # set initial direction based on direction Sphinx is facing
        location = self.LOCATION_DIRECTION_MATRIX[direction][0] # set initial location to be Sphinx
        location_list = []
        #infinite loop until function returns value, repeats per direction
        while(True):
            movement = self.LOCATION_DIRECTION_MATRIX[direction][1] #store step direction
            wall = self.LOCATION_DIRECTION_MATRIX[direction][2] #store wall at end of rank/file in direction
            oppo_idx = self.LOCATION_DIRECTION_MATRIX[direction][3] #store side of gamepiece laser will hit
            while location is not wall: #loop until location hits wall
                location_list.append(location) #store list of locations laser hit
                loc_state = board.get_state(location) #fetch Gamepiece if at location
                if loc_state is Gamepiece: #if Gamepiece at location
                    state = loc_state.reflect_state[oppo_idx] #fetch gamepiece interaction result
                    if state in self.LOCATION_DIRECTION_MATRIX: #if a reflection direction
                        direction = state #make new direction
                        break #inner while loop
                    else: #else if hit or block
                        self._last_beam = location_list #store location list for beam
                        return location, state #return location and state
                else: 
                    location = tuple(sum(coords) for coords in zip(location,movement)) #go to next location
            if location is wall:
                self._last_beam = location_list #store location list for beam
                return wall #return wall location

def Curator():
    #initialize Board with default state
    #initialize Players
    #loop for turn while win state is false
        #requests player action
            #click gamepiece on GUI, select action (Move/Rotate), select subaction (direction of movement or rotation)
        #validate then perform action
            #update GUI
        #wait for Player to press beam on GUI
            #update GUI
        #retrieve beam return (either wall location, or gamepiece location and state)
        #remove gamepiece if 'Hit'
        #check win state
    pass

def debug():
    '''
    Debug Interface: uncomment if __name__ statement to activate debug interface
    '''
    pass

if __name__ == '__main__': 
    debug()

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
