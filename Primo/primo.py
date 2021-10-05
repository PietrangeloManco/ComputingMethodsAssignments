"""Counts the occurrences of each alphabetical character in a given book."""
from collections import Counter
from timeit import default_timer as timer
import os
from matplotlib import pyplot
import pandas

def start():
    """--help option function."""
    print('type "--help" for instructions, "run" to execute the script.')
    choice = input()
    if choice == '--help':
        print('Insert a txt file path to get the letters occurences.')
        characters_counter()
        return
    if choice == 'run':
        characters_counter()
        return
    print('Invalid choice. Try again.\n')
    start()
    return

def check(path):
    """Checking the input file's validity."""
    if os.path.exists(path) and path.endswith('.txt'):
        return 'nice'
    print('Bad or non existing file. Try again.\n')
    characters_counter()
    return 'abort'

def characters_counter():
    """Actual counter of occurrences."""
    print('Insert your files path:\n')
    book_path = (input())
    if check(book_path) == 'abort':
        return
    with open(book_path) as book:
        letters_list = [ch.lower() for ch in book.read() if ch.isalpha()]
    counter = Counter(letters_list)
    occurrences_sum = sum(counter.values())
    occurrences_dict = sorted(counter.items())
    for key, value in occurrences_dict:
        print(f'{key} : {value*100/occurrences_sum:.4f} % ({value} occurrences)')
    histogram(occurrences_dict)
    return

def histogram(occ):
    """Making an histogram of the occurrences."""
    print('Do you want to see the occurrences histogram? (type y for yes, anything else for no.)\n')
    if input() == 'y':
        hist = pandas.DataFrame(occ, columns = ['letter', 'frequency'])
        hist.plot(kind = 'bar', x = 'letter')
        pyplot.show()
        return
    return

time_0 = timer()
start()
time_1 = timer()
print(f'\nTotal elapsed time: {(time_1-time_0): .4f} s')
