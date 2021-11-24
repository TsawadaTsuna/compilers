from semanticanalize import Node,abstractTree,tree,SymbolTable
from copy import deepcopy

def treeAdrsCodeGen(node,filename):
    file = open("project/"+filename,"w")
    auxtmp = 1
    auxbck = 1
    for hijo in node.childrens:
        if hijo.type == "=":
            genAssign(hijo,file,auxtmp)

def genAssign(node,file,aux):
    if not node.type == "=":
        print("error in recursion")
    else:
        if node.childrens[1].type == "OPERATION" or node.childrens[1].type == "CONCTENACION":
            naux = genOperation(node.childrens[1],file,aux)
            file.write(node.childrens[0].val + " = " +"T"+str(naux-1)+ "\n")
        else:
            file.write(node.childrens[0].val + " = " + node.childrens[1].val + "\n")

def genOperation(node,file,aux):
    naux = aux
    if node.childrens[1].type == "OPERATION":
        naux = genOperation(node.childrens[1],file,aux)
        file.write("T"+str(naux)+" = "+node.childrens[0].val+" + "+"T"+str(naux-1)+ "\n")
    else:
        file.write("T"+str(naux)+" = "+node.childrens[0].val+" + "+node.childrens[1].val+ "\n")
    return naux+1

treeAdrsCodeGen(tree,"tac.txt")

print("a")