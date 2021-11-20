from LexerParser import Node, abstractTree, names, parsefile

class SymbolTable:
    parent=None
    variables={}
    id=''
    children=None
    def __init__(self,id,parent=None):
        self.id=id
        self.parent=parent
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

#Lista de tablas de simbolos, cada tabla tendra su id i una referencia al subarbol para ver que sea de ese bloque especifico
#cambiar todo lo del proyecto a un folder
globalvars = SymbolTable("Global")
globalvars.addVar("a","int")
print("a")