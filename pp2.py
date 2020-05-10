import sys
import const
import lexanalysis
from treelib.treelib import Node, Tree
  

boolPrint = True

tree = Tree()
tree.create_node("   $Program:", "Program")  # root node
prevOperator = ""
parentNode = "Program"
prefix = ""


tok = lexanalysis.getNextToken()

def resetPrefix():
    global prefix
    prefix = ""
    return True
def setPrefix(st):
    global prefix
    prefix = st
    return True


def findCol(tok):
    return lexanalysis.find_column(lexanalysis.contents, tok)

def createParent(st):
    return st + str(tok.lineno) + "_" + str(findCol(tok))

def setParent(st):
    global parentNode
    parentNode = st
    return True

def printBool(st):
    #print(st)
    return True

def printError(st):
    global boolPrint
    if boolPrint:
        print(st)

assgnHead = ""
exprTree = Tree()
def createExprTree():
    global exprTree
    global exprTreeHead
    global lastTreeHead
    global prevOperator
    global currentTreeHead
    global assgnHead
    currentTreeHead = ""
    prevOperator = ""
    exprTreeHead = ""
    lastTreeHead = ""
    assgnHead = ""
    exprTree = Tree()
    return True


printBool(str(tok))

def updateTok():
    #printBool("printing from updatetok OXOXOXOXOXOXXOOXOXOXO")
    global tok
    tok = lexanalysis.getNextToken()
    printBool(str(tok))
    if tok != None:
        return True
    else:
        return False

def reportError(tok):
    global boolPrint
    if boolPrint:
        print()
        printError("*** Error line " + str(tok.lineno) + ".")
        printError(lexanalysis.lines[tok.lineno - 1])
        errorLine = ""
        length = findCol(tok) -1
        while length:
            errorLine += " "
            length -= 1
        for i in range(len(tok.value)):
            errorLine += "^"
        printError(errorLine)
        #print("column", findCol(tok), "token len", len(tok.value))
        printError("*** syntax error")
        boolPrint = False
        print()
        print()
    #pass


def Program():
    if tok == None:
        print("Empty program is syntactically incorrect.")
        return False
    printBool("inside program")
    return Decl() and  ProgramP()


def ProgramP():
    #updateTok()
    if tok != None:
        #updateTok()
        #if tok != None:
        return Program()
    else: 
        printBool("ending")
        return True



def Decl():
    global parentNode
    printBool("inside decl")
    printBool(tok.value)
    if tok.value in const.typeList or tok.value == const.VOID:
        printBool("method type  found")
        #this line added for AST
        methodReturnType = tok.value
        updateTok()
        prevParent = parentNode
        if tok.type == const.IDENT:
            identifier = tok.value
            updateTok()
            printBool("tok.value" + tok.value)
            if tok.value ==  const.LPAREN:
                
                tree.create_node("  " + str(tok.lineno) + "$FnDecl:", createParent("FnDecl"), parent = parentNode)
                parentNode =createParent("FnDecl")
                tree.create_node("   " + "$(return type) Type: " + methodReturnType, createParent("Type"), parent=parentNode)
                tree.create_node("  " + str(tok.lineno) + "$Identifier: " + identifier, createParent("Identifier"), parent=parentNode)
                return FunctionDecl() and setParent(prevParent)
            else:
                printBool("going to vardecl")
                tree.create_node("  " + str(tok.lineno) + "$VarDecl:", createParent("VarDecl"), parent = parentNode)
                parentNode =createParent("VarDecl")
                tree.create_node("   " + "$Type: " + methodReturnType, createParent("Type"), parent=parentNode)
                tree.create_node("  " + str(tok.lineno) + "$Identifier: " + identifier, createParent("Identifier"), parent=parentNode)
                return VariableDecl() and updateTok() and setParent(prevParent)
        else:
            reportError(tok)
            return False
    else:
        reportError(tok)

        printBool("error found")
        return False
    

