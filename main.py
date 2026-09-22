import subprocess
class Board():
    turn = 0
    moveSet = {'N': [-1, 0], 'E': [0, 1], 'S': [1, 0], 'W': [0, -1], 'NE': [-1, 1], 'NW': [-1, -1], 'SE': [1, 1], 'SW': [1, -1]}

    white_position = [[0, 1], [0, 3], [3, 2]]
    black_position = [[1, 2], [4, 1], [4, 3]]
    
    game_board = [
                    ['_', 'W1', '_', 'W2', '_'],
                    ['_', '_', 'B1', '_', '_'],
                    ['_', '_', '_', '_', '_'],
                    ['_', '_', 'W3', '_', '_'],
                    ['_', 'B2', '_', 'B3', '_']]

    def __str__(self):
        for x in Board.game_board:
            print(x)
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
        elif Board.game_board[position[0]][position[1]]!= '_': 
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
        
        self.game_board[current_position[0]][current_position[1]] = '_'
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
            else:
                print('Sorry! Not a legal move')
            

    print(x)
    print(f'{'Black' if x.turn else 'White'} has won!')



main()