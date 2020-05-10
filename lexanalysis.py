import lex
import sys

tokens = [
    
    'T_Identifier',
    'T_DoubleConstant',
    'DOT',
    'PLUS', 
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'PERCENTAGE', 
    'LESS',
    'GREATER',
    'EQL',
    'T_LessEqual',
    'T_GreaterEqual',
    'T_Equal',
    'T_NotEqual',
    'T_And',
    'T_Or',
    'NOT',
    'SEMICOLON',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'T_IntConstant',
    'T_StringConstant',
    'T_BoolConstant'
    
]


reserved_list = {
    'void': 'T_Void',
    'string': 'T_String',
    'while': 'T_While',
    'break': 'T_Break',
    'int': 'T_Int',
    'null': 'T_Null',
    'if': 'T_If',
    'Print': 'T_Print',
    'double': 'T_Double',
    'for': 'T_For',
    'else': 'T_Else',
    'ReadInteger': 'T_ReadInteger',
    'bool': 'T_Bool',
    'return': 'T_Return',
    'ReadLine': 'T_ReadLine'




}

operator_list = {
    'PLUS' : '+',
    'MINUS': '-',
    'MULTIPLY': '*',
    'DIVIDE': '/',
    'PERCENTAGE': '%', 
    'LESS': '<',
    'GREATER': '>',
    'EQL': '=',
    'NOT': '!',
    'SEMICOLON': ';',
    'COMMA': ',',
    'DOT': '.',
    'LPAREN': '(',
    'RPAREN': ')',
    'LBRACE': '{',
    'RBRACE': '}'
}

t_ignore  = ' \t'
t_EQL = r'='
t_PERCENTAGE = r'%'
t_LESS = r'<'
t_GREATER = r'>'
t_NOT = r'\!'
t_SEMICOLON = r';'
t_COMMA = r','
t_DOT = r'\.'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'


tokens += list(reserved_list.values())

def t_LessEqual(t):
    r'<='
    t.type = 'T_LessEqual'
    return t

def t_GreaterEqual(t):
    r'>='
    t.type = 'T_GreaterEqual'
    return t

def t_Equal(t):
    r'=='
    t.type = 'T_Equal'
    return t

def t_NotEqual(t):
    r'\!='
    t.type = 'T_NotEqual'
    return t

def t_And(t):
    r'\&\&'
    t.type = 'T_And'
    return t

def t_Or(t):
    r'\|\|'
    t.type = 'T_Or'
    return t

# r'[0-9]*\.[0-9]+(E?)\+?-?\d+'
def t_DoubleConstant(t):
    r'[0-9]+\.[0-9]*[Ee]?[+-]?\d+'
    t.type = 'T_DoubleConstant'
    return t

def t_BoolConstant(t):
    r'(true|false)'
    t.type = 'T_BoolConstant'
    return t

def t_COMMENT(t):
    r'(\/\*([^*]|[\r]|(\*+([^*\/]|[\r])))*\*+\/)|(\/\/.*)'
    line = t.value.count('\n')
    t.lexer.lineno += line
    pass
    # No return value. Token discarded


def t_IntConstant(t):
    r'(0[Xx][\da-fA-F]+|\d+)'
    t.type = 'T_IntConstant'
    return t

def t_PLUS(t):
    r'\+'
    t.type = 'PLUS'
    return t

def t_MINUS(t):
    r'\-'
    t.type = 'MINUS'
    return t

def t_DIVIDE(t):
    r'\/'
    t.type = 'DIVIDE'
    return t

def t_MULTIPLY(t):
    r'\*'
    t.type = 'MULTIPLY'
    return t



def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    size = len(t.value)
    #print("size is ", size)
    t.type = 'T_Identifier'
    if reserved_list.get(t.value) != None:
        t.type = reserved_list.get(t.value)
        return t
    if size > 31:
        t_error(t)
        return
    
    return t


def t_StringConstant(t):
    r'"[^\n|"]*(")?'
    #r'"[/d/D/w/W].*"'
    #r"^(?!\n).*$"
    #print("print in string ", t.value, " yoo bro!")
    t.type = 'T_StringConstant'
    if t.value[-1] != '\"' or (t.value[0] == '\"' and len(t.value) == 1):
        t_error(t)
        t.lexer.lineno += 1 
        return
    
    
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    #print("new line found")
    #t.lexpos = 0


# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    #print("lexpos ",token.lexpos)
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# Error handling rule
def t_error(t):
    print("************ inside error in lex *******")
    #print("*** Error line",  t.lineno, "\nIllegal character '%s'" % t.value)
    if t.type == 'T_Identifier':
        redirect_to_file("\n*** Error line " +  str(t.lineno) + ".")
        redirect_to_file("*** Identifier too long: \"" + t.value + "\"\n")
        redirect_to_file(t.value + " line " + str(t.lineno) + " cols " + str(find_column(contents, t)) + "-" + str(find_column(contents, t)+len(t.value) - 1) + " is " + t.type + "( truncated to " + t.value[:31] + ")")
    elif t.type == 'T_StringConstant':
        redirect_to_file("\n*** Error line " + str(t.lineno) + ".")
        redirect_to_file("*** Unterminated string constant: " + t.value + "\n")
    else:
        redirect_to_file("*** Error line" +  str(t.lineno) + "\nUnrecognized char '%s'" % str(t.value[0]) + "\n\n")

    t.lexer.skip(1)

lexar = lex.lex()

#redirect print to outfile
def redirect_to_file(text):
    #original = sys.stdout
    #sys.stdout = open(outFileName, 'a+')
    #print('This is your redirected text:')
    print(text)
    #sys.stdout = original



#read from file



fileName = str(sys.argv[1])
#outFileName = str(sys.argv[2])


contents = ''
f=open(fileName, 'r')
if f.mode == 'r':
    contents = f.read()
#print(contents)
lines = contents.splitlines()
#print(lines)
lexar.input(contents)
#lexar.input("1.12e-6")



def getNextToken():
    return lexar.token()


"""
while True:
    
    tok = lexar.token()
    if not tok:
        break
    

    val = ""

    type = tok.type
    if(operator_list.get(tok.type) != None):
        type = operator_list.get(tok.type)
        type = "\'" + type + "\'"
        
    if tok.type == "T_DoubleConstant":

        val = str(float(tok.value))
        if(val[-2:] == ".0"):
            val = val[:-2]
        val = " (value = " + val + ")"
        
        #redirect_to_file(tok.value + "\t\tline " + str(tok.lineno) + "cols " + str(find_column(contents, tok)) + "-" + str(find_column(contents, tok) + len(tok.value) - 1) + " is" + type + "  (value =" + str(float(tok.value)) + ")")

    elif tok.type == "T_IntConstant":
        if tok.value[:2] == '0X' or tok.value[:2] == '0x':
            val = " (value = " +  str(int(tok.value, 16)) + ")"
        else:
            val = " (value = " +  str(int(tok.value))  + ")"

    elif tok.type == "T_StringConstant" or tok.type == "T_BoolConstant":
        val = " (value = " + str(tok.value )+ ")"
        #redirect_to_file(tok.value + "\t\tline " + str(tok.lineno) + "cols " + str(find_column(contents, tok)) + "-" + str(find_column(contents, tok) +len(tok.value) - 1) + " is" + type + "  (value =" + str(tok.value )+ ")")
    
    #else: 
    redirect_to_file(tok.value + "\t\tline " + str(tok.lineno) + " cols " + str(find_column(contents, tok)) + "-" + str(find_column(contents, tok) + len(tok.value) - 1) + " is " + type + val)

"""

"""
print issues
handle string input(done)
handle error,
comment(done), 
number.out/badDouble,(calculate exact values)
hexa(calculate value for hex)
program.decaf to rest all(done)

create shell script
python 2.7
fox server
input all files
"""


"""
if tok.type == "T_DoubleConstant":
        print(tok.value, "\t\tline ", tok.lineno, "cols ", find_column(contents, tok), "-", find_column(contents, tok)+len(tok.value) - 1, " is", type, "  (value =",str(float(tok.value)),")")


    elif tok.type == "T_IntConstant" or tok.type == "T_StringConstant" or tok.type == "T_BoolConstant":
        print(tok.value, "\t\tline ", tok.lineno, "cols ", find_column(contents, tok), "-", find_column(contents, tok)+len(tok.value) - 1, " is", type, "  (value =",tok.value,")")
    
    else: 
        print(tok.value, "\t\tline ", tok.lineno, "cols ", find_column(contents, tok), "-", find_column(contents, tok)+len(tok.value) - 1, " is", type)
"""


"""
error print


if t.type == 'T_Identifier':
        print("*** Error line ", t.lineno,".")
        print("*** Identifier too long: \"", t.value, "\"\n")
        print(t.value, "line ", t.lineno, "cols ", find_column(contents, t), "-", find_column(contents, t)+len(t.value) - 1, " is", t.type, "( truncated to", t.value[:31], ")")
    elif t.type == 'T_StringConstant':
        print("*** Error line ", t.lineno,".")
        print("*** Unterminated string constant: ", t.value)
    else:
        print("*** Error line",  t.lineno, "\nUnrecognized char '%s'" % t.value[0], "\n\n")


"""
