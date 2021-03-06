# Written By: Tindur Sigurdason & Calen Irwin
# Written For: CISC-856 W21 (Reinforcement Learning) at Queen's U
# Purpose: Contains various Hnefatafl game related methods, such as state initialization and transition

# References:
# https://github.com/slowen/hnefatafl/blob/master/hnefatafl.py
# https://github.com/aigagror/GymGo

import numpy as np
from scipy import ndimage
from sklearn import preprocessing

import hnef_vars

# Initialization function that gives the initial state of the game
# In: rule set string, copenhagen or historical, copenhagen isn't implemented yet
# Out: numpy array state of shape (5, board size, board size) 
#       state[0]: binary matrix showing the position of all attacker pieces
#       state[1]: binary matrix (except a 2 representing the king) showing the position of all defender pieces
#       state[2]: starts as all zeros but state[2,0,0] is whose turn it is, 0 for attacker 1 for defender
#       state[3]: starts as all zeros but state[3,0,0] is a boolean representing whether the game is finished
#       state[4]: starts as all zeros but state[4,0,0] is the number of the turn
def init_state(rule_set):
    # Not implemented yet
    if rule_set == "copenhagen":
        state = np.zeros((hnef_vars.NUM_CHNLS, 11, 11))
        attacker_layout = np.array([[0,0,0,1,1,1,1,1,0,0,0],
                                    [0,0,0,0,0,1,0,0,0,0,0],
                                    [0,0,0,0,0,0,0,0,0,0,0],
                                    [1,0,0,0,0,0,0,0,0,0,1],
                                    [1,0,0,0,0,0,0,0,0,0,1],
                                    [1,1,0,0,0,0,0,0,0,1,1],
                                    [1,0,0,0,0,0,0,0,0,0,1],
                                    [1,0,0,0,0,0,0,0,0,0,1],
                                    [0,0,0,0,0,0,0,0,0,0,0],
                                    [0,0,0,0,0,1,0,0,0,0,0],
                                    [0,0,0,1,1,1,1,1,0,0,0]])
                            
        defender_layout = np.array([[0,0,0,0,0,0,0,0,0,0,0],
                                    [0,0,0,0,0,0,0,0,0,0,0],
                                    [0,0,0,0,0,0,0,0,0,0,0],
                                    [0,0,0,0,0,1,0,0,0,0,0],
                                    [0,0,0,0,1,1,1,0,0,0,0],
                                    [0,0,0,1,1,2,1,1,0,0,0],
                                    [0,0,0,0,1,1,1,0,0,0,0],
                                    [0,0,0,0,0,1,0,0,0,0,0],
                                    [0,0,0,0,0,0,0,0,0,0,0],
                                    [0,0,0,0,0,0,0,0,0,0,0],
                                    [0,0,0,0,0,0,0,0,0,0,0]])

        state[hnef_vars.ATTACKER] = attacker_layout
        state[hnef_vars.DEFENDER] = defender_layout
        return state
    
    elif rule_set == 'mini':
        state = np.zeros((hnef_vars.NUM_CHNLS, 5, 5))
        attacker_layout = np.array([[0,1,0,1,0],
                                    [1,0,0,0,1],
                                    [0,0,0,0,0],
                                    [1,0,0,0,1],
                                    [0,1,0,1,0]])

        defender_layout = np.array([[0,0,0,0,0],
                                    [0,0,1,0,0],
                                    [0,1,2,1,0],
                                    [0,0,1,0,0],
                                    [0,0,0,0,0]])

        state[hnef_vars.ATTACKER] = attacker_layout
        state[hnef_vars.DEFENDER] = defender_layout
        return state
        
    elif rule_set == "historical":
        state = np.zeros((hnef_vars.NUM_CHNLS, 9, 9))
        attacker_layout = np.array([[0,0,0,1,1,1,0,0,0],
                                    [0,0,0,0,1,0,0,0,0],
                                    [0,0,0,0,0,0,0,0,0],
                                    [1,0,0,0,0,0,0,0,1],
                                    [1,1,0,0,0,0,0,1,1],
                                    [1,0,0,0,0,0,0,0,1],
                                    [0,0,0,0,0,0,0,0,0],
                                    [0,0,0,0,1,0,0,0,0],
                                    [0,0,0,1,1,1,0,0,0]])

        defender_layout = np.array([[0,0,0,0,0,0,0,0,0],
                                    [0,0,0,0,0,0,0,0,0],
                                    [0,0,0,0,1,0,0,0,0],
                                    [0,0,0,0,1,0,0,0,0],
                                    [0,0,1,1,2,1,1,0,0],
                                    [0,0,0,0,1,0,0,0,0],
                                    [0,0,0,0,1,0,0,0,0],
                                    [0,0,0,0,0,0,0,0,0],
                                    [0,0,0,0,0,0,0,0,0]])

        state[hnef_vars.ATTACKER] = attacker_layout
        state[hnef_vars.DEFENDER] = defender_layout
        return state
    else:
        print("*Error: Given rule set has not been implemented.\n Existing rule sets are:\n-copenhagen\n-historial")
        return -1

