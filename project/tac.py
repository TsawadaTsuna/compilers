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
        elif hijo.type == "IF":
            naux, cond = getStrOperation(hijo.childrens[0],auxtmp)
            for ifhijo in hijo.childrens:
                if ifhijo.type == "if":
                    file.write(cond)
                    nauxt,nauxb=genBlock(ifhijo,naux,auxbck)
                    file.write("T"+str(naux-1)+" IFGOTO L"+str(nauxb-1)+"\n")
                    auxtmp=nauxt
                    auxbck=nauxb
                elif ifhijo.type == "ELIF":
                    naux, cond = getStrOperation(ifhijo.childrens[0],auxtmp)
                    for ififhijo in ifhijo.childrens:
                        if ififhijo.type == "elif":
                            file.write(cond)
                            nauxt,nauxb=genBlock(ififhijo,naux,auxbck)
                            file.write("T"+str(naux-1)+" ELSEIFGOTO L"+str(nauxb-1)+"\n")
                            auxtmp=nauxt
                            auxbck=nauxb
                elif ifhijo.type == "ELSE":
                    if ifhijo.childrens[0]:
                        nauxt,nauxb=genBlock(ifhijo.childrens[0],naux,auxbck)
                        file.write("ELSEGOTO L"+str(nauxb-1)+"\n")
                        auxtmp=nauxt
                        auxbck=nauxb
        elif hijo.type == "WHILE":
            naux, cond = getStrOperation(hijo.childrens[0],auxtmp)
            file.write(cond)
            nauxt,nauxb=genWhileBlock(hijo.childrens[1],naux,auxbck,naux)
            file.write("T"+str(naux-1)+" IFGOTO L"+str(nauxb-1)+"\n")
            auxtmp=nauxt
            auxbck=nauxb
        elif hijo.type == "FOR":
            nauxtmp,op=getStrAssign(hijo.childrens[0],auxtmp)
            file.write(op)
            nauxtmp,op1=getStrOperation(hijo.childrens[1],nauxtmp)
            file.write(op1)
            nauxt,nauxb=genForBlock(hijo.childrens[3],nauxtmp,auxbck,"T"+str(nauxtmp-1)+" IFGOTO L"+str(auxbck)+"\n",hijo.childrens[2],op1)
            file.write("T"+str(nauxtmp-1)+" IFGOTO L"+str(nauxb-1)+"\n")
            auxtmp=nauxt
            auxbck=nauxb

    for bck in blocks:
        file.write("\n"+bck)
    file.close()

def genBlock(node,auxtmp,auxbck):
    nauxtmp=auxtmp
    nauxbck=auxbck
    bck = "L"+str(auxbck)+"\n"
    for hijo in node.childrens:
        if hijo.type == "=":
            nauxtmp,inst=getStrAssign(hijo,auxtmp)
            bck=bck+inst
        elif hijo.type == "PRINT":
            nauxtmp,inst=getStrPrint(hijo,auxtmp)
            bck=bck+inst
        elif hijo.type == "IF":
            naux, cond = getStrOperation(hijo.childrens[0],auxtmp)
            for ifhijo in hijo.childrens:
                if ifhijo.type == "if":
                    bck=bck+(cond)
                    nauxt,nauxb=genBlock(ifhijo,naux,auxbck)
                    bck=bck+("T"+str(naux-1)+" IFGOTO L"+str(nauxb-1)+"\n")
                    nauxtmp=nauxt
                    nauxbck=nauxb
                elif ifhijo.type == "ELIF":
                    naux, cond = getStrOperation(ifhijo.childrens[0],auxtmp)
                    for ififhijo in ifhijo.childrens:
                        if ififhijo.type == "elif":
                            bck=bck+(cond)
                            nauxt,nauxb=genBlock(ififhijo,naux,auxbck)
                            bck=bck+("T"+str(naux-1)+" ELSEIFGOTO L"+str(nauxb-1)+"\n")
                            nauxtmp=nauxt
                            nauxbck=nauxb
                elif ifhijo.type == "ELSE":
                    if ifhijo.childrens[0]:
                        nauxt,nauxb=genBlock(ifhijo.childrens[0],naux,auxbck)
                        bck=bck+("ELSEGOTO L"+str(nauxb-1)+"\n")
                        auxtmp=nauxt
                        auxbck=nauxb
        elif hijo.type == "WHILE":
            naux, cond = getStrOperation(hijo.childrens[0],auxtmp)
            bck=bck+(cond)
            nauxt,nauxb=genWhileBlock(hijo.childrens[1],naux,auxbck,naux)
            bck=bck+("T"+str(naux-1)+" IFGOTO L"+str(nauxb-1)+"\n")
            nauxtmp=nauxt
            nauxbck=nauxb
        elif hijo.type == "FOR":
            nauxtmp,op=getStrAssign(hijo.childrens[0],auxtmp)
            bck=bck+(op)
            nauxtmp,op=getStrOperation(hijo.childrens[1],nauxtmp)
            bck=bck+(op)
            nauxt,nauxb=genForBlock(hijo.childrens[3],nauxtmp,auxbck,"T"+str(nauxtmp-1)+" IFGOTO L"+str(auxbck)+"\n",hijo.childrens[2],op)
            bck=bck+("T"+str(nauxtmp-1)+" IFGOTO L"+str(nauxb-1)+"\n")
            nauxtmp=nauxt
            nauxbck=nauxb

    #code
    blocks.append(bck)
    return nauxtmp+1,nauxbck+1

