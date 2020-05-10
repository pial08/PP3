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
typeMap = {const.INTCONSTANT.split("_")[1]: const.INT, const.DOUBLECONSTANT.split("_")[1]:const.DOUBLE, const.BOOLCONSTANT.split("_")[1]: const.BOOL, const.STRINGCONSTANT.split("_")[1]: const.STRING }
print(typeMap)
def getType(node):
    
    print("inside getType()")
    if "FieldAccess" in node.tag:
        print("fieldaccess found....")
        child = tree.children(node.identifier)
        if "Identifier" in child[0].tag:
            ident  = child[0].tag.split(":")[1].strip()
            type = symbolTable.get(ident)
            ############# if not found... type error
            if type == None:
                print("********variable not found in local")
                type = globalSymbolTable.get(ident):
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
    
    visited[str(v)] = True
    node = tree.get_node(v)
    #print("NODE......", node)
    if "Expr" in node.identifier:

        print("Expr found..^_^", node.tag)
        children = tree.children(node.identifier)
        left = children[0]
        operator = children[1]
        right = children[2]

        print("left", left, "right ", right)

        if "Expr" in left.tag:
            print("expr found in left")
            typeLeft = DFSUtil(left.identifier, visited)
            if typeLeft == "False":
                return 
        else:
            print("inside else... for left")
            typeLeft = getType(left)
        
        if "Expr" in right.tag:
            print("expr found in right")
            typeRight = DFSUtil(right.identifier, visited)
            if typeRight == "False":
                return
        else:
            print("inside else ... for right")
            typeRight = getType(right)

        print("printing types..", typeLeft)
        #returning any one is fine
        if typeLeft == typeRight:
            print("type matched...", typeLeft)
            print("operator ", operator.tag)
            if operator.tag.split(":")[1].strip() in const.booleanOperators:
                return "bool"
            
            return typeLeft
        elif typeLeft == None or typeRight == None:
            return "False"
        else:
            print("*** Incompatible operands: ",typeLeft, operator.tag.split(":")[1],  typeRight)
            return "False"

    elif "FnDecl" in node.identifier:
        print("inside fundecl handler...............")
        tempFunMap = {}
        counter = 0
        children = tree.children(node.identifier)
        print("len of children", len(children))
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
                print("symboltable... ^)^)^ before...", symbolTable)
                DFSUtil(child.identifier, visited)
                functions.append(tempFunMap)
                symbolTable.clear()
                print("symboltable... ^)^)^", symbolTable)
                print("functions...***VVV***...", functions)
                break
                #### check for return type matching
            
        return




   
    for i in tree.children(v): 
        #print(i)
        if visited.get(str(i.identifier)) == None:
            #print(i.identifier, " ",i.tag ) 
            #print("not found")
            if "AssignExpr" in i.tag:
                print("assignment expr found.....")
                fieldAccess = tree.children(i.identifier)
                childOfChild = tree.children(fieldAccess[0].identifier)
                identifier = childOfChild[0].tag.split(":")[1].strip()
                print(symbolTable)
                print("identifier = ", identifier)
                typeLeft = symbolTable.get(identifier)
                print("type = ", typeLeft)
                #do type check
                
                expr = tree.siblings(fieldAccess[0].identifier)
                print("Expr = ", expr)
                if "FieldAccess" in expr[1].tag or "Constant" in expr[1].tag:
                    typeRight = getType(expr[1])
                else:
                    typeRight = DFSUtil(expr[1].identifier, visited)
                print("TypeRight =", typeRight)
                if typeLeft != typeRight:
                    print("*** Error in assignment")
                continue
            elif "VarDecl" in i.tag:
                parent = tree.parent(i.identifier)
                print("parent should be program....", parent)
                
                children = tree.children(i.identifier)
                type = children[0].tag.split(":")[1].strip()
                identifier = children[1].tag.split(":")[1].strip()
                if parent.identifier == "Program":
                    globalSymbolTable[identifier] = type
                else:
                    symbolTable[identifier] = type
                print("symboltable ********************", symbolTable)
                print("global symboltable ********************", globalSymbolTable)

                continue
            elif "LogicalExpr" in i.tag:
                print("logical expr found")
                sthExpr = tree.children(i.identifier)
                print("Expr = ", sthExpr)
                if "FieldAccess" in sthExpr[1].tag or "Constant" in sthExpr[1].tag:
                    print("inside if field or const")
                    type = getType(sthExpr[1])
                else:
                    print("inside else field or const")
                    type = DFSUtil(i.identifier, visited)
                print("type =", type)
                continue
            elif "ForStmt" in i.tag or "WhileStmt" in i.tag:
                print("for found")
                breakFlag = True
                DFSUtil(i.identifier, visited)
                breakFlag = False
            elif "BreakStmt" in i.tag and breakFlag != True:
                print("*** break is only allowed inside a loop")
            
            elif "Call" in i.tag:
                #should return fun ret type
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
                        



            
            
            else:
                DFSUtil(i.identifier, visited)

        

def findFunByName(name):
    for function in functions:
        if function.ge(name) in not None:
            return function
    return None


def DFS(ROOT): 
  
    visited = {} 

  
    DFSUtil(ROOT, visited) 
    print("returning from DFS...")
  


tree = pp2.getAST()

tree.show(key = False, line_type = 'ascii-sp')
print(tree.size())
ROOT = tree.root
print(ROOT)

print("children.....", tree.children(ROOT)[0].identifier)


DFS(ROOT)





