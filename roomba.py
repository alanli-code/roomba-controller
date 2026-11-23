# --------------
# Author: Alan Li
# Date created: Oct 3 2026
# Date updated: Oct 21 2026
# Program description: A consoled-based Roomba controller simulator.
# --------------

import random
import math

# GLOBAL CONSTANTS
MOVE = 5
MOVE_TIME = 2
MAX_RUN_TIME = 600
MIN_COORD = -150
MAX_COORD = 150
TURN_TIME = 3
RIGHT = 'Right'
LEFT = 'Left'

def direction_name(dir_num):
    '''
    This function takes an integer in the interval [1, 4] and returns
    the corresponding direction.

    Parameters:
    dir_num (int): The integer input to determine the direction.

    Returns:
    direction (str or bool): One of four cardinal directions
    or False if invalid.

    Examples:
    >>> direction_name(1)
    'North'
    >>> direction_name(3)
    'South'
    >>> direction_name(-1)
    False
    '''
    # Returns the cardinal direction corresponding to the integer.
    if dir_num == 1:
        return 'North'
    elif dir_num == 2:
        return 'East'
    elif dir_num == 3:
        return 'South'
    elif dir_num == 4:
        return 'West'
    else:
        return False


def get_valid_coordinate(coord, min_coord, max_coord):
    '''
    This function checks if the given coordinate is within the minimum
    and maximum range.

    Parameters:
    coord (int): The coordinate being checked.
    min_coord (int): The minimum allowed coordinate.
    max_coord (int): The maximum allowed coordinate.

    Returns:
    is_valid (bool): Returns True if the given coordinate is within the
    interval, returns False if it's outside of it.

    Examples:
    >>> get_valid_coordinate(10, MIN_COORD, MAX_COORD)
    True
    >>> get_valid_coordinate(-10, MIN_COORD, MAX_COORD)
    True
    >>> get_valid_coordinate(-151, MIN_COORD, MAX_COORD)
    False
    '''
    # Checks whether the coordinate is within the valid range.
    is_valid = False
    if min_coord <= coord <= max_coord:
        is_valid = True
    return is_valid


def start_coords():
    '''
    This function obtains the starting coordinates and the direction
    that the roomba is facing.

    Parameters:
    None

    Returns:
    x_coord (int): The starting x-coordinate.
    y_coord (int): The starting y-coordinate.
    dir_num (int): The direction the roomba is facing as a number.

    Examples:
    >>> start_coords()
    Enter x coordinate of roomba:
    # User inputs 2
    Enter y coordinate of roomba:
    # User inputs 3
    Enter the direction number of the roomba
    (1-North, 2-East, 3-South, 4-West):
    # User inputs 1
    (2, 3, 1)
    >>> start_coords()
    Enter x coordinate of roomba:
    # User inputs -23
    Enter y coordinate of roomba:
    # User inputs 30
    Enter the direction number of the roomba
    (1-North, 2-East, 3-South, 4-West):
    # User inputs 2
    (-23, 30, 2)
    >>> start_coords()
    Enter x coordinate of roomba:
    # User inputs 410
    Enter x coordinate of roomba:
    # User inputs 149
    Enter y coordinate of roomba:
    # User inputs 2
    Enter the direction number of the roomba
    (1-North, 2-East, 3-South, 4-West):
    # User inputs 2
    (149, 2, 2)
    '''
    # Checks the x-coordinate and asks again until it is valid.
    x_coord = int(input('Enter x coordinate of roomba: '))
    while not get_valid_coordinate(x_coord, MIN_COORD, MAX_COORD):
        x_coord = int(input('Enter x coordinate of roomba: '))

    # Checks the y-coordinate and asks again until it is valid.
    y_coord = int(input('Enter y coordinate of roomba: '))
    while not get_valid_coordinate(y_coord, MIN_COORD, MAX_COORD):
        y_coord = int(input('Enter y coordinate of roomba: '))

    # Checks the direction and asks again until it is valid.
    dir_num = int(input('Enter the direction number of the roomba'
                        '(1-North, 2-East, 3-South, 4-West): '))
    while direction_name(dir_num) is False:
        dir_num = int(input('Enter the direction number of the roomba'
                            '(1-North, 2-East, 3-South, 4-West): '))

    return x_coord, y_coord, dir_num


