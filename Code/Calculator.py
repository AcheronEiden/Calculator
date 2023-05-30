from Tokenizer import TokenizeWrapper
import math
import time
from tokenize import TokenError

#-------------------------------------Built-in Functions---------------------------------------------
def fib(n):
    """ Returns the n-th Fibonacci number using memoization"""
    if n.is_integer() and n >= 0:
        memory = {0:0, 1:1}

        def fib_mem(n):
            if n not in memory:
                memory[n] = fib_mem(n - 1) + fib_mem(n - 2)
            return memory[n]
        return fib_mem(n)
    else:
        raise EvaluationError(f'Fib(n) only accepts positive integers, not {n}!')

def fac(n):
    """ Returns the factorial of n"""
    if n.is_integer():
        return math.factorial(int(n))
    else:
        raise EvaluationError('fac(n) only accepts integers, not {n}!')

def ln(n):
    """ Returns the natural logarithm of n"""
    if n > 0:
        return math.log(n)
    else:
        raise EvaluationError('Log(n) only accepts positive numbers, not {n}!')

def sin(n):
    """ Returns the sine of n"""
    return math.sin(n)

def cos(n):
    """ Returns the cosine of n"""
    return math.cos(n)

def tan(n):
    """ Returns the tangent of n"""
    return math.tan(n)

def exp(n):
    """ Returns the exponential of n"""
    return math.exp(n)

def summation(n):
    """ Returns the sum of a list n"""
    return sum(n)

def maximum(n):
    """ Returns the maximum of a list n"""
    return max(n)

def minimum(n):
    """ Returns the minimum of a list n"""
    return min(n)

def mean(n):
    """ Returns the mean of a list n"""
    return sum(n) / len(n)
#-------------------------------------My Custom Classes-----------------------------------------------------
# Example of a syntax error is missing paranthesis
class SyntaxError(Exception):
    def __init__(self, arg):
        self.arg = arg
        super().__init__(self.arg)

# Example of an evaluation error is division by zero
class EvaluationError(Exception):
    def __init__(self, arg):
        self.arg = arg
        super().__init__(self.arg)
#-------------------------------------Calculator Code------------------------------------------------
def statement(wtok, variables):
    """ See syntax chart in the documentation"""
    # Check if the user wants to quit
    if wtok.get_current() == 'quit':
        print('See you next time!')
        exit()
    # Check if the user wants to list all variables
    elif wtok.get_current() == 'vars':
        print('Variables: ')
        for key in variables:
            print(f'    {key:<8} = {variables[key]}')
    # Check if the user wants to clear all variables
    elif wtok.get_current() == 'clear':
        variables.clear()
        print('All variables cleared!')
    # Check if the user wants to clear a specific variable
    elif wtok.get_current() == 'clearvar':
        wtok.next()
        if wtok.is_name():
            if wtok.get_current() in variables:
                variables.pop(wtok.get_current())
                print(f'{wtok.get_current()} cleared!')
            else:
                print(f'{wtok.get_current()} does not exist!')
        else:
            raise SyntaxError('Expected a variable name')
    # Check if the user wants to see the help menu
    elif wtok.get_current() == 'help':
        print('Possible commands: ')
        print('    quit - Quits the program')
        print('    vars - Lists all variables')
        print('    clear - Clears all variables')
        print('    clearvar - Clears a specific variable')
        print('    help - Shows this help menu')
    else: # if the user wants to do a calculation
        result = assignment(wtok, variables) # current token
        if wtok.is_at_end() == False:
            raise SyntaxError('Expected end of line or an operator!')
        else:
            print(result)
            
def assignment(wtok, variables):
    """ See syntax chart in the documentation"""
    result = expression(wtok, variables) # current token
    while wtok.get_current() == '=':
        wtok.next() # go to next token
        if wtok.is_name():
            variables[wtok.get_current()] = result
        else: # token is no name
            raise SyntaxError("Expected variable name after =")
        wtok.next()
    return result

def expression(wtok, variables):
    """ See syntax chart in the documentation"""
    result = term(wtok, variables) # current token
    while wtok.get_current() == '+' or wtok.get_current() == '-':
        if wtok.get_current() == '+':
            wtok.next()
            result = result + term(wtok, variables)
        else: # we have a subtration sign
            wtok.next()
            result = result - term(wtok, variables)
    return result