def VariableDecl():
    printBool("inside var decl")
    if tok.value == const.SEMICOLON:
        printBool("semicolon found after var")
        return True
    else:
        reportError(tok)
        return False


def FunctionDecl():
    printBool("inside funcdecl")
    updateTok()
    forms  = Formals()
    
    updateTok()
    return forms  and StmtBlock()


def Formals():
    global parentNode
    printBool("inside formals")
    if tok.value == const.RPAREN:
        return True

    while True:
        printBool("inside formal while loop....")
        if tok.value in const.typeList:
            printBool("typelist found")
            prevParent = parentNode
            varType = tok.value
            updateTok()
            if tok.type == const.IDENT:
                identifier = tok.value
                updateTok()
                if tok.value == const.COMMA and (updateTok() and tok.value != const.RPAREN):

                    tree.create_node("  " + str(tok.lineno) + "$(formals) VarDecl:", createParent("VarDecl"), parent = parentNode)
                    parentNode =createParent("VarDecl")
                    tree.create_node("   " + "$Type: " + varType, createParent("Type"), parent=parentNode)
                    tree.create_node("  " + str(tok.lineno) + "$Identifier: " + identifier, createParent("Identifier"), parent=parentNode)
                    setParent(prevParent)
                    continue
                
                elif tok.value == const.RPAREN:
                    printBool("returning from formals")
                    tree.create_node("  " + str(tok.lineno) + "$(formals) VarDecl:", createParent("VarDecl"), parent = parentNode)
                    parentNode =createParent("VarDecl")
                    tree.create_node("   " + "$Type: " + varType, createParent("Type"), parent=parentNode)
                    tree.create_node("  " + str(tok.lineno) + "$Identifier: " + identifier, createParent("Identifier"), parent=parentNode)
                    return True  and setParent(prevParent)
            else:
                reportError(tok)
                return False
    
def StmtBlock():
    global parentNode
    prevParent = parentNode
    printBool("inside stmtBlock")
    
    tree.create_node("   " + "$(body) StmtBlock: ", createParent("StmtBlock"), parent=parentNode)
    parentNode = createParent("StmtBlock")
    if tok.value == const.LCURLEY:
        updateTok()
        if tok.value == const.RCURLEY:
            return True and setParent(prevParent)
        else:
            stmtBlckVar = VariableDeclRec() and printBool("token inside stmtBlock... " + tok.value) and  tok.value == const.RCURLEY
            updateTok()
            return stmtBlckVar  and setParent(prevParent)
                

        """
        elif tok.value in const.typeList:
            return VariableDeclRec()
        else:
            Stmt()
        """
def VariableDeclRec():
    printBool("inside varDecRec")
    #if tok.value == const.RCURLEY:
    #        return True
    global parentNode
    prevParent = parentNode
    varType = tok.value
    if tok.value in const.typeList and (updateTok() and tok.type == const.IDENT):
        
        identifier = tok.value
        tree.create_node("  " + str(tok.lineno) + "$VarDecl:", createParent("VarDecl"), parent = parentNode)
        parentNode =createParent("VarDecl")
        tree.create_node("   " + "$Type: " + varType, createParent("Type"), parent=parentNode)
        tree.create_node("  " + str(tok.lineno) + "$Identifier: " + identifier, createParent("Identifier"), parent=parentNode)
        setParent(prevParent)

        updateTok()
        return VariableDecl() and (updateTok() and VariableDeclRec()) 
    else:
        printBool("going to statement........................")
        #return Stmt()
        while True:
            printBool("inside while loop VarDeclRec !!!!!!!!!!!!!!!!!")
            if Stmt(): 
                if tok.value == const.RCURLEY:
                    printBool("returning true from VarDeclRec")
                    return True
                if tok.value == const.ELSE:
                    printBool("else found")
                    return True
                updateTok()
                
                pass
            else:
                return True
                


