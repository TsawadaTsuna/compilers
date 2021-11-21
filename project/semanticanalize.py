from LexerParser import Node, abstractTree, names, parsefile

class SymbolTable:
    parent=None
    variables={}
    id=''
    children=None
    block=0
    def __init__(self,id,block,parent=None):
        self.id=id
        self.parent=parent
        self.block=block
        if parent:
            parent.children=[self]
            #parent.children.append(self)

    def printInfo(self):
        print("id: ",self.id)
        if self.parent:
            print("parent: ", self.parent.id)
        if self.children:
            print("children:")
            for c in self.children:
                print(c.id)
    
    def addVar(self,name,type):
        self.variables[name]=type


#arbol de prueba:
tree=None
def generateTestTree():
    tree = Node("inicio","inicio")
    assign1=Node("assign","=",[Node("a","FLOAT"),Node("3","INT")])
    tree.childrens.append(assign1)
    op1=Node("+","CONCTENACION",[Node("hola","STRING"),Node("3","INT")])
    assign2=Node("assign","=",[Node("b","STRING"),op1])
    tree.childrens.append(assign2)
    elif1=Node("elif","ELIF",[Node("<","OPERATION",[Node("b","STRING"),Node("4","INT")]),
    Node("bloque","elif",[Node("assign","=",[Node("b","INT"),Node("*","OPERATION",[Node("2","INT"),Node("3","INT")])])])])
    else1=Node("else","ELSE",[Node("bloque","else",[Node("PRINT","PRINT",[Node("true","BOOLEAN")])])])
    if1=Node("if","IF",[Node("<","OPERATION",[Node("a","FLOAT"),Node("3","INT")]),Node("bloque","if",[Node("PRINT","PRINT",[Node("a","FLOAT")])]),elif1,else1])
    tree.childrens.append(if1)
    while1=Node("while","WHILE",[Node("and","OPERATION",[Node("!=","OPERTION",[Node("a","FLOAT")]),Node("==","OPERATION",[Node("3","INT"),Node("4","INT")])]),
    Node("bloque","while",[Node("PRINT","PRINT",[Node("b","STRING")])])])
    tree.childrens.append(while1)
    assignfor=Node("assign","=",[Node("i","INT"),Node("0","INT")])
    compfor=Node("<","OPERATION",[Node("i","INT"),Node("10","INT")])
    stepfor=Node("+","step",[Node("i","INT"),Node("1","INT")])
    bloquefor=Node("bloque","for",[Node("PRINT","PRINT",[Node("i","INT")])])
    for1=Node("for","FOR",[assignfor,compfor,stepfor,bloquefor])
    tree.childrens.append(for1)

    return tree
    
tree=generateTestTree()
#Lista de tablas de simbolos, cada tabla tendra su id i una referencia al subarbol para ver que sea de ese bloque especifico
#cambiar todo lo del proyecto a un folder

globalvars = SymbolTable("Global",id(tree))
symboltables=[globalvars]
print("a")

