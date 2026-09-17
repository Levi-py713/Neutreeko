class Piece():

    # position on board, 'white' or 'black'
    # def __init__(self, position, color):
    #     self.position = position
    #     self.color = color

    def __init__(self):
        pass

    def isInBounds(self, position):
        if position[0] > 4 or position[0] < 0 or position[1] > 4 or position[1] < 0:
            return False
        else:
            return True
            # Check if position is primitive, else moves position
    def DoMove(self, position: list[int], move: str): 
        moveSet = {'N': [-1, 0], 'E': [0, 1], 'S': [1, 0], 'W': [0, -1], 'NE': [-1, 1], 'NW': [-1, -1], 'SE': [1, 1], 'SW': [1, -1]}


        current_position = position

        while self.isInBounds([position[0] + moveSet[move][0], position[1] + moveSet[move][1]]) and Board.game_board[position[0] + moveSet[move][0]][position[1] + moveSet[move][1]] == '_':
            position[0] += moveSet[move][0]
            position[1] += moveSet[move][1]
            print(position)

        Board.game_board[current_position[0]][current_position[1]] = '_'
        Board.game_board[position[0]][position[1]] = 'XX'

        return 'Move Updated!'

        # Pre-scan before making move
        # 1. Fetch position and direction - if want to move 'north' check all squares ABOVE current position
        # 2. Loop over JUST that column and check

        # while Board.game_board[position[0]][position[1]] != 


    # Scaffolding

    #def GenerateMoves(self, position):
        raise NotImplementedError()

    def IsPrimitive(self, position):
        index = [0, 0]
        for color in ['X', 'O']:
            while index:



        index = [0, 0]
            

        raise NotImplementedError()


class Board():
    
    game_board = [
                    ['_', 'O', '_', 'O', '_'],
                    ['_', '_', 'X', '_', '_'],
                    ['_', '_', '_', '_', '_'],
                    ['_', '_', 'O', '_', '_'],
                    ['_', 'X', '_', 'X', '_']]

    def __str__(self):
        for x in Board.game_board:
            print(x)
        return ' '