def Stmt():
    
    printBool("inside stmt tok value" + str(tok))
    if tok.value == const.RCURLEY:
        printBool("returning after RCURLEY")
        return True

    #comment out due to debbuging
    #updateTok()
    if tok.value == const.IF:
        printBool("&&&&&& sending to if")
        if updateTok() and IfStmt():
            #updateTok()
            if tok.value == const.RCURLEY:
                printBool("RCURLEY found after ifSTMT......")
                return True
            else:
                return  Stmt()
    
    elif tok.value == const.WHILE:
        if updateTok() and WhileStmt():
            if tok.value == const.RCURLEY:
                printBool("RCURLEY found after WHILE_STMT......")
                return True
            else:
                printBool("STMT found instead of RCURLEY")
                return Stmt()

    #changing for
    elif tok.value == const.FOR:
        if updateTok() and ForStmt():
            if tok.value == const.RCURLEY:
                printBool("RCURLEY found after FOR_STMT......")
                return True
            else:
                printBool("STMT found instead of RCURLEY")
                return Stmt()

    #might need to add sth
    elif tok.value == const.BREAK:
        return updateTok() and BreakStmt() and updateTok() and Stmt()

    elif tok.value == const.RETURN:
        printBool("return found..............")
        return updateTok() and ReturnStmt()
    
    elif tok.value == const.PRINT: #and (updateTok() and tok.value == const.LPAREN):
        return updateTok() and PrintStmt() and updateTok() and Stmt()

    elif tok.value == const.SEMICOLON:
        printBool("semicolon found")
        return True

    elif tok.value == const.LCURLEY:
        
        return StmtBlock() and printBool("returning from stmtBlock() " + tok.value)
    
    elif createExprTree() and Expr() and tok.value == const.SEMICOLON:
        printBool("returning after getting expr() and semicolon")
        return True

    else:
        reportError(tok)
        return False    
        """
        printBool("return from stmt()")
        boolVar = Expr() and tok.value == const.SEMICOLON and updateTok()
        if boolVar == True and tok.value == const.ELSE:
            return True
        else:
            return Stmt()
        """
    
        #on getting "{", code for stmt-->stmtBlock



