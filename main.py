import os
from models import Game, Value, StringMode


MOVE_ENCODE = {'N': 0, 'E': 1, 'S': 2, 'W': 3, 'NE': 4, 'NW': 5, 'SE': 6, 'SW': 7}
SYMMETRIES = {}

class Neutreeko():
    id = 'neutreeko'
    #Can play any variant of square board, not solved though
    variants = ['5x5', '6x6']
    n_players = 2
    cyclic = True

    turn = 0

    #STRING TYPE MAY REMOVE
    stringType = None

    def __init__(self, variant_id: str):
        if variant_id not in self.variants:
            raise ValueError('variant not defined')
        self.variant_id = variant_id

        self.board_height = int(variant_id[:len(variant_id) // 2])
        self.board_length = int(variant_id[len(variant_id) // 2 + 1:])
        self.board_size = self.board_length * self.board_height
        self.actual_board_size = self.board_size - 1
        self.piv_point = self.board_length // 2
        self.directions = {'N': -self.board_length, 'E': 1, 'S': self.board_length, 'W': -1, 'NE': -self.board_length - 1, 'NW': -self.board_length + 1, 'SE': self.board_length - 1, 'SW': self.board_length + 1}

        # Pre-compute symmetries
    
    def _encode(self, black, white, turn):
        number = turn

        for loc in sorted(black) + sorted(white):
            number = number * self.board_size + loc

        return number

    def _decode(self, encoding):

        locs = []
        for _ in range(2 * self.board_length - 4):
            locs.append(encoding % self.board_size) 
            encoding //= self.board_size

        locs.reverse()
        black = tuple(locs[:len(locs) // 2])
        white = tuple(locs[len(locs) // 2:])
        turn = encoding

        return white, black, turn

    def start(self):
        black = []
        white = []
        for x in range(self.board_height // 2):
            if x % 2 == 0:
                if x == self.board_height // 2 - 1:
                    white.append((x * self.board_length) + (x + 1))
                    black.append((self.board_height * self.board_length - 1) - (x * self.board_height) - x - 1)
                    break
                if x == self.board_height // 2 - 2 and self.board_height % 2 == 0:
                    white.append((x * self.board_length) + (x + 1))
                    white.append(((x + 1) * self.board_length) - 2 - x)
                    black.append((self.board_height * self.board_length - 1) - (x * self.board_height) - x - 1)
                    black.append((self.board_height * self.board_length - 1) - ((x + 1) * self.board_height) + (x + 2))
                    break
                else:
                    white.append((x * self.board_length) + (x + 1))
                    white.append(((x + 1) * self.board_length) - 2 - x)
                    black.append((self.board_height * self.board_length - 1) - (x * self.board_height) - x - 1)
                    black.append((self.board_height * self.board_length - 1) - ((x + 1) * self.board_height) + (x + 2))

            else:
                if x == self.board_height // 2 - 2 and self.board_height % 2 == 0:
                    black.append((x * self.board_length) + (x + 1))
                    black.append(((x + 1) * self.board_length) - 2 - x)
                    white.append((self.board_height * self.board_length - 1) - (x * self.board_height) - x - 1)
                    white.append((self.board_height * self.board_length - 1) - ((x + 1) * self.board_height) + (x + 2))
                    break
                if x == self.board_height // 2 - 1:
                    black.append((x * self.board_length) + (x + 1))
                    white.append((self.board_height * self.board_length - 1) - (x * self.board_height) - x - 1)
                    break
                else:
                    black.append((x * self.board_length) + (x + 1))
                    black.append(((x + 1) * self.board_length) - 2 - x)
                    white.append((self.board_height * self.board_length - 1) - (x * self.board_height) - x - 1)
                    white.append((self.board_height * self.board_length - 1) - ((x + 1) * self.board_height) + (x + 2))


        return self._encode(
            black=tuple(black),
            white=tuple(white),
            turn=0
        )

    #Very slow, can be improved and universalized
    def to_string(self, encode: int, mode: StringMode):
        """
        """
        if self.stringType == None:
            self.stringType = mode

        white, black, turn = self._decode(encode)
        if turn:
            turn = 'White'
        else:
            turn = 'Black'

        if mode == StringMode.TUI:
            board = [[f'B{black.index((self.board_height * column) + row) + 1}' 
                        if ((self.board_height * column) + row in black) 
                            else f'W{white.index((self.board_height * column) + row) + 1}' 
                                if self.board_height * column + row in white 
                                    else '--' 
                                        for row in range(self.board_length)] 
                                            for column in range(self.board_height)]
            merged = []
            item = ''
            for i in range(len(board)):
                for j in range(len(board[0])):
                    item += ' ' 
                    item += board[i][j]
                merged.append(item)
                item = ''

            return '\n\n'.join(merged) + '\n' + f'Turn: {turn}'
        
        elif mode == StringMode.AUTOGUI:
            board = ['B' if ((self.board_height * column) + row in black) 
                        else 'W' if self.board_height * column + row in white 
                            else '-' for column in range(self.board_height) for row in range(self.board_length)]

            turn = '1' if turn == 0 else '2'
            return turn + "_" + "".join(board)

    def from_string(self, board_state: str):
        if board_state[-5] == "B":
            turn = 0
        else:
            turn = 1

        black_moves = [0 for _ in range(self.board_length - 2)]
        white_moves = [0 for _ in range(self.board_length - 2)]
        counter = self.actual_board_size
        while counter >= 0:
            if board_state[0] == 'W':
                white_moves[int(board_state[1]) - 1] = counter
                counter -= 1
            if board_state[0] == 'B':
                black_moves[int(board_state[1]) - 1] = counter
                counter -= 1
            if board_state[0] == '-':
                counter -= 1
            board_state = board_state[2:]
        return self._encode(tuple(black_moves), tuple(white_moves), turn)

    #Checks if you can move in that direction
    def can_move(self, position: int, direction: str, encoding: int):
        white, black, _ = self._decode(encoding)
        if (position + self.directions[direction] not in black) and (position + self.directions[direction] not in white) and position + self.directions[direction] <= self.actual_board_size and (position + self.directions[direction] >= 0):
            if direction in ['W', 'SW', 'NW'] and position % self.board_length == self.board_length - 1:
                return False
            if direction in ['E', 'SE', 'NE'] and position % self.board_length == 0:
                return False
            return True
        return False

    def do_move(self,  encoding: int, encoded_move: int): 
        white, black, turn = self._decode(encoding) 

        if self.stringType == StringMode.TUI:
            piece_number = encoded_move // 8 - 1
            real_move = list(MOVE_ENCODE)[(encoded_move) % 8]
        
        elif self.stringType == StringMode.AUTOGUI:
            print(encoding, encoded_move)
            if turn:
                piece_number = white.index(encoded_move // 10)
            else:
                print(black)
                print(encoded_move // 10)
                piece_number = black.index(encoded_move // 10)
            print(encoded_move)
            real_move = list(MOVE_ENCODE)[(encoded_move) % 10]

        if turn:

            position = white[piece_number]
            
            while self.can_move(position, real_move, encoding):
                position += self.directions[real_move]

            white = list(white)
            white[piece_number] = position
            white = tuple(white)

        else:
            position = black[piece_number]

            while self.can_move(position, real_move, encoding):
                position += self.directions[real_move]

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
        if self.stringType == StringMode.TUI:
            white, black, turn = self._decode(encoding)
            if turn:
                position = white
            else:
                position = black

            moves = []
            if self.primitive(encoding) !=  None:
                return moves # Maybe switch this, returns []
            else:
                #Moves encoded as piece (0, 1, 2) * move (0, 1, 2, 3, 4, 5, 6, 7)
                for move in self.directions.keys():
                    for i in range(len(position)):
                        if self.can_move(position[i], move, encoding):
                            moves.append(MOVE_ENCODE[move] + (8 * (i + 1)))

        #AUTOGUI DIFFERENT MOVE STRING
        elif self.stringType == StringMode.AUTOGUI:
            white, black, turn = self._decode(encoding)
            if turn:
                position = white
            else:
                position = black

            moves = []
            if self.primitive(encoding) !=  None:
                return moves # Maybe switch this, returns []
            else:
                #Moves encoded as piece (0, 1, 2) * move (0, 1, 2, 3, 4, 5, 6, 7)
                for move in self.directions.keys():
                    for i in range(len(position)):
                        if self.can_move(position[i], move, encoding):
                            moves.append(position[i] * 10 + move)
            
        return moves
                

    def primitive(self, encoding):
        # Grabs where the piece is slightly faster than a for loop
        # I think this would be faster if game stores each position
        white, black, turn = self._decode(encoding)

        just_moved = sorted(black) if turn else sorted(white)

        #All in a row
        if all([just_moved[i + 1] - just_moved[i] == 1 and just_moved[i + 1] // self.board_height == just_moved[i] // self.board_height for i in reversed(range(len(black) - 1))]):
            return Value.Loss
        elif all([just_moved[i + 1] - just_moved[i] == self.board_length and just_moved[i + 1] // self.board_height - just_moved[i] // self.board_height == 1 for i in reversed(range(len(black) - 1))]):
            return Value.Loss
        #Diagonal Check
        elif all([just_moved[i + 1] - just_moved[i] == self.board_length - 1 and just_moved[i + 1] // self.board_height - just_moved[i] // self.board_height == 1 for i in reversed(range(len(black) - 1))]):
            return Value.Loss
        elif all([just_moved[i + 1] - just_moved[i] == self.board_length + 1 and just_moved[i + 1] // self.board_height - just_moved[i] // self.board_height == 1 for i in reversed(range(len(black) - 1))]):
            return Value.Loss
        return None

    def hash_ext(self, encode: int):
        return encode


    def move_to_string(self, encoded_move: int, mode: StringMode):

        if mode == StringMode.TUI:
            piece_number = encoded_move // 8 - 1
            real_move = list(MOVE_ENCODE)[encoded_move % 8]

            return f'{piece_number + 1}{real_move}'
        elif mode == StringMode.AUTOGUI:
            # Adjust encoding so it has move
            real_move = list(MOVE_ENCODE)[encoded_move % 10]
            src = encoded_move // 10
            # from_cell = encoded_move // 10
            # to_cell = encoded_move % 10

            #M_source_destination_sound
            return f'M_{src}_{src + self.directions[real_move]}_x'


def main():
    x = Neutreeko('5x5')
    encode = x.start()

    #Turn starts as black
    while x.primitive(encode) == None:

        white, black, turn = x._decode(encode)

        print(x.to_string(encode, StringMode.AUTOGUI))

        if turn:
            prime_position = white
        else:
            prime_position = black
        statement = True
        
        while statement:
            decoded_move = input('What move would you like to make? Select piece # and DIRECTION, i.e. 1NE: ')
            actual_move = ''
            directioned_move = None
            while decoded_move:
                if decoded_move[0] in MOVE_ENCODE:
                    directioned_move = decoded_move[:]
                    break
                else:
                    actual_move += decoded_move[0]
                decoded_move = decoded_move[1:]
            
            if directioned_move == None or directioned_move not in MOVE_ENCODE.keys() or int(actual_move) < 1 or int(actual_move) > len(black):
                print('Sorry! Move not valid')

            elif x.can_move(prime_position[int(actual_move) - 1], directioned_move, encode):
                encode = x.do_move(encode, MOVE_ENCODE[directioned_move] + (8 * int(actual_move)))
                statement = False
            else:
                print("here")
                print('Sorry! Move not valid')
        os.system('clear')

    _, _, turn = x._decode(encode)
    os.system('clear')
    print(x.to_string(encode, None))
    if turn and x.primitive(encode) == Value.Loss:
        print('Black Wins')
        return
    print('White Wins')
    return


#main()

def test():
    x = Neutreeko('5x5')
    encode = x.start()
    print(x.to_string(encode, 1))
    print(x.to_string(encode, 2))

#test()