import collections

def anagram_arr(words_list, give_word):
    give_word_counter = collections.Counter(give_word)
    result = []
    for word in words_list:
        word = word.replace( '\n' , '' )
        if give_word_counter == collections.Counter(word):
            result.append(word.replace( '\n' , '' ))
    if result == []:
        return 'WE CAN NOT FIND THE ANAGRAM WORD !'
    else:
        return result

give_word = str(input())
f = open('words.txt', 'r')
words_list = f.readlines()
f.close()

##  全てのアナグラムを配列で出力
##  全く並べ替えてないワードも出力
print(anagram_arr(words_list, give_word))