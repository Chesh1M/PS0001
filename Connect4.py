import random
import numpy as np
import time

def convert_to_2d(board_1d):
    
    # initialize constant
    NUM_OF_COLS = 7
    
    board_2d = []
    temp = []
    
    # convert 1d list into 2d
    for x in range(int(len(board_1d) / 7)):
        for y in range(NUM_OF_COLS):
            temp.append(board_1d[7 * x + y])
        board_2d.append(temp)
        temp = []
    board_2d.reverse()
    
    return board_2d

def convert_to_1d(board_2d):
    
    # initialize constant
    NUM_OF_COLS = 7
    
    board_1d = np.array(board_2d).reshape(len(board_2d) * NUM_OF_COLS)
    
    return board_1d

def display_board(board):
    
    temp_board = board.copy()
    
    # replace every 0s in temp_board list into a whitespace
    for i in range(len(temp_board)):
        if temp_board[i] == 0:
            temp_board[i] = " "
   
    row_num = int(len(temp_board)/7)
    print("|---|---|---|---|---|---|---|")
    
    for row in range(row_num -1, -1, -1): 
        
        print(f"| {temp_board[row * 7]} | {temp_board[row * 7 + 1]} | {temp_board[row * 7 + 2]} | {temp_board[row * 7 + 3]} | {temp_board[row * 7 + 4]} | {temp_board[row * 7 + 5]} | {temp_board[row * 7 + 6]} |")
        print("|---|---|---|---|---|---|---|")

def check_move(board, turn, col, pop):
    
    # initialize constant
    NUM_OF_COLS = 7
    
    # calculate number of rows, -1 to match index of 0 to X num of rows
    num_of_rows = int((len(board) / NUM_OF_COLS) - 1)

    # player 1 turn
    if turn == 1:
        # check if there is a piece to pop
        if pop == True:
            if board[col] == 1: # check if 1 is available to be popped in the selected column (position of disc is 7 * i + j, i = rows, j = cols). Since checking bottom row, i = 0, leaving just j (column)
                return True
            else:
                return False

        # check if there is an empty spot to place a piece
        if pop == False:
            if board[7 * num_of_rows + col] == 0:
                return True
            else:
                return False

    # player 2 turn
    if turn == 2:
        # check if there is a piece to pop
        if pop == True:
            if board[col] == 2:
                return True
            else:
                return False

        # check if there is an empty spot to place a piece
        if pop == False:
            if board[7 * num_of_rows + col] == 0:
                return True
            else:
                return False


def apply_move(board, turn, col, pop):
    
    # initialize constant
    NUM_OF_COLS = 7
    
    # calculate number of rows, -1 to match index of 0 to X num of rows
    num_of_rows = int((len(board) / NUM_OF_COLS) - 1) # == 5
    temp_board = board.copy()
    
    # player 1 turn
    if turn == 1:
        if pop:  # pop a piece
            for x in range(num_of_rows):
                temp_board[7 * x + col] = temp_board[7 * (x + 1) + col]

            # replace top row with 0 if previously not empty
            if temp_board[7 * num_of_rows + col] != 0:
                temp_board[7 * num_of_rows + col] = 0

        else:  # place a piece
            for x in range(num_of_rows + 1):
                if temp_board[7 * x + col] == 0:
                    temp_board[7 * x + col] = 1
                    break

    # player 2 turn
    if turn == 2:
        if pop:  # pop a piece
            for x in range(num_of_rows):
                temp_board[7 * x + col] = temp_board[7 * (x + 1) + col]

            # replace top row with 0 if previously not empty
            if temp_board[7 * num_of_rows + col] != 0:
                temp_board[7 * num_of_rows + col] = 0

        else:  # place a piece
            for x in range(num_of_rows + 1):
                if temp_board[7 * x + col] == 0:
                    temp_board[7 * x + col] = 2
                    break

    return temp_board


