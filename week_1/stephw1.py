dictionary = open("/Users/ada/Desktop/step/words.txt", "r")
new_dictionary = {}

for word in dictionary:
    word = word.rstrip()  
    new_word = "".join(sorted(word)) 

    if new_word in new_dictionary.keys():
        new_dictionary[new_word].append(word)
    else:
        new_dictionary[new_word] = []
        new_dictionary[new_word].append(word)

def solution(random_word, dictionary):
    sorted_random_word = "".join(sorted(random_word))
    if sorted_random_word not in dictionary: 
        return "Not found"
    anagram = dictionary[sorted_random_word]
    return anagram

test_cases = ["cat", "a", "traces", "horse", "", "kelp"]
for word in test_cases:
    print(solution(word, new_dictionary))

import collections
print(collections.Counter("posoeitesimeegvl"))

