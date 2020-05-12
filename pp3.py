import pp2
import const
from treelib.treelib import Node, Tree

symbolTable = {}
functions = [] #[{"ident": ident, "ret": ret, "param1":"type(int)"...}, {}]
symbolTableStack = []
globalSymbolTable = {}
breakFlag = False
"""
change T_IntConstant to Intconstant
"""

def printBool(st):
    #print(st)
    return True



def reportError(st, node, error=None):
    lineCol = node.identifier.split(":")[1].split("_")
    line = lineCol[0]
    col = lineCol[1]
    print("")
    errorLinePrint = "*** Error line " + line + "."
    print(errorLinePrint)
    print(pp2.lexanalysis.lines[int(line) - 1])
    errorLine = ""
    length = int(col) - len(node.tag.split(":")[1].strip()) - 1
    if "Break" in node.tag:
        length = int(col) - 6
    if "(test)" in node.tag:
        length = len(pp2.lexanalysis.lines[int(line) - 1].split(";")[0])
    
    
    while length:
        errorLine += " "
        length -= 1
    for i in range(len(node.tag.split(":")[1].strip())):
        errorLine += "^"
    if "Break" in node.tag:
        errorLine += "^^^^^"
    if "(test)" in node.tag:
        for i in range(len(pp2.lexanalysis.lines[int(line) - 1].split(";")[0]) - 2):
            errorLine += "^"
    if error != None:
        print(error)
    else:
        print(errorLine)
    print(st)
    print("")

    #print("node in report error...", node)

typeMap = {const.INTCONSTANT.split("_")[1]: const.INT, const.DOUBLECONSTANT.split("_")[1]:const.DOUBLE, const.BOOLCONSTANT.split("_")[1]: const.BOOL, const.STRINGCONSTANT.split("_")[1]: const.STRING }
printBool(typeMap)
def getType(node):
    
    printBool("inside getType()")
    if "FieldAccess" in node.tag:
        printBool("fieldaccess found....")
        child = tree.children(node.identifier)
        if "Identifier" in child[0].tag:
            ident  = child[0].tag.split(":")[1].strip()
            type = symbolTable.get(ident)
            
            ############# if not found... type error
            if type == None:
                type = globalSymbolTable.get(ident)
                if type == None:
                    reportError("*** No declaration found for variable " + "\'" + ident + "\'", tree.children(node.identifier)[0])
                    return None
                else:
                    return type

            return type
    else:
        #param inside typeMap.get(param)
        #param =   5$(actuals)IntConstant: 5
        temp = node.tag.split(":")[0].split("$")[1]
        if ")" in temp:
            temp = temp.split(")")[1].strip()
        type =  typeMap.get(temp)      
        return type