def print_status(x_coord, y_coord, dir_num, elapsed_time):
    '''
    This function will print the location and time of the roomba
    at the time the function gets called.

    Parameters:
    x_coord (int): The x-coordinate of the roomba.
    y_coord (int): The y-coordinate of the roomba.
    dir_num (int): The numerical value of the roomba's direction.
    elapsed_time (int): The amount of time passed.

    Returns:
    None

    Examples:
    >>> print_status(1, 2, 1, 20)
    The roomba is at the location: (1, 2) facing North after
    0.33 minutes have passed.
    >>> print_status(0, 0, 1, 120)
    The roomba is at the location: (0, 0) facing North after
    2.0 minutes have passed.
    >>> print_status(2, 1, 2, 60)
    The roomba is at the location: (2, 1) facing East after
    1.0 minutes have passed.
    '''
    # Prints the coordinates, direction, and elapsed time in minutes.
    print(
        'The roomba is at the location: '
        + '(' + str(x_coord) + ', '
        + str(y_coord) + ') facing ' + direction_name(dir_num) + ' after '
        + str(round(elapsed_time / 60, 2)) + ' minutes have passed.'
        )


def turn_roomba(turn_dir, dir_num, elapsed_time):
    '''
    This function turns the roomba left or right and updates
    the elapsed time.

    Parameters:
    turn_dir (str): The direction the roomba should turn.
    dir_num (int): The current numerical direction of the roomba.
    elapsed_time (int): The current elapsed time.

    Returns:
    dir_num (int): The new numerical direction of the roomba.
    elapsed_time (int): The updated elapsed time.

    Examples:
    >>> turn_roomba('Right', 1, 0)
    (2, 3)
    >>> turn_roomba('Left', 1, 10)
    (4, 13)
    >>> turn_roomba('Right', 4, 20)
    (1, 23)
    '''
    # Returns the original values if the turn direction is invalid.
    if turn_dir != RIGHT and turn_dir != LEFT:
        return dir_num, elapsed_time

    # Adds the time required to turn the roomba.
    elapsed_time += TURN_TIME

    # Updates the direction and wraps it between 1 and 4.
    if turn_dir == RIGHT:
        dir_num = dir_num % 4 + 1
    elif turn_dir == LEFT:
        dir_num = (dir_num - 2) % 4 + 1

    return dir_num, elapsed_time


def input_turn_roomba(dir_num, elapsed_time):
    '''
    This function asks the user which direction to turn the roomba
    and continues turning until the user chooses to stop.

    Parameters:
    dir_num (int): The current numerical direction of the roomba.
    elapsed_time (int): The current elapsed time.

    Returns:
    dir_num (int): The new numerical direction of the roomba.
    elapsed_time (int): The updated elapsed time.

    Examples:
    >>> input_turn_roomba(1, 0)
    Which direction to turn the roomba (Left / Right)?
    # User inputs Right
    Turned. Should I stop?
    # User inputs Y
    Roomba is now facing: East
    (2, 3)
    >>> input_turn_roomba(4, 10)
    Which direction to turn the roomba (Left / Right)?
    # User inputs Left
    Turned. Should I stop?
    # User inputs y
    Roomba is now facing: South
    (3, 13)
    >>> input_turn_roomba(1, 0)
    Which direction to turn the roomba (Left / Right)?
    # User inputs Right
    Turned. Should I stop?
    # User inputs n
    Turned. Should I stop?
    # User inputs Y
    Roomba is now facing: South
    (3, 6)
    '''
    # Gets the direction the user wants the roomba to turn.
    turn_direction_choice = input(
        'Which direction to turn the '
        'roomba (Left / Right)? ')

    # Checks for invalid input.
    if (
        turn_direction_choice != 'Left' and
        turn_direction_choice != 'left' and
        turn_direction_choice != 'Right' and
        turn_direction_choice != 'right'):
        print('Invalid input, please try again!')
        return dir_num, elapsed_time

    # Converts lowercase input to the correct turn direction.
    if turn_direction_choice == 'right':
        turn_direction_choice = RIGHT
    elif turn_direction_choice == 'left':
        turn_direction_choice = LEFT

    # Turns the roomba once in the chosen direction.
    dir_num, elapsed_time = turn_roomba(
        turn_direction_choice,
        dir_num,
        elapsed_time
        )

    # Continues turning until the user chooses to stop.
    turn_continue_choice = input('Turned. Should I stop? ')
    while turn_continue_choice != 'Y' and turn_continue_choice != 'y':
        dir_num, elapsed_time = turn_roomba(
            turn_direction_choice,
            dir_num,
            elapsed_time
            )
        turn_continue_choice = input('Turned. Should I stop? ')

    # Prints the final direction after all turns are complete.
    print('Roomba is now facing:', direction_name(dir_num))
    return dir_num, elapsed_time