"""
Expr ::= LValue = Expr | Constant | LValue | Call | ( Expr ) |
    Expr + Expr | Expr - Expr | Expr * Expr | Expr / Expr |
    Expr % Expr | - Expr | Expr < Expr | Expr <= Expr |
    Expr > Expr | Expr >= Expr | Expr == Expr | Expr ! = Expr |
    Expr && Expr | Expr || Expr | ! Expr | ReadInteger ( ) |
    ReadLine ( )
"""
exprTreeHead = ""
lastTreeHead = ""
currentTreeHead = ""
unary = False
def Expr():
    global unary

    printBool("inside Expr")
    global exprTreeHead
    global lastTreeHead
    printBool(tok)
    global assgnHead
    global exprTree
    global prevOperator
    global currentTreeHead
    prevParent = parentNode
    #changed today
    """if tok.value == const.READINT:
        return True
    
    elif tok.value == const.READLINE:
        return True
    """

    if tok.value == const.LPAREN:
        printBool("((((((( leftParen found")
        #new code added and next token removed from if
        if (updateTok() and Expr()) and (printBool("*****bool print token... " + str(tok.value)) and tok.value == const.RPAREN):
            printBool("returning true.....")
            updateTok()
            if tok.value in const.operatorList:
                printBool("operator list found in lparen")
                return  updateTok() and Expr()
            else:
                return True
    


    elif tok.value == const.MINUS:
        tree.create_node("  " + str(tok.lineno) + "$" + prefix + "ArithmeticExpr:", createParent("ArithmeticExpr"), parent=parentNode)
        tree.create_node("  " + str(tok.lineno) + "$Operator: " + str(tok.value), createParent("Operator"), parent=createParent("ArithmeticExpr"))            
        setParent(prevParent)
        unary = True
        assgnHead = createParent("ArithmeticExpr")
        return (updateTok() and Expr())

    elif tok.value == const.NOT:
        tree.create_node("  " + str(tok.lineno) + "$" + prefix + "LogicalExpr:", createParent("LogicalExpr"), parent=parentNode)
        tree.create_node("  " + str(tok.lineno) + "$Operator: " + str(tok.value), createParent("Operator"), parent=createParent("LogicalExpr"))            
        setParent(prevParent)
        unary = True
        assgnHead = createParent("LogicalExpr")
        return updateTok() and Expr()
    
    elif tok.type == const.IDENT:
        identifier = tok.value
        printBool("var " + tok.value + "found")
        #print("token position", tok[20])
        updateTok()
        
        
        if tok.value == const.EQUAL:
            exprType = "AssignExpr"
            tree.create_node("  " + str(tok.lineno) + "$" + prefix + exprType + ":", createParent(exprType), parent=parentNode)
            resetPrefix()
            assgnHead = createParent(exprType)
            tree.create_node("  " + str(tok.lineno) + "$FieldAccess:", createParent("FieldAccess"), parent=assgnHead)
            tree.create_node("  " + str(tok.lineno) + "$Identifier: " + identifier, createParent("Identifier"), parent=createParent("FieldAccess"))
            tree.create_node("  " + str(tok.lineno) + "$Operator: " + str(tok.value), createParent("Operator"), parent=assgnHead)            
        elif tok.value in const.arithmaticOperator:
            exprType = "ArithmeticExpr"
        elif tok.value in const.relationalOperator:
            exprType = "RelationalExpr"
        elif tok.value in const.equalityOperator:
            exprType = "EqualityExpr"
        elif tok.value in const.logicalOperator:
            exprType = "LogicalExpr"
        
        if assgnHead == "":
            assgnHead = prevParent
        
        
        printBool("checkpoint ...2 ")
        if tok.value == const.LPAREN:
            if assgnHead == "":

                tree.create_node("  " + str(tok.lineno) + "$" + prefix + "Call:", createParent("Call"), parent = parentNode)
                tree.create_node("  " + str(tok.lineno) + "$Identifier: " + identifier, createParent("Identifier"), parent=createParent("Call"))
            else:
                tree.create_node("  " + str(tok.lineno) + "$" + prefix + "Call:", createParent("Call"), parent = assgnHead)
                tree.create_node("  " + str(tok.lineno) + "$Identifier: " + identifier, createParent("Identifier"), parent=createParent("Call"))
            
            
            setParent(createParent("Call"))
            printBool("checkpoint ... 3")
            updateTok()
            return Actuals() and setParent(prevParent)
        
        elif (tok.value == const.EQUAL) or (tok.value in const.operatorList):
            printBool("equal found")
            if tok.value in const.operatorList:
                currentOperator = str(tok.value)
                if prevOperator == "":
                    
                    exprTreeHead = createParent(exprType)
                    exprTree.create_node("  " + str(tok.lineno) + "$" +  exprType + ":", exprTreeHead)
                    exprTree.create_node("  " + str(tok.lineno) + "$FieldAccess:", createParent("FieldAccess"), parent=exprTreeHead)
                    exprTree.create_node("  " + str(tok.lineno) + "$Identifier: " + identifier, createParent("Identifier"), parent=createParent("FieldAccess"))
                    exprTree.create_node("  " + str(tok.lineno) + "$Operator: " + str(tok.value), createParent("Operator"), parent=exprTreeHead)            
                    prevOperator = currentOperator
                    lastTreeHead = exprTreeHead

                elif const.precedenceList[prevOperator] >= const.precedenceList[currentOperator]:

                    if currentTreeHead != "":
                        exprTree.create_node("  " + str(tok.lineno) + "$FieldAccess:", createParent("FieldAccess"), parent=currentTreeHead)

                        exprTree.create_node("  " + str(tok.lineno) + "$Identifier: " + identifier, createParent("Identifier"), parent=createParent("FieldAccess"))
                        currentTreeHead = ""
                    

                    else:
                        exprTree.create_node("  " + str(tok.lineno) + "$FieldAccess:", createParent("FieldAccess"), parent=exprTreeHead)

                        exprTree.create_node("  " + str(tok.lineno) + "$Identifier: " + identifier, createParent("Identifier"), parent=createParent("FieldAccess"))
                    
                    tempTree=Tree()
                    tempTreeHead = createParent(exprType)
                    tempTree.create_node("  " + str(tok.lineno) + "$" + exprType + ":", tempTreeHead)
                    tempTree.paste(tempTreeHead, exprTree)
                    tempTree.create_node("  " + str(tok.lineno) + "$Operator: " + str(tok.value), createParent("Operator"), parent=tempTreeHead)            
                    exprTree = tempTree
                    exprTreeHead = tempTreeHead
                    prevOperator = currentOperator
                    lastTreeHead = tempTreeHead 

                elif const.precedenceList[prevOperator] < const.precedenceList[currentOperator]:
                    tempTree=Tree()
                    tempTreeHead = createParent(exprType)
                    tempTree.create_node("  " + str(tok.lineno) + "$" + exprType + ":", tempTreeHead)
                    tempTree.create_node("  " + str(tok.lineno) + "$FieldAccess:", createParent("FieldAccess"), parent=tempTreeHead)
                    tempTree.create_node("  " + str(tok.lineno) + "$Identifier: " + identifier, createParent("Identifier"), parent=createParent("FieldAccess"))
                    tempTree.create_node("  " + str(tok.lineno) + "$Operator: " + str(tok.value), createParent("Operator"), parent=tempTreeHead)            
                    exprTree.paste(exprTreeHead, tempTree)
                    prevOperator = currentOperator
                    lastTreeHead = tempTreeHead
                    currentTreeHead = tempTreeHead



            return updateTok() and Expr()
        else:
            if exprTree:

                exprTree.create_node("  " + str(tok.lineno) + "$FieldAccess:", createParent("FieldAccess"), parent=lastTreeHead)
                exprTree.create_node("  " + str(tok.lineno) + "$Identifier: " + identifier, createParent("Identifier"), parent=createParent("FieldAccess"))
                tag = exprTree.__getitem__(exprTree.root).tag
                tag = tag.split("$")[0] + "$" + prefix + tag.split("$")[1]
                exprTree.update_node(exprTree.root, tag)
                tree.paste(assgnHead, exprTree)
                createExprTree()
            else:
                if unary == False:
                    tree.create_node("  " + str(tok.lineno) + "$" + prefix + "FieldAccess:", createParent("FieldAccess"), parent=assgnHead)
                else: 
                    tree.create_node("  " + str(tok.lineno) + "$" + "FieldAccess:", createParent("FieldAccess"), parent=assgnHead)
                tree.create_node("  " + str(tok.lineno) + "$Identifier: " + identifier, createParent("Identifier"), parent=createParent("FieldAccess"))

                unary = False

            setParent(prevParent)
            return True
        
        #elif tok.value in const.operatorList:
        #    return updateTok() and Expr()
            
    elif tok.type in const.constantList:
        printBool("constant found")
        constantVal = str(tok.value)

        if tok.type == const.DOUBLECONSTANT:
            temp = str(tok.value).split(".")
            if temp[1] == "0" and len(temp[1]) == 1:
                constantVal = temp[0]

        constants = str(tok.type).split("_")
        if str(tok.type) == const.STRINGCONSTANT:
            con = "$" + constants[1] + ": "
        else:
            con = "$" + constants[1] + ": "
        par = constants[1]
        updateTok()

        if tok.value in const.arithmaticOperator:
            exprType = "ArithmeticExpr"
        elif tok.value in const.relationalOperator:
            exprType = "RelationalExpr"
        elif tok.value in const.equalityOperator:
            exprType = "EqualityExpr"
        elif tok.value in const.logicalOperator:
            exprType = "LogicalExpr"

        #exprType = "ArithmeticExpr"
        if assgnHead == "":
            assgnHead = prevParent


        if tok.value in const.operatorList:
            printBool("operator found after constant")
            currentOperator = str(tok.value)
            if prevOperator == "":
                
                exprTreeHead = createParent(exprType)
                exprTree.create_node("  " + str(tok.lineno) + "$"  + exprType + ":", exprTreeHead)
                exprTree.create_node("  " + str(tok.lineno) + con + constantVal, createParent(par), parent=exprTreeHead)
                exprTree.create_node("  " + str(tok.lineno) + "$Operator: " + str(tok.value), createParent("Operator"), parent=exprTreeHead)            
                prevOperator = currentOperator
                lastTreeHead = exprTreeHead

            elif const.precedenceList[prevOperator] >= const.precedenceList[currentOperator]:

                if currentTreeHead != "":

                    exprTree.create_node("  " + str(tok.lineno) + con + constantVal, createParent(par), parent=currentTreeHead)
                    currentTreeHead = ""
                

                else:

                    exprTree.create_node("  " + str(tok.lineno) + con + constantVal, createParent(par), parent=exprTreeHead)
                
                tempTree=Tree()
                tempTreeHead = createParent(exprType)
                tempTree.create_node("  " + str(tok.lineno) + "$" + exprType + ":", tempTreeHead)
                tempTree.paste(tempTreeHead, exprTree)
                tempTree.create_node("  " + str(tok.lineno) + "$Operator: " + str(tok.value), createParent("Operator"), parent=tempTreeHead)            
                exprTree = tempTree
                exprTreeHead = tempTreeHead
                prevOperator = currentOperator
                lastTreeHead = tempTreeHead 

            elif const.precedenceList[prevOperator] < const.precedenceList[currentOperator]:
                tempTree=Tree()
                tempTreeHead = createParent(exprType)
                tempTree.create_node("  " + str(tok.lineno) + "$" + exprType + ":", tempTreeHead)
                tempTree.create_node("  " + str(tok.lineno) + con + constantVal, createParent(par), parent=tempTreeHead)
                tempTree.create_node("  " + str(tok.lineno) + "$Operator: " + str(tok.value), createParent("Operator"), parent=tempTreeHead)            
                exprTree.paste(exprTreeHead, tempTree)
                prevOperator = currentOperator
                lastTreeHead = tempTreeHead
                currentTreeHead = tempTreeHead

            





            return updateTok() and Expr()
            #return True
        elif tok.value == '.':
            updateTok()
            reportError(tok)
            return False

        else:
            #changed from return true to return Expr()
            if exprTree:
                exprTree.create_node("  " + str(tok.lineno) + con + constantVal, createParent(par), parent=lastTreeHead)
                tag = exprTree.__getitem__(exprTree.root).tag
                tag = tag.split("$")[0] + "$" + prefix + tag.split("$")[1]
                exprTree.update_node(exprTree.root, tag)
                tree.paste(assgnHead, exprTree)
                createExprTree()
                
            else:
                if unary == False:
                    tree.create_node("  " + str(tok.lineno) + "$" + prefix + constants[1] +": " + constantVal, createParent(par), parent=assgnHead)
                else:
                    tree.create_node("  " + str(tok.lineno) + "$" + constants[1] +": " + constantVal, createParent(par), parent=assgnHead)
                    

                unary = False

            setParent(prevParent)
            return True
    
    
    #elif tok.value == const.RPAREN:
    #    printBool("this part executed ***********************", tok)
    #    return True
    #ReadInteger ( )
    elif tok.value == const.READINT or tok.value == const.READLINE:
        printBool("readline or readint found............................")
        if assgnHead == "":
            assgnHead = prevParent
        tree.create_node("  " + str(tok.lineno) + "$" + str(tok.value) + "Expr:", createParent(str(tok.value)), parent=assgnHead)
        if (updateTok() and tok.value == const.LPAREN) and (updateTok() and tok.value == const.RPAREN):
            updateTok()
            return True
        else:
            reportError(tok)
            return False
    else:
        printBool("some error...")
        reportError(tok)
        return False


