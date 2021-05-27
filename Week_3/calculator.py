def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def readMultiplication(line, index):
    token = {'type': 'MULTIPLICATION'}
    return token, index + 1


def readDivision(line, index):
    token = {'type': 'DIVISION'}
    return token, index + 1


def readOpenParentheses(line, index):
    token = {'type': 'OPEN_PARENTHESES'}
    return token, index + 1


def readCloseParentheses(line, index):
    token = {'type': 'CLOSE_PARENTHESES'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMultiplication(line, index)
        elif line[index] == '/':
            (token, index) = readDivision(line, index)
        elif line[index] == '(':
            (token, index) = readOpenParentheses(line, index)
        elif line[index] == ')':
            (token, index) = readCloseParentheses(line, index)
        else:
            print(line[index])
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    if tokens[0]['type'] == 'NUMBER':
        tokens.insert(0, {'type': 'PLUS'})  # Insert a dummy '+' token
    return tokens


def evaluate(tokens):
    # Calculate inside parentheses
    tokens_remove_parentheses = remove_parentheses(tokens)
    # Calculate only multiplication and division
    tokens_evaluate_MultDiv = evaluate_MultiplicationDivision(
        tokens_remove_parentheses)
    # Calculate only Addition and Subtraction
    return evaluate_PlusMinus(tokens_evaluate_MultDiv)


# Remove parentheses recursively
def remove_parentheses(tokens):
    result_tokens = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'CLOSE_PARENTHESES':
            print('Syntax Error Due to Parentheses')
            exit(1)
        elif tokens[index]['type'] != 'OPEN_PARENTHESES':
            result_tokens.append(tokens[index])
            index += 1
        else:
            #  tokens[index]['type'] == 'OPEN_PARENTHESES'
            index += 1
            inside_parentheses_tokens = []
            inside_parentheses_count = 0  # Supports duplicate parentheses
            while index < len(tokens) and (
                    tokens[index]['type'] != 'CLOSE_PARENTHESES' or inside_parentheses_count != 0):
                inside_parentheses_tokens.append(tokens[index])
                if tokens[index]['type'] == 'OPEN_PARENTHESES':
                    inside_parentheses_count += 1
                elif tokens[index]['type'] == 'CLOSE_PARENTHESES':
                    inside_parentheses_count -= 1
                index += 1
            if index >= len(
                    tokens) or tokens[index]['type'] != 'CLOSE_PARENTHESES':
                print('Syntax Error Due to Parentheses')
                exit(1)
            else:
                # Calculate inside parentheses recursively
                tokenize_tokens = tokenize(
                    str(evaluate(inside_parentheses_tokens)))
                if result_tokens == []:
                    result_tokens.append(tokenize_tokens[0])
                    result_tokens.append(tokenize_tokens[1])
                else:
                    previous = result_tokens.pop()
                    if judge_PlusMinus(previous['type']):
                        result_tokens.append(
                            multiplication_operator(
                                tokenize_tokens[0]['type'],
                                previous['type']))
                        result_tokens.append(tokenize_tokens[1])
                    else:
                        result_tokens.append(previous)
                        result_tokens.append(tokenize_tokens[0])
                        result_tokens.append(tokenize_tokens[1])
                index += 1
    return result_tokens


# Return a formula that does not include multiplication and division
def evaluate_MultiplicationDivision(tokens):
    answer_tokens = []
    index = 1 
    # Insert a dummy '+' token
    if judge_Number(tokens[0]['type']):
        tokens.insert(0, {'type': 'PLUS'})

    #  No '/' or '*' at the beginning of a formula
    if judge_MultiplicationDivision(tokens[0]['type']):
        print('Invalid syntax')
        exit(1)
    elif len(tokens) <= 2:
        return tokens

    # Check tokens focusing on NUMBER
    while index < len(tokens):
        if judge_Number(tokens[index]['type']):
            if judge_PlusMinus(tokens[index - 1]['type']):
                if (index == 1) or judge_Number(tokens[index - 2]['type']):
                    #  ex. -2, +2
                    answer_tokens.append(tokens[index - 1])
                    answer_tokens.append(tokens[index])
                elif (index >= 4) and judge_MultiplicationDivision(tokens[index - 2]['type']):
                    if judge_Number(tokens[index - 3]['type']):
                        #  ex. -2/-2, -2/+2
                        pop_num = answer_tokens.pop()
                        pop_operator = answer_tokens.pop()
                        answer_tokens.append(multiplication_operator(
                            tokens[index - 1]['type'], pop_operator['type']))
                        answer_tokens.append(calculate_MultiplicationDivision(
                            pop_num['number'], tokens[index]['number'], tokens[index - 2]['type']))
                    else:
                        print('Invalid syntax')
                        exit(1)
                else:
                    print('Invalid syntax')
                    exit(1)
            elif index >= 2 and judge_MultiplicationDivision(tokens[index - 1]['type']):
                if judge_Number(tokens[index - 2]['type']):
                    # ex. -2/2, +2/2
                    pop_num = answer_tokens.pop()
                    answer_tokens.append(calculate_MultiplicationDivision(
                        pop_num['number'], tokens[index]['number'], tokens[index - 1]['type']))
                else:
                    print('Invalid syntax')
                    exit(1)
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer_tokens


# Calculate the formula that include only PLUS and MINUS
def evaluate_PlusMinus(tokens):
    answer = 0
    if tokens[0]['type'] == 'NUMBER':
        tokens.insert(0, {'type': 'PLUS'})
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


# Operator Multiplication and Division
def multiplication_operator(operator1, operator2):
    if operator1 != 'PLUS' and operator1 != 'MINUS':
        print('Invalid syntax')
        exit(1)
    if operator2 != 'PLUS' and operator2 != 'MINUS':
        print('Invalid syntax')
        exit(1)
    if operator1 == operator2:
        return {'type': 'PLUS'}
    else:
        return {'type': 'MINUS'}


# Perform multiplication or division
# Positive / negative is calculated elsewhere
def calculate_MultiplicationDivision(num1, num2, operator_type):
    if operator_type == 'MULTIPLICATION':
        return {'type': 'NUMBER', 'number': num1 * num2}
    elif operator_type == 'DIVISION':
        if num2 == 0:
            print('Division by zero')
            exit(1)
        else:
            return {'type': 'NUMBER', 'number': num1 / num2}
    else:
        print('Invalid syntax')
        exit(1)


def judge_PlusMinus(operator):
    if operator == 'PLUS' or operator == 'MINUS':
        return True
    else:
        return False


def judge_MultiplicationDivision(operator):
    if operator == 'MULTIPLICATION' or operator == 'DIVISION':
        return True
    else:
        return False


def judge_Number(text):
    if text == 'NUMBER':
        return True
    else:
        return False


def test(line):
    tokens = tokenize(line)
    actualAnswer = evaluate(tokens)
    expectedAnswer = eval(line)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print("FAIL! (%s should be %f but was %f)" %
              (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
    print("==== Test started! ====")
# Test case + - * /
    test("0")
    test("10")
    test("10.020")
    test("+10")
    test("+10.32")
    test("-3")
    test("-5.02")
    test("1+2")
    test("1+2.03")
    test("2.03+1")
    test("2.03607+1.20938")
    test("1-2")
    test("1-2.03")
    test("2.03-1")
    test("2.03607-1.20938")
    test("+5-6.80")
    test("-6.80+5")
    test("-5-6.80")
    test("+5+6.80")
    test("5*6")
    test("5*6.098")
    test("5.0987*6.098")
    test("2.03*4.09")
    test("2/4")
    test("2/4.099")
    test("4.099/2")
    test("2.098/4.099")
    test("10.098/-10.0987")
    test("10.098/+10.0987")
    test("10.098*-10.0987")
    test("10.098*+10.0987")
    test("-10.098/10.0987")
    test("+10.098/10.0987")
    test("-10.098*10.0987")
    test("+10.098*10.0987")
    test("-10.098/-10.0987")
    test("+10.098/+10.0987")
    test("-10.098/+10.0987")
    test("+10.098/-10.0987")
    test("-10.098*-10.0987")
    test("+10.098*+10.0987")
    test("-10.098*+10.0987")
    test("+10.098*-10.0987")
    test("+10*-10")
    test("+10/+10")
    test("10+10+10")
    test("+10+10+10")
    test("+10.0987+10.001+10.001")
    test("+10+10+10+10")
    test("-10-10-10-10")
    test("+10-10+10-10")
    test("-10.00*-2.02*-3.02")
    test("10.00*-2.02/3.02")
    test("10.00*2.02/3.02")
    test("+10.00/+2.02/+3.02")
    test("+10.0+2.03*3.02-110*10-10")
    test("-2.03/3.02+10.0-110")
    test("3.0+4*2-1/5")
    
# Test case About Parentheses
    test("(2)")
    test("(-3.02)")
    test("(5.00+2.03)")
    test("((5.02+2))")
    test("5+(-2)")
    test("5+(+2)")
    test("5+(2)")
    test("(5)+2")
    test("(5)-2")
    test("(-5)-2")
    test("(-5)+(-2)")
    test("-(-5)+(-2)")
    test("-(+5)+(-2)")
    test("(3+5)*(-8-9)")
    test("-(3+5)*+(-8-9)")
    test("+(3+5)/-(-8-9)")
    test("-3*(1-11.09)*-5")
    test("-3*(11-11.00)*-5")
    test("(-3*(11-11.00)*-5)")
    test("((2+3)/(4+7))/5+7")
    test("((2-3)*(4+7))/(5-7)")
    test("(((2-3)+(4+7))/(5-7))")
    test("(((2-3)+(4+7))/(5-7))+(((2-3)*3)+(2*(4+5)))*6")
    print("==== Test finished! ====\n")


runTest()
while True:
    print('> ', end="")
    line = input()
    if(line != ""):
        tokens = tokenize(line)
        answer = evaluate(tokens)
        print("answer = %f\n" % answer)
