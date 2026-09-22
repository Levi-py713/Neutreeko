import os
class Board():
    moveSet = {'N': [-1, 0], 'E': [0, 1], 'S': [1, 0], 'W': [0, -1], 'NE': [-1, 1], 'NW': [-1, -1], 'SE': [1, 1], 'SW': [1, -1]}

    white_position = [[0, 1], [1, 3], [3, 2]]
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

    def DoMove(self, name:str, position: list[int], move: str): 


        current_position = [position[0], position[1]]

        while self.canMove([position[0] + self.moveSet[move][0], position[1] + self.moveSet[move][1]]):
            position[0] += self.moveSet[move][0]
            position[1] += self.moveSet[move][1]
            print(position)

        Board.game_board[current_position[0]][current_position[1]] = '_'
        Board.game_board[position[0]][position[1]] = name

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
    turn = "black"
    not_turn = "white"
    x = Board()
    while not x.IsPrimitive():
        print(x)
        move = input(f'Turn: {turn}, pick a piece and move (e.g B1N): ')
        os.system('clear')
        if turn == 'black':
            x.DoMove(move[:2], x.black_position[int(move[1]) - 1], move[2:])
        else:
            x.DoMove(move[:2], x.white_position[int(move[1]) - 1], move[2:])
        turn, not_turn = not_turn, turn
    print(x)
    print(f'{not_turn} has won!')



main()