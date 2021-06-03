import random
from copy import deepcopy
import os
import time


def alphabet(letter):
    alphabet = (
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
        'W',
        'X', 'Y',
        'Z')

    return alphabet[letter]


def dictionary_coordinates(board):
    dict_cords_num = all_coordinates(board)
    dict_cords_let = all_coordinates_with_letters(board)
    all_moves_dict = dict(zip(dict_cords_let, dict_cords_num))
    return all_moves_dict


def choose_board_size():
    choose_size = True
    while choose_size:
        try:
            int_size = int(input('Please choose board size from 5 to 10: '))

            if int_size in range(5,11):
                return int_size
        except ValueError:
            print('Incorrect, please choose number between 5 and 10!')


def board_list(choose_board_size):
    board = []
    for row_in_board in range(choose_board_size):
        board.append(['0'] * choose_board_size)
    return board


def board():
    final_list = board_list(choose_board_size())

    return final_list


def print_board_1_player(board1):
    print_numbers(board1, 1)
    for row in range(len(board1)):
        print(end=alphabet(row) + ' ')
        for col in range(len(board1[row])):
            print(end=board1[row][col] + ' ')
        print('')
    print('')


def print_numbers(board, number):
    for players in range(number):
        print(end=' ' * 2)
        for num in range(len(board)):
            print(end=str(num + 1) + ' ')
        print(end='\t')
    print('')


def print_board_2_players(board1, board2):
    print_numbers(board1, 2)
    for row in range(len(board1)):
        print(end=alphabet(row) + ' ')
        for col in range(len(board1[row])):
            print(end=board1[row][col] + ' ')
        print(end='\t' + alphabet(row) + ' ')
        for col in range(len(board2[row])):
            print(end=board2[row][col] + ' ')
        print('')
    print('')


def all_coordinates_with_letters(board):
    moves = []
    for row_coordinate in range(len(board)):
        for col_coordinate in range(len(board[row_coordinate])):
            moves.append(alphabet(row_coordinate) + str(col_coordinate + 1))

    return moves


def all_coordinates(board):
    moves = []
    for row_coordinate in range(len(board)):
        for col_coordinate in range(len(board[row_coordinate])):
            moves.append([row_coordinate, col_coordinate])

    return moves


def check_taken_coordinats(board):
    invalid_moves = []
    for row_coordinate in range(len(board)):
        for col_coordinate in range(len(board[row_coordinate])):
            if board[row_coordinate][col_coordinate] != '0':
                invalid_moves.append([row_coordinate, col_coordinate])

    return invalid_moves


def check_free_coordinats(board):
    valid_moves = []
    for row_coordinate in range(len(board)):
        for col_coordinate in range(len(board[row_coordinate])):
            if board[row_coordinate][col_coordinate] == '0':
                valid_moves.append([row_coordinate, col_coordinate])

    return valid_moves


def check_taken_coordinates_around(taken_coordinates):
    invalid_moves = []
    for list in range(len(taken_coordinates)):
        taken = taken_coordinates[list]
        if taken[0] == 0 and taken[1] == 0:
            invalid_moves.append([taken[0], taken[1]])
            invalid_moves.append([taken[0], taken[1] + 1])
            invalid_moves.append([taken[0] + 1, taken[1]])
        else:
            invalid_moves.append([taken[0], taken[1]])
            invalid_moves.append([taken[0], taken[1] + 1])
            invalid_moves.append([taken[0], taken[1] - 1])
            invalid_moves.append([taken[0] + 1, taken[1]])
            invalid_moves.append([taken[0] - 1, taken[1]])

    no_duplicates = []
    for coordinate in invalid_moves:
        if coordinate not in no_duplicates:
            no_duplicates.append(coordinate)

    return no_duplicates


def valid_move(board):
    free_space = check_free_coordinats(board)
    taken_space = check_taken_coordinates_around(check_taken_coordinats(board))
    valid_move = []
    for coordinate in free_space:
        if coordinate not in taken_space:
            valid_move.append(coordinate)
    return valid_move


def orientation_input():
    input_loop = True
    while input_loop:
        orientation = input('Please, input orientation of the ship: (V)ertical/(H)orizontal ').upper()
        if orientation != 'V' and orientation != 'H':
            print('Please input V for Vertical or H for Horizontal ')
            input_loop = True
        else:
            return orientation


def ai_orientation_input():
    input_loop = True
    choices = ["V", "H"]
    while input_loop:
        ai_orientation = random.choice(choices)

        return ai_orientation