def Actuals():
    setPrefix("(actuals) ")
    printBool("inside actuals")
    if tok.value == const.RPAREN:
        return True
    

    while True:
        printBool("tok at begin of while in actuals..." + str(tok))
        if createExprTree() and not Expr():
            reportError(tok)
            return False
        printBool("Tok value inside actuals....." + str(tok))
        if tok.value == const.COMMA and (updateTok() and tok.value != const.RPAREN):
            #updateTok()
            continue
        
        if tok.value == const.RPAREN:
            updateTok()
            return resetPrefix() and True
        else:
            reportError(tok)
            return False
    

    
def IfStmt():
    prevParent = parentNode
    tree.create_node("   $IfStmt:", createParent("IfStmt"), parent=prevParent)
    setParent(createParent("IfStmt"))
    
    printBool("inside ifStmt")
    if tok.value == const.LPAREN:
        setPrefix("(test) ")
        ifVar = (updateTok() and createExprTree() and Expr()) and (printBool("if ..." + str(tok.value)) and  tok.value == const.RPAREN)
        setPrefix("(then) ")
        if not ifVar:
            printBool("error inside if")
            reportError(tok)
            return False
        if updateTok() and (printBool("calling stmt() from if")) and not Stmt():
            printBool("ret false from ifStmt")
            reportError(tok)
            return False
        printBool("-----------" + str(tok))
        if tok.value == const.SEMICOLON:
            updateTok()
        
        
            
        if  tok != None and tok.value == const.ELSE:
            setPrefix("(else) ")
            printBool("else found!!!")
            updateTok()
            if not Stmt():
                printBool("returning false from else*****")
                reportError(tok)
                return False 
            else:
                printBool("true for if with else------------------------------------"+ str(tok))
                return True and setParent(prevParent) and resetPrefix()
        else:
            printBool("true for if-----------XXXX-------------------------"+ str(tok))
            return True and setParent(prevParent) and resetPrefix()
    else:
        reportError(tok)
        return False


