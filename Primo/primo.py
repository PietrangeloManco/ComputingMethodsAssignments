"""Counts the occurrences of each alphabetical character in a given book."""
from collections import Counter
from timeit import default_timer as timer
import os
from matplotlib import pyplot as plt
import pandas

def start():
    """--help option function."""
    print('\nType "--help" for instructions, "run" to execute the script.\n')
    choice = input()
    if choice == '--help':
        print('\nInsert a txt file path to get the letters occurences.\n')
        return 'ok'
    if choice == 'run':
        return 'ok'
    print('\nInvalid choice. Try again.\n')
    return 'ohno'

def check(path):
    """Checking the input file's validity."""
    if os.path.exists(path) and path.endswith('.txt'):
        return 'nice'
    print('\nBad or nonexisting file. Try again.\n')
    return 'abort'

def characters_counter(bookpath):
    """Actual counter of occurrences."""
    letters_list, lines_list, words_number = book_creation(bookpath)
    letters_counter = Counter(letters_list)
    occurrences_sum = sum(letters_counter.values())
    occurrences_dict = sorted(letters_counter.items())
    for key, value in occurrences_dict:
        print(f'{key} : {value*100/occurrences_sum:.4f} % ({value} occurrences)')
    print('\nDo you want to see the given book stats? (y for yes, anything else for no).\n')
    if input() == 'y':
        basic_stats(occurrences_sum, lines_list, words_number)
    return occurrences_dict

def histogram(occ):
    """Making an histogram of the occurrences."""
    print('\nDo you want to see the occurrences histogram? (y for yes, anything else for no).\n')
    if input() == 'y':
        hist = pandas.DataFrame(occ, columns = ['letter', 'frequency'])
        hist.plot(kind = 'bar', x = 'letter')
        plt.show()
        return
    return

def book_lenght(text):
    """Asking the user if he wants to skip some pages."""
    print('\nDo you want to skip some lines? (y for yes, anything else for no).\n')
    if input() == 'y':
        print('\nWhich line should I start with?\n')
        while True:
            try:
                init = int(input()) - 1
                break
            except ValueError:
                print('\nInvalid choice. Try again.\n')
        if 0 < init < len(text):
            print('\nWhich line shoud I stop with?\n')
            while True:
                try:
                    last = int(input()) - 1
                    break
                except ValueError:
                    print('\nInvalid choice. Try again.\n')
            if last > 0 and init < last < len(text):
                effective_text = text[init:last]
                return effective_text
    return text

def book_creation(bpath):
    """Takes a book and does stuff with it."""
    with open(bpath) as book:
        book_lines = book.readlines()
        effective_book_lines = book_lenght(book_lines)
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

time_0 = timer()
while True:
    if start() == 'ok':
        break
print('\nInsert your files path:\n')
while True:
    book_path = (input())
    if check(book_path) == 'nice':
        break
oc_dict = characters_counter(book_path)
histogram(oc_dict)
time_1 = timer()
print(f'\nTotal elapsed time: {(time_1-time_0): .4f} s\n')
