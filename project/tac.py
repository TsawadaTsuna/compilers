from semanticanalize import Node,abstractTree,tree,SymbolTable
from copy import deepcopy

blocks = []

def treeAdrsCodeGen(node,filename):
    file = open("project/"+filename,"w")
    auxtmp = 1
    auxbck = 1
    for hijo in node.childrens:
        if hijo.type == "=":
            auxtmp=genAssign(hijo,file,auxtmp)
        elif hijo.type == "PRINT":
            auxtmp=genPrint(hijo,file,auxtmp)

def genAssign(node,file,aux):
    naux = aux
    if not node.type == "=":
        print("error in recursion")
    else:
        if node.childrens[1].type == "OPERATION" or node.childrens[1].type == "CONCTENACION":
            naux = genOperation(node.childrens[1],file,aux)
            file.write(node.childrens[0].val + " = " +"T"+str(naux-1)+ "\n")
        else:
            file.write(node.childrens[0].val + " = " + node.childrens[1].val + "\n")
    return naux

def genPrint(node,file,aux):
    naux = aux
    if node.childrens[0].type == "OPERATION" or node.childrens[0].type == "CONCTENACION":
        naux = genOperation(node.childrens[0],file,aux)
        file.write("print "+"T"+str(naux-1)+ "\n")
    else:
        file.write("print "+ node.childrens[0].val + "\n")
    return naux

def genOperation(node,file,aux):
    naux = aux
    if node.childrens[1].type == "OPERATION":
        naux = genOperation(node.childrens[1],file,aux)
        file.write("T"+str(naux)+" = "+node.childrens[0].val+" "+node.val+" "+"T"+str(naux-1)+ "\n")
    else:
        file.write("T"+str(naux)+" = "+node.childrens[0].val+" "+node.val+" "+node.childrens[1].val+ "\n")
    return naux+1

treeAdrsCodeGen(tree,"tac.txt")

print("a")