def check_victory(board, who_played):
    
    # initialize constant
    NUM_OF_COLS = 7
    
    # convert board input into 2D list
    board_2d = convert_to_2d(board)
    
    # create winning lists and define player numbers
    if who_played == 1:
        winList1 = ["1111"]
        winList2 = ["2222"]
        other_player = 2
    else:
        winList1 = ["2222"]
        winList2 = ["1111"]
        other_player = 1
    
    # set initial boolean values
    who_played_wins = False
    other_player_wins = False
    
    # here, we convert 4 pieces on the board into a string and check for each player if theirs is contained in the winning lists above
    # check horizontal locations for victory
    for row in range(len(board_2d)):
        for col in range(NUM_OF_COLS - 3):
            
            if str(board_2d[row][col]) + str(board_2d[row][col+1]) + str(board_2d[row][col+2]) + str(board_2d[row][col+3]) in winList1: 
                who_played_wins = True
            
            if str(board_2d[row][col]) + str(board_2d[row][col+1]) + str(board_2d[row][col+2]) + str(board_2d[row][col+3]) in winList2:
                other_player_wins = True
    
    # check vertical locations for victory
    for col in range(NUM_OF_COLS):
        for row in range(len(board_2d) - 3):
            
            if str(board_2d[row][col]) + str(board_2d[row+1][col]) + str(board_2d[row+2][col]) + str(board_2d[row+3][col]) in winList1:
                who_played_wins = True
            
            if str(board_2d[row][col]) + str(board_2d[row+1][col]) + str(board_2d[row+2][col]) + str(board_2d[row+3][col]) in winList2:
                other_player_wins = True

    # check positively sloped diagonals
    for col in range(NUM_OF_COLS - 3):
        for row in range(3, len(board_2d)):
            
            if str(board_2d[row][col]) + str(board_2d[row-1][col+1]) + str(board_2d[row-2][col+2]) + str(board_2d[row-3][col+3]) in winList1:
                who_played_wins = True
            
            if str(board_2d[row][col]) + str(board_2d[row-1][col+1]) + str(board_2d[row-2][col+2]) + str(board_2d[row-3][col+3]) in winList2:
                other_player_wins = True

    # check negatively sloped diagnoals
    for col in range(NUM_OF_COLS - 3):
        for row in range(len(board_2d) - 3):
            
            if str(board_2d[row][col]) + str(board_2d[row+1][col+1]) + str(board_2d[row+2][col+2]) + str(board_2d[row+3][col+3]) in winList1:
                who_played_wins = True
                
            if str(board_2d[row][col]) + str(board_2d[row+1][col+1]) + str(board_2d[row+2][col+2]) + str(board_2d[row+3][col+3]) in winList2:
                other_player_wins = True
    
    if who_played_wins == True and other_player_wins == True: # if both players win after current player pops, victory goes to other player
        return other_player
    
    elif who_played_wins == True: # only current player wins
        return who_played
    
    else:
        return 0 # no win conditions met