def genWhileBlock(node,auxtmp,auxbck,condi):
    nauxtmp=auxtmp
    nauxbck=auxbck
    bck = "L"+str(auxbck)+"\n"
    for hijo in node.childrens:
        if hijo.type == "=":
            nauxtmp,inst=getStrAssign(hijo,auxtmp)
            bck=bck+inst
        elif hijo.type == "PRINT":
            nauxtmp,inst=getStrPrint(hijo,auxtmp)
            bck=bck+inst
        elif hijo.type == "IF":
            naux, cond = getStrOperation(hijo.childrens[0],auxtmp)
            for ifhijo in hijo.childrens:
                if ifhijo.type == "if":
                    bck=bck+(cond)
                    nauxt,nauxb=genBlock(ifhijo,naux,auxbck)
                    bck=bck+("T"+str(naux-1)+" IFGOTO L"+str(nauxb-1)+"\n")
                    nauxtmp=nauxt
                    nauxbck=nauxb
                elif ifhijo.type == "ELIF":
                    naux, cond = getStrOperation(ifhijo.childrens[0],auxtmp)
                    for ififhijo in ifhijo.childrens:
                        if ififhijo.type == "elif":
                            bck=bck+(cond)
                            nauxt,nauxb=genBlock(ififhijo,naux,auxbck)
                            bck=bck+("T"+str(naux-1)+" ELSEIFGOTO L"+str(nauxb-1)+"\n")
                            nauxtmp=nauxt
                            nauxbck=nauxb
                elif ifhijo.type == "ELSE":
                    if ifhijo.childrens[0]:
                        nauxt,nauxb=genBlock(ifhijo.childrens[0],naux,auxbck)
                        bck=bck+("ELSEGOTO L"+str(nauxb-1)+"\n")
                        nauxtmp=nauxt
                        nauxbck=nauxb
        elif hijo.type == "WHILE":
            naux, cond = getStrOperation(hijo.childrens[0],auxtmp)
            bck=bck+(cond)
            nauxt,nauxb=genWhileBlock(hijo.childrens[1],naux,auxbck,naux)
            bck=bck+("T"+str(naux-1)+" IFGOTO L"+str(nauxb-1)+"\n")
            nauxtmp=nauxt
            nauxbck=nauxb
        elif hijo.type == "FOR":
            nauxtmp,op=getStrAssign(hijo.childrens[0],auxtmp)
            bck=bck+(op)
            nauxtmp,op=getStrOperation(hijo.childrens[1],nauxtmp)
            bck=bck+(op)
            nauxt,nauxb=genForBlock(hijo.childrens[3],nauxtmp,auxbck,"T"+str(nauxtmp-1)+" IFGOTO L"+str(auxbck)+"\n",hijo.childrens[2],op)
            bck=bck+("T"+str(nauxtmp-1)+" IFGOTO L"+str(nauxb-1)+"\n")
            nauxtmp=nauxt
            nauxbck=nauxb


    bck=bck+"T"+str(condi-1)+" IFGOTO L"+str(nauxbck)+"\n"
    blocks.append(bck)
    return nauxtmp+1,nauxbck+1

