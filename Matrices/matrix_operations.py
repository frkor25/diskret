matrix = list[list]

# matrix_operations

def matrix_product(a: matrix, b: matrix) -> matrix:
    """Returns matrix product of a and b."""
    product_matrix = [[0 for col in b[0]] for row in a]
    i = 0
    while i < len(a):
        j = 0
        while j < len(b[0]):
            product_matrix[i][j] = sum([a[i][k]*b[k][j] for k in range(len(b))])
            j += 1
        i += 1
    return product_matrix

def power_matrix(a: matrix, exponent: int) -> matrix:
    """Returns matrix to the power of exponent."""
    if exponent == 1:
        return a
    else:
        return matrix_product(a, power_matrix(a, exponent-1))
    

def matrix_bool_product(a: matrix, b: matrix) -> matrix:
    """Returns the boolean product of two boolean matrices a and b ⊙."""
    bool_product_matrix = [[0 for col in b[0]] for row in a]
    i = 0
    while i < len(a):
        j = 0
        while j < len(b[0]):
            bool_product_matrix[i][j] = 1 if any([a[i][k] == 1 and b[k][j] == 1 for k in range(len(b))]) else 0
            j += 1
        i += 1
    return bool_product_matrix

def matrix_join(a: matrix, b: matrix) -> matrix:
    """Returns the joined matrix of two boolean matrices a and b ∨."""
    joined_matrix = [[0 for col in a[0]] for row in a]
    i = 0
    while i < len(a):
        j = 0
        while j < len(a[i]):
            if a[i][j] == 1 or b[i][j] == 1:
                joined_matrix[i][j] = 1
            else:
                joined_matrix[i][j] = 0
            j += 1
        i += 1
    return joined_matrix

def matrix_meet(a: matrix, b: matrix) -> matrix:
    """Returns the meet of two boolean matrices a and b ∧."""
    meet_matrix = [[0 for col in a[0]] for row in a]
    i = 0
    while i < len(a):
        j = 0
        while j < len(a[0]):
            if a[i][j] == 1 and b[i][j] == 1:
                meet_matrix[i][j] = 1
            else:
                meet_matrix[i][j] = 0
            j += 1
        i += 1
    return meet_matrix


def matrix_add(a: matrix, b: matrix) -> matrix:
    """Returns the sum of two matrices a and b."""
    added_matrix = [[0 for col in a[0]] for row in a]
    i = 0
    while i < len(a):
        j = 0
        while j < len(a[0]):
            added_matrix[i][j] = a[i][j] + b[i][j]
            j += 1
        i += 1
    return added_matrix


def is_symmetric_matrix(a: matrix) -> bool:
    """Checks if matrix is symmetric."""
    symmetric = True
    if len(a) != len(a[0]):
        symmetric = False
    i = 0
    while i < len(a) and symmetric:
        j = 0
        while j < len(a[0]) and symmetric:
            symmetric = a[i][j] == a[j][i]
            j += 1
        i += 1
    return symmetric


def transpose_matrix(a: matrix) -> matrix:
    """Transposes a matrix."""
    transposed_matrix = [[0 for row in a] for col in a[0]]
    i = 0
    while i < len(a):
        j = 0
        while j < len(a[0]):
            transposed_matrix[j][i] = a[i][j]
            j += 1
        i += 1
    return transposed_matrix


def print_matrix(a: matrix) -> None:
    """Prints matrix with a proper forma.t"""
    for row in a:
        print(" ".join(str(num) for num in  row))
