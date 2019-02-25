from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        output = []  #template, tuples not changeable

        askpeg1 = parse_input("fact: (on ?X peg1)")
        askpeg2 = parse_input("fact: (on ?X peg2)")
        askpeg3 = parse_input("fact: (on ?X peg3)")

        selfask = [self.kb.kb_ask(askpeg1), self.kb.kb_ask(askpeg2),self.kb.kb_ask(askpeg3)]

        for answer in selfask:
            disks = []
            if answer:
                disks = []
                for a in answer:
                    disks.append(int(a['?X'][-1]))
                disks.sort()
            output.append(tuple(disks))
        return tuple(output)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        present_state = self.getGameState()
        mov_state = str(movable_statement).split(" ")
        disk = str(movable_statement.terms[0])
        old_peg = str(movable_statement.terms[1])
        new_peg = str(movable_statement.terms[2])

        #retract disk on old peg
        self.kb.kb_retract(parse_input("fact: (on %s %s)" % (disk, old_peg)))

        #retract disk on top of old peg
        self.kb.kb_retract(parse_input("fact: (top %s %s)" % (disk, old_peg)))

        #if old peg is now empty add that fact
        if len(present_state[int(mov_state[2][-1])-1]) == 1:
            self.kb.kb_assert(parse_input("fact: (empty %s)" % old_peg))
        
        #if not empty, make secondary peg the top
        else:
            top = "disk" + str(present_state[int(mov_state[2][-1])-1][1])
            self.kb.kb_assert(parse_input("fact: (top %s %s)" % (top, old_peg)))

        #if new peg was empty, remove that fact       
        if len(present_state[int(mov_state[3][-2])-1]) == 0:
            self.kb.kb_retract(parse_input('fact: (empty ' + new_peg))
        
        #if new peg had disks on it, remove previous top peg and add facts for the new top peg
        else:
            top = "disk" + str(present_state[int(mov_state[3][-2])-1][0])
            self.kb.kb_retract(parse_input('fact: (top ' + top + ' ' + new_peg))
        self.kb.kb_assert(parse_input("fact: (top %s %s)" % (disk, new_peg)))
        self.kb.kb_assert(parse_input("fact: (on %s %s)" % (disk, new_peg)))
        return

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        output = []
        for i in range(3):
            x = i + 1
            row = []
            for j in range(3):
                y = j + 1
                tile_ask = parse_input("fact: (coordinate ?X pos%d pos%d" % (y, x))
                query = self.kb.kb_ask(tile_ask)

                if query:
                    tile_query = query[0]['?X']
                    if tile_query == 'empty':
                        row.append(-1)
                    else:
                        row.append(int(tile_query[-1]))
            output.append(tuple(row))
        return tuple(output)


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        tile  = str(movable_statement.terms[0])
        x_old = str(movable_statement.terms[1])
        y_old = str(movable_statement.terms[2])
        x_new = str(movable_statement.terms[3])
        y_new = str(movable_statement.terms[4])
        
        self.kb.kb_retract(parse_input("fact: (coordinate %s %s %s)" % (tile, x_old, y_old)))
        self.kb.kb_retract(parse_input("fact: (coordinate empty %s %s)" % (x_new, y_new)))
        self.kb.kb_assert(parse_input("fact: (coordinate %s %s %s)" % (tile, x_new, y_new)))
        self.kb.kb_assert(parse_input("fact: (coordinate empty %s %s)" % (x_old, y_old)))


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
