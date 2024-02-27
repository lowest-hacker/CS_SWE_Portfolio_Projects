# Author: Casey Bellew
# GitHub username: Psykibear
# Date: 5/30/2023
# Description: Writing a class called Othello that allows two people to play text-based Othello


class Player:
    """
    setting up player class to house the name of the player and the color that the user chooses. the only
    available colors will be black and white.
    """

    def __init__(self, name, color):
        self._name = name
        self._color = color


class Othello:
    """
    setting up the class for the othello game where the user will be able to grab the player's name and color to then
    allow that player to make a move based on the color they are playing while checking if it is a valid move, if not
    then what the valid moves are, and verifying whether the game has ended with the players move including the winner
    of the game.
    """

    def __init__(self):
        self._board = [['.' for item in range(10)] for item in range(10)]
        self._board[4][4] = 'O'
        self._board[4][5] = 'X'
        self._board[5][5] = 'O'
        self._board[5][4] = 'X'
        self._board[0][0] = "*"
        self._board[0][1] = "*"
        self._board[0][2] = "*"
        self._board[0][3] = "*"
        self._board[0][4] = "*"
        self._board[0][5] = "*"
        self._board[0][6] = "*"
        self._board[0][7] = "*"
        self._board[0][8] = "*"
        self._board[0][9] = "*"
        self._board[9][0] = "*"
        self._board[9][1] = "*"
        self._board[9][2] = "*"
        self._board[9][3] = "*"
        self._board[9][4] = "*"
        self._board[9][5] = "*"
        self._board[9][6] = "*"
        self._board[9][7] = "*"
        self._board[9][8] = "*"
        self._board[9][9] = "*"
        self._board[1][0] = "*"
        self._board[2][0] = "*"
        self._board[3][0] = "*"
        self._board[4][0] = "*"
        self._board[5][0] = "*"
        self._board[6][0] = "*"
        self._board[7][0] = "*"
        self._board[8][0] = "*"
        self._board[1][9] = "*"
        self._board[2][9] = "*"
        self._board[3][9] = "*"
        self._board[4][9] = "*"
        self._board[5][9] = "*"
        self._board[6][9] = "*"
        self._board[7][9] = "*"
        self._board[8][9] = "*"
        self._players = []

    def print_board(self):
        """
        Setups the board to be printed through a for loop
        :return:
        prints out the board by row then by column through nested for loop
        """
        for row in range(0, 10):
            for column in range(0, 10):
                print(self._board[row][column], end=' ')
            print()

    def create_player(self, player_name, color):
        """
        lets the user create a new player for the game
        :param player_name: string to be stored for display pending winner
        :param color: player's piece color; setup to be black or white
        :return:
        returns the appended list of players with the player name and color
        """
        player = Player(player_name, color)
        self._players.append(player)

    def return_winner(self):
        """
        method to check for the winner based on the number of spaces filled with each of the values for the
        specified colors.
        :return:
        returns the print method for the winner based on the count of the color pieces or a tie if they are equal.
        """
        black_count = 0
        white_count = 0
        for row in self._board[1:9]:
            for cell in row[1:9]:
                if cell == 'X':
                    black_count += 1
                elif cell == 'O':
                    white_count += 1

        if black_count > white_count:
            winner = [player for player in self._players if player._color == 'black'][0]
            return print("Winner is black player: " + winner._name)
        elif white_count > black_count:
            winner = [player for player in self._players if player._color == 'white'][0]
            return print("Winner is white player: " + winner._name)
        else:
            return print("It's a tie.")

    def return_available_positions(self, color):
        """
        sets up the method to store all the available positions for the specified player (based on their color)
        :param color: specified player's color
        :return:
        returns the list of available positions that the user can move if the position they are attempting to move to
        is an invalid position.
        """
        available_positions = []
        for row in range(1, 9):
            for column in range(1, 9):
                if self._board[row][column] == '.':
                    if self.validate_move(row, column, color):
                        available_positions.append((row, column))
        return available_positions

    def validate_move(self, row, column, color):
        """
        method to validate that the move is one that can be made by the specified player and their corresponding color
        :param color: specified color of the player that wants to make a move
        :param row: specified row in the make a move position
        :param column: specified column in the make a move position
        :return:
        checks whether the move that the player wants to make of a specific color is a valid move for them to make.
        """
        if self._board[row][column] != '.':
            return False
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, -1), (-1, 1)]:
            move_column, move_row = row + direction[0], column + direction[1]
            if color == 'white' and self._board[move_column][move_row] == 'X':
                return False
            elif color == 'black' and self._board[move_column][move_row] == 'O':
                return False
            while self._board[move_column][move_row] != '.' and self._board[move_column][move_row] != '.':
                if self._board[move_column][move_row] == 'X':
                    return True
                elif self._board[move_column][move_row] == 'O':
                    return True
                move_column += direction[0]
                move_row += direction[1]
            return False

    def play_game(self, color, piece_position):
        """
        sets up the method for the users to play the othello game based on their color and the position they want
        to make a move in.
        :param color: specifies the color of the player making their move
        :param piece_position: specifies the move the player is wanting to make
        :return:
        returns the available positions if the user inputs an invalid move, followed by making the move for the player
        if it is valid, printing the board, and verifying if the game is over and the winner is determined.
        """
        row, column = piece_position
        if not self.validate_move(row, column, color):
            print("Invalid move")
            print("Here are the valid moves:")
            available_moves = self.return_available_positions(color)
            print(available_moves)
            return
        self.make_move(color, piece_position)
        self.print_board()

        if not self.player_available_moves():
            print("Game has ended.")
            print(self.return_winner())

    def make_move(self, color, piece_position):
        """
        allows the user to make a move while "playing the game"
        :param color: allows the user to input the color that is to be moved
        :param piece_position: allows the user to input the position to place the piece
        :return:
        makes a move for the player by placing an X for a white piece set with a O for a black piece set
        """
        row, column = piece_position
        if color == 'white':
            self._board[row][column] = 'X'
        else:
            self._board[row][column] = 'O'
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            self.player_move(row, column, direction, color)
        return self._board

    def player_move(self, row, column, direction, color):
        """
        After verifying that the move is a valid move then by the definition of the game it "flips the piece
        to be the appropriate color of the player
        :param row: defined by the first number in the player move
        :param column: defined by the second number in the player move
        :param direction: steps through the possible "directions" in the for loop within the make_move method
        :param color: player defined color to make a move
        :return:
        changes the value of the position the player wants to make a move to corresponding with the player's color
        """
        move_column, move_row = row + direction[0], column + direction[1]
        if self._board[move_column][move_row] == 'X' or 'O':
            return
        while self._board[move_row][move_column] != '.' and self._board[move_row][move_column] != '.':
            if self._board[move_column][move_row] == 'X' or 'O':
                while (move_column, move_row) != (row, column):
                    if color == 'white':
                        self._board[move_column][move_row] = 'O'
                    elif color == 'black':
                        self._board[move_column][move_row] = 'X'
                    move_column -= direction[0]
                    move_row -= direction[1]
                return
            move_column += direction[0]
            move_row += direction[1]

    def player_available_moves(self):
        """
        Sets up the move check to verify whether the game is over based on overall available moves.
        :return:
        returns TRUE or FALSE for whether there are still available moves without specifying the player or color.
        """
        for row in range(1, 9):
            for column in range(1, 9):
                if self._board[row][column] == '.':
                    for player in self._players:
                        if self.validate_move(row, column, player._color):
                            return True
        return False
