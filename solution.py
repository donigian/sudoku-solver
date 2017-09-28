assignments = []
units = {}
peers = {}
unitlist = []
cols = '123456789'
rows = 'ABCDEFGHI'

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

# represent diagonal unit and cross diagonal unit
diag_units = [[row_letter + col_number for (row_letter, col_number) in zip(list(rows), list(cols))]]
diag_units_cross = [[row_letter_cross_diag + col_number_cross_diag for (row_letter_cross_diag, col_number_cross_diag) in zip(list(rows), list(cols[::-1]))]]
unitlist = row_units + column_units + square_units + diag_units + diag_units_cross

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    naked_twins_found = find_naked_twins(values)

    # Eliminate the naked twins as possibilities for their peers
    eliminate_twins(values, naked_twins_found)
    return values

def find_naked_twins(values):
    """
    Find all naked twins instances
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    :return:
        a dictionary with twins as keys and a list of boxes which contain the twin. indexing
        by twin allows us to easily lookup boxes which contain that value as we would in a
        linked list fashion
    """
    twins_found = {}
    for twin, box in [(values[box], box) for box in values.keys() if len(values[box]) == 2]:
        if twin in twins_found:
            twins_found[twin].add(box)
        else:
            twins_found[twin] = {box}

    # since its possible to have a unique box value which is of size 2 let's
    # remove boxes which only contain a single value of length 2
    twins_found = {value: boxes for (value, boxes) in twins_found.items() if len(boxes) > 1}
    return twins_found

def eliminate_twins(values, naked_twins_found):
    """
    :param values: a dictionary of the form {'box_name': '123456789', ...}
    :param naked_twins_found: dict with twins found, key represents values, value represents boxes
    :return: naked twins eliminated
    """
    # iterate over row, column, square and diagonal units respectively
    for unit in unitlist:
        for i in range(0, len(unit)):
            first_box = unit[i]
            first_box_value = values[first_box]
            if first_box_value in naked_twins_found:
                # compare first box with all other boxes to find twin
                for j in range(i + 1, len(unit)):
                    second_box = unit[j]
                    if second_box in naked_twins_found[first_box_value]:
                        # twin found, remove pair of digits from all other peers
                        for digit in first_box_value:
                            other_unit_boxes = [box for box in unit if box not in {first_box, second_box} ]
                            for peer in other_unit_boxes:
                                assign_value(values, peer, values[peer].replace(digit, ''))
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Input: A grid in string form.
    Output: A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    # Write a function that will take as an input, the sudoku in dictionary form,
    # run through all the boxes, applying the eliminate technique,
    # and return the resulting sudoku in dictionary form.
    solved_boxes = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_boxes:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # could be stalled due to naked twins variation, thus let's check
        if stalled:
            values = naked_twins(values)
            solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
            stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def solve(grid):
    return search(grid_values(grid))

def search(values):
    "Using depth-first search and propagation, try all possible values."

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier

    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!

    # Chose one of the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')