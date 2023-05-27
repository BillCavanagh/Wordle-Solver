from words import *
import turtle
import random
import wordle_gui as GUI
# solution 
SOLUTION = ""
SOLUTION_DICT = dict() # solution_dict[letter_in_solution] = "[Indexes]"

def init():
    global SOLUTION
    global SOLUTION_DICT
    # draw wordle words
    GUI.draw_wordle_grid()
    # create file of possible words given the length input
    init_wordle_words()
    # pick a random word from said file to be the solution
    with open(INPUT_FILE) as file:
        SOLUTION = random.choice(file.read().splitlines())
    # init SOLUTION_DICT for processing guesses
    for index,chr in enumerate(SOLUTION):
        if chr in SOLUTION_DICT:
            SOLUTION_DICT[chr].append(index)
        else:
            SOLUTION_DICT[chr] = [index]
    print(SOLUTION)
def make_guess(guess):
    if len(guess) != len(SOLUTION):
        raise ValueError("Invalid Guess")
    guess_dict = {x : "" for x in range(len(guess))} # guess_dict[index] = "G" = Green/Correct or "Y" = "Yellow/In word" or "" = "Gray/Not in word"
    # find which letters are already in the right spot in the solution
    for index,chr in enumerate(guess):
        if chr == SOLUTION[index]:
            guess_dict[index] = "G"
    # find which letters are in the solution and not already found to be in the right spot
    for index,chr in enumerate(guess):
        if chr in SOLUTION_DICT:
            for _ in SOLUTION_DICT[chr]:
                if guess_dict[index] == "":
                    guess_dict[index] = "Y"
    return guess_dict

def check_guess(guess,guess_dict):
    for guess in guess_dict:
        if guess_dict[guess] == "G":
            continue
        else: 
            return False
    return True
def round():
    found_letters_exact = dict()
    found_letters_unknown = dict()
    excluded_letters = set()
    for word_num in range(1,7):
        letter_count = possible_words(found_letters_exact,found_letters_unknown,excluded_letters)
        input("Next: ")
        letter_weights = get_letter_weights(letter_count)
        guess = get_best_guess(letter_weights)
        guess = guess.strip()
        print(guess)
        guess_dict = make_guess(guess)
        GUI.write_word(guess,word_num,guess_dict)
        duplicates_processed = set()
        for index in guess_dict:
            letter = guess[index]
            if guess_dict[index] == "G":
                found_letters_exact[index] = letter 
                if letter in found_letters_unknown: # if the guessed letter is one of the unknown letters
                    found_letters_unknown[letter][1] -= 1 # remove one from the unknown letters amount
                    if found_letters_unknown[letter][1] == 0: # if none are left then remove that letter from unknowns
                        found_letters_unknown.pop(letter)
                    else:
                        found_letters_unknown[letter][1].append(index)
            elif guess_dict[index] == "Y":
                if not letter in found_letters_unknown: # if the letter isnt already a key initialize it
                    found_letters_unknown[letter] = [[index],1]
                else: # if not add its position to the not possible positions for a letter
                    found_letters_unknown[letter][0].append(index)
                    if letter in duplicates_processed:
                        continue
                    letter_copies = list(re.finditer(letter,guess))
                    print(letter_copies)
                    total_unknowns = len(letter_copies)
                    if len(letter_copies) > 1: # if there are two instances of an unknown letter twice in the guess, add 1 to its unknown counter
                        for match in letter_copies:
                            if guess_dict[match.start()] == "G":
                                total_unknowns -= 1
                        found_letters_unknown[letter][1] += total_unknowns
                        duplicates_processed.add(letter)
            elif guess_dict[index] == "":
                excluded_letters.add(letter)
        # check if guess was completely correct
        if (check_guess(guess,guess_dict)):
            return word_num
            
        
def main():
    random.seed(5)
    init()
    init_wordle_words()
    print(round())
    input()
if __name__ == '__main__':
    main()


    


        
        
        
