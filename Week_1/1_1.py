import collections

def counter_return(words_list):
    words_list_Counter = []
    for tmp in words_list:
        Counter = collections.Counter(tmp.replace( '\n' , '' ))
        words_list_Counter.append(Counter)
    return words_list_Counter

def anagram_arr(words_list, words_list_Counter, Give_word):
    tmp = collections.Counter(Give_word)
    result = []
    for i, comp in enumerate(words_list_Counter):
        if tmp == comp:
            result.append(words_list[i].replace( '\n' , '' ))
    if result == []:
        return 'WE CAN NOT FIND THE ANAGRAM WORD !'
    else:
        return result

Give_word = str(input())
f = open('words.txt', 'r')
words_list = f.readlines()
f.close()
words_list_Counter = counter_return(words_list)

##  全てのアナグラムを配列で出力
##  全く並べ替えてないワードも出力
print(anagram_arr(words_list, words_list_Counter, Give_word))