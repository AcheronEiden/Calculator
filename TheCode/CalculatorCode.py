""" This is the main code for the calculator. Here is the code that will
    ask the suer for input => send the input through the TokenizeWrapper and
    start by breaking the lines into tokens that get sent to the main process.
"""
from tokenizer import TokenizeWrapper
from tokenize import TokenError
from ErrorHandling import *
from Structure import *

def main():
    # Already saved variables
    variables = {'ans': 0.0}

    setup_file = 'Setup.txt' # file that will be read at the start of the calculator to check for eventuall bugs
    lines_from_file = ''

    # Here so that the user can use the calculator without having to type in the file name every time
    try:
        with open(setup_file, 'r') as file:
            lines_from_file = file.readlines()
    except FileNotFoundError:
        pass

    while True:
        # Lets the calculator read the setup file and use the lines in the file as input
        if lines_from_file:
            line = lines_from_file.pop(0).strip() # pop the first line from the list and remove the \n with strip()
            print('\nSetup: ', line)
        else:
            line = input('\nInput >>> ').strip()

        # Do nothing if a line is empty or starts with a comment character
        if line == '' or line[0] == '#':
            continue
        wtok = TokenizeWrapper(line) # send the line to the TokenizeWrapper
        while True:
            try:
                result = statement(wtok, variables)
                variables['ans'] = result
                print(f"Answer: {result}")
            except SyntaxError as se:
                print('*** Syntax error:', se)
                print(f" Error occured at {wtok.get_current()} just after {wtok.get_previous()}")
            except EvaluationError as ee:
                print('*** Evaluation error:', ee)
            except TokenError as te:
                print('*** Token error: Unbalanced parentheses')

# Main loop that will run when this script is directly run
if __name__ == '__main__':
    main()