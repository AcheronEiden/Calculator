""" Responsible for handling errors """

# Example of syntax error is missing a parenthesis
class SyntaxError(Exception):
    """ Raised when a syntax error occurs """
    def __init__(self, message):
        self.message = message
        super().__init(self.message)

# Example of evaluation error is division with zero
class EvaluationError(Exception):
    """ Raised when an evaluation error occurs """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)