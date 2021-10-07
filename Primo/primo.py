"""Counts the occurrences of each alphabetical character in a given book."""
from collections import Counter
from timeit import default_timer as timer
import argparse
import sys
import pandas
from matplotlib import pyplot as plt

def check(path):
    """Checking the input file's validity."""
    if path.endswith('.txt'):
        return 'nice'
    print('\nBad or nonexisting file. Try again.\n')
    return 'abort'

def characters_counter(letters_list):
    """Actual counter of occurrences."""
    letters_counter = Counter(letters_list)
    occurrences_sum = sum(letters_counter.values())
    occurrences_dict = sorted(letters_counter.items())
    for key, value in occurrences_dict:
        print(f'{key} : {value*100/occurrences_sum:.4f} % ({value} occurrences)')
    return occurrences_dict, occurrences_sum

def histogram(occ):
    """Making an histogram of the occurrences."""
    hist = pandas.DataFrame(occ, columns = ['letter', 'frequency'])
    hist.plot(kind = 'bar', x = 'letter')
    plt.show()

def book_lenght(text, fline, lline):
    """Asking the user if he wants to skip some pages."""
    if lline == -1:
        lline = len(text)
    if 0 <= fline <= lline <= len(text):
        effective_text = text[fline:lline]
        return effective_text
    print('\nInvalide line choices.\n')
    sys.exit()

def book_creation(bpath, firstline, lastline):
    """Takes a book and does stuff with it."""
    with open(bpath) as book:
        book_lines = book.readlines()
        effective_book_lines = book_lenght(book_lines, firstline, lastline)
    wordcount = 0
    for line in effective_book_lines:
        wordcount += len(line.split())
    with open('New_book.txt', 'w') as effective_book_w:
        for item in effective_book_lines:
            effective_book_w.write('%s\n' % item)
    with open('New_book.txt', 'r') as  effective_book_r:
        ext_letters_list = [ch.lower() for ch in effective_book_r.read() if ch.isalpha()]
    return [ext_letters_list, effective_book_lines, wordcount]

def basic_stats(book_characters, book_lines, book_words):
    """Some prints of book stats."""
    num_of_lines = 0
    for item in book_lines:
        if item != '\n':
            num_of_lines += 1
    print(f'\nThe number of characters is {book_characters}.\n')
    print(f'\nThe number of non blank lines is {num_of_lines}.\n')
    print(f'\nThe number of words is {book_words}.\n')

parser = argparse.ArgumentParser()
parser.add_argument("book", type = str, help = "Book file to work on.")
parser.add_argument("-histogram", "-hi", help = "Shows the histogram plot.", action = "store_true")
parser.add_argument("-stats", "-s", help = "Shows the books stats.", action = "store_true")
parser.add_argument("-startb", "-st", type = int, default = 0, help = "Read the book from here.")
parser.add_argument("-endb", "-e", type = int, default = -1, help = "Read the book ending here.")
args = parser.parse_args()
time_0 = timer()
if check(args.book) == 'abort':
    sys.exit()
lett_list, l_list, w_number = book_creation(args.book, args.startb, args.endb)
oc_dict, oc_sum = characters_counter(lett_list)
if args.histogram:
    histogram(oc_dict)
if args.stats:
    basic_stats(oc_sum, l_list, w_number)
time_1 = timer()
print(f'\nTotal elapsed time: {(time_1-time_0): .4f} s\n')