def computer_move(board, turn, level):
    
    # initialize constant
    NUM_OF_COLS = 7
    
    # define player/bot numbers
    if turn == 1:
        turn_bot = 1
        turn_player = 2
    elif turn == 2:
        turn_bot = 2
        turn_player = 1

    if level == 1: # easy (computer picks random moves)

        while True:

            col = random.randint(0, 6) # randomly pick column
            pop = random.choice([True, False]) # randomly pick pop or not
            
            if check_move(board, turn_bot, col, pop) == False:
                continue

            else:
                return col, pop
            
    elif level == 2: # medium
        
        while True:

            # initialise list to keep track of scores (default 1) assigned for each move using list comprehension
            # 0: illegal or loses instantly, 1: neither win nor lose, 2: prevents direct loss for bot 3: direct win for bot
            
            scoreList1 = [1 for x in range(7)] # for piece placement
            scoreList2 = [1 for x in range(7)] # for pop move
            
            # look for any moves by bot that directly leads to other player winning, or moves that directly leads to the bot winning
            for col in range(NUM_OF_COLS):
                
                # if bot's piece placement is legal
                if check_move(board, turn_bot, col, False) == True:
                 
                    # bot applies move
                    temp_board1 = apply_move(board, turn_bot, col, False)
                    
                    # if bot directly wins
                    if check_victory(temp_board1, turn_bot) == turn_bot:
                        
                        scoreList1[col] = 3
                        
                        break # bot immediately plays this move to win                    
                    
                    # otherwise, check if this leads to player winning after
                    for col2 in range(NUM_OF_COLS):
                          
                        # if move legal
                        if check_move(temp_board1, turn_player, col2, False) == True:
                             
                            # player applies move
                            temp_board2 = apply_move(temp_board1, turn_player, col2, False)
                              
                            # if player wins
                            if check_victory(temp_board2, turn_player) == turn_player:
                             
                                # bot should not play the initial move
                                scoreList1[col] = 0
                                
                # if bot's piece placement move is illegal
                else:
                    
                    scoreList1[col] = 0
                    
                # if bot's pop move is legal
                if check_move(board, turn_bot, col, True) == True:
                    
                    # bot applies move
                    temp_board1 = apply_move(board, turn_bot, col, True)
                    
                    # if bot directly wins
                    if check_victory(temp_board1, turn_bot) == turn_bot:
                        
                        scoreList2[col] = 3
                        
                        break # bot immediately plays this move to win
                        
                    # otherwise, check if any of player's moves leads to player winning after
                    ## check player's piece placement after bot's move
                    for col2 in range(NUM_OF_COLS):
                        
                        # if move legal
                        if check_move(temp_board1, turn_player, col2, False) == True:
                            
                            # player applies move
                            temp_board2 = apply_move(temp_board1, turn_player, col2, False)

                            # if player wins after player's move
                            if check_victory(temp_board2,turn_player) == turn_player:
                                scoreList2[col] = 0
                    
                    ## check player's pop move after bot's move
                    for col2 in range(NUM_OF_COLS):
                        
                        # if move legal
                        if check_move(temp_board1, turn_player, col2, True) == True:
                            
                            # player applies move
                            temp_board2 = apply_move(temp_board1, turn_player, col, True)

                            # if player wins after player's move
                            if check_victory(temp_board2, turn_player) == turn_player:
                                scoreList2[col] = 0
                        
                # if bot's pop move is illegal
                else:
                    
                    scoreList2[col] = 0
                                                                           
            # look for any direct wins for player in the current board state, and if so, look for ways in which bot can block
            for col in range(NUM_OF_COLS):
                
                # if player's piece placement move is legal
                if check_move(board, turn_player, col, False) == True:
                    
                    # player applies move
                    temp_board1 = apply_move(board, turn_player, col, False)
                    
                    # if player wins from piece placement
                    if check_victory(temp_board1, turn_player) == turn_player:
                        
                        # bot plays that move in place of player
                        scoreList1[col] = 2
                    
                # if player's pop move is legal
                if check_move(board, turn_player, col, True) == True:
                    
                    # player applies move
                    temp_board2 = apply_move(board, turn_player, col, True)
                    
                    # if player wins from pop move
                    if check_victory(temp_board2, turn_player) == turn_player:
                        
                        # find any pop move by bot that can prevent player from winning
                        for col2 in range(NUM_OF_COLS):
                            
                            # if move legal 
                            if check_move(temp_board2, turn_bot, col2, True) == True:
                                
                                # bot applies move
                                temp_board2 = apply_move(board, turn_bot, col2, True)
                                
                                # if player wins after bot's move
                                if check_victory(temp_board2, turn_player) == turn_player:
                                    
                                    scoreList2[col2] = 0 # bot should avoid this move
                                
                                # otherwise, check if this prevents the player from winning by doing the same pop move as before
                                else:
                                
                                    # player applies move to another hypothetical board
                                    temp_board3 = apply_move(temp_board2, turn_player, col, True)
                                    
                                    # if player wins
                                    if check_victory(temp_board3, turn_player) != turn_player:
                                        scoreList2[col2] = 2 # bot plays this move to prevent other player from winning

                                    else:
                                        scoreList2[col2] = 0 # bot should avoid this move as it does not prevent player from winning
                                        
                            # if move illegal
                            else:
                                scoreList2[col2] = 0
                                
            # combine both score lists together, then find the highest scores
            scoreList3 = scoreList1 + scoreList2
            score = max(scoreList3)

            # to find the index position of the highest scores
            indexList = []

            for i in range(NUM_OF_COLS):
                if scoreList1[i] == score:
                    indexList.append((i, False))

                if scoreList2[i] == score:
                    indexList.append((i, True))

            # randomly select index position with highest score
            col, pop = random.choice(indexList)
            
            return col, pop

