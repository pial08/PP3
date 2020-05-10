#Declare tokens
SEMICOLON = ";"
INT = "int"
DOUBLE = "double"
BOOL = "bool"
STRING = "string"
VOID = "void"
COMMA = ","
IF = "if"
ELSE = "else"
FOR = "for"
WHILE = "while"
BREAK = "break"
RETURN = "return"
PRINT = "Print"
###################
PLUS = "+"
MINUS = "-"
MULTIPLY = "*"
DIVIDE = "/"
MOD = "%"
EQUAL = "="
NOT = "!"
EEQUAL = "=="
NOTEQUAL = "!="
LESS = "<"
GREATER = ">"
LESSEQUAL = "<="
GREATEREQUAL = ">="
AND = "&&"
OR = "||"

operatorList = [PLUS, MINUS, MULTIPLY, DIVIDE, MOD, EEQUAL, NOTEQUAL, LESS, GREATER, LESSEQUAL, GREATEREQUAL, AND, OR]
###################
READINT = "ReadInteger"
READLINE = "ReadLine"
LCURLEY = "{"
RCURLEY = "}"
LPAREN = "("
RPAREN = ")"

##use regex???
IDENT = "T_Identifier"
INTCONSTANT = "T_IntConstant"
DOUBLECONSTANT = "T_DoubleConstant"
BOOLCONSTANT = "T_BoolConstant"
STRINGCONSTANT = "T_StringConstant"
NULL = "null"

constantList = [INTCONSTANT, DOUBLECONSTANT, BOOLCONSTANT, STRINGCONSTANT]
relationalOperator = [GREATER, GREATEREQUAL, LESS, LESSEQUAL]
equalityOperator = [EEQUAL, NOTEQUAL]
logicalOperator = [AND, OR, NOT]
arithmaticOperator = [PLUS, MINUS, MULTIPLY, DIVIDE, MOD]



typeList = [INT, DOUBLE, BOOL, STRING, NULL]


precedenceList = {"!": 8, "*": 7, "/": 7, "%": 7 , "+": 6, "-": 6, "<":5, "<=": 5, ">": 5, ">=": 5, "==": 4, "!=": 4, "&&": 3, "||": 2, "=": 1}

booleanOperators = [GREATER, GREATEREQUAL, LESS, LESSEQUAL, EEQUAL, NOTEQUAL]