def ForStmt():
    prevParent = parentNode
    tree.create_node("   $ForStmt:", createParent("ForStmt"), parent=prevParent)
    setParent(createParent("ForStmt"))
    

    if tok.value == const.LPAREN:
        #semicolon found for( ;  )
        printBool("lparen found")
        setPrefix("(init) ")
        if updateTok() and tok.value == const.SEMICOLON:
            tree.create_node("   $" + prefix + "Empty:", createParent("Empty"), parent=parentNode)
            printBool("First expresion not found")
            pass
        # for(i = 1;)
        elif createExprTree() and not Expr() or ( tok.value != const.SEMICOLON):
            printBool("second part is returning false")
            reportError(tok)
            return False

        # for( i = 1; i > 5;)
        printBool("token..." + str(tok))
        updateTok()
        setPrefix("(test) ")
        if createExprTree() and not Expr() or  (printBool("inside if~~~~~~~" + tok.value) and  not tok.value == const.SEMICOLON):
            printBool("second part also returning false")
            reportError(tok)
            return False 
        # for( i = 1; i > 5; )
        updateTok()
        setPrefix("(step) ")
        printBool("entering final part tok = "+ str(tok))
        if tok.value == const.RPAREN:
            tree.create_node("   $" + prefix + "Empty:", createParent("Empty"), parent=parentNode)
            printBool("----------returning true from  without third part")
            return updateTok() and Stmt() and setParent(prevParent)

        elif createExprTree() and Expr() and printBool("from third part......" + tok.value) and tok.value == const.RPAREN:
            printBool("++++++returning true from  with third part")
            return updateTok() and Stmt() and setParent(prevParent)
        #return true
    else:
        reportError(tok)
        return False