def term(wtok, variables):
    """ See syntax chart in the documentation"""
    result = factor(wtok, variables) # current token
    while wtok.get_current() == '*' or wtok.get_current() == '/':
        if wtok.get_current() == '*':
            wtok.next()
            result = result * factor(wtok, variables)
        else: # we have a division sign
            wtok.next()
            divisor = factor(wtok, variables)
            if divisor == 0:
                raise EvaluationError('ZeroDivisionError')
            else: # divisor is non-zero
                result = result / divisor
    return result

def factor(wtok, variables):
    """ See syntax chart in the documentation"""
    function_1 = {"sin": sin, "cos": cos, 'tan': tan ,"exp": exp, "ln": ln, "fib": fib, "fac": fac}
    function_lst = {"sum": summation, "max": maximum, "min": minimum, "mean": mean}
    function_0 = {"pi": math.pi, "e": math.e, 'time': time.ctime}

    # Check if the current token is a left paranthesis
    if wtok.get_current() == '(':
        wtok.next()
        result = assignment(wtok, variables) # current token
        if wtok.get_current() != ')':
            raise SyntaxError('Expected )')
        else: # got a right parantheses
            wtok.next()

    # Check if the current token is in function_1
    elif wtok.get_current() in function_1:
        wtok.next()
        if wtok.get_current() == '(':
            result = function_1[wtok.get_previous()](assignment(wtok, variables))  # current token
        else: # there is no left parantheses
            raise SyntaxError('Expected (')

    # Check if the current token is in function_lst
    elif wtok.get_current() in function_lst:
        wtok.next()
        result = function_lst[wtok.get_previous()](arglist(wtok, variables)) # current token

    # Check if the current token is in function_0
    elif wtok.get_current() in function_0:
        result = function_0[wtok.get_current()] # current token
        wtok.next()

    # Check if the current token is a name
    elif wtok.is_name():
        if wtok.get_current() in variables:
            result = variables[wtok.get_current()] # current token
        else: # no memory of such variable name
            raise EvaluationError(f'No defined variable by the name of {wtok.get_current()}')
        wtok.next()

    # Check if the current token is a number
    elif wtok.is_number():
        result = float(wtok.get_current()) # current token
        wtok.next()

    # Check if the current token is a minus sign
    elif wtok.get_current() == '-':
        wtok.next()
        result = -1 * factor(wtok, variables) # current token

    else: # got something other than what is allowed into the factor function (see chart)
        raise SyntaxError('Expected (, defined function, name, number or minus sign!')
    return result

def arglist(wtok, variables):
    """ See syntax chart in the documentation"""
    arguments = [] # this is the list of arguments
    if wtok.get_current() == '(':
        wtok.next()
        arguments.append(assignment(wtok, variables)) # add to list of arguments as current token
    else:
        raise SyntaxError("Expected (")
    # As long as the current token is a comma, we have more arguments
    # and need to redo the above if statement
    while wtok.get_current() == ',':
        wtok.next()
        arguments.append(assignment(wtok, variables)) # add to list of arguments as current token
    if wtok.get_current() != ')':
        raise SyntaxError("Expected closing )")
    else:
        wtok.next()
        return arguments

#-------------------------------------Main Code------------------------------------------------------
def main():
    # Alread defined variables
    variables = {"ans": 0.0}

    init_file = 'Setup.txt' # file that will be read at the start of the calculator
                            # to check for eventual bugs
    lines_from_file = ''

    # Here so that each line from the setup file is read and executed line-by-line
    try:
        with open(init_file, 'r') as file:
            lines_from_file = file.readlines()
    except FileNotFoundError:
        pass

    while True:
        # If there are lines from the setup file, execute them, remove them from the file
        # and print them. strip() removes the \n at the end of each line
        if lines_from_file:
            line = lines_from_file.pop(0).strip()
            print('init  :', line)
        else:
            line = input('\nInput : ')
        # Do nothing if the line is empty or starts with a comment character
        if line == '' or line[0] == '#':
            continue
        wtok = TokenizeWrapper(line)
        try:
            result = statement(wtok, variables)
            variables['ans'] = result

        except SyntaxError as se:
            print("*** Syntax error: ", se)
            print(f"Error occurred at '{wtok.get_current()}' just after '{wtok.get_previous()}'")

        except EvaluationError as ce:
            print("*** Evaluation error: ", ce)

        except TokenError as te:
            print('*** Syntax error: Unbalanced parentheses')

# Main loop that will run when this script is directly executed
if __name__ == "__main__":
    main()