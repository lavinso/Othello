# Author: Sonja Lavin
# GitHub username: lavinso
# Date: 5/22/23
# Description: Portfolio Project. Write a class that allows two people to play text-based Othello.
# In this game, two players take turns placing their colored pieces on 8x8 board. The objective is to capture
# the opponent's pieces and have the majority of your own pieces on the board at the end of the game


class Board:
    """
    A game board is represented by a 10x10 grid.
    Edge: * (star)
    Black piece: X
    White piece: O
    Empty space: .  (dot)
    Each position on the board is represented by a (row, column) pair.
    """
    def __init__(self, number_rows=10, number_columns=10):
        """
        Initializes board class. Can take no parameters and assigns default value of 10 for row and column. For
        othello game, this is the correct number of rows and columns. However, if someone wants to change the grid,
        they can by passing different values as parameters. All data members are private.
        """
        self._number_rows = number_rows
        self._number_columns = number_columns
        # if I wanted to make it so user cannot change the size of the game board, I would have the init method take no
        # parameters and then assign data members self._row = 10 and self_column = 10
        self._game_board = []  # initializes game_board as an empty list
        for _ in range(self._number_rows - 2):
            # start filling in the game play part of the board, add top and bottom edges at end
            row = ["*"]
            # starts a new row, represented by a list, starting with edge symbol (*)
            for _ in range(self._number_columns-2):
                row.append(".")
                # fills in rest of row with . (dot) until second to last symbol
            row.append("*")
            # adds edge symbol (*) to end of the list
            self._game_board.append(row)
            # adds the row to the body, loop continues until you have 8 body rows
        self._game_board.insert(0, ["*" for _ in range(self._number_columns)])
        # adds the top boarder row
        self._game_board.append(["*" for _ in range(self._number_columns)])
        # adds the bottom border row

    def get_game_board(self):
        """returns game board"""
        return self._game_board

    def display_board(self):
        """returns the board as a 2d representation"""
        board_string = ""
        for row in self._game_board:
            board_string += " ".join(row) + "\n"
        return board_string

    def add_tokens_to_start_game(self):
        """adds initial tokens to board for start of game"""
        self._game_board[4][4] = "O"
        # if you wanted to make this generalizable to larger boards, it would be
        # self._body[int(number_rows/2 - 1)][int(number_columns/2-1)]
        self._game_board[5][5] = "O"
        # if you wanted to make this generalizable to larger boards, it would be
        # self._body[int(number_rows/ 2)][int(number_columns/ 2)]
        self._game_board[4][5] = "X"
        # if you wanted to make this generalizable to larger boards, it would be
        # self._body[int(number_rows/2-1)][int(number_columns/ 2)]
        self._game_board[5][4] = "X"
        # if you wanted to make this generalizable to larger boards, it would be
        # self._body[int(number_rows/2)][int(number_columns/ 2 - 1)]

    def add_change_tokens(self, position, token):
        """function to be used by othello class to add or change tokens on the board.
        parameters: position is a list [row, column]
        token = "X" or "O"
        """
        self._game_board[position[0]][position[1]] = token

    def count_black_tokens(self):
        """returns the number of black tokens (X's) on the board. To be called on by the Othello class"""
        count = 0
        for row, row_list in enumerate(self.get_game_board()):  # iterates through every row looking for X
            for column, value in enumerate(row_list):
                if value == "X":
                    count += 1
        return count

    def count_white_tokens(self):
        """returns the number of white tokens (O's) on the board. To be called on by the Othello class"""
        count = 0
        for row, row_list in enumerate(self.get_game_board()):  # iterates through every row looking for O
            for column, value in enumerate(row_list):
                if value == "O":
                    count += 1
        return count


