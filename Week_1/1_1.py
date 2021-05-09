import collections

def counter_return(words_list):
    words_list_counter = []
    for tmp in words_list:
        counter = collections.Counter(tmp.replace( '\n' , '' ))
        words_list_counter.append(counter)
    return words_list_counter

def anagram_arr(words_list, words_list_counter, give_word):
    tmp = collections.Counter(give_word)
    result = []
    for i, comp in enumerate(words_list_counter):
        if tmp == comp:
            result.append(words_list[i].replace( '\n' , '' ))
    if result == []:
        return 'WE CAN NOT FIND THE ANAGRAM WORD !'
    else:
        return result

give_word = str(input())
f = open('words.txt', 'r')
words_list = f.readlines()
f.close()
words_list_counter = counter_return(words_list)

##  全てのアナグラムを配列で出力
##  全く並べ替えてないワードも出力
print(anagram_arr(words_list, words_list_counter, give_word))