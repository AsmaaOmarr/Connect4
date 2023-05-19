import numpy as np
import pygame
import sys
import math
from threading import Timer
import random

def Connect4TopLevel():
    #variable definitions
    ROWS = 6
    COLS = 7
    Computer_turn = 0
    AI_TURN = 1
    Computer_PIECE = 1
    AI_PIECE = 2
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    #Function Definitions
    def create_board():
        board = np.zeros((ROWS, COLS))
        return board


    def drop_piece(board, row, col, piece):
        board[row][col] = piece


    def is_valid_location(board, col):
        return (board[:, col] == 0).any()


    def get_next_open_row(board, col):
        for r in range(ROWS):
            if board[r][col] == 0:
                return r
            

    def winning_move(board, piece):
        # checking horizontal 'windows' of 4 for win
        for c in range(COLS-3):
            for r in range(ROWS):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # checking vertical 'windows' of 4 for win
        for c in range(COLS):
            for r in range(ROWS-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # checking positively sloped diagonals for win
        for c in range(COLS-3):
            for r in range(3, ROWS):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True

        # checking negatively sloped diagonals for win
        for c in range(3,COLS):
            for r in range(3, ROWS):
                if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
                    return True


    def print_board(board):
        print(np.flip(board,0))


    def draw_board(board): 
        for c in range(COLS):
            for r in range(ROWS):
                pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE ))
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
                
        for c in range(COLS):
            for r in range(ROWS):
                if board[r][c] == 1:
                        pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE/2), height-int(r* SQUARESIZE + SQUARESIZE/2)), circle_radius)
                elif board[r][c] == 2 :
                        pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE/2), height-int(r* SQUARESIZE  + SQUARESIZE/2)), circle_radius)
        pygame.display.update()    


    def is_terminal_node(board):
        return winning_move(board, Computer_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


    def evaluate_window(window, piece):
        # by default the oponent is the player
        opponent_piece = Computer_PIECE

        # if we are checking from the player's perspective, then the oponent is AI
        if piece == Computer_PIECE:
            opponent_piece = AI_PIECE

        # initial score of a window is 0
        score = 0

        # based on how many friendly pieces there are in the window, we increase the score
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        # or decrese it if the oponent has 3 in a row
        if window.count(opponent_piece) == 3 and window.count(0) == 1:
            score -= 4 

        return score    


    def score_position(board, piece):

        score = 0

        # score center column --> we are prioritizing the central column because it provides more potential winning windows
        center_array = [int(i) for i in list(board[:,COLS//2])]
        center_count = center_array.count(piece)
        score += center_count * 6

        # below we go over every single window in different directions and adding up their values to the score
        # score horizontal
        for r in range(ROWS):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(COLS - 3):
                window = row_array[c:c + 4]
                score += evaluate_window(window, piece)

        # score vertical
        for c in range(COLS):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(ROWS-3):
                window = col_array[r:r+4]
                score += evaluate_window(window, piece)

        # score positively sloped diagonals
        for r in range(3,ROWS):
            for c in range(COLS - 3):
                window = [board[r-i][c+i] for i in range(4)]
                score += evaluate_window(window, piece)

        # score negatively sloped diagonals
        for r in range(3,ROWS):
            for c in range(3,COLS):
                window = [board[r-i][c-i] for i in range(4)]
                score += evaluate_window(window, piece)

        return score


    def minimax(board, depth, alpha, beta, maximizing_player):

        # all valid locations on the board
        valid_locations = get_valid_locations(board)

        # boolean that tells if the current board is terminal
        is_terminal = is_terminal_node(board)

        # if the board is terminal or depth == 0
        # we score the win very high and a draw as 0
        if depth == 0 or is_terminal:
            if is_terminal: # winning move 
                if winning_move(board, AI_PIECE):
                    return (None, 10000000)
                elif winning_move(board, Computer_PIECE):
                    return (None, -10000000)
                else:
                    return (None, 0)
            # if depth is zero, we simply score the current board
            else: # depth is zero
                return (None, score_position(board, AI_PIECE))

        # if the current board is not rerminal and we are maximizing
        if maximizing_player:

            # initial value is what we do not want - negative infinity
            value = -math.inf

            # this will be the optimal column. Initially it is random
            column = random.choice(valid_locations)

            # for every valid column, we simulate dropping a piece with the help of a board copy
            # and run the minimax on it with decresed depth and switched player
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, AI_PIECE)
                # recursive call
                new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
                # if the score for this column is better than what we already have
                if new_score > value:
                    value = new_score
                    column = col
                # alpha is the best option we have overall
                alpha = max(value, alpha) 
                # if alpha (our current move) is greater (better) than beta (opponent's best move), then 
                # the oponent will never take it and we can prune this branch
                if alpha >= beta:
                    break

            return column, value
        
        # same as above, but for the minimizing player
        else: # for thte minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                b_copy = board.copy()
                drop_piece(b_copy, row, col, Computer_PIECE)
                new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(value, beta) 
                if alpha >= beta:
                    break
            return column, value


    def get_valid_locations(board):
        valid_locations = []
        
        for column in range(COLS):
            if is_valid_location(board, column):
                valid_locations.append(column)

        return valid_locations


    def end_game():
        global game_over
        game_over = True
        print(game_over)

    #gui
    board = create_board()
    print_board(board)
    game_over = False
    not_over = True
    turn = random.randint(Computer_turn,AI_TURN)
    pygame.init()
    SQUARESIZE = 100
    width = COLS * SQUARESIZE
    height = (ROWS+1) * SQUARESIZE
    size = (width,height)
    circle_radius = int(SQUARESIZE/2 - 5)
    screen = pygame.display.set_mode(size)
    myfont= pygame.font.SysFont("monospace" ,60)
    draw_board(board)
    pygame.display.update()

    #game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # if event.type == pygame.MOUSEMOTION:
            #     pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            #     posx = event.pos[0]
            #     if turn == Computer_turn:
            #         pygame.draw.circle(screen,RED,(posx,int(SQUARESIZE/2)),circle_radius)
            #     else:
            #         pygame.draw.circle(screen,YELLOW,(posx,int(SQUARESIZE/2)),circle_radius)

            # pygame.display.update()
            
            # pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
        #wait for computer turn
        if turn == Computer_turn and not game_over and not_over :
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            if is_valid_location(board,col):
                #computer's turn after 0.5 ms
                pygame.time.wait(200)
                row = get_next_open_row(board,col)
                drop_piece(board,row,col,Computer_PIECE)

                if winning_move(board,Computer_PIECE):
                    label = myfont.render("AI PLAYER 1 WINS !", 1 ,RED)
                    screen.blit(label,(40,10))
                    game_over = True
                            

                print_board(board)
                draw_board(board)

                turn +=1
                turn = turn % 2

        #wait for ai turn      
        if turn == AI_TURN and not game_over and not_over :
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            if is_valid_location(board, col):
                #ai play its turn after 0.5 ms
                pygame.time.wait(200)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                if winning_move(board, AI_PIECE):
                    print("AI WINS :) Congratulations !!!")
                    label = myfont.render("AI PLAYER 2 WINS :)", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    not_over = False
                    t = Timer(3.0, end_game)
                    t.start()
            draw_board(board)    
            turn += 1
            turn = turn % 2

    #when game is over it will close board after 3 ms
        if game_over:
            pygame.time.wait(3000)






                    



                



                    