def initial_coordinates(player_board):
    input_loop = True
    while input_loop:
        start = input('Please give initial coordinate:').upper()
        if start not in dictionary_coordinates(player_board).keys():
            print('Please input valid coordinate!')
            input_loop = True
        else:
            return dictionary_coordinates(player_board)[start]


def ship(player_board, length):
    placement_loop = True
    y = valid_move(player_board)

    while placement_loop:
        x = initial_coordinates(player_board)
        if x not in y:
            print('Wrong!')
        if x in y:
            if length == 1:
                player_board[x[0]][x[1]] = 'X'
                return player_board
            if length > 1:
                orientation = orientation_input()

                for leng in range(length):
                    if orientation == 'V':
                        if (x[0] + length) <= len(player_board):
                            player_board[x[0] + leng][x[1]] = 'X'
                        else:
                            print('Wrong!')
                            ship(player_board, length)

                    if orientation == 'H':
                        if (x[1] + length) <= len(player_board):
                            player_board[x[0]][x[1] + leng] = 'X'
                        else:
                            print('Wrong!')
                            ship(player_board, length)
                return player_board


def ai_ship(player_board, length):
    placement_loop = True
    y = valid_move(player_board)

    while placement_loop:
        rand_row = random.randint(0, len(player_board) - 1)
        rand_col = random.randint(0, len(player_board) - 1)
        x = [rand_row, rand_col]

        time.sleep(1)
        if x not in y:
            print('Wrong!')
        if x in y:
            if length == 1:
                player_board[x[0]][x[1]] = 'X'
                return player_board
            if length > 1:
                orientation = ai_orientation_input()

                for leng in range(length):
                    if orientation == 'V':
                        if (x[0] + length) <= len(player_board):
                            player_board[x[0] + leng][x[1]] = 'X'
                        else:
                            print('Wrong!')

                    if orientation == 'H':
                        if (x[1] + length) <= len(player_board):
                            player_board[x[0]][x[1] + leng] = 'X'
                        else:
                            print('Wrong!')

                return player_board


def placement(current_player, mode):
    if mode == "P":
        if len(current_player) == 5 or len(current_player) == 6:
            print_board_1_player(current_player)
            print("You are going to be putting a ships with sizes : 1, 1 and 2")
            ship(current_player, 1)
            os.system("cls")
            print_board_1_player(current_player)
            ship(current_player, 1)
            os.system("cls")
            print_board_1_player(current_player)
            ship(current_player, 2)
            os.system("cls")
            print_board_1_player(current_player)

        elif len(current_player) == 7 or len(current_player) == 8:
            print_board_1_player(current_player)
            print("You are going to be putting a ships with sizes : 1, 2 and 2")
            ship(current_player, 1)
            os.system("cls")
            print_board_1_player(current_player)
            ship(current_player, 2)
            os.system("cls")
            print_board_1_player(current_player)
            ship(current_player, 2)
            os.system("cls")
            print_board_1_player(current_player)

        elif len(current_player) == 9 or len(current_player) == 10:
            print_board_1_player(current_player)
            print("You are going to be putting a ships with sizes : 1, 2 and 3")
            ship(current_player, 1)
            os.system("cls")
            print_board_1_player(current_player)
            ship(current_player, 2)
            os.system("cls")
            print_board_1_player(current_player)
            ship(current_player, 3)
            os.system("cls")
            print_board_1_player(current_player)

    elif mode == "C":
        if len(current_player) == 5 or len(current_player) == 6:
            ai_ship(current_player, 1)
            ai_ship(current_player, 1)
            ai_ship(current_player, 2)

        elif len(current_player) == 7 or len(current_player) == 8:
            ai_ship(current_player, 1)
            ai_ship(current_player, 2)
            ai_ship(current_player, 2)

        elif len(current_player) == 9 or len(current_player) == 10:
            ai_ship(current_player, 1)
            ai_ship(current_player, 2)
            ai_ship(current_player, 3)


def is_over(board_length):
    if len(board_length) == 5 or len(board_length) == 6:
        ships = 4

    elif len(board_length) == 7 or len(board_length) == 8:
        ships = 5

    if len(board_length) == 9 or len(board_length) == 10:
        ships = 6
    return ships


def shooting_phase(enemy_player_board, hidden_board):
    dictionary_rows = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9}
    guess = input("Where do you want to shoot? ").upper()
    list_of_guess_coordinates = list(guess)
    row_position = dictionary_rows[list_of_guess_coordinates[0]]
    column_position = int(list_of_guess_coordinates[1]) - 1
    if enemy_player_board[row_position][column_position] == "X":
        print("CORRECT")
        hidden_board[row_position][column_position] = "H"
        enemy_player_board[row_position][column_position] = "H"

    elif hidden_board[row_position][column_position] == "H":
        print("You already hit it ")
        shooting_phase(enemy_player_board, hidden_board)

    elif hidden_board[row_position][column_position] == "M":
        print("You already missed it ")
        shooting_phase(enemy_player_board, hidden_board)

    else:
        hidden_board[row_position][column_position] = "M"
        print("SORRY")
        time.sleep(2)