def WhileStmt():
    prevParent = parentNode
    tree.create_node("   $WhileStmt:", createParent("WhileStmt"), parent=prevParent)
    setParent(createParent("WhileStmt"))
    setPrefix("(test) ")
    if tok.value == const.LPAREN:
        
        whileVar = (updateTok() and createExprTree() and Expr()) and (printBool("while!!!!!!!!!!!!!" + str(tok.value)) and tok.value == const.RPAREN)
        if not whileVar:
            printBool("error inside while.....")
            reportError(tok)
            return False
        
        if updateTok() and not Stmt():
            printBool("false in while O_O_O_O_O_O_O_O_")
            reportError(tok)
            return False           
        printBool("true for while...."+ str(tok))
        return True and setParent(prevParent) and resetPrefix()
    else:
        reportError(tok)
        return False


def ReturnStmt():
    printBool("inside return stmt()"+ str(tok))
    prevParent = parentNode
    tree.create_node("  " + str(tok.lineno) + "$ReturnStmt:", createParent("ReturnStmt"), parent=parentNode)
    par = createParent("ReturnStmt")
    if tok.value == const.SEMICOLON:
        tree.create_node("   $Empty:", createParent("Empty"), parent=par)
        return True and setParent(prevParent)
    elif createExprTree() and Expr()  and (tok.value == const.SEMICOLON) and updateTok():
        return True and setParent(prevParent)
    else:
        reportError(tok)
        return False