class Player:
    """
    Represents a player in the game. Contains Player name (string) and Piece color (string): "black" or "white".
    """
    def __init__(self, player_name, piece_color):
        self._player_name = player_name
        self._piece_color = piece_color
        # color can be "black" or "white"
        if self._piece_color == "white":
            self._token = "O"
        else:
            self._token = "X"

    def get_player_name(self):
        """returns player name"""
        return self._player_name

    def get_piece_color(self):
        """returns player's color"""
        return self._piece_color

    def set_name(self, new_name):
        """changes player's name"""
        self._player_name = new_name

    def set_color(self, new_color):
        """changes player's color"""
        self._piece_color = new_color

    def get_token(self):
        """returns players token, X or O"""
        return self._token


class Othello:
    """
    Object that represents the game as played.
    It contains information about the players and the board, so it must communicate with these classes.
    Access each position value on the board by ** self._board[row][column].
    """

    def __init__(self):
        self._board = Board()
        self._board.add_tokens_to_start_game()  # initializes the board with starting tokens
        self._player_list = []  # list of player objects
        self._black_player = None  # space holder for player object after player is created
        self._white_player = None  # space holder for player object after player is created

    def look_up_player_by_color(self, piece_color):
        """internal function to return the Player object corresponding to the color"""
        for player_object in self._player_list:
            if player_object.get_piece_color() == piece_color:
                return player_object
        return None

    def create_player(self, player_name, piece_color):
        """ Creates a player object with the given name and color and adds it to the player list"""
        if piece_color == "black":
            self._black_player = Player(player_name, piece_color)
            self._player_list.append(self._black_player)
        if piece_color == "white":
            self._white_player = Player(player_name, piece_color)
            self._player_list.append(self._white_player)

    def print_board(self):
        """Uses method from Board class to print out the board in 2d, including the boundaries"""
        print(self._board.display_board())

    def return_available_positions(self, piece_color, current=None, compare=None, direction=None, valid_moves=None):
        """ Checks board for all possible positions for player to move, returns a list of these positions"""
        player = self.look_up_player_by_color(piece_color)  # instead, I could make an if statement
        # if piece_color = "white" player = self._white_player. I could also have used a dictionary instead of a list
        # for the player list where the keyword is "black" or "white" and the value is the player. The readme
        # specifically mentions a player list though, so I did not go this route.
        if player == self._black_player:
            opponent = self._white_player
        else:
            opponent = self._black_player

        if current is None:  # first time function is called
            valid_moves = []
            for row, row_list in enumerate(self._board.get_game_board()):
                # iterates through every row looking for player's position, it would be better to skip row 0 and 9
                for column, value in enumerate(row_list):
                    if value == player.get_token():
                        current = (row, column)  # this is the coordinates for the player's position
                        if self._board.get_game_board()[row][column+1] == opponent.get_token():
                            self.return_available_positions(piece_color, current, (row, column+2), "right", valid_moves)
                        if self._board.get_game_board()[row][column-1] == opponent.get_token():
                            self.return_available_positions(piece_color, current, (row, column - 2), "left", valid_moves)
                        if self._board.get_game_board()[row+1][column] == opponent.get_token():
                            self.return_available_positions(piece_color, current, (row+2, column), "down", valid_moves)
                        if self._board.get_game_board()[row-1][column] == opponent.get_token():
                            self.return_available_positions(piece_color, current, (row-2, column), "up", valid_moves)
                        if self._board.get_game_board()[row-1][column+1] == opponent.get_token():
                            self.return_available_positions(piece_color, current, (row-2, column+2), "diagonal up right", valid_moves)
                        if self._board.get_game_board()[row+1][column+1] == opponent.get_token():
                            self.return_available_positions(piece_color, current, (row+2, column+2), "diagonal down right", valid_moves)
                        if self._board.get_game_board()[row-1][column-1] == opponent.get_token():
                            self.return_available_positions(piece_color, current, (row-2, column-2), "diagonal up left", valid_moves)
                        if self._board.get_game_board()[row+1][column-1] == opponent.get_token():
                            self.return_available_positions(piece_color, current, (row+2, column-2), "diagonal down left", valid_moves)

        else:
            if self._board.get_game_board()[compare[0]][compare[1]] == ".":
                # if there is a player piece, opponent piece(s), then open space
                valid_moves.append(compare)
                return valid_moves

            if self._board.get_game_board()[compare[0]][compare[1]] == player.get_token() or self._board.get_game_board()[compare[0]][compare[1]] == "*":
                # if the next position is the player's token or edge it is not a valid move, do not add to the list
                return

            if self._board.get_game_board()[compare[0]][compare[1]] == opponent.get_token():
                # if there is another opponent token in the line, continue to follow to see if there is an open position
                if direction == "right":
                    self.return_available_positions(piece_color, current, (compare[0], compare[1] + 1), "right", valid_moves)
                if direction == "left":
                    self.return_available_positions(piece_color, current, (compare[0], compare[1] - 1), "left", valid_moves)
                if direction == "down":
                    self.return_available_positions(piece_color, current, (compare[0] + 1, compare[1]), "down", valid_moves)
                if direction == "up":
                    self.return_available_positions(piece_color, current, (compare[0] - 1, compare[1]), "up", valid_moves)
                if direction == "diagonal up right":
                    self.return_available_positions(piece_color, current, (compare[0] - 1, compare[1] + 1), "diagonal up right", valid_moves)
                if direction == "diagonal down right":
                    self.return_available_positions(piece_color, current, (compare[0] + 1, compare[1] + 1), "diagonal down right", valid_moves)
                if direction == "diagonal up left":
                    self.return_available_positions(piece_color, current, (compare[0] - 1, compare[1] - 1), "diagonal up left", valid_moves)
                if direction == "diagonal down left":
                    self.return_available_positions(piece_color, current, (compare[0] + 1, compare[1] - 1), "diagonal down left", valid_moves)

        return valid_moves

    def return_winner(self):
        """
        Returns 'Winner is white player: player’s name' when white player wins the game.
        Returns 'Winner is black player: player’s name' when black player wins the game.
        Returns 'It's a tie' if black and white player has the same number of pieces on the board when the game ends.
        """
        # function is called after game has ended, and it has been verified that neither player has any available moves
        white_token_count = self._board.count_white_tokens()
        black_token_count = self._board.count_black_tokens()
        if white_token_count > black_token_count:
            return "Winner is white player:", self._white_player.get_player_name()
        if black_token_count > white_token_count:
            return "Winner is black player:", self._black_player.get_player_name()
        if black_token_count == white_token_count:
            return "It's a tie"

    def make_move(self, color, piece_position, compare=None, direction=None, possible_flip=None):
        """
        Puts a piece of the specified color at the given position and updates the board accordingly, then returns
        the current board (as a 2d list). This is an internal method and is meant to be called by play_game.
        Assumes only valid positions are passed.
        """

        player = self.look_up_player_by_color(color)
        if player == self._black_player:
            opponent = self._white_player
        else:
            opponent = self._black_player

        if compare is None:  # first time function is called
            row = piece_position[0]
            column = piece_position[1]
            self._board.add_change_tokens([piece_position[0], piece_position[1]], player.get_token())
            # places players token in desired spot, self._board.get_game_board()[row][column] = player.get_token()

            possible_flip = []
            if self._board.get_game_board()[row][column+1] == opponent.get_token():
                possible_flip.append((row, column+1))
                self.make_move(color, piece_position, [row, column+2], "right", possible_flip)
            if self._board.get_game_board()[row][column-1] == opponent.get_token():
                possible_flip.append((row, column - 1))
                self.make_move(color, piece_position, [row, column-2], "left", possible_flip)
            if self._board.get_game_board()[row+1][column] == opponent.get_token():
                possible_flip.append((row+1, column))
                self.make_move(color, piece_position, [row+2, column], "down", possible_flip)
            if self._board.get_game_board()[row-1][column] == opponent.get_token():
                possible_flip.append((row-1, column))
                self.make_move(color, piece_position, [row-2, column], "up", possible_flip)
            if self._board.get_game_board()[row+1][column+1] == opponent.get_token():
                possible_flip.append((row+1, column+1))
                self.make_move(color, piece_position, [row+2, column+2], "diagonal down right", possible_flip)
            if self._board.get_game_board()[row-1][column+1] == opponent.get_token():
                possible_flip.append((row-1, column+1))
                self.make_move(color, piece_position, [row-2, column+2], "diagonal up right", possible_flip)
            if self._board.get_game_board()[row+1][column-1] == opponent.get_token():
                possible_flip.append((row+1, column-1))
                self.make_move(color, piece_position, [row+2, column-2], "diagonal down left", possible_flip)
            if self._board.get_game_board()[row-1][column-1] == opponent.get_token():
                possible_flip.append((row-1, column-1))
                self.make_move(color, piece_position, [row-2, column-2], "diagonal up left", possible_flip)

        else:
            if self._board.get_game_board()[compare[0]][compare[1]] == player.get_token():
                # if there is an opponent in between two player pieces
                if isinstance(possible_flip[0], tuple):  # if there are multiple positions to flip
                    for position in possible_flip:
                        self._board.add_change_tokens((position[0], position[1]), player.get_token())
                        # flips all opponents tokens in the list
                    return
                else:  # if there is only one position to flip
                    position = possible_flip
                    self._board.add_change_tokens((position[0], position[1]), player.get_token())  # flips token
                    return

            elif self._board.get_game_board()[compare[0]][compare[1]] == "*" or self._board.get_game_board()[compare[0]][compare[1]] == ".":
                # if there are not two player pieces in between consecutive opponent pieces
                possible_flip.clear()  # resets list so that positions stored in this recursive step are cleared.
                return

            elif self._board.get_game_board()[compare[0]][compare[1]] == opponent.get_token():
                possible_flip.append((compare[0], compare[1]))
                if direction == "right":
                    self.make_move(color, piece_position, [compare[0], compare[1]+1], "right", possible_flip)
                if direction == "left":
                    self.make_move(color, piece_position, [compare[0], compare[1] - 1], "left", possible_flip)
                if direction == "down":
                    self.make_move(color, piece_position, [compare[0]+1, compare[1]], "down", possible_flip)
                if direction == "up":
                    self.make_move(color, piece_position, [compare[0]-1, compare[1]], "up", possible_flip)
                if direction == "diagonal down right":
                    self.make_move(color, piece_position, [compare[0] +1, compare[1]+1], "diagonal down right", possible_flip)
                if direction == "diagonal up right":
                    self.make_move(color, piece_position, [compare[0] - 1, compare[1] + 1], "diagonal up right", possible_flip)
                if direction == "diagonal down left":
                    self.make_move(color, piece_position, [compare[0] + 1, compare[1] - 1], "diagonal down left", possible_flip)
                if direction == "diagonal up left":
                    self.make_move(color, piece_position, [compare[0] - 1, compare[1] - 1], "diagonal down left", possible_flip)

        return self._board.get_game_board()

    def play_game(self, piece_color, piece_position):
        """ Checks if player with the given color can move to given position. If position is an invalid move, returns
        "Invalid move", and prints "Here are the valid moves:" followed by a list of possible positions. If the position
        is valid, makes that move and updates the board and player's positions list. If the game is ended at that point,
        the function prints "Game is ended white piece: number  black piece: number" and calls the return_winner method.
        """

        row = piece_position[0]
        column = piece_position[1]
        legal_move = False
        for position in self.return_available_positions(piece_color):
            if position == (row, column):
                self.make_move(piece_color, piece_position)
                # if position is a valid move, makes the move by placing player token and updating the board
                legal_move = True

        if not legal_move:
            # if the position is not a valid move, prints a list of valid moves and returns invalid move.
            print("Here are the valid moves:", self.return_available_positions(piece_color))
            return "Invalid move"

        if self.return_available_positions("black") == [] and self.return_available_positions("white") == []:
            print("Game is ended white piece:", self._board.count_white_tokens(), "black piece:", self._board.count_black_tokens())
            self.return_winner()