def ai_shooting_phase(enemy_player_board, hidden_board):
    rand_row = random.randint(0, len(enemy_player_board) - 1)
    rand_col = random.randint(0, len(enemy_player_board) - 1)

    if enemy_player_board[rand_row][rand_col] == "X":
        hidden_board[rand_row][rand_col] = "H"
        enemy_player_board[rand_row][rand_col] = "H"

    elif hidden_board[rand_row][rand_col] == "H":
        ai_shooting_phase(enemy_player_board, hidden_board)

    elif hidden_board[rand_row][rand_col] == "M":
        ai_shooting_phase(enemy_player_board, hidden_board)

    else:
        hidden_board[rand_row][rand_col] = "M"


def turns_limit():
    limit = int(input("Choose a number between 5 and 50 to settle a limit of turns: "))
    if limit in range(5, 51):
        return limit
    else:
        print("That is wrong, try again")


def who_won(player, hid_board_player1, hid_board_player2):
    lives1 = is_over(player)
    occurances_of_h_2 = sum(s.count("H") for s in hid_board_player2)
    occurances_of_h_1 = sum(s.count("H") for s in hid_board_player1)
    if occurances_of_h_2 == lives1:
        print("Player 1 wins!")
        play_again()
    elif occurances_of_h_1 == lives1:
        print("Player 2 wins!")
        play_again()


def play_again():
    again = input("Do you want to play again: Y/N ").upper()
    if again == "Y":
        main()
    elif again == "N":
        return False
    else:
        print("Try again, I didn't understand it ")


def main():
    os.system("cls")
    print(
        "Welcome in the game of battleships. You will be able to choose, whether you want to play with another person or with a computer.\nAfter you place all of your ships, you will see two board, one on the left is yours with its current state, and on the right is the board of your enemy. Good luck! ")
    to_copy = board()
    player1 = deepcopy(to_copy)
    player2 = deepcopy(to_copy)
    hidden_board_player1 = deepcopy(to_copy)
    hidden_board_player2 = deepcopy(to_copy)
    turns = turns_limit()
    mode = input("Do you want to play with a (P)erson or with a (C)omputer?").upper()
    if mode == "P" or mode == "C":
        os.system("cls")
        if mode == "P":

            placement(player1, "P")
            os.system("cls")
            print("Next player's placement phase")

            placement(player2, "P")
            os.system("cls")

            while True:
                print("Player's 1 move")
                print("Turns left:" + str(turns))
                print_board_2_players(hidden_board_player1, hidden_board_player2)
                shooting_phase(player2, hidden_board_player2)
                turns -= 1
                who_won(player1, hidden_board_player1, hidden_board_player2)
                time.sleep(2)
                os.system("cls")
                print("Player's 2 move")
                print("Turns left:" + str(turns))
                print_board_2_players(hidden_board_player1, hidden_board_player2)
                shooting_phase(player1, hidden_board_player1)
                turns -= 1
                who_won(player1, hidden_board_player1, hidden_board_player2)
                time.sleep(2)
                os.system("cls")

        elif mode == "C":
            placement(player1, "P")
            os.system("cls")
            placement(player2, "C")
            os.system("cls")

            while True:
                print("This is your turn")
                print("Turns left:" + str(turns))
                print_board_2_players(player1, hidden_board_player2)
                shooting_phase(player2, hidden_board_player2)
                turns -= 1
                os.system("cls")
                who_won(player1, hidden_board_player1, hidden_board_player2)
                ai_shooting_phase(player1, hidden_board_player1)
                turns -= 1
                who_won(player1, hidden_board_player1, hidden_board_player2)
    else:
        print("Try again, I didn't understand it ")
        main()


os.system("cls")
print("""
     _           _   _   _           _     _       
    | |         | | | | | |         | |   (_)      
    | |__   __ _| |_| |_| | ___  ___| |__  _ _ __  
    | '_ \ / _` | __| __| |/ _ \/ __| '_ \| | '_ \ 
    | |_) | (_| | |_| |_| |  __/\__ \ | | | | |_) |
    |_.__/ \__,_|\__|\__|_|\___||___/_| |_|_| .__/ 
                                        | |    
                                        |_| 
    
        Cezary Czarkowski
    """)
time.sleep(3)
main()
