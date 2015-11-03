"""
Algorithmic Thinking Part 2
Project 4: Computing alignment of Sequences

Author: Weikang Sun
Date: 11/2/15

CodeSkulptor source:
http://www.codeskulptor.org/#user40_tbt1hSyQm6_25.py
"""

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Function to build a scoring matrix given the alphabet, diagonal score,
    off-diagonal score, and dash score. 
    Returns dictionary of dictionaries.
    """
    
    alphabet_dash = list(alphabet) + ["-"]
    score_matrix = {}
    
    for entry_row in alphabet_dash:
        matrix_row = {}
        for entry_column in alphabet_dash:
            if entry_row is "-" or entry_column is "-":
                matrix_row[entry_column] = dash_score
            elif entry_column is entry_row:
                matrix_row[entry_column] = diag_score
            else:
                matrix_row[entry_column] = off_diag_score
        
        score_matrix[entry_row] = matrix_row
        
    return score_matrix


def print_scoring_matrix(scoring_matrix):
    """ Helper function to print scoring matrix nicely """
    
    for row in scoring_matrix.keys():
        print str(row) + ": " + str(scoring_matrix[row])


def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag = True):
    """
    Function to compute the alignment matrix for two sequences given
    those sequences and the scoring matrix. Global flag dictates whether
    a global or local alignment should be computed.
    Returns a matrix.
    """
    
    len_x = len(seq_x) + 1
    len_y = len(seq_y) + 1
    
    # first create an empty grid of the right dimensions
    align_matrix = [[0 for dummy_col in range(len_y)] for dummy_row in range(len_x)]
    
    # global flag allows negative scores
    if global_flag:
        # fill out leftmost column with incrementing dash score
        for row in range(1, len_x ):
            align_matrix[row][0] = align_matrix[row - 1][0] + \
                                   scoring_matrix[seq_x[row - 1]]["-"]
        
        # fill out uppermost row with increment dash score
        for col in range(1, len_y):
            align_matrix[0][col] = align_matrix[0][col - 1] + \
                                   scoring_matrix["-"][seq_y[col - 1]]
 
    # iteratively fill out the rest of the matrix
    for row in range(1, len_x):
        for col in range(1, len_y):
            align_matrix[row][col] = max(align_matrix[row - 1][col - 1] + 
                                         scoring_matrix[seq_x[row - 1]][seq_y[col - 1]],
                                         align_matrix[row - 1][col] + 
                                         scoring_matrix[seq_x[row - 1]]["-"],
                                         align_matrix[row][col - 1] + 
                                         scoring_matrix["-"][seq_y[col - 1]])
            if not global_flag:
                # must be all positive or 0
                align_matrix[row][col] = max(align_matrix[row][col], 0)
    
    return align_matrix


def print_alignment_matrix(align_matrix):
    """ Helper function to print  alignment matrix nicely"""
    for row in range(len(align_matrix)):
        print align_matrix[row]
        
    return


def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Function to compute the global alignment of two sequences given the 
    scoring matrix and their global alignment matrix.
    Returns a tuple of the form (score, align_x, align_y)
    """
    
    row = len(seq_x)
    col = len(seq_y)
    align_x = ""
    align_y = ""
    
    while row != 0 and col != 0:
        # checks along diagonal
        if alignment_matrix[row][col] == alignment_matrix[row - 1][col - 1] + \
                                     scoring_matrix[seq_x[row - 1]][seq_y[col - 1]]:
            align_x = seq_x[row - 1] + align_x
            align_y = seq_y[col - 1] + align_y
            row -= 1
            col -= 1
        else:
            # checks along row
            if alignment_matrix[row][col] == alignment_matrix[row - 1][col] + \
                                        scoring_matrix[seq_x[row - 1]]["-"]:
                align_x = seq_x[row - 1] + align_x
                align_y = "-" + align_y
                row -= 1
            else:
                align_x = "-" + align_x
                align_y = seq_y[col - 1] + align_y
                col -= 1
                
    while row != 0:
        align_x = seq_x[row - 1] + align_x
        align_y = "-" + align_y
        row -= 1
        
    while col != 0:
        align_x = "-" + align_x
        align_y = seq_y[col - 1] + align_y
        col -= 1
                
    
    return (alignment_matrix[-1][-1], align_x, align_y)


def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Function to compute the local alignment of two sequences given the
    scoring matrix and their local alignment matrix.
    Returns a tuple of the form (score, align_x, align_y)
    """
    
    row = 0
    col = 0
    max_value = 0
    
    # find the maximum value and grid coordinates in the alignment matrix
    for row_i in range(len(seq_x) + 1):
        for col_j in range(len(seq_y) + 1):
            value = alignment_matrix[row_i][col_j]
            if value > max_value:
                max_value = value
                row = row_i
                col = col_j
    
    align_x = ""
    align_y = ""
    
    while row != 0 and col != 0:
        # checks along diagonal
        if alignment_matrix[row][col] == alignment_matrix[row - 1][col - 1] + \
                                     scoring_matrix[seq_x[row - 1]][seq_y[col - 1]]:
            align_x = seq_x[row - 1] + align_x
            align_y = seq_y[col - 1] + align_y
            row -= 1
            col -= 1
        else:
            # checks along row
            if alignment_matrix[row][col] == alignment_matrix[row - 1][col] + \
                                        scoring_matrix[seq_x[row - 1]]["-"]:
                align_x = seq_x[row - 1] + align_x
                align_y = "-" + align_y
                row -= 1
            else:
                align_x = "-" + align_x
                align_y = seq_y[col - 1] + align_y
                col -= 1
        if alignment_matrix[row][col] == 0:
            break
    
    return (max_value, align_x, align_y)