def row_configuration():
    
    # Set while loop to check whether user wants to configure rows
    while True:        
        configure_rows = input("Would you like to change number of rows? (y/n): ")
        
        # If user wants to config num of rows
        if configure_rows == 'y' or configure_rows == 'Y':     

            # Set while loop to check whether user selected appropriate number of rows
            while True:                
                # Try this block of code first
                try:

                    NUM_OF_ROWS = int(input("How many rows do you want?: "))
                    if 5 <= NUM_OF_ROWS <= 8:
                        return NUM_OF_ROWS

                    # If user selects a number not from 5 to 8
                    else:
                        print("\nERROR: Please select an INTEGER from 5 to 8 only\n") 
                        continue

                # If ValueError appears (meaning user did not select an integer), print error message instead of crashing the program                       
                except ValueError:
                    print("\nERROR: Please select an INTEGER from 5 to 8 only\n") 

            # End loop for checking whether user wants to configure rows
            break 
        
        # If user does not want to config num of rows                
        elif configure_rows == 'n' or configure_rows == 'N':
            # Set default num of rows as 6
            return 6

        else:
            print("\nERROR: Please select yes or no (y/n) only\n")

def select_player():
    
    # Randomly select player 1 or 2
    coin_toss = random.randint(1, 2)
    
    if coin_toss == 1:            
        print("\nPlayer 1 starts first")
        turn = 1
    else:
        print("\nPlayer 2 starts first")
        turn = 2
        
    return turn

def player_choice():
    
    # get user input for column
    while True: 
        try:
                                               
            col = int(input("Select column 1-7: "))
            print()
    
            # check if column selected is valid
            if 1 <= col <= 7:
                # match column selection to array index
                col -= 1
                break

            # if user selects an invalid column
            else:
                print("\nERROR: Please select an INTEGER from 1 to 7 only\n")  
                                         
        except ValueError: 
            
            # if user did not select an integer 
            print("\nERROR: Please select an INTEGER from 1 to 7 only\n")  
            
    # get user input for pop
    while True:
        
        pop = input("Do you want to pop a piece? (y/n): ")
        
        if pop == 'y' or pop == 'Y':
            
            # set pop to True
            pop = True
            break
            
        elif pop == 'n' or pop == 'N':
            
            # set pop to False
            pop = False
            break
            
        else:
            
            # if user selects an invalid option for whether to pop a piece
            print("\nERROR: Please select yes or no (y/n) only\n")
            
    return col, pop