# Returns whose turn it is based on the state given
def turn(state):
    if state is not None:
        return int(np.max(state[hnef_vars.TURN_CHNL]))

# Method for checking whether a capture has taken place
# In: state (current state), action (action taken by current player)
# Out: state (new state)
def check_capture(state, action):
    # current player
    current_player = turn(state)
    # other player
    other_player = np.abs(current_player - 1)
    # defender
    df = hnef_vars.DEFENDER
    # attacker
    at = hnef_vars.ATTACKER
    # board size
    board_size = state.shape[1]
    # throne location
    throne = (board_size // 2, board_size // 2)

    # new location of moved piece
    x, y = action[1]

    ## capturing normal pieces normally
    
    # capturing upwards
    if x > 1 and state[other_player][x-1][y] == 1 and state[current_player][x-2][y] > 0:
        state[other_player][x-1][y] = 0

    # capturing downwards
    if x < board_size - 2 and state[other_player][x+1][y] == 1 and state[current_player][x+2][y] > 0:
        state[other_player][x+1][y] = 0
    
    # capturing left
    if y > 1 and state[other_player][x][y-1] == 1 and state[current_player][x][y-2] > 0:
        state[other_player][x][y-1] = 0

    # capturing right
    if y < board_size - 2 and state[other_player][x][y+1] == 1 and state[current_player][x][y+2] > 0:
        state[other_player][x][y+1] = 0
    
    ## capturing normal pieces with the throne
    
    # if the king is on the throne then the white pieces cant be captured in this way
    if (current_player == at and state[df][throne[0]][throne[0]] < 2):
        # capturing upwards
        if x > 1 and state[other_player][x-1][y] == 1 and np.mean((x-2, y) == throne):
            state[other_player][x-1][y] = 0
        # capturing downwards
        elif x < board_size - 2 and state[other_player][x+1][y] == 1 and np.mean((x+2, y) == throne):
            state[other_player][x+1][y] = 0
        # capturing left
        elif y > 1 and state[other_player][x][y-1] == 1 and np.mean((x, y-2) == throne):
            state[other_player][x][y-1] = 0
        # capturing right
        elif y < board_size - 2 and state[other_player][x][y+1] == 1 and np.mean((x, y+2) == throne):
            state[other_player][x][y+1] = 0
    
    ## capturing the king normally

    # capturing upwards
    if x > 1 and state[df][x-1][y] == 2 and state[at][x-2][y] > 0 and state[df][throne[0]][throne[0]] < 2:
        state[df][x-1][y] = 0
        state[hnef_vars.DONE_CHNL] = 1
        return state

    # capturing downwards
    if x < board_size - 2 and state[df][x+1][y] == 2 and state[at][x+2][y] > 0 and state[df][throne[0]][throne[0]] < 2:
        state[df][x+1][y] = 0
        state[hnef_vars.DONE_CHNL] = 1
        return state
    
    # capturing left
    if y > 1 and state[df][x][y-1] == 2 and state[at][x][y-2] > 0 and state[df][throne[0]][throne[0]] < 2:
        state[df][x][y-1] = 0
        state[hnef_vars.DONE_CHNL] = 1
        return state

    # capturing right
    if y < board_size - 2 and state[df][x][y+1] == 2 and state[at][x][y+2] > 0 and state[df][throne[0]][throne[0]] < 2:
        state[df][x][y+1] = 0
        state[hnef_vars.DONE_CHNL] = 1
        return state

    ## capturing the king on the throne
    if (state[df][throne[0]][throne[0]] == 2 
        and state[at][throne[0]-1][throne[0]] > 0
        and state[at][throne[0]+1][throne[0]] > 0
        and state[at][throne[0]][throne[0]-1] > 0
        and state[at][throne[0]][throne[0]+1] > 0):
        state[df][throne[0]][throne[0]] = 0
        state[hnef_vars.DONE_CHNL] = 1
        return state

    ## capturing the king next to the throne

    if current_player == at:
        # king is above throne
        if state[df][throne[0]-1][throne[0]] == 2 and state[at][throne[0]-1][throne[0]-1] > 0 and state[at][throne[0]-1][throne[0]+1] > 0 and state[at][throne[0]-2][throne[0]] > 0:
            state[df][throne[0]-1][throne[0]] = 0
            state[hnef_vars.DONE_CHNL] = 1
            return state
        # king is below throne  
        elif state[df][throne[0]+1][throne[0]] == 2 and state[at][throne[0]+1][throne[0]-1] > 0 and state[at][throne[0]+1][throne[0]+1] > 0 and state[at][throne[0]+2][throne[0]] > 0:
            state[df][throne[0]+1][throne[0]] = 0
            state[hnef_vars.DONE_CHNL] = 1
            return state
        # king is left of throne 
        elif state[df][throne[0]][throne[0]-1] == 2 and state[at][throne[0]-1][throne[0]-1] > 0 and state[at][throne[0]+1][throne[0]-1] > 0 and state[at][throne[0]][throne[0]-2] > 0:
            state[df][throne[0]][throne[0]-1] = 0
            state[hnef_vars.DONE_CHNL] = 1
            return state
        # king is right of throne 
        elif state[df][throne[0]][throne[0]+1] == 2 and state[at][throne[0]-1][throne[0]+1] > 0 and state[at][throne[0]+1][throne[0]+1] > 0 and state[at][throne[0]][throne[0]+2] > 0:
            state[df][throne[0]][throne[0]+1] = 0
            state[hnef_vars.DONE_CHNL] = 1
            return state

    return state

# State transition function
# In: state (current state), action (action taken by current player)
# Out: state (new state)
def next_state(state, action):

    # define the current player
    current_player = turn(state)
    
    # assert that the action is valid i.e. that the action is in state[valid_actions]
    valid_moves = compute_valid_moves(state)

    if action not in valid_moves:
        print("Action not in valid moves")
        assert False

    if state[current_player][action[0][0]][action[0][1]] == 2:
        state[current_player][action[0][0]][action[0][1]] = 0
        state[current_player][action[1][0]][action[1][1]] = 2
    else:
        state[current_player][action[0][0]][action[0][1]] = 0
        state[current_player][action[1][0]][action[1][1]] = 1

    # check if the player just captured a piece and update the state if so
    state = check_capture(state, action)

    # switch turns
    state[hnef_vars.TURN_CHNL][0][0] = np.abs(current_player - 1)

    return state

# Function for finding all actions for a given piece located at (x, y) on the board
# In: state (current state), x-position of piece, y-position of piece
# Out: list of all possible actions where action a = ((x, y), (new_x, new_y))
def actions_for_piece(state, x, y):
    actions = []

    board_size = state.shape[1]

    # the position of every piece
    full_board = state[hnef_vars.ATTACKER] + state[hnef_vars.DEFENDER]

    throne = (board_size // 2, board_size // 2)
    # can the piece move up?
    if x > 0:
        pos_x = x
        pos_y = y 
        # continue until on the edge or about to collide with another piece
        while pos_x > 0 and not full_board[pos_x - 1, y]:
            pos_x -= 1
            # the action isn't possible if the destination is the throne, except if the piece is the king
            if ((full_board[x, y] == 2 and ((pos_x, y) == throne))) or (((pos_x, y) != throne)):
                actions.append(((x, y), (pos_x, y)))

    # can the piece move down?
    if x < board_size - 1:
        pos_x = x
        pos_y = y
        # continue until on the edge or about to collide with another piece
        while pos_x < board_size - 1 and not full_board[pos_x + 1, y]:
            pos_x += 1

            if ((full_board[x, y] == 2 and ((pos_x, y) == throne))) or (((pos_x, y) != throne)):
                actions.append(((x, y), (pos_x, y)))

    # can the piece move left?
    if y > 0:
        pos_x = x
        pos_y = y
        while pos_y > 0 and not full_board[x, pos_y - 1]:
            pos_y -= 1

            if ((full_board[x, y] == 2 and ((x, pos_y) == throne))) or (((x, pos_y) != throne)):
                actions.append(((x, y), (x, pos_y)))
                
    # can the piece move right?
    if y < board_size - 1:
        pos_x = x
        pos_y = y
        while pos_y < board_size - 1 and not full_board[x, pos_y + 1]:
            pos_y += 1

            if ((full_board[x, y] == 2 and ((x, pos_y) == throne))) or (((x, pos_y) != throne)):
                actions.append(((x, y), (x, pos_y)))

    return actions

# Function that computes all valid moves for a given state
# In: state (current state)
# Out: list of all possible actions for all pieces of the current player 
#      where action a = ((x, y), (new_x, new_y))
def compute_valid_moves(state):
    actions = []

    board_size = state.shape[1]

    current_player = turn(state)

    # Iterate through the entire board
    for i in range(board_size):
            for j in range(board_size):
                # if the current player has a piece at (i,j), check for valid actions
                if state[current_player, i, j]:
                    piece_actions = actions_for_piece(state, i, j)

                    for a in piece_actions:
                        actions.append(a)
    return actions

## Not finished, will probably need DFS to properly check
# In: state (current state), action (possible actions for current player)
# Out: list of all possible actions for all pieces of the current player 
#      where action a = ((x, y), (new_x, new_y))
def check_enclosure(state, action):
    board_size = state.shape[1] # get board size
    wall_positions = [] # holds wall positions for specific board size

    # populate wall positions array with tuples of (row_index, col_index)
    for i in range(board_size): # row index loop
        for j in range(board_size): # col index loop
            # bottom or top wall indices
            if i == 0 or i == board_size - 1:
                wall_positions.append((i,j))
            # side walls
            elif j == 0 or j == board_size -1:
                wall_positions.append((i,j))

    # list comprehension to check if a wall position is within the list of 
    # possible actions for the defender
    # appends those locations if they exist in the action list
    # wall_moves = [pos for pos in wall_positions if pos in action]

    # not as pretty but still works
    # should we break early or add some terminating condition?
    wall_moves = []
    
    for pos in wall_positions:
        for a in action:
            if a[1] == pos:
                wall_moves.append(pos)

    # if no defender pieces can move to a wall then they are either enclosed or 
    # there are no remaining defender pieces
    # either way the game is over and the attacker wins
    if len(wall_moves) == 0:
        return True, hnef_vars.ATTACKER
    else:
        return False, -1

# Function for checking if the game is over
# In: state (current state), action (action that was just taken)
# Out: boolean (is the game over?), player who won
def is_over(state, action):
    at = hnef_vars.ATTACKER
    df = hnef_vars.DEFENDER
    full_board = state[at] + state[df]
    board_size = state.shape[1]    
    # current player
    player = int(np.max(state[hnef_vars.TURN_CHNL]))
    # other player
    other_player = np.abs(player - 1)
    # has the king been captured?
    if np.max(state[df]) < 2:
        # print("***King captured")
        return True, at
    # has the king escaped?
    elif np.max(state[df][0]) == 2 or np.max(state[df][:,0]) == 2 or np.max(state[df][:,board_size-1]) == 2 or np.max(state[df][board_size-1]) == 2:
        # print("***King escaped")
        return True, df
    # has the attacker enclosed the defender? NOT IMPLEMENTED
    # elif check_enclosure(state,action)[0]:
    #     return True, at
    # no win
    else:
        return False, -1

# Method for simulating a step taken, without changing the current state
# In: state (current state), action (action selected)
# Out: New state, int reward, boolean representing whether the game is finished
def simulate_step(state, action):
    state_copy = np.copy(state)
    new_state = simulate_next_state(state_copy, action)
    done, winner = is_over(state_copy, action) 

    if not done:
            reward = 0
    else:
        current_player = turn(state_copy)
        if current_player == winner:
            reward =  1
        else:
            reward = 0

    return np.copy(new_state), reward, done

# State transition simulation method
# In: state (current state), action (action taken by current player)
# Out: state (new state)
def simulate_next_state(state, action):
    state_copy = np.copy(state)

    # define the current player
    current_player = turn(state_copy)

    # assert that the action is valid i.e. that the action is in state[valid_actions]
    valid_moves = compute_valid_moves(state)

    # if action not in valid_moves:
    #     print("Valid moves: ", valid_moves)
    #     print(str(state))
    #     print("***Invalid action: ", action)
    #     assert False

    if state_copy[current_player][action[0][0]][action[0][1]] == 2:
        state_copy[current_player][action[0][0]][action[0][1]] = 0
        state_copy[current_player][action[1][0]][action[1][1]] = 2
    else:
        state_copy[current_player][action[0][0]][action[0][1]] = 0
        state_copy[current_player][action[1][0]][action[1][1]] = 1

    # check if the player just captured a piece and update the state if so
    state_copy = check_capture(state_copy, action)

    state_copy[hnef_vars.TURN_CHNL][0][0] = np.abs(current_player - 1)

    return np.copy(state_copy)

# String method to show the state of the board
# In: state (current state)
# Out: board_str string of the board
def str(state):
    board_str = ' '

    size = state.shape[1]
    for i in range(size):
        board_str += '   {}'.format(i)
    board_str += '\n  '
    board_str += '----' * size + '-'
    board_str += '\n'
    for i in range(size):
        board_str += '{} |'.format(i)
        for j in range(size):
            if state[0, i, j] == 1:
                board_str += ' A'
            elif state[1, i, j] == 1:
                board_str += ' D'
            elif state[1, i, j] == 2:
                board_str += ' K'
            else:
                board_str += '  '

            board_str += ' |'

        board_str += '\n  '
        board_str += '----' * size + '-'
        board_str += '\n'

    t = turn(state)
    board_str += '\tTurn: {}'.format('Attacker' if t == 0 else 'Defender')
    return board_str