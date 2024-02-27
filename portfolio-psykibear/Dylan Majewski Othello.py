# Author: Dylan Majewski
# GitHub username: DylanMajewski
# Date: 5-24-2023
# Description: Portfolio Project; codes othello to be played with two players and enforces rules
# extra long docstrings for Halfway Progress Report

class Player:
    """Represents a Player with a name and color to be used by Othello Class"""

    def __init__(self, name, color):
        """
        Constructor for Player class.
        Takes parameters name and color both as strings and initializes respective members.
        All data members are private.
        """
        self._name = name
        self._color = color

    def get_name(self):
        """take no parameters; returns name of player"""
        return self._name

    def get_color(self):  # I didn't use this since I made set list positions for each player color
        """take no parameters; returns color of player"""
        return self._color

    def set_name(self, name):
        """takes one parameter name as a string and sets name attribute to that"""
        self._name = name

    def set_color(self, color):
        """takes one parameter color as a string and sets color attribute to that"""
        self._color = color


class Othello:
    """
    Represents a game of Othello with players and a board that will facilitate play in its methods.
    It uses a list Player Objects to store player information
    """

    def __init__(self):
        """
        Constructor for Othello class. Takes no parameters.
        Initializes the board with two black and white pieces each in correct positions.
        Initializes empty list for players to be added to in create_player().
        Initializes directions for _flipper().
        Initializes empty list of moves to be populated by make_move(), checked by _valid_turn(),
        and printed by print_board().
        Initializes dictionary of color codes to easily convert.
        All data members are private.
        """

        self._board = [
            ["*", "*", "*", "*", "*", "*", "*", "*", "*", "*"],  # row 0
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],  # row 1
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],  # row 2
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],  # row 3
            ["*", ".", ".", ".", "O", "X", ".", ".", ".", "*"],  # row 4
            ["*", ".", ".", ".", "X", "O", ".", ".", ".", "*"],  # row 5
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],  # row 6
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],  # row 7
            ["*", ".", ".", ".", ".", ".", ".", ".", ".", "*"],  # row 8
            ["*", "*", "*", "*", "*", "*", "*", "*", "*", "*"]  # row 9
        ]  # X is black, O is white, * is edge, . is empty space

        self._players = [None, None]  # black, white
        self._directions = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        # up, down, left, right, up-left, up-right, down-left, down-right
        self._moves = []  # [{color: color, position: coords}]; index + 1 is move number
        self._color_codes = {"black": "X", "white": "O"}
        self._game_over = False

    def print_board(self, coords=None):
        """
        takes one optional parameter: coords
        if coords is not Falsey, board will print with coordinate indicators (not README required).
        otherwise will print plainly
        """

        if coords:
            print("  C a b c d e g h i")
            print("    1 2 3 4 5 6 7 8")
        for row_num, row in enumerate(self._board):
            if coords and not row_num:
                print("R", ' '.join(row))
            elif coords and row_num == 9:
                print(" ", ' '.join(row))
            elif coords:
                print(row_num, ' '.join(row))
            else:
                print(' '.join(row))

    def print_moves(self, system=None):
        """
        not README required
        Prints moves that have been made in same format as entered as to be copied for other use
        One optional parameter: system
        if nothing passed, moves will be printed as they were entered
        passing 'Letters' will print all as ("column letter", row integer)
        passing 'Numbers' will print all as (row integer, column integer)
        """

        for index, move in enumerate(self._moves):
            if not system:
                print("Move " + str(index + 1) + ":", '"' + move["color"] + '",', move["position"])
            elif system == "Letters":
                if type(move["position"][0]) is int:
                    print("Move " + str(index + 1) + ":", '"' + move["color"] + '",', ((chr(move["position"][1] + 96)),
                                                                                       move["position"][0]))
                else:
                    print("Move " + str(index + 1) + ":", '"' + move["color"] + '",', move["position"])
            elif system == "Numbers":
                if type(move["position"][0]) is str:
                    print("Move " + str(index + 1) + ":", '"' + move["color"] + '",', (move["position"][1],
                                                                                       (ord(move["position"][0]) - 96)))
                else:
                    print("Move " + str(index + 1) + ":", '"' + move["color"] + '",', move["position"])

    def create_player(self, player_name, color):
        """
        Takes two parameters: player_name and color
        player_name is a string
        color must be "black" or "white"
        creates player object of passed name and color and adds to player list inside Othello object
        passing the same color multiple times will update player name of that color
        """

        if color == "black":
            if not self._players[0]:
                self._players[0] = Player(player_name, color)
            else:
                self._players[0].set_name(player_name)
        if color == "white":
            if not self._players[1]:
                self._players[1] = Player(player_name, color)
            else:
                self._players[1].set_name(player_name)

    def return_winner(self, count=None):
        """
        Take one optional parameter: count (not README required)
        calls counter() to determine who has won or is winning if count is not passed
        count is a list of [number black, number white] and if passed calculates the winner from that
        Returns string saying winner or tie.
        """

        if not count:
            # both return_winner() and play_game() have to figure out who won,
            # so when calling from play_game() I let it do the work
            count = self._counter()  # black, white

        if self._game_over:
            if count[0] > count[1]:
                if self._players[0]:
                    return "Winner is black player: " + self._players[0].get_name()
                else:
                    return "Winner is black player"  # game could be played without players
            elif count[0] < count[1]:
                if self._players[1]:
                    return "Winner is white player: " + self._players[1].get_name()
                else:
                    return "Winner is white player"
            else:
                return "It's a tie"
        else:
            if count[0] > count[1]:
                if self._players[0]:
                    return "Black player is winning: " + self._players[0].get_name()
                else:
                    return "Black player is winning"  # game could be played without players
            elif count[0] < count[1]:
                if self._players[1]:
                    return "White player is winning: " + self._players[1].get_name()
                else:
                    return "White player is winning"
            else:
                return "It's currently a tie"

    def return_available_positions(self, color, letter=None):
        """
        takes one mandatory parameter: color
        and one optional parameter: letter (not README required)
        color is a string that indicates which color's valid moves are to be returned.
        calls _flipper() with color code, (row integer, column integer), and each direction without move activation
        saves all valid positions as returned true by _flipper()
        if something not Falsey is passed for letter, returned values will be ("column letter", row integer),
        otherwise will return as (row integer, column integer).
        used by play_game() and _valid_turn().
        returns list of available positions.
        """

        available_positions = []

        for row_num, row in enumerate(self._board):
            for col_num, element in enumerate(row):
                possible = False
                if element == ".":  # goes through every element and only checks empty spaces
                    for direction in self._directions:  # runs every direction
                        if self._flipper(self._color_codes[color], (row_num, col_num), direction):
                            # if any direction works, then the position works, and we don't need to check more
                            possible = True
                            break
                if possible and letter:  # if letters format, convert to that
                    available_positions.append((chr(col_num + 96), row_num))
                elif possible:
                    available_positions.append((row_num, col_num))

        return available_positions

    def make_move(self, color, piece_position):
        """
        take two parameters: color and piece_position
        color is a string that indicates which color is making the move, converts it to color code.
        piece_position is a tuple of the position that the chip will be placed and does so.
        piece_position can be either (row integer, column integer) or ("column letter", row integer)
        calls _flipper() with color code, position as (row integer, column integer), direction, and move activation
        saves the move as entered into the moves member
        returns the board
        this method does not respect move validity
        """

        original_input = piece_position

        if type(piece_position[0]) is str:  # converts letter to integer so standard notation can be used
            piece_position = piece_position[1], ord(piece_position[0].lower()) - 96

        row_num, col_num = piece_position
        color_code = self._color_codes[color]

        self._board[row_num][col_num] = color_code  # sets position to color code

        for direction in self._directions:  # for every direction, flip pieces if possible
            self._flipper(color_code, piece_position, direction, True)  # True flips

        self._moves.append({"color": color, "position": original_input})  # adds move to moves as inputted

        return self._board

    def play_game(self, color, piece_position, other_color=None):
        """
        take two parameters: color and piece_position
        color is a string that indicates which color is making the move.
        piece_position is a tuple of the position that the chip will be placed.
        piece_position can be either (row integer, column integer) or ("column letter", row integer).
        calls _valid_turn() with color to see if it's colors turn, and if so will save the returned other color.
        checks to see if position is valid in return_available_positions() and if not prints list of available positions
        in inputted position system.
        if valid turn and move, then it calls make_move() with same passed values.
        after move is over, it calls return_available_positions() for both colors, and if both empty, calls
        counter() and prints the respective scores for each player, then simply calls self.return_winner()
        Only will return "Invalid move" only if an invalid move has been made
        """

        if not other_color:  # this is only here so that _valid_turn() isn't called twice when using play_game_simple()
            other_color = self._valid_turn(color)  # returns "Invalid move" if invalid, otherwise the other color
            # autograder hates walrus notation

            if other_color == "Invalid move":  # checks if turn order is correct; not in README
                return "Invalid move"

        if type(piece_position[0]) is str:  # converts letter to lowercase and tells positions to return with letters
            available_positions = self.return_available_positions(color, True)
            piece_position = piece_position[0].lower(), piece_position[1]
        else:
            available_positions = self.return_available_positions(color)

        if piece_position not in available_positions:  # checks to see if passed position is valid, returns valid moves
            print("Here are the valid moves:", available_positions)
            return "Invalid move"

        self.make_move(color, piece_position)  # make_move() actually executes; play_game() only checks validity

        if not self.return_available_positions(color) and not self.return_available_positions(other_color):
            # if there are no more available positions for either player after move is made, the game is over
            self._game_over = True
            count = self._counter()  # black, white

            print("Game is ended white piece:", count[1], "black piece:", count[0])

            self.return_winner(count)
            # README simply says to call it, not return it; I pass the count to avoid double calculations

    def play_game_simple(self, play):  # bonus; not in README
        """
        not README required
        takes one parameter: play
        parameter is either col letter + row num or row num + col num, eg "b4" = "42"
        determines current color's turn as returned by _valid_turn()
        calls and returns play_game() with current color and position as tuple
        """

        color, other_color = self._valid_turn()  # gets the color of the current turn and other color or "Invalid move"

        if color == "Invalid move":  # will only trip if game is over
            return "Invalid move"

        if type(play[0]) is str:
            first = play[0]
        else:
            first = int(play[0])

        return self.play_game(color, (first, int(play[1])), other_color)

    def play_game_quick(self, plays):
        """
        not README required
        takes one parameter: plays
        plays is a string of moves as copied from List of Moves in games on https://www.liveothello.com/livegames.php
        like "d3e3f4g3f3c5h3f2c4c3e2e1b3h4h5a3"
        translates that string to be formatted to pass into play_game_simple()
        """

        for index, character in enumerate(plays):
            if not index % 2:
                self.play_game_simple(plays[index] + plays[index + 1])

    def _flipper(self, color_code, piece_position, direction, move=None):
        """
        takes three mandatory parameters: color_code, piece_position, and direction
        takes on optional parameter: move
        color_code is a string "X" or "O" for black and white respectively
        piece_position is a tuple of (row integer, column integer)
        direction is a tuple that indicates coordinate displacement
        move is an indicator that says to flip pieces or not
        checks pieces in passed direction to see if a move is valid this way, recursively calls itself
        returns true for possible and false for not possible; only used by return_available_positions()
        if possible and a move is indicated, it flips the pieces as the recursion returns up
        """

        row_num, col_num = piece_position  # separates coords
        row_change, col_change = direction  # I structured direction to be similar to be easier for parallel coding

        next_row = row_num + row_change
        next_col = col_num + col_change
        next_val = self._board[next_row][next_col]

        if next_val == color_code and self._board[row_num][col_num] == ".":
            # stops returning incorrect true if next tile from open space matches; doesn't affect flipping behavior
            return False

        if next_val == "*" or next_val == ".":
            # if next position is blank or an edge, then it did not find same color piece
            return False

        if next_val == color_code:  # if same color is found, then direction works, returns True
            return True

        if self._flipper(color_code, (next_row, next_col), direction, move):
            # if next piece isn't edge, empty, or same, it is the other color and recursion continues in same direction
            if move:  # if recursion is true, then flip piece if making a move, and regardless return true
                self._board[next_row][next_col] = color_code
            return True

        return False

    def _counter(self):
        """
        takes no parameters
        returns list of each players' count [black, white]
        """

        counter = [0, 0]  # black, white

        for row in self._board[1:9]:  # skips boundaries
            for element in row[1:9]:
                if element == "X":
                    counter[0] += 1
                elif element == "O":
                    counter[1] += 1

        return counter

    def _valid_turn(self, color=None):  # bonus; not in README
        """
        takes optional parameter: color
        returns the color of the current turn if color is not passed
        if color string is passed, it tests to see if it is the current turn
        (black starts, colors alternate unless one doesn't have moves)
        if it is not the passed color's turn, then it prints text to indicate and returns "Invalid move"
        if it is the passed color's turn, then it returns the other color
        """

        if self._game_over:
            print("The game is over; no more moves can be made")
            if not color:
                return "Invalid move", "expects a second value here"
            return "Invalid move"

        if not self._moves and (not color or color == "white"):  # if no moves have been made, black must start
            if not color:
                return "black", "white"
            print("Black makes the first move")
            return "Invalid move"

        if not color:
            test_color = self._moves[-1]["color"]  # if returning current turn's color, then this is needed below
        else:
            test_color = color

        if test_color == "white":
            other_color = "black"
        else:
            other_color = "white"

        if self._moves and self._moves[-1]["color"] == test_color and self.return_available_positions(other_color):
            # checks that players take turns unless the other player can't; make_move() uses are recorded
            if not color:
                return other_color, test_color
            print(other_color[0].upper() + other_color[1:] + "'s turn")
            return "Invalid move"

        if not color:  # if color not passed, then expected to return the current turn's color
            return test_color, other_color
        return other_color  # otherwise expected to return the other color


