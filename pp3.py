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
                print("********variable not found in local")
                type = globalSymbolTable.get(ident)
                if type == Node:
                    return "False"
                else:
                    return type

            return type
    else:
        #param inside typeMap.get(param)
        #param =   5$IntConstant: 5
        type =  typeMap.get(node.tag.split(":")[0].split("$")[1])      
        return type

def DFSUtil(v, visited): 
    global symbolTable
    visited[str(v)] = True
    node = tree.get_node(v)
    printBool("NODE......" +  str(node))
    if "Expr" in node.identifier:

        printBool("Expr found..^_^" +  node.tag)
        children = tree.children(node.identifier)
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

        printBool("printing types.." + typeLeft)
        #returning any one is fine
        if typeLeft == typeRight:
            printBool("type matched..." + typeLeft)
            printBool("operator " + operator.tag)
            if operator.tag.split(":")[1].strip() in const.booleanOperators:
                return "bool"
            
            return typeLeft
        elif typeLeft == None or typeRight == None:
            return "False"
        else:
            print("*** Incompatible operands: ",typeLeft, operator.tag.split(":")[1].strip(),  typeRight)
            return "False"

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
                    printBool("return found")
                    returnExpr = tree.siblings(returnChild.identifier)[-1]
                    if "Constant" in returnExpr.tag:
                        type = getType(returnExpr)
                    else:
                        type = DFSUtil(tree.siblings(returnChild.identifier)[-1].identifier, visited)
                    if type != tempFunMap["returnType"]:
                        print("*** Incompatible return: ",type, "given, ", tempFunMap["returnType"], " expected")
                else:
                    printBool("... not sure")
                printBool("functions table..." + str(functions))
                symbolTable.clear()
                break
                #### check for return type matching
            
        return




   
    for i in tree.children(v): 
        #printBool(i)
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
                printBool("expr" +  str(expr))
                if "FieldAccess" in expr[1].tag or "Constant" in expr[1].tag:
                    typeRight = getType(expr[1])
                else:
                    print(expr)
                    typeRight = DFSUtil(expr[1].identifier, visited)
                if typeLeft != typeRight:
                    print("typeright", typeRight)
                    print("*** Error in assignment")
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
                printBool("logical expr found")
                sthExpr = tree.children(i.identifier)
                if "FieldAccess" in sthExpr[1].tag or "Constant" in sthExpr[1].tag:
                    printBool("inside if field or const")
                    type = getType(sthExpr[1])
                else:
                    printBool("inside else field or const")
                    type = DFSUtil(i.identifier, visited)
                printBool("type =" +  type)
                continue
            elif "ForStmt" in i.tag or "WhileStmt" in i.tag:
                printBool("for found")
                breakFlag = True
                DFSUtil(i.identifier, visited)
                breakFlag = False
            elif "BreakStmt" in i.tag and breakFlag != True:
                print("*** break is only allowed inside a loop")
            
            elif "Call" in i.tag:
                #should return fun ret type
                print("funCall found")
                children = tree.children(i.identifier)
                numOfParam = len(children) - 1
                funName = children[0].tag.split(":")[1].strip()
                function = findFunByName(funName)
                if function == None:
                    print("***   Function called before declaration...")
                else:
                    numberofParamInTable = len(function) - 2
                    if numberofParamInTable != numOfParam:
                        print("*** Function ", funName, "expects ", numberofParamInTable, "arguments but ", numOfParam, "given")
                    else:
                        for i in range(1, len(children)):
                            if "FieldAccess" in children[i].tag or "Constant" in children[i].tag:
                                print("constant found")
                                
                                type = getType(children[i])
                            else:
                                print("constant not found")
                                type = DFSUtil(children[i].identifier, visited)
                            if type != function["param_" + str(i)]:
                                print("Incompatible argument ", i, ":", type, "given, ", function["param_" + str(i)],  "expected")
                            else:
                                printBool("good to go...")
            



                        



            
            
            else:
                DFSUtil(i.identifier, visited)

        

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

tree.show(key = False, line_type = 'ascii-sp')
print(tree.size())
ROOT = tree.root
print(ROOT)

print("children.....", tree.children(ROOT)[0].identifier)


DFS(ROOT)