def DFSUtil(v, visited): 
    global symbolTable
    global breakFlag
    visited[str(v)] = True
    node = tree.get_node(v)
    if "Expr" in node.identifier:

        children = tree.children(node.identifier)
        if len(children) == 2:
            type = getType(children[1])
            return type
        else:

            left = children[0]
            operator = children[1]
            right = children[2]

            #printBool("left", left, "right ", right)

            if "Expr" in left.tag:
                printBool("expr found in left")
                typeLeft = DFSUtil(left.identifier, visited)
                if typeLeft == "False":
                    return 
            else:
                printBool("inside else... for left")
                typeLeft = getType(left)
            
            if "Expr" in right.tag:
                printBool("expr found in right")
                typeRight = DFSUtil(right.identifier, visited)
                if typeRight == "False":
                    return
            else:
                printBool("inside else ... for right")
                typeRight = getType(right)

            printBool("printing types.." + str(typeLeft))
            #returning any one is fine
            if typeLeft == typeRight:
                printBool("type matched..." + typeLeft)
                printBool("operator " + operator.tag)
                if operator.tag.split(":")[1].strip() in const.booleanOperators:
                    return "bool"
                
                return typeLeft
            elif typeLeft == None or typeRight == None:
                return None
            else:
                reportError("*** Incompatible operands: " + typeLeft + " " + operator.tag.split(":")[1].strip() + " " + typeRight,  operator)
                return None

    elif "FnDecl" in node.tag:
        printBool("inside fundecl handler...............")
        tempFunMap = {}
        counter = 1
        children = tree.children(node.identifier)
        for child in children:
            if "(return type)" in child.tag:
                tempFunMap["returnType"] = child.tag.split(":")[1].strip()
            elif "Identifier" in child.tag:
                funName = child.tag.split(":")[1].strip()
                
                tempFunMap["identifier"] = funName
            
            elif "(formals)" in child.tag:
                childOfChild = tree.children(child.identifier)
                type = childOfChild[0].tag.split(":")[1].strip()
                tempFunMap["param_" + str(counter)] = type
                counter += 1
                #putting vardecl in table
                identifier = childOfChild[1].tag.split(":")[1].strip()
                symbolTable[identifier] = type

            elif "(body)" in child.tag:
                DFSUtil(child.identifier, visited)
                functions.append(tempFunMap)
                #work on void return
                returnChild = None
                returnChildren = tree.children(child.identifier)
                printBool("<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>")
                for child in returnChildren:
                    printBool(child)
                    if "ReturnStmt" in child.tag:
                        printBool("return found")

                        returnChild = child

                printBool("RETURN CHILD..." +  str(returnChild))
                if returnChild != None:
                    returnExpr = tree.siblings(returnChild.identifier)[-1]
                    if "Constant" in returnExpr.tag:
                        type = getType(returnExpr)
                    else:
                        type = DFSUtil(tree.siblings(returnChild.identifier)[-1].identifier, visited)
                    if type != tempFunMap["returnType"]:
                        reportError("*** Incompatible return: " + type, " given, " + tempFunMap["returnType"] + " expected", returnChild)
                else:
                    printBool("... not sure")
                printBool("functions table..." + str(functions))
                symbolTable.clear()
                break
                #### check for return type matching
            
        return
    
    elif "Call" in node.tag:
        #should return fun ret type
        children = tree.children(node.identifier)
        numOfParam = len(children) - 1
        funName = children[0].tag.split(":")[1].strip()
        function = findFunByName(funName)
        if function == None:
            reportError("*** No declaration for Function " + "\'" + funName + "\'" + "found", children[0])
        else:
            numberofParamInTable = len(function) - 2
            if numberofParamInTable != numOfParam:
                reportError("*** Function " + "\'" + funName + "\'" + " expects " + numberofParamInTable + "arguments but " + numOfParam + "given", children[0])
            else:
                for i in range(1, len(children)):
                    if "FieldAccess" in children[i].tag or "Constant" in children[i].tag:
                        
                        type = getType(children[i])
                    else:
                        type = DFSUtil(children[i].identifier, visited)
                    if type != function["param_" + str(i)]:
                        reportError("***Incompatible argument " + str(i) + ": " + type + " given, " + function["param_" + str(i)] + " expected", children[i])
                        
                    else:
                        printBool("good to go...")
        return function["returnType"]
    
    elif "FieldAccess" in node.tag or "Constant" in node.tag:
        
        type = getType(node)
        return type
    elif "ReadInteger" in node.tag:
        return "int"
    elif "ReadLine" in node.tag:
        return "string"


    



    for i in tree.children(v): 
        printBool("child of i....******" + str(i))
        if visited.get(str(i.identifier)) == None:
            #printBool(i.identifier, " ",i.tag ) 
            #printBool("not found")
            if "AssignExpr" in i.tag:
                printBool("assignment expr found.....")
                fieldAccess = tree.children(i.identifier)
                childOfChild = tree.children(fieldAccess[0].identifier)
                identifier = childOfChild[0].tag.split(":")[1].strip()
                printBool(symbolTable)
                printBool("identifier = " + identifier)
                typeLeft = symbolTable.get(identifier)
                printBool("type = " + typeLeft)
                #do type check
                
                expr = tree.siblings(fieldAccess[0].identifier)
                if "FieldAccess" in expr[1].tag or "Constant" in expr[1].tag:
                    typeRight = getType(expr[1])
                else:
                    typeRight = DFSUtil(expr[1].identifier, visited)
                if typeLeft != typeRight and not (typeLeft == None or typeRight == None):
                    reportError("*** Incompatible operands: " + typeLeft + " = " + typeRight, expr[0])
                continue
            elif "VarDecl" in i.tag:
                parent = tree.parent(i.identifier)
                
                children = tree.children(i.identifier)
                type = children[0].tag.split(":")[1].strip()
                identifier = children[1].tag.split(":")[1].strip()
                if parent.identifier == "Program":
                    globalSymbolTable[identifier] = type
                else:
                    symbolTable[identifier] = type
                printBool("symboltable ********************" + str(symbolTable))
                printBool("global symboltable ********************"+ str(globalSymbolTable))

                continue
            elif "LogicalExpr" in i.tag:
                sthExpr = tree.children(i.identifier)
                if "FieldAccess" in sthExpr[1].tag or "Constant" in sthExpr[1].tag:
                    printBool("inside if field or const")
                    type = getType(sthExpr[1])
                else:
                    printBool("inside else field or const")
                    type = DFSUtil(i.identifier, visited)
                if type != "bool" and type != None:
                    reportError("*** Incompatible operand: "+ sthExpr[0].tag.split(":")[1].strip() + " " + str(type), sthExpr[0])  
                printBool("type =" +  str(type))
                continue
            
            elif "ForStmt" in i.tag or "WhileStmt" in i.tag:
                breakFlag = True
                children = tree.children(i.identifier)
                if "ForStmt" in i.tag:
                    type = DFSUtil(children[1].identifier, visited)
                    chld = children[1]
                elif "WhileStmt" in i.tag:
                    type = DFSUtil(children[0].identifier, visited)
                    chld = children[0]
                DFSUtil(i.identifier, visited)
                if type != "bool":
                    reportError("*** Test expression must have boolean type", chld)
                breakFlag = False
            
            
            elif "BreakStmt" in i.tag and breakFlag != True:
                reportError("*** break is only allowed inside a loop", i)
            
            elif "Call" in i.tag:
                #should return fun ret type
                children = tree.children(i.identifier)
                numOfParam = len(children) - 1
                funName = children[0].tag.split(":")[1].strip()
                function = findFunByName(funName)
                if function == None:
                    reportError("*** No declaration for Function " + "\'" + funName + "\'" + "found", children[0])
                else:
                    numberofParamInTable = len(function) - 2
                    if numberofParamInTable != numOfParam:
                        reportError("*** Function " + "\'" + funName + "\'" + " expects " + str(numberofParamInTable) + " arguments but " + str(numOfParam) + " given", children[0])
                    else:
                        for j in range(1, len(children)):
                            if "FieldAccess" in children[j].tag or "Constant" in children[j].tag:
                                
                                type = getType(children[j])
                            else:
                                type = DFSUtil(children[j].identifier, visited)
                            
                            
                            if type != function["param_" + str(j)]:
                                err = calculateErrLine(children[j])
                                reportError("***Incompatible argument " + str(j) + ": " + type + " given, " + function["param_" + str(j)] + " expected", children[j], err)
                            else:
                                printBool("good to go...")
            
            elif "IfStmt" in i.tag:
                type = DFSUtil(tree.children(i.identifier)[0].identifier, visited)
                if type != "bool" and type != None:
                    err = calculateErrLine(tree.children(i.identifier)[0])
                    reportError("*** Test expression must have boolean type", i, err)  
                continue

            elif "PrintStmt" in i.tag:
                counter = 1
                children = tree.children(i.identifier)
                for child in children:
                    if "DoubleConstant" in child.tag:
                        reportError("*** Incompatible argument " + str(counter) +": double given, int/bool/string expected", child)
                    elif "Constant" in child.tag or "FieldAccess" in child.tag:
                        type = getType(child)
                    elif "Call" in child.tag:
                        childOfCall = tree.children(child.identifier)
                        identifier = childOfCall[0].tag.split(":")[1].strip()
                        function = findFunByName(identifier)
                        type = function["returnType"]
                    else: 
                        type = DFSUtil(child.identifier,visited)
                    if type == "double":
                        error = calculateErrLine(child)
                        reportError("*** Incompatible argument " + str(counter) +": double given, int/bool/string expected", child, error)
                    counter += 1





                        



            
            
            else:
                DFSUtil(i.identifier, visited)


