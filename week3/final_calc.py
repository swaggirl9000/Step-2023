#! /usr/bin/python3

def read_number(line, index):
    '''
    Input: string expression, current index
    Output: token (type of input and value), updated index
    Function: Reads in the string expression and current index and formulates the number from the expression. 
              While the index is less than the length of the expression and the current index in the expression 
              is a digit, the number is created. It works for both integers and decimals. 
    '''
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_divide(line, index):
    token = {'type': 'DIV'}
    return token, index + 1

def read_multiply(line, index):
    token = {'type': 'MULT'}
    return token, index + 1

def read_parent(line, index):
    if line[index] == "(":
        token = {'type': 'OPEN'}
    elif line[index] == ")":
        token = {'type': 'CLOSE'}
    return token, index+1

def read_int(line, index):
    token = {'type': 'INT'}
    return token, index + 3

def read_abs(line, index):
    token = {'type': 'ABS'}
    return token, index + 3

def read_round(line, index):
    token = {'type': 'ROUND'}
    return token, index + 5

def tokenize(line):
    '''
    Input:  line
    Output: list of tokens 
    Function: Creates a list of the tokens inside of the line string expression. 
              While index is valid, it loops through the string and calls the read_number 
              function, read_plus function, read_minus function to collect the correct tokens. 
    '''
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == "(":
            (token, index) = read_parent(line, index)
        elif line[index] == ")":  
            (token, index) = read_parent(line, index) 
        elif line[index:index+3] == "int":
            (token, index) = read_int(line, index) 
        elif line[index:index+3] == "abs":
            (token, index) = read_abs(line, index) 
        elif line[index:index+5] == "round":
            (token, index) = read_round(line, index) 
        else:
            print(tokens)
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def evaluate_md(tokens):
    '''
    Input: list of tokens
    Output: evaluated list of tokens 
    Function: The function firstly evaluates any division and multiplication. 
    '''
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'MULT':
                tokens[index-2]['number'] *= tokens[index]['number']
                del tokens[index-1:index+1]
                index -=1
            elif tokens[index - 1]['type'] == 'DIV':
                if tokens[index]['number'] == "0":
                    print("Error: Division by Zero")
                    exit(1)
                tokens[index-2]['number'] /= tokens[index]['number']
                del tokens[index-1:index+1]
                index -=1
        index += 1
    return tokens

def preform_calc(tokens):
    '''
    Input: list of tokens
    Output: Evaluated answer
    Function: This function performs addition and subtraction, as well as any modifications the answer 
              such as int(), round(), abs().

    '''
    answer = 0
    index =  1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            elif tokens[index-1]['type'] == "ABS":
                answer += abs(tokens[index]['number'])
            elif tokens[index-1]['type'] == "INT":
                answer += int(tokens[index]['number'])
            elif tokens[index-1]['type'] == "ROUND":
                answer += round(tokens[index]['number'])
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer

def evaluate(tokens, start_index=0):
    '''
    Input: list of tokens
    Output: Evaluated answer
    Function: Goes through tokens list and evaluates the answer following the rules of PEMDAS.
    '''
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = start_index + 1
    par_counter = 0
    par_index = 0

    while index < len(tokens):
        if tokens[index]['type'] == "OPEN":
            if par_counter == 0:
                par_index = index
            par_counter += 1
        elif tokens[index]['type'] == "CLOSE":
            par_counter -=1
            if par_counter == 0:
                res = evaluate(tokens[par_index+1:index])
                tokens[par_index:index+1] = [{'type': 'NUMBER', 'number': res}]
                index = par_index + 1
        index += 1
    tokens = evaluate_md(tokens)
    answer = preform_calc(tokens)
    return answer

def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("1.02+1.2")
    test("8.91/9.78+87*4/21")
    test("2/1+9.7654231-1.23+8/7*1.1")
    test("3+1/4-2")
    # test("3/0")
    test("2/2/7*7+8+2/3")
    test("(1+2)*2")
    test("(2*5)")
    test("(2*5)+2")
    test("(2+(1*2))+2")
    test("((3*8)/(2+1)+2)")
    test("(((3*8)+23)/(2+1)+2)")
    test("((1.3*8)/(2.002+1.98)+(1.97*2.8))+1.9/(8.8)")
    test("abs(-2+3)+round(-1.2)")
    test("round(1.55+int(2.3+3.8)+(2*8))")
    test("abs(round(-2/3))+round(1.55+int(2.3+3.8))")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)