def move_roomba(move, x_coord, y_coord, dir_num, elapsed_time):
    '''
    This function moves the roomba five units in the given relative
    direction if the resulting coordinate is valid.

    Parameters:
    move (str): The direction the roomba should move.
    x_coord (int): The current x-coordinate of the roomba.
    y_coord (int): The current y-coordinate of the roomba.
    dir_num (int): The current numerical direction of the roomba.
    elapsed_time (int): The current elapsed time.

    Returns:
    x_coord (int): The updated x-coordinate of the roomba.
    y_coord (int): The updated y-coordinate of the roomba.
    elapsed_time (int): The updated elapsed time.

    Examples:
    >>> move_roomba('Forward', 0, 0, 1, 0)
    (0, 5, 10)
    >>> move_roomba('Left', 10, 10, 2, 20)
    (10, 15, 30)
    >>> move_roomba('Forward', 0, 150, 1, 20)
    Can not move!
    (0, 150, 20)
    '''
    # Converts the move into direction of travel.
    move_dir = 0

    if move == 'Forward':
        move_dir = dir_num
    elif move == 'Backward':
        move_dir = (dir_num + 1) % 4 + 1
    elif move == 'Left':
        move_dir = (dir_num + 2) % 4 + 1
    elif move == 'Right':
        move_dir = dir_num % 4 + 1

    # Returns the original values if the movement direction is invalid.
    if move_dir == 0:
        return x_coord, y_coord, elapsed_time

    # Calculates the new coordinates before performing the movement.
    new_x = x_coord
    new_y = y_coord

    if move_dir == 1:
        new_y += MOVE
    elif move_dir == 2:
        new_x += MOVE
    elif move_dir == 3:
        new_y -= MOVE
    elif move_dir == 4:
        new_x -= MOVE

    # Moves only if the new coordinates are within the valid range.
    if (
        get_valid_coordinate(new_x, MIN_COORD, MAX_COORD) and
        get_valid_coordinate(new_y, MIN_COORD, MAX_COORD)
        ):
        x_coord = new_x
        y_coord = new_y
        elapsed_time += MOVE_TIME * MOVE
    else:
        print('Can not move!')

    return x_coord, y_coord, elapsed_time


def input_move_roomba(x_coord, y_coord, dir_num, elapsed_time):
    '''
    This function asks the user which direction to move the roomba
    and performs the move if the input is valid.

    Parameters:
    x_coord (int): The current x-coordinate of the roomba.
    y_coord (int): The current y-coordinate of the roomba.
    dir_num (int): The current numerical direction of the roomba.
    elapsed_time (int): The current elapsed time.

    Returns:
    x_coord (int): The updated x-coordinate of the roomba.
    y_coord (int): The updated y-coordinate of the roomba.
    elapsed_time (int): The updated elapsed time.

    Examples:
    >>> input_move_roomba(0, 0, 1, 0)
    Which direction should the roomba move (Forward / Backward / Left / Right)?
    # User inputs Forward
    (0, 5, 10)
    >>> input_move_roomba(0, 0, 2, 10)
    Which direction should the roomba move (Forward / Backward / Left / Right)?
    # User inputs Left
    (0, 5, 20)
    >>> input_move_roomba(0, 0, 1, 10)
    Which direction should the roomba move (Forward / Backward / Left / Right)?
    # User inputs Up
    Invalid input, try again.
    (0, 0, 10)
    '''
    # Gets the direction the user wants the roomba to move.
    direction_move_roomba = input(
        'Which direction should the roomba move '
        '(Forward / Backward / Left / Right)? '
        )

    # Returns to the main menu if the movement input is invalid.
    if (
        direction_move_roomba != 'Forward' and
        direction_move_roomba != 'Backward' and
        direction_move_roomba != 'Left' and
        direction_move_roomba != 'Right'
        ):
        print('Invalid input, try again.')
        return x_coord, y_coord, elapsed_time

    # Performs the requested valid movement.
    x_coord, y_coord, elapsed_time = move_roomba(
        direction_move_roomba,
        x_coord,
        y_coord,
        dir_num,
        elapsed_time
        )

    return x_coord, y_coord, elapsed_time