def calculateErrLine(child):
    errorLine = ""
    if "Call" in child.tag:
        childOfChild = tree.children(child.identifier)
        beginCol = childOfChild[0].identifier.split(":")[1].split("_")[1]
        endCol = childOfChild[-1].identifier.split(":")[1].split("_")[1]
        numberOfChar = int(endCol) - int(beginCol) + 1 + 2
        numberOfWhiteSpace = int(endCol)  - numberOfChar
        
        
    
    elif "(actuals)" in child.tag or "(test)" in child.tag:
        lineNo = child.tag.split("$")[0].strip()
        line = pp2.lexanalysis.lines[int(lineNo) - 1]
        if "," not in line:
            #single expr exists
            
            numberOfChar = len(line.split(")")[0].split("(")[1])
            numberOfWhiteSpace = len(line.split(")")[0]) - numberOfChar

            
    elif "ReadInteger" in child.tag or "ReadLine" in child.tag:
        lineNo = child.tag.split("$")[0].strip()
        line = pp2.lexanalysis.lines[int(lineNo) - 1]
        numberOfWhiteSpace = len(line.split("(")[0]) + 1
        numberOfChar = len(child.identifier.split(":")[0]) + 2


    for i in range(numberOfWhiteSpace):
        errorLine += " "
    for i in range(numberOfChar):
        errorLine += "^"  

    return errorLine

def findFunByName(name):
    for function in functions:
        printBool(function)
        if function.get("identifier") == name:
            return function
    return None


def DFS(ROOT): 
  
    visited = {} 

  
    DFSUtil(ROOT, visited) 
    printBool("returning from DFS...")
  


tree = pp2.getAST()

#tree.show(key = False, line_type = 'ascii-sp')
#print(tree.size())
ROOT = tree.root
#print(ROOT)

#print("children.....", tree.children(ROOT)[0].identifier)


DFS(ROOT)