# Hassan 3 – 61 Verstuyft J. (European Grand Prix Ghent 2017)
# https://www.liveothello.com/livegames.php?GameID_0=5137&TournamentID=350
# game = Othello()
# game.create_player("VERSTUYFT", "white")
# game.create_player("HASSAN", "black")
# game.play_game("black", (8, 3))  # invalid
# game.play_game("black", ("d", 3))
# game.play_game("white", ("h", 5))  # invalid
# game.play_game("white", (8, 5))  # invalid
# game.play_game("white", (3, 5))
# game.play_game("black", (4, 6))
# game.play_game("white", (3, 7))
# game.play_game("black", (3, 6))
# game.play_game("white", (5, 3))
# game.play_game("black", (3, 8))
# game.play_game("white", (2, 6))
# game.play_game("black", (4, 3))
# game.play_game("white", (3, 3))
# game.play_game("black", (2, 5))
# game.play_game("white", (1, 5))
# game.play_game("black", (3, 2))
# game.play_game("white", (4, 8))
# game.play_game("black", (5, 8))
# print(game.return_winner())
# game.create_player("test", "white")
# game.play_game("white", (3, 1))
# game.print_board()
# print(game.return_winner())
# game.print_moves()

# Hassan 3 – 61 Verstuyft J. (European Grand Prix Ghent 2017)
# https://www.liveothello.com/livegames.php?GameID_0=5137&TournamentID=350
# game = Othello()
# game.create_player("VERSTUYFT", "white")
# game.create_player("HASSAN", "black")
# game.play_game_quick("d3e3f4g3f3c5h3f2c4c3e2e1b3h4h5a3")
# game.print_board()
# game.print_moves()

