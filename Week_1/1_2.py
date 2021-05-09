import collections

def read_file(filename):
    f = open(filename, 'r')
    file_data = f.readlines()
    f.close
    return file_data


def counter_return(words_list):
    words_list_counter = []
    for tmp in words_list:
        counter = collections.Counter(tmp.replace( '\n' , '' ))
        words_list_counter.append(counter)
    return words_list_counter


def words_list_sort(words_list):
    return sorted(words_list, key=score_calculation, reverse=True)


def anagram_return(words_list, words_list_counter, give_word):
    give_word_counter = collections.Counter(give_word)
    result = []

    #  スコアが高い順にソートされているので, 初めに見つけたアナグラムが一番スコアが高い
    for i, words_list_counter_key in enumerate(words_list_counter):
        flag = 1
        for key in words_list_counter_key:
            if int(give_word_counter[key]) < int(words_list_counter_key[key]):
                flag = 0
                break
        if flag:
            word = words_list[i].replace('\n', '' )
            return word
    return 'WE CAN NOT FIND THE ANAGRAM WORD !'


def score_calculation(word):
    score = 0
    for key in word:
        if key in ['a', 'e', 'h', 'i', 'n', 'o', 'r', 's', 't']:
            score += 1
        if key in ['c', 'd', 'l', 'm', 'u']:
            score += 2
        if key in ['b', 'f', 'g', 'p', 'v', 'w', 'y']:
            score += 3
        if key in ['j', 'k', 'q', 'x', 'z']:
            score += 4
    return score


def output_file(words_list, words_list_counter, input_filename, output_filename):
    input_list = read_file(input_filename)
    f = open(output_filename, 'w', encoding='UTF-8')
    result = []
    for input_list_word in input_list:
        input_list_word = input_list_word.replace('\n', '' )
        anagram = anagram_return(words_list, words_list_counter, input_list_word)
        result.append(anagram + '\n')
    f.writelines(result)
    f.close()
    return 


#  Input Dictionary File, Score's Order
words_list = words_list_sort(read_file('words.txt'))
words_list_counter = counter_return(words_list)


#  Output
output_file(words_list, words_list_counter, 'small.txt', 'small_answer.txt')
output_file(words_list, words_list_counter, 'medium.txt', 'medium_answer.txt')
output_file(words_list, words_list_counter, 'large.txt', 'large_answer.txt')
