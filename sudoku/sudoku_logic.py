import random
import numpy as np

def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + startRow][j + startCol] == num:
                return False
    return True

def find_empty_location(board, l):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                l[0] = row
                l[1] = col
                return True
    return False

def solve_sudoku(board):
    l = [0, 0]
    if not find_empty_location(board, l):
        return True
    row, col = l
    nums = list(range(1,10))
    random.shuffle(nums)
    for num in nums:
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0
    return False


def generate_sudoku_solution():
    board = np.zeros((9, 9), dtype=int)
    nums = list(range(1,10))
    random.shuffle(nums)
    board[0] = nums
    if solve_sudoku(board):
        return board
    return None


def generate_puzzle(difficulty):
    solution_board = generate_sudoku_solution()
    clues = int()   
    if difficulty == 'test':
        clues = 80
    if difficulty == 'easy':
        clues = 40  
    if difficulty == 'medium':
        clues = 30
    if difficulty == 'hard':
        clues = 20
    if solution_board is not None:
        board = remove_numbers_to_create_puzzle(solution_board.tolist(), clues)
        return board, solution_board

def remove_numbers_to_create_puzzle(board, clues):
    puzzle_board = np.copy(board)
    count = 81 - clues
    while count > 0:
        i, j = random.randint(0, 8), random.randint(0, 8)
        if puzzle_board[i][j] != 0:
            puzzle_board[i][j] = 0
            count -= 1
    return puzzle_board

    
    
def check_sudoku_board(board):
    # Check each row
    for row in board:
        if not is_valid_group(row):
            return False

    # Check each column
    for col in range(9):
        if not is_valid_group([board[row][col] for row in range(9)]):
            return False

    # Check each 3x3 square
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            if not is_valid_box(board, box_row, box_col):
                return False

    # If all checks pass
    return True

def is_valid_group(group):
    """Check if a group (row/column) contains unique numbers from 1 to 9."""
    return sorted(group) == list(range(1, 10))

def is_valid_box(board, start_row, start_col):
    """Check if a 3x3 box contains unique numbers from 1 to 9."""
    numbers = []
    for row in range(3):
        for col in range(3):
            numbers.append(board[start_row + row][start_col + col])
    return is_valid_group(numbers)

def check_sudoku_solution(board):
    errors = {'rows': [], 'columns': [], 'boxes': []}
    print(board)

    # Convert board to only numbers for validation
    num_board = [[cell['value'] for cell in row] for row in board]

    # Check each row
    for i, row in enumerate(num_board):
        if not is_valid_group(row):
            errors['rows'].append(i)

    # Check each column
    for j in range(9):
        column = [num_board[i][j] for i in range(9)]
        if not is_valid_group(column):
            errors['columns'].append(j)

    # Check each 3x3 square
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            if not is_valid_box(num_board, box_row, box_col):
                errors['boxes'].append((box_row // 3, box_col // 3))

    is_correct = not (errors['rows'] or errors['columns'] or errors['boxes'])
    print(is_correct, errors)
    return is_correct, errors
