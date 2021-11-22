from LexerParser import Node, abstractTree, names, parsefile

class SymbolTable:
    parent=None
    variables=dict({})
    id=''
    #children=None
    block=0
    def __init__(self,id,block,parent=None):
        self.id=id
        self.parent=parent
        self.block=block
        self.variables=dict({})
        #if parent:
            #parent.children=[self]
            #parent.children.append(self)

    def printInfo(self):
        print("id: ",self.id)
        if self.parent:
            print("parent: ", self.parent.id)
        print("variables: ", self.variables)
        #if self.children:
            #print("children:")
            #for c in self.children:
                #print(c.id)
    
    def addVar(self,name,type):
        self.variables[name]=type


#arbol de prueba:
tree=None
def generateTestTree():
    tree = Node("inicio","inicio")
    assign1=Node("assign","=",[Node("a","FLOAT",isvar=True),Node("3","INT")])
    tree.childrens.append(assign1)
    op1=Node("+","CONCTENACION",[Node("hola","STRING"),Node("3","INT")])
    assign2=Node("assign","=",[Node("b","STRING",isvar=True),op1])
    tree.childrens.append(assign2)
    elif1=Node("elif","ELIF",[Node("<","OPERATION",[Node("b","STRING",isvar=True),Node("4","INT")]),
    Node("bloque","elif",[Node("assign","=",[Node("b","INT",isvar=True),Node("*","OPERATION",[Node("2","INT"),Node("3","INT")])])])])
    else1=Node("else","ELSE",[Node("bloque","else",[Node("PRINT","PRINT",[Node("true","BOOLEAN")])])])
    if1=Node("if","IF",[Node("<","OPERATION",[Node("a","FLOAT",isvar=True),Node("3","INT")]),Node("bloque","if",[Node("PRINT","PRINT",[Node("a","FLOAT",isvar=True)]),Node("assign","=",[Node("g","BOOLEAN",isvar=True),Node("true","BOOLEAN")])]),elif1,else1])
    tree.childrens.append(if1)
    while1=Node("while","WHILE",[Node("and","OPERATION",[Node("!=","OPERTION",[Node("a","FLOAT",isvar=True)]),Node("==","OPERATION",[Node("3","INT"),Node("4","INT")])]),
    Node("bloque","while",[Node("PRINT","PRINT",[Node("b","STRING",isvar=True)])])])
    tree.childrens.append(while1)
    assign3=Node("assign","=",[Node("i","INT",isvar=True),Node("0","INT")])
    tree.childrens.append(assign3)
    assignfor=Node("assign","=",[Node("i","INT",isvar=True),Node("0","INT")])
    compfor=Node("<","OPERATION",[Node("i","INT",isvar=True),Node("10","INT")])
    stepfor=Node("+","step",[Node("i","INT",isvar=True),Node("1","INT")])
    bloquefor=Node("bloque","for",[Node("PRINT","PRINT",[Node("i","INT",isvar=True)])])
    for1=Node("for","FOR",[assignfor,compfor,stepfor,bloquefor])
    tree.childrens.append(for1)

    return tree
    
#Arbol de pruebas   
tree=generateTestTree()
#parsefile("code.txt")
#tree=abstractTree

#globalvars = SymbolTable("Global",id(tree))
symboltables=[]

def getScopeTable(id):
    for t in symboltables:
        if t.block==id:
            return t
    return None

def createScopes(node,parentScope):
    if node:
        actualScope = SymbolTable(node.val,id(node),parentScope)
        symboltables.append(actualScope)
        for hijo in node.childrens:
            if hijo:
                if hijo.type == "=":
                    actualScope.addVar(hijo.childrens[0].val,hijo.childrens[0].type)
                elif hijo.type == "IF":
                    addVariablesOfBlock(hijo.childrens[1],actualScope)
                    createScopes(hijo,actualScope)
                elif hijo.type == "ELIF":
                    addVariablesOfBlock(hijo.childrens[1],actualScope)
                    createScopes(hijo,parentScope)
                elif hijo.type == "ELSE":
                    addVariablesOfBlock(hijo.childrens[0],actualScope)
                    createScopes(hijo,parentScope)
                elif hijo.type == "WHILE":
                    addVariablesOfBlock(hijo.childrens[1],actualScope)
                    createScopes(hijo,actualScope)
                elif hijo.type == "FOR":
                    addVariablesOfBlock(hijo.childrens[3],actualScope)
                    createScopes(hijo,actualScope)
        

def addVariablesOfBlock(node,scope):
    if node:
        for hijo in node.childrens:
            if hijo:
                if hijo.type == "=":
                    scope.addVar(hijo.childrens[0].val,hijo.childrens[0].type)
                elif hijo.type == "IF":
                    createScopes(hijo,scope)
                elif hijo.type == "ELIF":
                    createScopes(hijo,scope)
                elif hijo.type == "ELSE":
                    createScopes(hijo,scope)
                elif hijo.type == "WHILE":
                    createScopes(hijo,scope)
                elif hijo.type == "FOR":
                    createScopes(hijo,scope)
        
def checkScopes(node,scope):
    if not scope:
        actualScope = getScopeTable(id(node))
    else:
        actualScope=scope
    if node:
        for hijo in node.childrens:
            if hijo:
                if hijo.type == "IF":
                    subcheck=checkScopes(hijo,None)
                    if not subcheck:
                        return False
                elif hijo.type == "ELIF":
                    subcheck=checkScopes(hijo,None)
                    if not subcheck:
                        return False
                elif hijo.type == "ELSE":
                    subcheck=checkScopes(hijo,None)
                    if not subcheck:
                        return False
                elif hijo.type == "WHILE":
                    subcheck=checkScopes(hijo,None)
                    if not subcheck:
                        return False
                elif hijo.type == "FOR":
                    subcheck=checkScopes(hijo,None)
                    if not subcheck:
                        return False
                elif hijo.isvar:
                    if not checkVariable(hijo.childrens[0].val,actualScope):
                        return False
                else:
                    subcheck=checkScopes(hijo,actualScope)
                    if not subcheck:
                        return False
    return True

def checkVariable(var,scope):
    if not scope:
        return False
    else:
        if var in scope.variables:
            return True
        else:
            checkVariable(var,scope.parent)

createScopes(tree,None)
for t in symboltables:
    t.printInfo()
print(checkScopes(tree,None))
#print(symboltables[0].printInfo())
print("a")

