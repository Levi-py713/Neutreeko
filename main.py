import os
from models import Game, Value, StringMode


DIRECTIONS = {'N': 5, 'E': -1, 'S': -5, 'W': 1, 'NE': 4, 'NW': 6, 'SE': -6, 'SW': -4}
MOVE_ENCODE = {'N': 0, 'E': 1, 'S': 2, 'W': 3, 'NE': 4, 'NW': 5, 'SE': 6, 'SW': 7}
TIE_CACHE = {}

class Neutreeko():
    id = 'neutreeko'
    variants = ['5x5']
    n_players = 2
    cyclic = True

    turn = 0

    def __init__(self, variant_id: str):
        if variant_id not in self.variants:
            raise ValueError('variant not defined')
        self.variant_id = variant_id

        self.board_width = int(variant_id[0])
        self.board_length = int(variant_id[2])
        self.board_size = self.board_length * self.board_width
    
    def _encode(self, black, white, turn):
        number = 10 * turn
        for loc in black + white:
            number = number * self.board_size + loc
        if number in TIE_CACHE:
            TIE_CACHE[number] += 1
        else:
            TIE_CACHE[number] = 0
        return number

    def _decode(self, encoding):
        locs = []
        for _ in range(6):
            locs.append(encoding % 25) 
            encoding //= 25

        locs.reverse()
        black = tuple(locs[:3])
        white = tuple(locs[3:])
        turn = encoding // 10

        return white, black, turn

    def start(self):
        return self._encode(
            black=(7, 21, 23),
            white=(1, 3, 17),
            turn=0
        )

    #Very slow, can be improved and universalized
    def to_string(self, encode: int):
        board = [['__', '__', '__', '__', '__'], 
                 ['__', '__', '__', '__', '__'], 
                 ['__', '__', '__', '__', '__'], 
                 ['__', '__', '__', '__', '__'], 
                 ['__', '__', '__', '__', '__']]
        white, black, turn = self._decode(encode)
        
        for i in range(3):
            board[4 - white[i] // 5][4 - white[i] % 5] = f'W{i + 1}'
            board[4 - black[i] // 5][4 - black[i] % 5] = f'B{i + 1}'

        merged = []
        for i in range(len(board)):
            merged.append(board[i][0] + '  ' + board[i][1] + '  ' +  board[i][2] + '  ' +  board[i][3] + '  ' +  board[i][4])

        return '\n\n'.join(merged) + f'  Turn: {turn}'

    def from_string(self, board_state: str):
        turn = int(board_state[-1])
        black_moves = [0, 0, 0]
        white_moves = [0, 0, 0]
        counter = self.board_size - 1
        while counter >= 0:
            if board_state[0] == 'W':
                white_moves[int(board_state[1]) - 1] = counter
                counter -= 1
            if board_state[0] == 'B':
                black_moves[int(board_state[1]) - 1] = counter
                counter -= 1
            if board_state[0] == '_':
                counter -= 1
            board_state = board_state[2:]
        return self._encode(tuple(black_moves), tuple(white_moves), turn)

    #Checks if you can move in that direction
    def can_move(self, position: int, direction: str, encoding: int):
        white, black, _ = self._decode(encoding)
        if (position + DIRECTIONS[direction] not in black) and (position + DIRECTIONS[direction] not in white) and position + DIRECTIONS[direction] <= self.board_size - 1 and (position + DIRECTIONS[direction] >= 0):
            if direction in ['W', 'SW', 'NW'] and position % 5 == 4:
                return False
            if direction in ['E', 'SE', 'NE'] and position % 5 == 0:
                return False
            return True
        return False

    def do_move(self,  encoding: int, encoded_move: int): 
        white, black, turn = self._decode(encoding) 
        piece_number = encoded_move // 8 - 1
        real_move = list(MOVE_ENCODE)[(encoded_move - turn * 8) % 8]

        if turn:
            position = white[piece_number]

            while self.can_move(position, real_move, encoding):
                position += DIRECTIONS[real_move]

            white = list(white)
            white[piece_number] = position
            white = tuple(white)

        else:
            position = black[piece_number]

            while self.can_move(position, real_move, encoding):
                position += DIRECTIONS[real_move]

            black = list(black)
            black[piece_number] = position
            black = tuple(black)

        encode = self._encode(black, white, 1 - turn)

        return encode

        # Pre-scan before making move
        # 1. Fetch position and direction - if want to move 'north' check all squares ABOVE current position
        # 2. Loop over JUST that column and check

    # Scaffolding
    #Needs to return all pieces on the board and their possible positions
    def generate_moves(self, encoding):
        #Needs to be piece and move
        white, black, turn = self._decode(encoding)
        if turn:
            position = white
        else:
            position = black

        moves = []
        if self.primitive(encoding):
            return moves # Maybe switch this, returns []
        else:
            #Moves encoded as piece (0, 1, 2) * move (0, 1, 2, 3, 4, 5, 6, 7)
            for move in DIRECTIONS.keys():
                for i in range(len(position)):
                    if self.can_move(position[i], move, encoding):
                        moves.append(MOVE_ENCODE[move] + (8 * i))
        
        return moves
                

    def primitive(self, encoding):
        # Grabs where the piece is slightly faster than a for loop
        # I think this would be faster if game stores each position
        white, black, turn = self._decode(encoding)

        if TIE_CACHE[encoding] == 2:
            return Value.Draw

        just_moved = sorted(black) if turn else sorted(white)

        #All in a row
        if (just_moved[2] - just_moved[1] == 1 and just_moved[1] - just_moved[0] == 1):
            return Value.Loss
        elif (just_moved[2] - just_moved[1] == 5 and just_moved[1] - just_moved[0] == 1):
            return Value.Loss
        #Diagonal Check
        elif (just_moved[2] - just_moved[1] == 4 and just_moved[1] - just_moved[0] == 4):
            return Value.Loss
        elif (just_moved[2] - just_moved[1] == 6 and just_moved[1] - just_moved[0] == 6):
            return Value.Loss
        return None

    def hash_ext(self, encode: int):
        return encode

    def move_to_string(self, encoded_move: int, mode: StringMode):
        piece_number = encoded_move // 8 - 1
        real_move = list(MOVE_ENCODE)[(encoded_move - turn * 8) % 8]

        return f'{piece_number}{real_move}'


def main():
    x = Neutreeko('5x5')
    encode = x.start()

    #Turn starts as black
    while x.primitive(encode) == None:

        white, black, turn = x._decode(encode)
        os.system('clear')
        print(x.to_string(encode))
        if turn:
            print("WHITE'S TURN")
            prime_position = white
        else:
            print("BLACK'S TURN")
            prime_position = black
        statement = True
        
        while statement:
            decoded_move = input('What move would you like to make? Select piece # and DIRECTION, i.e. 1NE: ')
            if decoded_move[1:] not in MOVE_ENCODE.keys() or (decoded_move[0] != '1' and decoded_move[0] != '2' and decoded_move[0] != '3'):
                print('Sorry! Move not valid')

            elif x.can_move(prime_position[int(decoded_move[0]) - 1], decoded_move[1:], encode):
                encode = x.do_move(encode, MOVE_ENCODE[decoded_move[1:]] + (8 * int(decoded_move[0])))
                statement = False
            else:
                print('Sorry! Move not valid')

    _, _, turn = x._decode(encode)
    os.system('clear')
    print(x.to_string(encode))
    if turn and x.primitive(encode) == Value.Loss:
        print('Black Wins')
        return
    elif x.primitive(encode) == Value.Draw:
        return ("Draw! Three repetitions of board state")
    print('White Wins')
    return


#main()

# THIS IS THE UPDATED VERSION
import os
DIRECTIONS = {'N': 5, 'E': -1, 'S': -5, 'W': 1, 'NE': 4, 'NW': 6, 'SE': -6, 'SW': -4}
MOVE_ENCODE = {'N': 0, 'E': 1, 'S': 2, 'W': 3, 'NE': 4, 'NW': 5, 'SE': 6, 'SW': 7}

WHITE_INIT = {(0, 1), (0, 3), (3, 2)}
BLACK_INIT = {(1, 2), (4, 1), (4, 3)}

class Neutreeko():
    id = 'neutreeko'
    variants = ["5x5"]
    n_players = 2
    cyclic = True

    turn = 0

    def __init__(self, variant_id: str):
        if variant_id not in self.variants:
            raise ValueError("variant not defined")
        self.variant_id = variant_id

        self.board_width = int(variant_id[0])
        self.board_length = int(variant_id[2])
        self.board_size = self.board_length * self.board_width
    
    def _encode(self, black, white, turn):
        number = turn
        for loc in black + white:
            number = number * 25 + loc
        return number

    def _decode(self, encoding):
        locs = []
        for _ in range(6):
            locs.append(encoding % 25) 
            encoding //= 25

        locs.reverse()
        black = tuple(locs[:3])
        white = tuple(locs[3:])
        turn = encoding

        return white, black, turn

    def start(self):
        return self._encode(
            black=(7, 21, 23),
            white=(1, 3, 17),
            turn=0
        )

    def __str__(self, encode):
        board = [['__', '__', '__', '__', '__'], 
                 ['__', '__', '__', '__', '__'], 
                 ['__', '__', '__', '__', '__'], 
                 ['__', '__', '__', '__', '__'], 
                 ['__', '__', '__', '__', '__']]
        white, black, _ = self._decode(encode)
        for i in range(3):
            board[4 - white[i] // 5][4 - white[i] % 5] = f'W{i + 1}'
            board[4 - black[i] // 5][4 - black[i] % 5] = f'B{i + 1}'
        for x in board:
            for y in x:
                print(y, end='  ')
            print('\n')

        return " "

    #Checks if you can move in that direction
    def can_move(self, position: int, direction: str, encoding: int):
        white, black, _ = self._decode(encoding)
        if (position + DIRECTIONS[direction] not in black) and (position + DIRECTIONS[direction] not in white) and position + DIRECTIONS[direction] <= self.board_size - 1 and (position + DIRECTIONS[direction] >= 0):
            if direction in ['W', 'SW', 'NW'] and position % 5 == 4:
                print("W, SW, NW")
                return False
            if direction in ['E', 'SE', 'NE'] and position % 5 == 0:
                print("E, SE, NE")
                return False
            return True
        return False

    def do_move(self,  encoding: int, encoded_move: int): 
        white, black, turn = self._decode(encoding) 
        piece_number = encoded_move // 8 - 1
        real_move = list(MOVE_ENCODE)[(encoded_move - turn * 8) % 8]

        if turn:
            position = white[piece_number]

            while self.can_move(position, real_move, encoding):
                position += DIRECTIONS[real_move]

            white = list(white)
            white[piece_number] = position
            white = tuple(white)

        else:
            position = black[piece_number]

            while self.can_move(position, real_move, encoding):
                position += DIRECTIONS[real_move]

            black = list(black)
            black[piece_number] = position
            black = tuple(black)

        encode = self._encode(black, white, 1 - turn)

        return encode

        # Pre-scan before making move
        # 1. Fetch position and direction - if want to move 'north' check all squares ABOVE current position
        # 2. Loop over JUST that column and check

    # Scaffolding
    #Needs to return all pieces on the board and their possible positions
    def GenerateMoves(self, encoding):
        #Needs to be piece and move
        white, black, turn = self._decode(encoding)
        if turn:
            position = white
        else:
            position = black

        moves = []
        if self.IsPrimitive(encoding):
            return moves # Maybe switch this, returns []
        else:
            #Moves encoded as piece (0, 1, 2) * move (0, 1, 2, 3, 4, 5, 6, 7)
            for move in DIRECTIONS.keys():
                for i in range(len(position)):
                    if self.can_move(position[i], move, encoding):
                        moves.append(MOVE_ENCODE[move] + (8 * i))
        
        return moves
                

    def IsPrimitive(self, encoding):
        # Grabs where the piece is slightly faster than a for loop
        # I think this would be faster if game stores each position
        white, black, turn = self._decode(encoding)
        
        for position_list in [white,black]:
            sorted_list = sorted(position_list)

            #All in a row
            if (sorted_list[2] - sorted_list[1] == 1 and sorted_list[1] - sorted_list[0] == 1):
                return turn
            elif (sorted_list[2] - sorted_list[1] == 5 and sorted_list[1] - sorted_list[0] == 1):
                return turn
            #Diagonal Check
            elif (sorted_list[2] - sorted_list[1] == 4 and sorted_list[1] - sorted_list[0] == 4):
                return turn
            elif (sorted_list[2] - sorted_list[1] == 6 and sorted_list[1] - sorted_list[0] == 6):
                return turn
        return None

def main():
    x = Neutreeko("5x5")
    encode = x.start()

    #Turn starts as black
    while x.IsPrimitive(encode) == None:

        white, black, turn = x._decode(encode)
        os.system("clear")
        print(x.__str__(encode))
        if turn:
            print("WHITE'S TURN")
            prime_position = white
        else:
            print("BLACK'S TURN")
            prime_position = black
        statement = True
        
        while statement:
            decoded_move = input("What move would you like to make? Select piece # and DIRECTION, i.e. 1NE: ")
            if decoded_move[1:] not in MOVE_ENCODE.keys() or (decoded_move[0] != '1' and decoded_move[0] != '2' and decoded_move[0] != '3'):
                print("Sorry! Move not valid")

            elif x.can_move(prime_position[int(decoded_move[0]) - 1], decoded_move[1:], encode):
                encode = x.do_move(encode, MOVE_ENCODE[decoded_move[1:]] + (8 * int(decoded_move[0])))
                statement = False
            else:
                print("Sorry! Move not valid")

    _, _, turn = x._decode(encode)
    print(x.__str__(encode))
    if turn:
        print("Black Wins")
        return
    print("White Wins")
    return


main()