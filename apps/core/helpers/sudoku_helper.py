from django.http.request import QueryDict

DICT_SQUARES_INDEXES = {0: 0, 1: 0, 2: 0, 3: 3, 4: 3, 5: 3, 6: 6, 7: 6, 8: 6}
DIMENSION_OF_SUDOKU_TABLE = 9

def validate_the_numerical_values_and_fill_the_matrix(matrix: list, introduced_values: list, request_post: QueryDict) -> str | None:
    error_msg = None
    i = 1
    while i <= DIMENSION_OF_SUDOKU_TABLE and error_msg is None:
        j = 1
        while j <= DIMENSION_OF_SUDOKU_TABLE and error_msg is None:
            value_cell = request_post.get(f"cell_{i}{j}") or "0"
            if value_cell.isnumeric() and len(value_cell) == 1:
                matrix[i - 1][j - 1] = int(value_cell)
                if value_cell != "0":
                    introduced_values.append(f"cell_{i}{j}")
            else:
                error_msg = "The value cell must be numeric and between 1 and 9."
            j += 1
        i += 1
    return error_msg

def is_valid_sudoku(matrix: list) -> bool:
    is_valid = True
    #~ Verify if the table is 9x9
    acum = 0
    for row in matrix:
        is_valid = len(row) == DIMENSION_OF_SUDOKU_TABLE
        acum += len(row)
    if acum != DIMENSION_OF_SUDOKU_TABLE**2:
        is_valid = False
    #~ Verify if the sudoku table is well-structured
    i = 0
    while i < DIMENSION_OF_SUDOKU_TABLE and is_valid:
        j = 0
        while j < DIMENSION_OF_SUDOKU_TABLE and is_valid:
            value_cell = matrix[i][j]
            if value_cell != 0:
                for k in set(range(DIMENSION_OF_SUDOKU_TABLE)) - {j}:
                    if matrix[i][k] == value_cell:
                        is_valid = False
                        break
                for k in set(range(DIMENSION_OF_SUDOKU_TABLE)) - {i}:
                    if matrix[k][j] == value_cell:
                        is_valid = False
                        break
                square_index_row = DICT_SQUARES_INDEXES[i]
                square_index_column = DICT_SQUARES_INDEXES[j]
                for k in range(square_index_row, square_index_row + 3):
                    for p in range(square_index_column, square_index_column + 3):
                        if matrix[k][p] == value_cell and (k != i or p != j):
                            is_valid = False
                            break
            j += 1
        i += 1
    #~ Verify all the empty cells of the table can have at least one posible value.
    i = 0
    while i < DIMENSION_OF_SUDOKU_TABLE and is_valid:
        j = 0
        while j < DIMENSION_OF_SUDOKU_TABLE and is_valid:
            if matrix[i][j] == 0:
                is_valid = len(_get_posible_values_of_cell(matrix, i, j)) >= 1
            j += 1
        i += 1

    return is_valid

def _get_posible_values_of_cell(matrix: list, i: int, j: int) -> list:
    posible_values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for k in range(DIMENSION_OF_SUDOKU_TABLE):
        if matrix[i][k] != 0 and matrix[i][k] in posible_values:
            posible_values.remove(matrix[i][k])
    for k in range(DIMENSION_OF_SUDOKU_TABLE):
        if matrix[k][j] != 0 and matrix[k][j] in posible_values:
            posible_values.remove(matrix[k][j])
    square_index_row = DICT_SQUARES_INDEXES[i]
    square_index_column = DICT_SQUARES_INDEXES[j]
    for k in range(square_index_row, square_index_row + 3):
        for p in range(square_index_column, square_index_column + 3):
            if matrix[k][p] != 0 and matrix[k][p] in posible_values:
                posible_values.remove(matrix[k][p])
    return posible_values

def solve_sudoku(matrix: list):
    #~ Solve the sudoku table using back-tracking algorithm template.
    _solve_sudoku0(matrix, 0, 0, [True])

def _solve_sudoku0(matrix: list, i: int, j: int, incompleted: list) -> None:
    if i < DIMENSION_OF_SUDOKU_TABLE and j < DIMENSION_OF_SUDOKU_TABLE:
        if matrix[i][j] == 0:
            posible_values = _get_posible_values_of_cell(matrix, i, j)
            k = 0
            while k < len(posible_values) and incompleted[0]:
                matrix[i][j] = posible_values[k]
                _solve_sudoku0(matrix, i, j + 1, incompleted)
                k += 1
                if incompleted[0]:
                    matrix[i][j] = 0
        else:
            _solve_sudoku0(matrix, i, j + 1, incompleted)
    elif i < DIMENSION_OF_SUDOKU_TABLE:
        _solve_sudoku0(matrix, i + 1, 0, incompleted)
    else:
        incompleted[0] = False