def genForBlock(node,auxtmp,auxbck,condi,step,compar):
    nauxtmp=auxtmp
    nauxbck=auxbck
    bck = "L"+str(auxbck)+"\n"
    for hijo in node.childrens:
        if hijo.type == "=":
            nauxtmp,inst=getStrAssign(hijo,auxtmp)
            bck=bck+inst
        elif hijo.type == "PRINT":
            nauxtmp,inst=getStrPrint(hijo,auxtmp)
            bck=bck+inst
        elif hijo.type == "IF":
            naux, cond = getStrOperation(hijo.childrens[0],auxtmp)
            for ifhijo in hijo.childrens:
                if ifhijo.type == "if":
                    bck=bck+(cond)
                    nauxt,nauxb=genBlock(ifhijo,naux,auxbck)
                    bck=bck+("T"+str(naux-1)+" IFGOTO L"+str(nauxb-1)+"\n")
                    nauxtmp=nauxt
                    nauxbck=nauxb
                elif ifhijo.type == "ELIF":
                    naux, cond = getStrOperation(ifhijo.childrens[0],auxtmp)
                    for ififhijo in ifhijo.childrens:
                        if ififhijo.type == "elif":
                            bck=bck+(cond)
                            nauxt,nauxb=genBlock(ififhijo,naux,auxbck)
                            bck=bck+("T"+str(naux-1)+" ELSEIFGOTO L"+str(nauxb-1)+"\n")
                            nauxtmp=nauxt
                            nauxbck=nauxb
                elif ifhijo.type == "ELSE":
                    if ifhijo.childrens[0]:
                        nauxt,nauxb=genBlock(ifhijo.childrens[0],naux,auxbck)
                        bck=bck+("ELSEGOTO L"+str(nauxb-1)+"\n")
                        nauxtmp=nauxt
                        nauxbck=nauxb
        elif hijo.type == "WHILE":
            naux, cond = getStrOperation(hijo.childrens[0],auxtmp)
            bck=bck+(cond)
            nauxt,nauxb=genWhileBlock(hijo.childrens[1],naux,auxbck,naux)
            bck=bck+("T"+str(naux-1)+" IFGOTO L"+str(nauxb-1)+"\n")
            nauxtmp=nauxt
            nauxbck=nauxb
        elif hijo.type == "FOR":
            nauxtmp,op=getStrAssign(hijo.childrens[0],auxtmp)
            bck=bck+(op)
            nauxtmp,op=getStrOperation(hijo.childrens[1],nauxtmp)
            bck=bck+(op)
            nauxt,nauxb=genForBlock(hijo.childrens[3],nauxtmp,auxbck,"T"+str(nauxtmp-1)+" IFGOTO L"+str(auxbck)+"\n",hijo.childrens[2],op)
            bck=bck+("T"+str(nauxtmp-1)+" IFGOTO L"+str(nauxb-1)+"\n")
            nauxtmp=nauxt
            nauxbck=nauxb


    #bck=bck+step+"\n"
    st=""
    if step.childrens[1].type == "OPERATION":
        nauxt,st=getStrOperation(step.childrens[1])
        bck=bck+st+step.childrens[0].val+" = T"+str(naux-1)+"\n"
        nauxtmp=nauxt
    else:
        bck=bck+step.childrens[0].val+" = "+step.childrens[0].val+" "+step.val+" "+step.childrens[1].val+"\n"
    #bck=bck+"T"+str(nauxtmp)+" = "+step.childrens[0].val+"\n"
    bck=bck+compar
    bck=bck+condi
    blocks.append(bck)
    return nauxtmp+1,nauxbck+1

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

def getStrAssign(node,aux):
    naux = aux
    comp=""
    if node.childrens[1].type == "OPERATION" or node.childrens[1].type == "CONCTENACION":
        naux,compn = getStrOperation(node.childrens[1],aux)
        comp = compn+(node.childrens[0].val + " = " +"T"+str(naux-1)+ "\n")
    else:
        comp=(node.childrens[0].val + " = " + node.childrens[1].val + "\n")
    return naux+1,comp

def genPrint(node,file,aux):
    naux = aux
    if node.childrens[0].type == "OPERATION" or node.childrens[0].type == "CONCTENACION":
        naux = genOperation(node.childrens[0],file,aux)
        file.write("print "+"T"+str(naux-1)+ "\n")
    else:
        file.write("print "+ node.childrens[0].val + "\n")
    return naux

def getStrPrint(node,aux):
    naux = aux
    comp=""
    if node.childrens[0].type == "OPERATION" or node.childrens[0].type == "CONCTENACION":
        naux,compn = getStrOperation(node.childrens[0],aux)
        comp = compn+("print "+"T"+str(naux-1)+ "\n")
    else:
        comp=("print "+ node.childrens[0].val + "\n")
    return naux+1,comp

def genOperation(node,file,aux):
    naux = aux
    if node.childrens[1].type == "OPERATION":
        naux = genOperation(node.childrens[1],file,aux)
        file.write("T"+str(naux)+" = "+node.childrens[0].val+" "+node.val+" "+"T"+str(naux-1)+ "\n")
    else:
        file.write("T"+str(naux)+" = "+node.childrens[0].val+" "+node.val+" "+node.childrens[1].val+ "\n")
    return naux+1

def getStrOperation(node,aux):
    naux = aux
    comp=""
    if node.childrens[1].type == "OPERATION" or node.childrens[1].type == "CONCTENACION":
        naux,compn = getStrOperation(node.childrens[1],aux)
        comp = compn+("T"+str(naux)+" = "+node.childrens[0].val+" "+node.val+" "+"T"+str(naux-1)+ "\n")
    else:
        comp = ("T"+str(naux)+" = "+node.childrens[0].val+" "+node.val+" "+node.childrens[1].val+ "\n")
    return naux+1,comp

# define genIf

treeAdrsCodeGen(tree,"tac.txt")

print("a")