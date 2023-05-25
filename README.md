# Calculator

The calculator will be built upon the parsing technique called *recursive descent*. The calculator will use tokenization to operate, meaning that it will break up a sequence of strings into units (for example characters) called tokens that leads to sepcific functions/operations/methods. Errors will be handled using *exceptions*.
-----------------------------------------------------------------------------------------------------------
The calculator will follow the following principle:
* An *expression* is a sequence of one or more *terms* seperated by + or -
* A *term* is a sequence of one o more *factors* seperated by * or /
* A *factor* is a *number*, a *variable* or an *expression* enclosed by paranthesis.

A general *tokenizer* specificies the rules for how the tokens work together, but I don't know much about how tokenizer's work so will use a provided interface class called *TokenizeWrapper* (given in the course 1TD722 at Uppsala University). The class is a simple interface class for the standard module *Tokenize*. Example of the tokenizer (the tokenizer ignores blank spaces!):

![image](https://github.com/AcheronEiden/Calculator/assets/76567363/ff7d08c8-907d-4be7-9f1f-f45b3b48114b)

-----------------------------------------------------------------------------------------------------------
**TokenizeWrapper**
![image](https://github.com/AcheronEiden/Calculator/assets/76567363/8378e5fb-725f-483d-88ac-33f320733dce)
-----------------------------------------------------------------------------------------------------------
