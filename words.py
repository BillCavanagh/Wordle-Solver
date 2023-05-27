INIT_FILE = 'python-projects\wordle\All_English_Words.txt'
INPUT_FILE = 'python-projects\wordle\wordle_words.txt'
POSSIBLE_WORDS_FILE = 'python-projects\wordle\possible_words.txt'
WORDLE_LENGTH = 5
import time
import re
def init_wordle_words():
    with open(INIT_FILE,'r') as All_English_Words:
        with open(INPUT_FILE,'w') as wordle_words:
            for word in All_English_Words:
                word = word.strip()
                length = len(word)
                if not(word.isalpha() and WORDLE_LENGTH == length):
                    continue
                else:
                    word = word.upper()
                    wordle_words.write(word+'\n')
def excluded_letters_match(word,excluded_letters):
    # 1) Check if the word has none of the exluded letters 
    for letter in word:
        if letter in excluded_letters:
            return False
    return True
def found_letters_match(word,found_letters_exact):
    # 2) Check if the word has the same letters in the same positions as is already found
    for index in found_letters_exact:
        if not (word[index] == found_letters_exact[index]): # if letter in certain position is not present continue
            return False
    return True
def unknown_letters_match(word,found_letters_exact,found_letters_unknown):
    # 3) Check if the word has the same or more letters of each letter where the position is unknown
    if word == "COROT":
        print(found_letters_unknown)
    for letter in found_letters_unknown:
        matches_in_word = list(re.finditer(letter,word)) # get matches of a unknown letter in a potential word
        invalid_positions = set()
        for index in found_letters_exact:
            if found_letters_exact[index] == letter:
                invalid_positions += index
        invalid_positions.update(found_letters_unknown[letter][0])
        unknown_letters_left = found_letters_unknown[letter][1]
        for match in matches_in_word:
            pos = match.start()
            if pos in invalid_positions:
                continue
            else:
                unknown_letters_left -= 1
        if unknown_letters_left > 0:
            return False
    return True
def possible_words(found_letters_exact=dict(),found_letters_unknown=dict(),excluded_letters=set()):
    '''
    found_letters_exact input should be in the format: found_letters_exact[position] = letter
    ex: found_letters_exact[0] = "A"
    found_letters_unknown input should be in the format: found_letters_unknown[letter] = [[positions],amount_of_unknown]
    ex: found_letters_unknown["A"] = [[1,4],2]
    excluded_letters input should be in the format: exluded_letters(letters)
    ex: excluded_letters = set("H","A","P","Y")
    outputs all words that follow these three conditions into "possible_words.txt" as well as a dictionary of all letters and their total number of occurances
    '''
    letter_count = dict.fromkeys("ABCDEFGHIJKLMNOPQRSTUVWXYZ",0)
    with open(INPUT_FILE,'r') as words:
        with open(POSSIBLE_WORDS_FILE,'w') as possible_words:
            for word in words: 
                word = word.strip().upper()
                if word == "UNADD":
                    print(excluded_letters)
                    print(found_letters_exact)
                    print(found_letters_unknown)
                if (excluded_letters_match(word,excluded_letters) and found_letters_match(word,found_letters_exact) and unknown_letters_match(word,found_letters_exact,found_letters_unknown)):
                    # if all conditions are met write the word to possible_words.txt
                    possible_words.write(word+'\n')
                    # add letters to letter count for use in determining best word to guess later
                    for letter in word:
                        letter_count[letter] += 1
                else:
                    continue
    return letter_count
def get_letter_weights(letter_count):
    letter_weights = dict.fromkeys("ABCDEFGHIJKLMNOPQRSTUVWXYZ",0)
    with open(POSSIBLE_WORDS_FILE) as possible_words:
        total_letter_count = (len(possible_words.read().splitlines())) * WORDLE_LENGTH
    for letter in letter_weights:
        weight = letter_count[letter] / total_letter_count
        letter_weights[letter] = weight
    return letter_weights
def get_best_guess(letter_weights):
    with open(POSSIBLE_WORDS_FILE,'r') as possible_words:
        best_word_score = 0
        best_word = "" # first index is the best guess, last index is the worst guess
        for word in possible_words:
            word = word.split()[0]
            different_chrs = len(set(word))
            word_score = different_chrs
            for letter in word:
                word_score += letter_weights[letter]
            if word_score > best_word_score:
                best_word = word
                best_word_score = word_score
    return best_word
def main():
    found_letters_exact = dict()
    found_letters_unknown = dict()
    excluded_letters = set(["E","T","H","C","N","B"])
    multiple_unknowns = dict()
    found_letters_exact[1] = "O"
    found_letters_exact[4] = "R"
    found_letters_exact[3] = "A"
    found_letters_unknown["L"] = [0]
    init_wordle_words()
    start = time.perf_counter()
    possible_words(found_letters_exact,found_letters_unknown,excluded_letters)
    end = time.perf_counter()
    print("Time to process possible words: ", end-start,"s",sep='')
if __name__ == '__main__':
    main()