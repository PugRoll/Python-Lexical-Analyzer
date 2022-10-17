charDict = {
    "LETTER" : 0,
    "DIGIT" : 1,
    "UNKNOWN": 99

}
#Token Classes
tokenDict = {
    "INT LIT" : 10,
    "IDENT" : 11,
    "ASSIGN_OP" : 20,
    "ADD_OP" : 21,
    "SUB_OP" : 22,
    "MULT_OP": 23,
    "DIV_OP": 24,
    "LEFT_PAREN": 25,
    "RIGHT_PAREN": 26,
    "EOF" : -1
}


#Global Variables
_char_class = 0
lexeme = []
nextChar = '\\n'
lexLen = 0
_next_token = -1
token = 0
END_OF_FILE = ''
in_fp = open("input.txt", "r")
out_fp = open("output.txt", "w")


def add_char(): 
    global lexLen
    global lexeme
    if lexLen <= 98 :
        lexeme.append(nextChar)
    else :
        print("Error - lexeme is too long \m\n")
#End of addChar declaration

def lookup(ch):
    global _next_token
    match ch:
        case '(':
            add_char()
            _next_token = tokenDict["LEFT_PAREN"]
        case ')':
            add_char()
            _next_token = tokenDict["RIGHT_PAREN"]
        case '+':
            add_char()
            _next_token = tokenDict["ADD_OP"]
        case '-':
            add_char()
            _next_token = tokenDict["SUB_OP"]
        case '*':
            add_char()
            _next_token = tokenDict["MULT_OP"]
        case '/':
            add_char()
            _next_token = tokenDict["DIV_OP"]
        case _:
            add_char()
            _next_token = tokenDict["EOF"] 

    return _next_token
#End of lookup declaration

 

def get_char():
    global _char_class 
    global nextChar
    #Read the next character from file     
    nextChar = in_fp.read(1)
    
    #Assign a character class to the character
    if  nextChar != END_OF_FILE :
        if nextChar.isalpha():
            _char_class = charDict["LETTER"]
        elif nextChar.isdigit():
            _char_class = charDict["DIGIT"]
        else:
            _char_class = charDict["UNKNOWN"]
    else:
        _char_class = tokenDict["EOF"]
#End of get_char() declaration

def get_non_blank():
    global nextChar
    #Continually look for the next character when encountering white space
    while nextChar.isspace(): 
        get_char()
#End of getNonBlank() declaration


def lex():
    global _lex_len
    global _char_class
    global charDict
    global _next_token
    _lex_len = 0
    get_non_blank()

    #Match case statement, unfortunately integer literals were needed here to make it work
    match _char_class:
        case 0:
            add_char()
            get_char()
            while _char_class == charDict["LETTER"] or _char_class == charDict["DIGIT"] :
                add_char()
                get_char()
            _next_token = tokenDict["IDENT"]
        case 1:
            add_char()
            get_char()
            while _char_class == charDict["DIGIT"]:
                add_char()
                get_char()
            _next_token = tokenDict["INT LIT"]
        case 99:
            lookup(nextChar)
            get_char()
        case -1:
            _next_token = tokenDict["EOF"] 
            lexeme.append('E')
            lexeme.append('O')
            lexeme.append('F')
    #Print out results
    print("Next token is: %d, Next lexeme is %s\n" 
    %(_next_token,
    ( ''.join(lexeme)))) #Some seriously ugly formatting to print the list nicely

    #Write to output file
    out_fp.write("Next token is: %d, Next lexeme is %s\n" % (_next_token,( ''.join(lexeme))))

    #Clear the list for the next lexeme
    lexeme.clear()
    return _next_token
#End of lex function


with in_fp and out_fp:
    get_char()
    lex()
    while _next_token != tokenDict["EOF"]:
        lex()
    in_fp.close()
    out_fp.close()