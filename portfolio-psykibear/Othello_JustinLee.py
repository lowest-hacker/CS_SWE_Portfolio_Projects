# Author: Justin Lee
# GitHub username: joonsmoons
# Date: 5/11/2023
# Description: Class for Player, GameBoard and Othello.

from itertools import chain


class Player:
    """
    Player class represents a player in the game. Used by Othello class.
    This player has a player_name, color("black" or "white") and piece/move("O" or "X").
    """

    def __init__(self, player_name, color):
        """
        The constructor for Fence class. Takes parameters player_name and color.
        Initializes the required data members. All data members are private.

        :param player_name: player name
        :param color: color
        """
        self._player_name = player_name
        self._color = color
        self._move = 'X' if self._color == 'black' else 'O'

    def get_player_name(self):
        """
        Getter method for player_name.
        Used by Othello class to get player's name to print out the winner.

        :return: the player's name
        """
        return self._player_name


class Othello:
    """
    Othello class to represent the Othello game played by two players.
    The "black" colored player always starts first.
    Uses the Player class to initialize the players.
    Returns the 2-D game board if the player makes a valid move,
    or returns available moves if the player makes an invalid move.
    If there is a winner, prints descriptions about the winning player.
    """

    def __init__(self):
        """
        Constructor for the Othello class. Takes no parameters.
        Initializes the 10x10 game board. [where edge="*", black piece="X", white piece="O", empty space="."]
        Also initializes the players dictionary that contain the players playing the game and history of the moves played.
        At the beginning, white pieces are at position (4,4) and (5,5) and black pieces are at (4,5) and (5,4).
        All data members are private.
        """
        board = []
        edges = list(chain(range(9), range(90, 100),
                     range(0, 100, 10), range(9, 100, 10)))
        for i in range(100):
            if i in edges:
                board.append('*')
            else:
                board.append('.')
        self._board = [board[i:i+10] for i in range(0, len(board), 10)]
        self._players = {}
        self._moves = {'X': [], 'O': []}
        self.make_move('black', (4, 5))
        self.make_move('white', (4, 4))
        self.make_move('black', (5, 4))
        self.make_move('white', (5, 5))

    def print_board(self):
        """
        Prints the Othello board in 2D string format.
        Frequently used to check if move is updated after a change.

        :return:
        """
        for row in self._board:
            print(' '.join(row))

    def create_player(self, player_name, color):
        """
        Creates a player with the given name and color("black" or "white") and adds it into the players dictionary.
        Uses Player class to initialize player with the given parameters.

        :param player_name: name of player
        :param color: color of player piece
        :return:
        """
        player = Player(player_name, color)
        move = self.get_move_by_color(color)
        self._players[move] = player

    def get_move_by_position(self, piece_position):
        """
        Gets the current move("O" or "X") given the piece position(e.g. (1,0)).

        :param piece_position: position of the piece
        :return: move of the given position
        """
        return self._board[piece_position[0]][piece_position[1]]

    def get_player_by_move(self, move):
        """
        Gets the player by the move("O" or "X") of the player.

        :param move: move that was played
        :return: the Player object
        """
        return self._players[move]

    @staticmethod
    def get_move_by_color(color):
        """
        Get the move("O" or "X") from the given color("white" or "black").

        :param color: color of the player
        :return: move of the player
        """
        return 'X' if color == 'black' else 'O'

    def get_moves(self, color):
        """
        Get the move("O" or "X") history given the color("white" or "black").

        :param color: color of the player
        :return: history of moves made
        """
        return self._moves[color]

    def return_winner(self):
        """
        Check the number of moves made by each player, and return the winning player(color and name).
        If black and white player has the same number of pieces on the board when the game end, return the tie result.
        Uses the Player's get_player_name() to get the winning player's name.

        :return: description of the game results
            Winner is white player: player_name - if winner is the white player
            Winner is black player: player_name - if winner is the black player
            It's a tie - if there is no winner
        """
        if len(self._moves['O']) > len(self._moves['X']):
            print_result = f"Winner is white player: {self.get_player_by_move('O').get_player_name()}"
            print(print_result)
            return print_result
        elif len(self._moves['O']) < len(self._moves['X']):
            print_result = f"Winner is black player: {self.get_player_by_move('X').get_player_name()}"
            print(print_result)
            return print_result
        else:
            print_result = "It's a tie"
            print(print_result)
            return print_result

    @staticmethod
    def return_shift_position(position, direction):
        """
        Gets the position given the position and direction of the shift.

        :param position: position of player
        :param direction: direction of shift
        :return: new position
        """
        if direction == 'left':
            return position[0], position[1] - 1
        elif direction == 'right':
            return position[0], position[1] + 1
        elif direction == 'top':
            return position[0] - 1, position[1]
        elif direction == 'bottom':
            return position[0] + 1, position[1]
        elif direction == 'top-left':
            return position[0] - 1, position[1] - 1
        elif direction == 'bottom-left':
            return position[0] + 1, position[1] - 1
        elif direction == 'top-right':
            return position[0] - 1, position[1] + 1
        elif direction == 'bottom-right':
            return position[0] + 1, position[1] + 1

    def return_available_position_for_direction(self, position, direction, opponent_move, end_string='.'):
        """
        Return the available positions for a given direction.

        :param position: position of player
        :param direction: direction to check
        :param opponent_move: move of opponent player (opponent is "X" if player is "O", vice versa)
        :param end_string: string that decides the breaking point of the loop
        :return: (available position, history of positions until that position)
        """
        position = self.return_shift_position(position, direction)
        history = []
        while self.get_move_by_position(position) == opponent_move:
            history.append(position)
            position = self.return_shift_position(position, direction)
            if self.get_move_by_position(position) == end_string:
                return position, history

    def return_available_positions(self, player_color):
        """
        Returns all possible positions for the player with the given color to move on the current board.
        It will iterate through all moves played and through all directions to find playable positions.
        To capture pieces, a player must place their piece adjacent to an opponent's piece, forming a
        straight line of adjacent pieces (horizontal, vertical, or diagonal) with their piece at each end.
        Multiple chains/directions of pieces can be captured all at once in a single move, and the captured
        pieces are converted to the capturing player's color.
        The game starts with four pieces placed in the middle of the board, forming a square with
        same-colored pieces on a diagonal.

        :param player_color: color of player ("black" or "white")
        :return: sorted available positions [(x1, y1), (x2, y2), ...]
        """
        move = self.get_move_by_color(player_color)
        positions = self._moves[move]
        opponent_move = 'O' if move == 'X' else 'X'
        available_positions = list()
        for position in positions:
            directions = ['left', 'right', 'top', 'bottom',
                          'top-left', 'bottom-left', 'top-right', 'bottom-right']
            for direction in directions:
                available_position = self.return_available_position_for_direction(
                    position, direction, opponent_move)
                if available_position is not None:
                    available_positions.append(available_position)
        available_positions = sorted(
            list(set([position[0] for position in available_positions])))
        return available_positions

    def make_move(self, player_color, piece_position):
        """
        Puts a piece of the specified color at the given position and updates the board accordingly,
        then return the current board(as a 2d list).
        The method will iterate through all directions to find positions that are to be filled and
        updated them as the move is played.
        Assumes the move is valid.

        :param player_color: color of player ("black" or "white")
        :param piece_position: position of move (x, y)
        :return: game board
        """
        self._board[piece_position[0]][piece_position[1]
                                       ] = self.get_move_by_color(player_color)
        move = self.get_move_by_color(player_color)
        self._moves[move].append(piece_position)
        opponent_move = 'O' if move == 'X' else 'X'
        fill_positions = list()
        directions = ['left', 'right', 'top', 'bottom',
                      'top-left', 'bottom-left', 'top-right', 'bottom-right']
        for direction in directions:
            fill_position = self.return_available_position_for_direction(
                piece_position, direction, opponent_move, move)
            if fill_position is not None:
                fill_positions.append(fill_position)
        fill_positions = list(chain.from_iterable(
            [position[1] for position in fill_positions]))
        for position in fill_positions:
            self._board[position[0]][position[1]] = move
            self._moves[move].append(position)
            self._moves[opponent_move].remove(position)
        return self._board

    def check_game_ended(self):
        """
        Checks if the game has ended.

        :return:
            True - if game ended
            False - if game has not ended
        """
        all_available_positions = len(self.return_available_positions(
            'black')) + len(self.return_available_positions('white'))
        return True if all_available_positions == 0 else False

    def play_game(self, player_color, piece_position):
        """
        Attempts to make a move for the player with the given color at the specified position.
        Returns the winner of the game if game is ended, or the board if the game has not ended,
        or return invalid move if move is invalid and not part of the available positions.

        :param player_color: color of player ("black" or "white")
        :param piece_position: position of player move (x, y)
        :return:
            Output of return_winner() - if game ended
            None - if the game has not ended
            Invalid input - if move is invalid
        """
        available_positions = self.return_available_positions(player_color)
        if piece_position in available_positions:
            self.make_move(player_color, piece_position)
            if self.check_game_ended():
                return self.return_winner()
            else:
                return
        else:
            print("Here are the valid moves:", available_positions)
            return "Invalid move"