# KASHIWABARA 32 – 32 TASTET (European Othello Championship 2023 round 6)
# https://www.liveothello.com/livegames.php?GameID_0=9453&TournamentID=615&GameID_1=0
# game = Othello()
# game.create_player("TASTET", "white")
# game.create_player("KASHIWABARA", "black")
# game.play_game_simple("c4")
# game.play_game_quick("e3f6e6f5c5f4g6f7d6e7d8h6d3b5b4c7d7c3a6b3a3f2f3e8c6c8g4b6g5h"
#                      "5f1h4g7d2g8c2e2e1a7g1c1g3h3d1h1b1f8b2a1h8h7h2g2a4a5a2b8a8b7")
# game.print_board()
# print(game.return_winner())
# game.print_moves()

# game = Othello()
# game.create_player("Helen", "white")
# game.create_player("Leo", "black")
# game.make_move("black", (5, 6))
# game.print_board()
# game.play_game("white", (7, 6))
# print(game.return_available_positions("black"))
# game.play_game("black", (3, 3))
# game.play_game("white", (4, 6))
# game.print_board()
# print(game.return_available_positions("black"))
# game.play_game("black", (3, 3))
# game.print_board()
# game.play_game("black", (3, 5))
# game.print_moves()
#
# test = Othello()
# test.print_board()
# print(test.return_available_positions("white"))
# test.make_move("black", (3, 4))
# test.print_board()
# test.make_move("white", (3, 3))
# test.print_board()