def menu():
    
    # initialize constant
    NUM_OF_COLS = 7
    
    while True:
        try:
            # Prompt user for game mode (pvp, vs cpu (easy), vs cpu (medium))
            game_options = ["PvP", "Player vs CPU (Easy)", "Player vs CPU (Medium)"]
            print(f"1: {game_options[0]}")
            print(f"2: {game_options[1]}")
            print(f"3: {game_options[2]}")
            game_mode = int(input("Please select the game mode: ")) # game mode: 1=pvp, 2=easy cpu, 3=medium cpu     
        
            if game_mode < 1 or game_mode > 3:
                print("\nInvalid choice, please only select either 1,2 or 3!\n")
            else:
                break
        except:
            print("\nInvalid choice, please only select either 1,2 or 3!\n")
                
        
    # Prompt whether user would like to configure number of rows
    print("\nDefault number of rows: 6")
    print("Min number of rows is 5")
    print("Max number of rows is 8")

    # Set number of rows
    NUM_OF_ROWS = row_configuration()
    
    print("\n" + "="*40)
    print(f"GAME MODE SELECTED: {game_options[game_mode-1].upper()}")
    print(f"NUMBER OF ROWS SELECTED: {NUM_OF_ROWS}")
    print("="*40 + "\n")

    # Initialize board with list comprehension
    board = [0 for x in range(NUM_OF_COLS * NUM_OF_ROWS)]

    # Gamemode: PVP
    if game_mode == 1:
        
        # See who starts first
        turn = select_player()
    
        # game start
        while True:
            
            # player 1's turn
            if turn == 1:

                # Turn Preparation
                display_board(board)
                print(f"\nPlayer {turn}'s turn")

                # start loop for player 1 turn
                while True:
                    
                    # player selects a column and whether to pop
                    col, pop = player_choice()
                    
                    if pop == True:

                        # if move is illegal
                        if check_move(board, turn, col, pop) == False:
                            
                            # print error message
                            print("\nERROR: You have entered an invalid move\n")

                            continue # back to column selection

                        # if move is legal, apply move                                
                        else:

                            board = apply_move(board, turn, col, pop)
                            
                            break # exit loop and move to change of turn
                    
                    elif pop == False:

                        # if move is illegal
                        if check_move(board, turn, col, pop) == False:
                            
                            # print error message
                            print("\nERROR: You have entered an invalid move\n")

                            continue # back to column selection

                        # if move is legal, apply move
                        else:

                            board = apply_move(board, turn, col, pop)
                            
                            break # exit loop and move to change of turn
                                             
                # if victory conditions met
                if check_victory(board, turn) == turn:
                    display_board(board)
                    print("\n" + "="*40)
                    print("Congratulations! Player 1 won!")
                    print("="*40 + "\n")
                    break
                
                # if no win conditions met
                else: 
                    
                    # set turn to player 2
                    turn = 2 
                
            # player 2's turn
            else:
                
                # Turn Preparation
                display_board(board)
                print(f"\nPlayer {turn}'s turn")

                # start loop for player 1 turn
                while True:
                    
                    # player selects a column and whether to pop
                    col, pop = player_choice()
                    
                    if pop == True:

                        # if move is illegal
                        if check_move(board, turn, col, pop) == False:
                            
                            # print error message
                            print("\nERROR: You have entered an invalid move\n")
                                
                            continue # back to column selection

                        # if move is legal, apply move                                
                        else:

                            board = apply_move(board, turn, col, pop)
                            
                            break # exit loop and move to change of turn
                    
                    elif pop == False:

                        # if move is illegal
                        if check_move(board, turn, col, pop) == False:
                            
                            # print error message
                            print("\nERROR: You have entered an invalid move\n")
                                
                            continue # back to column selection


                        # if move is legal, apply move
                        else:

                            board = apply_move(board, turn, col, pop)
                            
                            break # exit loop and move to change of turn
                                             
                # if victory conditions met
                if check_victory(board, turn) == turn: # if win
                    display_board(board)
                    print("\n" + "="*40)
                    print("Congratulations! Player 2 won!")
                    print("="*40 + "\n")
                    break
                    
                # if no victory conditions met
                else:
                    
                    # set turn to player 1
                    turn = 1 
                    
    # Gamemode: Player vs. CPU
    elif game_mode == 2 or game_mode == 3:
        
        # select computer level difficulty
        if game_mode == 2:
            level = 1
        elif game_mode == 3:
            level = 2
        
        # See who starts first
        cpu_num = random.randint(1, 2)
        print(f"Computer is player {cpu_num}!")
        
        if cpu_num == 1:
            player_num = 2
        else:
            player_num =1
            
        turn = select_player()
        
        while True:
            
            # player's turn
            if turn != cpu_num:
                
                # Turn Preparation
                display_board(board)
                print("\nPlayer's turn")

                # start loop for player's turn
                while True:
                    
                    col, pop = player_choice()
                    
                    if pop == True:

                        # if move is illegal
                        if check_move(board, turn, col, pop) == False:
                            
                            # print error message
                            print("\nERROR: You have entered an invalid move\n")
                                
                            continue # back to column selection

                        # if move is legal, apply move                                
                        else:

                            board = apply_move(board, turn, col, pop)
                            
                            break # exit loop and move to change of turn
                    
                    elif pop == False:
                        
                        # if move is illegal
                        if check_move(board, turn, col, pop) == False:
                            
                            # print error message
                            print("\nERROR: You have entered an invalid move\n")
                            
                            continue # back to column selection

                        # if move is legal, apply move
                        else:

                            board = apply_move(board, turn, col, pop)
                            
                            break # exit loop and move to change of turn
                                             
                # if win conditions met
                if check_victory(board, turn) == turn:
                    display_board(board)
                    print("\n" + "="*40)
                    print("Congratulations! Player has won!")
                    print("="*40 + "\n")
                    break
                
                # if no win conditions met
                else: 
                    
                    # set turn to computer's
                    turn = cpu_num
                    
            # computer's turn
            else:
                
                # turn preparation
                display_board(board)                
                print("\nIt is the computer's turn")
                time.sleep(1.5)
                    
                # computer makes their move
                col, pop = computer_move(board, turn, level)
                board = apply_move(board, turn, col, pop) 

                # message if cpu chose to pop a piece
                if pop == True:
                    print(f"Computer popped out column {col + 1}")

                # message if cpu chose to place a piece    
                else: 
                    print(f"Computer placed a piece in column {col + 1}")
                
                # if win conditions met
                if check_victory(board, turn) == cpu_num:
                    display_board(board)
                    print("\n" + "="*40)
                    print("Too bad! CPU won")
                    print("="*40 + "\n")
                    break
                    
                # if no win conditions met
                else:
                    
                    # set turn to player's
                    turn = player_num
    
if __name__ == "__main__":
    menu()





    
