from collections import Counter

dictionary = open("/Users/ada/Desktop/step/words.txt", "r")
new_dictionary = {} #key: sorted word, value: all anagrams

SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]

#store all words into an array
with open("/Users/ada/Desktop/step/small.txt", "r") as file:
    long_words = [w.strip() for w in file.readlines()]

#create new_dictionary
for word in dictionary:
    word = word.rstrip()  
    new_word = "".join(sorted(word)) 

    if new_word in new_dictionary.keys():
        new_dictionary[new_word].append(word)
    else:
        new_dictionary[new_word] = []
        new_dictionary[new_word].append(word)

#Checks if word from dictionary is a sub anagram based off of character count
def isFromAnagram(long_word, word_from_dictionary):
    long_count = Counter(long_word)
    dic_count = Counter(word_from_dictionary)
    for char, count in dic_count.items():
        if count > long_count[char]:
            return False
    return True

#checks if word has the highest score in the dictionary to append to external answer files
def highest_score(long_words, dictionary):
    for lword in long_words:
        highest_score = 0
        highest_score_ana = ""
        for word, ana in dictionary.items():
            if isFromAnagram(lword, word):
                score = sum(SCORES[ord(c)- ord("a")] for c in word)
                if score > highest_score:
                    highest_score = score
                    highest_score_ana = ana[0]
        with open("small_answer.txt", "a") as file:
            file.write(f'{highest_score_ana}\n')

highest_score(long_words, new_dictionary)