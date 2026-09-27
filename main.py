import os
class Board():
    turn = 0
    moveSet = {'N': [-1, 0], 'E': [0, 1], 'S': [1, 0], 'W': [0, -1], 'NE': [-1, 1], 'NW': [-1, -1], 'SE': [1, 1], 'SW': [1, -1]}

    white_position = [[0, 1], [0, 3], [3, 2]]
    black_position = [[1, 2], [4, 1], [4, 3]]
    
    game_board = [
                    ['__', 'W1', '__', 'W2', '__'],
                    ['__', '__', 'B1', '__', '__'],
                    ['__', '__', '__', '__', '__'],
                    ['__', '__', 'W3', '__', '__'],
                    ['__', 'B2', '__', 'B3', '__']]

    def __str__(self):
        for x in Board.game_board:
            for y in x:
                print(y, end='  ')
            print('\n')
        return ' '
    # position on board, 'white' or 'black'
    # def __init__(self, position, color):
    #     self.position = position
    #     self.color = color

    def __init__(self):
        pass

    #Checks if you can move in that direction
    def canMove(self, position):
        if position[0] > len(Board.game_board) - 1 or position[0] < 0 or position[1] > len(Board.game_board) - 1 or position[1] < 0:
            return False
        elif Board.game_board[position[0]][position[1]]!= '__': 
            return False
        else:
            return True
            # Check if position is primitive, else moves position

    def DoMove(self, piece: int, position: list[int], move: str): 


        current_position = [position[0], position[1]]

        while self.canMove([position[0] + self.moveSet[move][0], position[1] + self.moveSet[move][1]]):
            position[0] += self.moveSet[move][0]
            position[1] += self.moveSet[move][1]

        if current_position == [position[0], position[1]]:
            return "Didn't Move"
        
        self.game_board[current_position[0]][current_position[1]] = '__'
        self.game_board[position[0]][position[1]] = f'{'W' if self.turn else 'B'}{piece}'
        self.turn = 1 - self.turn

        return "Moved"

        # Pre-scan before making move
        # 1. Fetch position and direction - if want to move 'north' check all squares ABOVE current position
        # 2. Loop over JUST that column and check

    # Scaffolding

    def GenerateMoves(self, position):
        moves = []
        if self.IsPrimitive() == 'primitive':
            return 'primitive'
        else:
            for move in self.moveSet.keys():
                if self.canMove([position[0] + self.moveSet[move][0], position[1] + self.moveSet[move][1]]):
                    moves.append(move)
        return moves
                

    def IsPrimitive(self):
        # Grabs where the piece is slightly faster than a for loop
        # I think this would be faster if game stores each position

        for position_list in [Board.white_position, Board.black_position]:
            sorted_list = sorted([position_list[0], position_list[1], position_list[2]], key= lambda x: x[0] + x[1])
            #Checks if it differs by one horizontally or vertically
            #maybe too complex
            if (sorted_list[0][0] + 1 == sorted_list[1][0] and sorted_list[1][0] +1 == sorted_list[2][0]) or (sorted_list[0][1] + 1 == sorted_list[1][1] and sorted_list[1][1] + 1 == sorted_list[2][1]):
                #Horizontal
                if sorted_list[0][0] == sorted_list[1][0] and sorted_list[1][0] == sorted_list[2][0]:
                    return True
                #Vertical
                elif sorted_list[0][1] == sorted_list[1][1] and sorted_list[1][1] == sorted_list[2][1]:
                    return True
            #Diagonal
                elif (sorted_list[0][0] + 1 == sorted_list[1][0] and sorted_list[1][0] + 1 == sorted_list[2][0]) and (sorted_list[0][1] + 1 == sorted_list[1][1] and sorted_list[1][1] + 1 == sorted_list[2][1]):
                    return True
        return False

def main():
    x = Board()
    while not x.IsPrimitive():
        print(x)
        catch = True
        while catch:
            move = input(f'Turn: {'white' if x.turn else 'black'}, pick a piece and move (e.g 1N): ')
            if ((len(move) == 2 or len(move) == 3) and (move[0] == '1' or move[0] == '2' or move[0] == '3') and (move[1:] in Board.moveSet)):
                if not x.turn:
                    valid = x.DoMove(move[0] , x.black_position[int(move[0]) - 1], move[1:])
                else:
                    valid = x.DoMove(move[0] , x.white_position[int(move[0]) - 1], move[1:])
                if valid == "Didn't Move":
                    print('Sorry! Not a legal move')
                else:
                    catch = False
                    os.system("clear")
            else:
                print('Sorry! Not a legal move')
            

    print(x)
    print(f'{'Black' if x.turn else 'White'} has won!')



main()

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