import os
from models import Game, Value, StringMode


MOVE_ENCODE = {'N': 0, 'E': 1, 'S': 2, 'W': 3, 'NE': 4, 'NW': 5, 'SE': 6, 'SW': 7}

class Neutreeko():
    id = 'neutreeko'
    # variants = ['5x5', '6x6', '7x7', '9x9', '11x11', '13x13', '111x111']
    variants = ['5x5', '6x6']
    n_players = 2
    cyclic = True

    turn = 0

    def __init__(self, variant_id: str):
        if variant_id not in self.variants:
            raise ValueError('variant not defined')
        self.variant_id = variant_id

        self.board_height = int(variant_id[:len(variant_id) // 2])
        self.board_length = int(variant_id[len(variant_id) // 2 + 1:])
        self.board_size = self.board_length * self.board_height
        self.actual_board_size = self.board_size - 1
        self.directions = {'N': self.board_length, 'E': -1, 'S': -self.board_length, 'W': 1, 'NE': self.board_length - 1, 'NW': self.board_length + 1, 'SE': -self.board_length - 1, 'SW': -self.board_length + 1}
    
    def _encode(self, black, white, turn):
        number = 10 * turn


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
        turn = encoding // 10

        return white, black, turn

    def start(self):
        black = []
        white = []
        for x in range(self.board_height // 2):
            
            if x % 2 == 0:
                # Even-sized boards
                if x == self.board_height // 2 - 1:
                    white.append((x * self.board_length) + (x + 1))
                    black.append((self.board_height * self.board_length - 1) - (x * self.board_height) - x - 1)
                else:
                    white.append((x * self.board_length) + (x + 1))
                    white.append(((x + 1) * self.board_length) - 2 - x)
                    black.append((self.board_height * self.board_length - 1) - (x * self.board_height) - x - 1)
                    black.append((self.board_height * self.board_length - 1) - ((x + 1) * self.board_height) + (x + 2))
            
            else:
                if x == self.board_height // 2 - 1:
                    black.append((x * self.board_length) + (x + 1))
                    white.append((self.board_height * self.board_length - 1) - (x * self.board_height) - x - 1)
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
        white, black, turn = self._decode(encode)
        if mode == StringMode.TUI:
            if turn:
                turn = 'White'
            else:
                turn = 'Black'

            board = [[f'B{black.index((self.board_height * column) + row) + 1}' 
                        if ((self.board_height * column) + row in black) 
                            else f'W{white.index((self.board_height * column) + row) + 1}' 
                                if self.board_height * column + row in white 
                                    else '--' 
                                        for row in reversed(range(self.board_length))] 
                                            for column in reversed(range(self.board_height))]

            merged = []
            item = ''
            for i in range(len(board)):
                for j in range(len(board[0])):
                    item += ' ' 
                    item += board[i][j]
                merged.append(item)
                item = ''

            return '\n\n'.join(merged) + '\n' + f'Turn: {turn}'

        # AutoGUI case
        board = ''.join('B' if i in black else 'W' if i in white else '-'
            for i in range(self.board_size))
        return f"{turn + 1}_{board}"
            

    def from_string(self, board_state: str):
        # if self.stringType == StringMode.TUI:
            # if board_state[-5] == "B":
            #     turn = 0
            # else:
            #     turn = 1
        turn_state, board = board_state.split('_')
        turn = int(turn_state) - 1
        if turn not in (0, 1) or len(board) != self.board_size:
            raise ValueError("Invalid position!")

        black_moves = []
        white_moves = []
        for counter in range(self.board_size):
            if board[counter] == 'W':
                white_moves.append(counter)
            if board[counter] == 'B':
                black_moves.append(counter)
        return self._encode(tuple(black_moves), tuple(white_moves), turn)

    #Checks if you can move in that direction
    def can_move(self, position: int, direction: str, encoding: int):
        white, black, _ = self._decode(encoding)
        if (position + self.directions[direction] not in black) and (position + self.directions[direction] not in white) and position + self.directions[direction] <= self.actual_board_size and (position + self.directions[direction] >= 0):
            if direction in ['E', 'SE', 'NE'] and position % self.board_length == self.board_length - 1:
                return False
            if direction in ['W', 'SW', 'NW'] and position % self.board_length == 0:
                return False
            return True
        return False

    def do_move(self,  encoding: int, encoded_move: int): 
        white, black, turn = self._decode(encoding) 

        if turn:

            position = encoded_move % self.board_size
            
            # while self.can_move(position, real_move, encoding):
            #     position += self.directions[real_move]

            white = list(white)
            white[white.index(encoded_move // self.board_size)] = position
            white = tuple(white)

        else:
            position = encoded_move % self.board_size

            # while self.can_move(position, real_move, encoding):
            #     position += self.directions[real_move]
            
            black = list(black)
            black[black.index(encoded_move // self.board_size)] = position
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
        moves = []
        white, black, turn = self._decode(encoding)
        if turn:
            position = white
        else:
            position = black

        #AUTOGUI DIFFERENT MOVE STRING
        # elif self.stringType == StringMode.AUTOGUI:

        if self.primitive(encoding) !=  None:
            return moves # Maybe switch this, returns []

        #Moves encoded as piece (0, 1, 2) * move (0, 1, 2, 3, 4, 5, 6, 7)
        for move in self.directions.keys():
            for i in range(len(position)):
                dest = position[i]
                # while self.can_move(position[i], move, encoding):
                while self.can_move(dest, move, encoding):
                    dest += self.directions[move]
                if dest != position[i]:
                    # moves.append(position[i] * self.board_size + dest)
                    moves.append(position[i] * self.board_size + dest)
        
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
        src = encoded_move // self.board_size
        dest = encoded_move % self.board_size
        
        if mode == StringMode.AUTOGUI:
            return f'M_{src}_{dest}_x'

        row_change = dest // self.board_length - src // self.board_length
        col_change = dest % self.board_length - src % self.board_length
        direction = ''
        if row_change < 0:
            direction += 'N'
        elif row_change > 0:
            direction += 'S'
        if col_change > 0:
            direction += 'E'
        elif col_change < 0:
            direction += 'W'
        return f'{src}{direction}'


def main():
    x = Neutreeko('111x111')
    encode = x.start()

    #Turn starts as black
    while x.primitive(encode) == None:

        white, black, turn = x._decode(encode)

        print(x.to_string(encode, None))

        if turn:
            prime_position = white
        else:
            prime_position = black
        statement = True
        
        while statement:
            decoded_move = input('What move would you like to make? Select piece # and DIRECTION, i.e. 1NE: ')
            actual_move = ''
            while decoded_move:
                if decoded_move[0] in MOVE_ENCODE:
                    directioned_move = decoded_move[:]
                    break
                else:
                    actual_move += decoded_move[0]
                decoded_move = decoded_move[1:]
                
            if directioned_move not in MOVE_ENCODE.keys() or int(actual_move) < 1 or int(actual_move) > len(black):
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


# main()