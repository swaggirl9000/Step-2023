#This is an updated version of my previous assignment where the time complexity is (i think) improved
#26 * N * M where N in the number of words and M is the size of the dictionary
dictionary = open("/Users/ada/Desktop/step/week_1/words.txt", "r")
new_dictionary = {} #key: sorted word, value: all anagrams
long_words = {} #key = long word value = occurance vector

SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]

#calculates the score of the anagram
def get_score(word):
    score = sum(SCORES[ord(c)- ord("a")] for c in word)
    return score

#calculates the occurance array of each character in a word
def get_occurance(word):
    occur = [0] * 26
    for ch in word:
        pos = ord(ch)- ord("a")
        occur[pos] += 1
    return occur

#store all words into a dictionary
with open("/Users/ada/Desktop/step/week_1/medium.txt", "r") as file:
    for w in file.readlines():
        w = w.strip()
        long_words[w] = get_occurance(w)
 
#new dictionary where key: sorted word
# values are occurance vector, score, list of all anagrams
for word in dictionary:
    word = word.rstrip()  
    new_word = "".join(sorted(word)) 

    if new_word in new_dictionary.keys():
        new_dictionary[new_word][2].append(word)
    else:
        new_dictionary[new_word] = [[],[],[]]
        new_dictionary[new_word][0] = get_occurance(word)
        new_dictionary[new_word][1] = get_score(new_word)
        new_dictionary[new_word][2].append(word)

#goes through occurance arrays and compares    
def isFromAnagram(locc, ana):
    for i in range(26):
        if locc[i] < ana[i]:
            return False
    return True

def highest_score(long_words, dictionary):
    for lword, locc in long_words.items():
        highest_score = 0
        highest_score_ana = ""
        for word, ana in new_dictionary.items():
            if isFromAnagram(locc, ana[0]):
                if ana[1] > highest_score:
                    highest_score = ana[1]
                    highest_score_ana = ana[2][0]
        with open("med_answer_update.txt", "a") as file:
            file.write(f'{highest_score_ana}\n')

highest_score(long_words, new_dictionary)