def roam_room(x_coord, y_coord, dir_num, elapsed_time):
    '''
    This function randomly moves or turns the roomba until the
    maximum run time is reached and then prints its final status.

    Parameters:
    x_coord (int): The current x-coordinate of the roomba.
    y_coord (int): The current y-coordinate of the roomba.
    dir_num (int): The current numerical direction of the roomba.
    elapsed_time (int): The current elapsed time.

    Returns:
    x_coord (int): The final x-coordinate of the roomba.
    y_coord (int): The final y-coordinate of the roomba.
    dir_num (int): The final numerical direction of the roomba.
    elapsed_time (int): The final elapsed time.

    Examples:
    >>> roam_room(0, 0, 1, 600)
    The roomba is at the location: (0, 0) facing North after
    10.0 minutes have passed.
    (0, 0, 1, 600)
    >>> roam_room(10, -5, 2, 610)
    The roomba is at the location: (10, -5) facing East after
    10.17 minutes have passed.
    (10, -5, 2, 610)
    >>> roam_room(-20, 30, 4, 605)
    The roomba is at the location: (-20, 30) facing West after
    10.08 minutes have passed.
    (-20, 30, 4, 605)
    '''
    # Randomly chooses whether the roomba moves or turns.
    while elapsed_time < MAX_RUN_TIME:
        turn_or_move = random.random()
        if turn_or_move < 0.5:
            # Randomly chooses one of the four relative movement directions.
            move_chance = random.random()
            if move_chance < 0.25:
                move = 'Forward'
            elif 0.25 <= move_chance < 0.5:
                move = 'Backward'
            elif 0.5 <= move_chance < 0.75:
                move = 'Left'
            else:
                move = 'Right'
            x_coord, y_coord, elapsed_time = move_roomba(
                move,
                x_coord,
                y_coord,
                dir_num,
                elapsed_time
                )
        else:
            # Randomly chooses whether to turn left or right.
            right_or_left = random.random()
            if right_or_left < 0.5:
                turn_dir = LEFT
            else:
                turn_dir = RIGHT
            dir_num, elapsed_time = turn_roomba(
                turn_dir,
                dir_num,
                elapsed_time
                )

    # Prints the final status once the maximum run time is reached.
    print_status(x_coord, y_coord, dir_num, elapsed_time)

    return (
        x_coord,
        y_coord,
        dir_num,
        elapsed_time
    )


