"""
Provide code and solution for Application 4

Author: Weikang Sun
Date: 11/7/15

CodeSkulptor source:
http://www.codeskulptor.org/#user40_lwvHBczIBP_16.py
"""

DESKTOP = False

import math
import random
import urllib2

if DESKTOP:
    import matplotlib.pyplot as plt
    import alg_project4_solution as student
else:
    import simpleplot
    import user40_tbt1hSyQm6_26 as student
    import codeskulptor
    
    codeskulptor.set_timeout(100)
    

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict


def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)
    
    # read in files as string
    words = word_file.read()
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list


def question1():
    """ determine local alignment of human and fruitfly eyeless protein """
    
    # load sequences and scoring matrix
    score_matrix = read_scoring_matrix(PAM50_URL)
    human_eyeless = read_protein(HUMAN_EYELESS_URL)
    fruitfly_eyeless = read_protein(FRUITFLY_EYELESS_URL)
    
    # compute local alignment matrix
    align_matrix = student.compute_alignment_matrix(human_eyeless, fruitfly_eyeless, 
                                                    score_matrix, False)
    
    # compute local alignment score and sequences
    score, human_align, fruitfly_align = student.compute_local_alignment(human_eyeless, fruitfly_eyeless,
                                                                         score_matrix, align_matrix)
    
    print "Score: " + str(score)
    print "Human: " + human_align
    print "FrFly: " + fruitfly_align
    
    return


def question2():
    """ determine global alignment of consensusPAX 
    with local human and frfly sequences
    """
    
    # load sequences and scoring matrix
    score_matrix = read_scoring_matrix(PAM50_URL)
    human_seq = "HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEKQQ"
    frfly_seq = "HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ"
    consensus_pax = read_protein(CONSENSUS_PAX_URL)
    
    # compute human and fruitfly global alignment matrix with consensus pax
    human_align_matrix = student.compute_alignment_matrix(human_seq, consensus_pax, score_matrix, True)
    frfly_align_matrix = student.compute_alignment_matrix(frfly_seq, consensus_pax, score_matrix, True)
    
    # compute human and fruitfly global alignment sequences
    score_human, human_align, consensus_align = student.compute_global_alignment(human_seq, consensus_pax, 
                                                                                 score_matrix, human_align_matrix)
    score_fly, frfly_align, consensus_align_2 = student.compute_global_alignment(frfly_seq, consensus_pax,
                                                                                 score_matrix, frfly_align_matrix)
    
    # compute percentages match for human and fruitfly
    human_count = 0.0
    for index in range(len(human_align)):
        if human_align[index] == consensus_align[index]:
            human_count += 1
            
    frfly_count = 0.0
    for index in range(len(frfly_align)):
        if frfly_align[index] == consensus_align_2[index]:
            frfly_count += 1
            
    print "% Human: " + str(human_count / len(human_align) * 100)
    print "Hmn: " + human_align
    print "PAX: " + consensus_align
    
    print ""
    
    print "% FrFly: " + str(frfly_count / len(frfly_align) * 100)
    print "Fly: " + frfly_align
    print "PAX: " + consensus_align_2
    

def question4():
    """ create hypothesis testing distribution """
    
    null_dist = {}
    if DESKTOP:
        # load sequences and scoring matrix
        score_matrix = read_scoring_matrix(PAM50_URL)
        human_eyeless = read_protein(HUMAN_EYELESS_URL)
        fruitfly_eyeless = read_protein(FRUITFLY_EYELESS_URL)

        # generate the null distribution
        null_dist = generate_null_distribution(human_eyeless, fruitfly_eyeless, score_matrix, 1000)
    else:
        # previously calculated using desktop python
        null_dist = {38: 1, 39: 1, 40: 6, 41: 8, 42: 17, 43: 31, 44: 41, 45: 47, 46: 65, 47: 76,
                     48: 66, 49: 63, 50: 62, 51: 69, 52: 69, 53: 57, 54: 49, 55: 37, 56: 26, 57: 30,
                     58: 33, 59: 23, 60: 25, 61: 20, 62: 5, 63: 11, 64: 11, 65: 7, 66: 5, 67: 4,
                     68: 5, 69: 4, 70: 5, 71: 3, 72: 3, 73: 4, 74: 1, 75: 2, 80: 3, 81: 1, 82: 1,
                     85: 1, 87: 1, 92: 1}
        
    # normalize null_dist
    for key in null_dist.keys():
        null_dist[key] /= float(1000)
        
    simpleplot.plot_bars("Normalized Null Distribution of Human and Fruitfly Local Alignment (n=1000 trials)",
                         800, 600, "Local Alignment Score", "Distribution", [null_dist])
     
        
