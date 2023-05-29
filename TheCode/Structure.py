""" Responsible for how to handle the character tokens """
from tokenizer import TokenizeWrapper
import math
from ErrorHandling import *
import time

#----------------------------------------------------Built-in functions----------------------------------------------------
def fib(n):
    """ Returns the nth Fibonacci number """
    # Using memoization
    if n.is_integer() and n >= 0:
        memory = {0: 0, 1: 1}
        def fib_mem(n):
            if n not in memory:
                memory[n] = fib_mem(n - 1) + fib_mem(n - 2)
            return memory[n]
        return fib_mem(n)
    else:
        raise EvaluationError(f'fib() only accepts positive integers, not {n}')

def fac(n):
    """ Returns the factorial of n """
    if n.is_integer():
        return math.factorial(n)
    else:
        raise EvaluationError(f'fac() only accepts integers, not {n}')

def log(n):
    """ Returns the natural logarithm of n """
    if n > 0:
        return math.log(n)
    else:
        raise EvaluationError(f'log() only accepts positive numbers, not {n}')

def sin(n):
    """ Returns the sine of n """
    return math.sin(n)

def cos(n):
    """ Returns the cosine of n """
    return math.cos(n)

def tan(n):
    """ Returns the tangent of n """
    return math.tan(n)

def exp(n):
    """ Returns e to the power of n """
    return math.exp(n)

def maximum(n):
    """ Returns the maximum value of a list n """
    return max(n)

def minimum(n):
    """ Returns the minimum value of a list n """
    return min(n)

def mean(n):
    """ Returns the mean value of a list n """
    return sum(n) / len(n)
#--------------------------------------------------------------------------------------------------------------------------
def statement(wtok, variables):
    """ See syntax chart in the documentation """
    # Check if the user wants to quit
    if wtok.get_current() == 'quit':
            print('See you later!')
            exit()
    # Check if the user wants to list all variables
    elif wtok.get_current() == 'vars':
        print('Varaibles: ')
        for key in variables:
            print(f"    {key:<8} = {variables[key]}")
    # Check if the user wants to clear all variables
    elif wtok.get_current() == 'clear':
        variables.clear()
        print('All variables cleared')
    # Check if the user wants to see the help menu
    elif wtok.get_current() == 'help':
        print('Possible commands: ')
        print('    quit -- to exit\n')
        print('    vars -- to list all defined variables\n')
        print('    clear -- to clear all defined variables\n')
        print('    help -- to view the above list again')
    else: # If the user wants to do a calculation
        result = assignment(wtok, variables)
        if wtok.is_at_end() == False:
            raise SyntaxError('Expected end of line or an operator!', wtok)
        else:
            return result

def assignment(wtok, variables):
    """ See syntax chart in the documentation """
    result = expression(wtok, variables)
    while wtok.get_current() == '=':
        wtok.next()
        if wtok.is_name():
            variables[wtok.get_current()] = result
        else:
            raise SyntaxError('Expected variable name after =', wtok)
        wtok.next()
    return result

def expression(wtok, variables):
    """ See syntax chart in the documentation """
    result = term(wtok, variables)
    while wtok.get_current() in ('+', '-'):
        if wtok.get_current() == '+':
            wtok.next()
            result += term(wtok, variables)
        else:
            wtok.next()
            result -= term(wtok, variables)
        if wtok.is_at_end():
            break  # Exit the loop if there are no more terms
    return result

def term(wtok, variables):
    """ See syntax chart in the documentation """
    result = factor(wtok, variables)
    while wtok.get_current() in ('*', '/'):
        if wtok.get_current() == '*':
            wtok.next()
            result *= factor(wtok, variables)
        else:
            wtok.next()
            divisor = factor(wtok, variables)
            if divisor == 0:
                raise EvaluationError('Division by zero!')
            result /= divisor
    return result

def factor(wtok, variables):
    """ See syntax chart in the documentation """

    # Single-argument functions
    functions_1 = {
        'fib': fib,
        'fac': fac,
        'log': log,
        'sin': sin,
        'cos': cos,
        'tan': tan,
        'exp': exp,
        'maximum': maximum,
        'minimum': minimum,
    }

    # No-argument functions
    functions_0 = {
        'time': time.ctime,
        'pi': math.pi,
        'e': math.e,
    }
    # Check if the current token is a parenthesis
    if wtok.get_current() == '(':
        wtok.next()
        result = assignment(wtok, variables)
        if wtok.get_current() != ')':
            raise SyntaxError('Expected )', wtok)
        else:
            wtok.next()
    # Check if the current token is a function with one argument
    elif wtok.get_current() in functions_1:
        wtok.next()
        if wtok.get_current() == '(':
            result = functions_1[wtok.get_previous()](assignment(wtok, variables))
        else:
            raise SyntaxError('Expected (', wtok)
    # Check if the current token is a function with no arguments
    elif wtok.get_current() in functions_0:
        wtok.next()
        result = functions_0[wtok.get_previous()]()
    # Check if the current token is a number
    elif wtok.is_number():
        result = wtok.get_current()
        wtok.next()
    # Check if the current token is a variable
    elif wtok.is_name():
        if wtok.get_current() in variables:
            result = variables[wtok.get_current()]
            wtok.next()
        else:
            raise EvaluationError(f'Undefined variable: {wtok.get_current()}')
    # Check if the current token is a negative number
    elif wtok.get_current() == '-':
        wtok.next()
        result = -factor(wtok, variables)
    else:
        raise SyntaxError('Expected number, variable, or (', wtok)