def BreakStmt():
    if tok.value == const.SEMICOLON:
        prevParent = parentNode
        tree.create_node("  " + str(tok.lineno) + "$" + prefix + "BreakStmt:", createParent("BreakStmt"), parent=parentNode)
        printBool("inside breakstmt() "+ str(tok))
        return True and setParent(prevParent)
    else:
        reportError(tok)
        return False

#PrintStmt  --> Print ( Expr + , ) ;
#input printBool(a, " ");
def PrintStmt():
    #LPRAREN checking removed from the caller method
    global parentNode
    prevParent = parentNode
    tree.create_node("    $PrintStmt:", createParent("PrintStmt"), parent=parentNode)
    par = createParent("PrintStmt")
    setPrefix("(args) ")
    printBool("PPPPPPPPPP>>..>>>>>>>>inside print stmt"+ str(tok))
    if  tok.value == const.LPAREN: 
        while True and setParent(par):
            printBool("inside print loop")
            updateTok()
            if createExprTree() and not Expr():
                printBool("returning false from printStmt")
                reportError(tok)
                return False
            if tok.value == const.COMMA:
                printBool(",,,,,,,,,,,,, comma found")
                #updateTok()
                setParent(prevParent)
                continue
            elif tok.value == const.RPAREN:
                printBool("Rparenn found ........in print ")
                updateTok()
                printBool(tok)
                if  tok != None and tok.value == const.SEMICOLON:
                    printBool("returning true")
                    return True and setParent(prevParent) and resetPrefix()
                else:
                    printBool("returning false")
                    reportError(tok)
                    return False
            
    else:
        reportError(tok)
        return False
    
def getAST():
    if Program():
        return tree
    

def main():
    #printBool(Program())

    #    printBool("true")
    if Program():
        print("")
        tree.show(key = False, line_type = 'ascii-sp')
    
if __name__ == "__main__":
    main()
    




###########""""""""""
"""
   
    elif tok.value == const.LPAREN:
        printBool("((((((( leftParen found")
        #new code added and next token removed from if
        if (updateTok() and Expr()) and (printBool("*****bool print token... " + str(tok.value)) and tok.value == const.RPAREN):
            printBool("returning true.....")
            updateTok()
            if tok.value == const.SEMICOLON:
                return True
            else:
                return  updateTok() and Expr()
    """



"""
    else:
        printBool("going to Expr from here")
        return (Expr() and  tok.value == const.SEMICOLON) and (updateTok() and Stmt())

    """