board = Board()
game = Othello()
game.print_board()
game.create_player("Fiona", "black")
game.create_player("Mom", "white")
game.play_game("black", (5, 6))
game.print_board()
game.play_game("white", (4, 6))
game.print_board()
game.play_game("black", (3, 6))
game.print_board()
game.play_game("white", (6, 4))
game.print_board()
game.play_game("black", (4, 3))
game.print_board()
game.play_game("white", (5, 7))
game.print_board()

game.play_game("black", (7, 4))
game.print_board()
game.play_game("white", (3, 3))
game.print_board()
game.play_game("black", (5, 8))
game.print_board()
game.play_game("white", (6, 6))
game.print_board()
game.play_game("black", (3, 4))
game.print_board()
game.play_game("white", (2, 6))
game.print_board()
game.play_game("black", (3, 2))
game.print_board()
game.play_game("white", (2, 2))
game.print_board()
game.play_game("black", (4, 7))
game.print_board()
game.play_game("white", (4, 8))
game.print_board()
game.play_game("black", (2, 7))
game.print_board()
game.play_game("white", (5, 3))
game.print_board()
game.play_game("black", (7, 6))
game.print_board()
game.play_game("white", (8, 6))
game.print_board()
game.play_game("black", (5, 2))
game.print_board()
game.play_game("white", (1, 8))
game.print_board()
game.play_game("black", (1, 6))
game.print_board()
game.play_game("white", (6, 3))
game.print_board()
game.play_game("black", (1, 1))
game.print_board()
game.play_game("white", (2, 5))
game.print_board()
game.play_game("black", (4, 2))
game.print_board()
game.play_game("white", (6, 5))
game.print_board()
game.play_game("black", (2, 4))
game.print_board()
game.play_game("white", (8, 4))
game.print_board()
game.play_game("black", (2, 8))
game.print_board()
game.play_game("white", (5, 1))
game.print_board()
game.play_game("black", (7, 7))
game.print_board()
game.play_game("white", (7, 8))
game.print_board()
game.play_game("black", (7, 3))
game.print_board()
game.play_game("white", (2, 3))
game.print_board()
game.play_game("black", (8, 8))
game.print_board()
game.play_game("white", (7, 2))
game.print_board()
game.play_game("black", (8, 1))
game.print_board()
game.play_game("white", (3, 8))
game.print_board()
game.play_game("black", (1, 3))
game.print_board()
game.play_game("white", (1, 2))
game.print_board()
game.play_game("black", (2, 1))
game.print_board()
game.play_game("white", (1, 4))
game.print_board()
game.play_game("black", (1, 5))
game.print_board()
game.play_game("white", (3, 1))
game.print_board()
game.play_game("black", (3, 5))
game.print_board()
game.play_game("white", (3, 7))
game.print_board()
game.play_game("black", (4, 1))
game.print_board()
game.play_game("white", (5, 1))
game.print_board()
game.play_game("black", (6, 1))
game.print_board()
game.play_game("white", (6, 2))
game.print_board()
game.play_game("black", (6, 7))
game.print_board()
game.play_game("white", (1, 7))
game.print_board()
game.play_game("black", (6, 8))
game.print_board()
game.play_game("white", (7, 1))
game.print_board()
game.play_game("black", (7, 5))
game.print_board()
game.play_game("white", (8, 5))
game.print_board()
game.play_game("black", (8, 3))
game.print_board()
game.play_game("white", (8, 7))
game.print_board()
game.play_game("white", (8, 2))
game.print_board()
print(game.return_winner())