def adjust_roomba(x_coord, y_coord, dir_num, elapsed_time):
    '''
    This function randomly turns the roomba and moves it forward
    a random number of times to adjust after hitting an obstacle.

    Parameters:
    x_coord (int): The current x-coordinate of the roomba.
    y_coord (int): The current y-coordinate of the roomba.
    dir_num (int): The current numerical direction of the roomba.
    elapsed_time (int): The current elapsed time.

    Returns:
    x_coord (int): The adjusted x-coordinate of the roomba.
    y_coord (int): The adjusted y-coordinate of the roomba.
    dir_num (int): The adjusted numerical direction of the roomba.
    elapsed_time (int): The updated elapsed time.

    Examples:
    The following are possible results because this function is random.
    >>> adjust_roomba(0, 0, 1, 0)
    (5, 0, 2, 23)
    >>> adjust_roomba(10, 10, 2, 20)
    (10, 5, 3, 43)
    >>> adjust_roomba(-10, 5, 4, 100)
    (-10, -5, 3, 133)
    '''
    # Randomly chooses a left or right turn.
    turn_chance = random.random()

    if turn_chance < 0.5:
        adjust_turn = RIGHT
    else:
        adjust_turn = LEFT

    # Turns the roomba before trying to move away from the obstacle.
    dir_num, elapsed_time = turn_roomba(
        adjust_turn,
        dir_num,
        elapsed_time
        )

    # Randomly chooses between one and ten forward movements.
    move_times = int(random.random() * 10) + 1

    # Calculates where the roomba would end after all movements.
    new_x = x_coord
    new_y = y_coord

    if dir_num == 1:
        new_y += move_times * MOVE
    elif dir_num == 2:
        new_x += move_times * MOVE
    elif dir_num == 3:
        new_y -= move_times * MOVE
    else:
        new_x -= move_times * MOVE

    # Checks whether the complete movement remains within the room.
    if (
        get_valid_coordinate(new_x, MIN_COORD, MAX_COORD) and
        get_valid_coordinate(new_y, MIN_COORD, MAX_COORD)
        ):
        move_counter = 1

        # Performs each forward movement.
        while move_counter <= move_times:
            x_coord, y_coord, elapsed_time = move_roomba(
                'Forward',
                x_coord,
                y_coord,
                dir_num,
                elapsed_time
                )
            move_counter += 1

        return (
            x_coord,
            y_coord,
            dir_num,
            elapsed_time + 10
            )

    # Tries another random adjustment if this movement is not valid.
    return adjust_roomba(
        x_coord,
        y_coord,
        dir_num,
        elapsed_time
        )


def sweep(x_coord, y_coord, dir_num, elapsed_time, ctr):
    '''
    This function recursively moves the roomba through its sweep
    pattern while updating and printing its status.

    Parameters:
    x_coord (int): The current x-coordinate of the roomba.
    y_coord (int): The current y-coordinate of the roomba.
    dir_num (int): The current numerical direction of the roomba.
    elapsed_time (int): The current elapsed time.
    ctr (int): The current step of the sweep.

    Returns:
    x_coord (int): The final x-coordinate of the roomba.
    y_coord (int): The final y-coordinate of the roomba.
    dir_num (int): The final numerical direction of the roomba.
    elapsed_time (int): The final elapsed time.
    ctr (int): The counter after the sweep is completed.

    Examples:
    >>> sweep(0, 0, 1, 0, 8)
    The roomba is at the location: (-5, 0) facing West after
    0.22 minutes have passed.
    (-5, 0, 4, 13, 9)
    >>> sweep(10, 10, 2, 20, 8)
    The roomba is at the location: (10, 15) facing North after
    0.55 minutes have passed.
    (10, 15, 1, 33, 9)
    >>> sweep(-5, 5, 4, 30, 8)
    The roomba is at the location: (-5, 0) facing South after
    0.72 minutes have passed.
    (-5, 0, 3, 43, 9)
    '''
    # Completes the anti-clockwise half of the sweep.
    if ctr > 4:
        if ctr > 8:
            return (
                x_coord,
                y_coord,
                dir_num,
                elapsed_time,
                ctr
                )
        if ctr == 5:
            dir_num, elapsed_time = turn_roomba(LEFT, dir_num, elapsed_time)
        dir_num, elapsed_time = turn_roomba(LEFT, dir_num, elapsed_time)
        x_coord, y_coord, elapsed_time = move_roomba(
            'Forward',
            x_coord,
            y_coord,
            dir_num,
            elapsed_time
            )
        ctr += 1
        print_status(x_coord, y_coord, dir_num, elapsed_time)
        return sweep(x_coord, y_coord, dir_num, elapsed_time, ctr)

    # Completes the clockwise half of the sweep.
    dir_num, elapsed_time = turn_roomba(RIGHT, dir_num, elapsed_time)
    x_coord, y_coord, elapsed_time = move_roomba(
        'Forward',
        x_coord,
        y_coord,
        dir_num,
        elapsed_time
        )
    ctr += 1
    print_status(x_coord, y_coord, dir_num, elapsed_time)
    return sweep(x_coord, y_coord, dir_num, elapsed_time, ctr)