def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """ null distribution generator """

    scoring_distribution = {}
    for dummy_trial in range(num_trials):
        y_index = range(len(seq_y))
        # shuffle the y sequence
        random.shuffle(y_index)
        rand_y = ""

        for index in y_index:
            rand_y += seq_y[index]

        # compute local alignment matrix
        align_matrix = student.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)

        # compute local alignment score
        score, x_align, y_align = student.compute_local_alignment(seq_x, rand_y, scoring_matrix, align_matrix)

        if scoring_distribution.has_key(score):
            scoring_distribution[score] += 1
        else:
            scoring_distribution[score] = 1
    
    return scoring_distribution
    

def question5():
    """ determine null distribution mean and standard deviation """
    
    null_dist = {38: 1, 39: 1, 40: 6, 41: 8, 42: 17, 43: 31, 44: 41, 45: 47, 46: 65, 47: 76,
                 48: 66, 49: 63, 50: 62, 51: 69, 52: 69, 53: 57, 54: 49, 55: 37, 56: 26, 57: 30,
                 58: 33, 59: 23, 60: 25, 61: 20, 62: 5, 63: 11, 64: 11, 65: 7, 66: 5, 67: 4,
                 68: 5, 69: 4, 70: 5, 71: 3, 72: 3, 73: 4, 74: 1, 75: 2, 80: 3, 81: 1, 82: 1,
                 85: 1, 87: 1, 92: 1}
    
    # find mean
    mean = 0
    for key in null_dist.keys():
        mean += key / float(1000) * null_dist[key]
        
    print mean
    
    # find standard deviation
    variance = 0
    for key in null_dist.keys():
        variance += (key - mean) ** 2 / float(1000) * null_dist[key]
    stdev = variance ** 0.5
    
    print stdev
    
    # find z-score
    score = 875
    z_score = (score - mean) / stdev
    
    print z_score


def question7(seq_x, seq_y):
    """ determine scoring matrix of edit distance algorithm """
    
    diag_score = 2
    off_diag_score = 1
    dash_score = 0
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    score_matrix = student.build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
    
    align_matrix = student.compute_alignment_matrix(seq_x, seq_y, score_matrix, True)
    score, align_x, align_y = student.compute_global_alignment(seq_x, seq_y, score_matrix, align_matrix)
    
    edit_distance = len(seq_x) + len(seq_y) - score
    
    print "Edit distance: " + str(edit_distance)
    print align_x
    print align_y


def question8():
    """ edit distance tester """
    
    word_list = read_words(WORD_LIST_URL)
    
    print "One edit distance from humble:"
    print check_spelling("humble", 1, word_list)
    print "Two edit distance from firefly:"
    print check_spelling("firefly", 2, word_list)
    
    
def check_spelling(checked_word, dist, word_list):
    """ helper function to determine all words edit distance away """
    
    diag_score = 2
    off_diag_score = 1
    dash_score = 0
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    score_matrix = student.build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score)
    
    words = []
    
    for word in word_list:
        align_matrix = student.compute_alignment_matrix(checked_word, word, score_matrix, True)
        score, align_x, align_y = student.compute_global_alignment(checked_word, word,
                                                                   score_matrix, align_matrix)
    
        edit_distance = len(checked_word) + len(word) - score
        
        if edit_distance <= dist:
            words.append(word)
    
    return words
