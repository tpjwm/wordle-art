# Example:
# Wordle 817 5/6   input word: RAYON
#⬛⬛⬛🟨🟨        CLEAR
#⬛⬛🟨⬛⬛        GHOST                 
#⬛⬛⬛⬛🟨        MILKY
#🟨⬛🟨🟨🟩        ADORN
#🟩🟩🟩🟩🟩        RAYON
#⬛⬛⬛⬛⬛        

import numpy as np
from collections import Counter, defaultdict


# Specify the path to your text file
file_path = "words.txt"

# Read words from the file into a list
with open(file_path, "r") as file:
    words_list = [line.strip() for line in file]

words = np.array(words_list)

input_word = input("Enter 5 letter word (or use wordle word by default): ")
if input_word == "":
    #TODO: find today's wordle answer for default
    input_word = "exert"

# Validate
if (len(input_word) != 5 or input_word not in words):
    print("Invalid word")
    exit()

def compare_word(guess, solution):
    matches = defaultdict(int)
    colors = ["⬛"] * len(guess)

    for index, (g, s) in enumerate(zip(guess, solution)):
        if g == s:
            colors[index] = "🟩"
            # colors[index] = "🟨"
            matches[g] += 1
        elif g in solution:
            colors[index] = "🟨"

    if matches:
        counts_in_solution = Counter(solution)

        for index, (g, s) in enumerate(zip(guess, solution)):
            if g != s and matches[g] == counts_in_solution[g]:
                colors[index] = "⬛"

    return colors

pattern_to_words = {}
for word in words:
    # print(f"{word}: {scores}")
    pattern = compare_word(word, input_word)
    pattern = tuple(pattern)
    if pattern in pattern_to_words:
        pattern_to_words[pattern].append(word)
    else:
        pattern_to_words[pattern] = [word]

# all of the words that do not have any matching letters with input_word
# print(pattern_to_words["⬛","⬛","⬛","⬛","⬛"])

# Function to parse patterns from a file and store them in a dictionary
def parse_patterns(file_path):
    patterns = {}
    current_pattern_name = None
    current_pattern = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                if current_pattern_name is None:
                    current_pattern_name = line
                else:
                    current_pattern.append(list(line))
            elif current_pattern_name is not None:
                patterns[current_pattern_name] = current_pattern
                current_pattern_name = None
                current_pattern = []

    if current_pattern_name is not None:
        patterns[current_pattern_name] = current_pattern

    return patterns


# File path to the text file containing patterns
file_path = "valid-art.txt"

# Parse patterns from the file
images_dict = parse_patterns(file_path)

# Testing the patterns
# print (images_dict)
# for row in images_dict["checkerboard"]:
#     print("".join(row))

# Create an array of most popular words
file_path = "popular_words.txt"

# Read words from the file into a list
with open(file_path, "r") as file:
    words_list = [line.strip() for line in file]

pop_words = np.array(words_list)

def get_pop_word(input_words):
    for i in range(0,len(pop_words)):
        if (pop_words[i] in input_words):
            return pop_words[i]
    return input_words[0]

#TODO: make some patterns in the art agnostic to pattern color 
#       the only exception is the full green line can't exist
#       anywhere except the end of an image

#       maybe - a flag in valid-art.txt to say if we care about colors?
#       then add a check just for full green line

# Match patterns from our pattern:wordlist dictionary to our images and display them
for img in images_dict:
    final_image = []
    for row in images_dict[img]:
        t_row = tuple(row)
        if tuple(t_row) in pattern_to_words:
            output_word = get_pop_word(pattern_to_words[t_row])
            final_image.append([t_row,output_word])
        else:
            print("\nwell poop, cant make ",{img},"\n")
            final_image.clear()
            break
    for row in final_image:
        print("".join(row[0]))
    for row in final_image:
        print("".join(row[1]))
    final_image.clear()