def print_distance(orig_x, orig_y, current_x, current_y):
    '''
    This function calculates and prints the distance between the
    original and current coordinates of the roomba.

    Parameters:
    orig_x (int): The original x-coordinate of the roomba.
    orig_y (int): The original y-coordinate of the roomba.
    current_x (int): The current x-coordinate of the roomba.
    current_y (int): The current y-coordinate of the roomba.

    Returns:
    None

    Examples:
    >>> print_distance(0, 0, 3, 4)
    I have traveled 5.0 meters far.
    >>> print_distance(1, 1, 1, 1)
    I have traveled 0.0 meters far.
    >>> print_distance(-2, -3, 1, 1)
    I have traveled 5.0 meters far.
    '''
    # Calculates the displacement distance from the original position.
    roomba_displacement = round(math.sqrt(
        math.pow(current_x - orig_x, 2) +
        math.pow(current_y - orig_y, 2)), 2
        )
    print('I have traveled ' + str(roomba_displacement) + ' meters far.')


def control_menu():
    '''
    This function runs the roomba controller menu and lets the user
    choose actions until the roomba is turned off or must recharge.

    Parameters:
    None

    Returns:
    None

    Examples:
    >>> control_menu()
    Welcome to the Roomba Controller!
    # User inputs starting coordinates 0, 0, direction 1, then option 7
    I have traveled 0.0 meters far.
    Turning off!
    >>> control_menu()
    Welcome to the Roomba Controller!
    # User inputs starting coordinates 5, 5, direction 2, then option 7
    I have traveled 0.0 meters far.
    Turning off!
    >>> control_menu()
    Welcome to the Roomba Controller!
    # User inputs starting coordinates -5, 10, direction 4, then option 7
    I have traveled 0.0 meters far.
    Turning off!
    '''
    # Welcomes the user and initializes the roomba.
    print('Welcome to the Roomba Controller!')
    x_coord, y_coord, dir_num = start_coords()
    orig_x = x_coord
    orig_y = y_coord
    elapsed_time = 0
    menu_choice = 0

    # Repeats the controller menu until shutdown or recharge is required.
    while menu_choice != 7 and elapsed_time < MAX_RUN_TIME:
        print(
            'Please select an option below:\n'
            '1. Reinitialize the roomba\n'
            '2. Move the roomba\n'
            '3. Turn the roomba\n'
            '4. Let the roomba roam\n'
            '5. Let the roomba do one sweep\n'
            '6. Get the roomba\'s status\n'
            '7. Turn off the roomba'
            )
        menu_choice = int(input())

        # Performs the action selected from the controller menu.
        if menu_choice == 1:
            x_coord, y_coord, dir_num = start_coords()
            orig_x = x_coord
            orig_y = y_coord
            elapsed_time += 120
        elif menu_choice == 2:
            old_time_elapsed = elapsed_time
            x_coord, y_coord, elapsed_time = input_move_roomba(
                x_coord,
                y_coord,
                dir_num,
                elapsed_time
                )
            # Checks for an obstacle only if the roomba actually moved.
            if old_time_elapsed < elapsed_time:
                obstacle_chance = random.random()
                if obstacle_chance < 0.2:
                    print('Roomba hit an obstacle! Adjusting!')
                    x_coord, y_coord, dir_num, elapsed_time = adjust_roomba(
                        x_coord,
                        y_coord,
                        dir_num,
                        elapsed_time
                        )
                print_status(x_coord, y_coord, dir_num, elapsed_time)
        elif menu_choice == 3:
            dir_num, elapsed_time = input_turn_roomba(dir_num, elapsed_time)
            print_status(x_coord, y_coord, dir_num, elapsed_time)
        elif menu_choice == 4:
            x_coord, y_coord, dir_num, elapsed_time = roam_room(
                x_coord,
                y_coord,
                dir_num,
                elapsed_time
                )
        elif menu_choice == 5:
            x_coord, y_coord, dir_num, elapsed_time, ctr = sweep(
                x_coord,
                y_coord,
                dir_num,
                elapsed_time,
                1
                )
        elif menu_choice == 6:
            print_status(x_coord, y_coord, dir_num, elapsed_time)
        elif not 1 <= menu_choice <= 7:
            print('Please enter valid option!')
        if elapsed_time >= MAX_RUN_TIME:
            print('Roomba has to recharge.')

    # Prints the final displacement before turning the roomba off.
    print_distance(orig_x, orig_y, x_coord, y_coord)
    print('Turning off!')
    return


control_menu()