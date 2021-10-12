
tokens = []
symbols ={}
casterror = False
class Node:
    def __init__(self, data):
        self.children = []
        self.data = data

    def insertData(self, data):
        node = Node(data)
        self.children.append(node)
        return node

    def insertNode(self, node):
        self.children.append(node)

    def preorden(self, node):
        print(node.data)
        l = node.children.copy()
        for e in l:
            self.preorden(e)

    def posorden(self, node):
        l = node.children.copy()
        for e in l:
            self.posorden(e)
        print(node.data)
    
    def genLists(self,node,list1, list2):
        l = node.children.copy()
        for e in l:
            self.genLists(e,list1,list2)
        if node.data == "assign" or node.data == "plus" or node.data == "minus":
            list2.append(node.data)
        else:
            list1.append(node.data)
        #print(node.data)

pTree = Node("program")

def scanner(name):
    #file = open('input.txt')
    file = open(name)
    lines = file.readlines()
    file.close()
    flo = False
    inte = False
    for line in lines:
        l=line.strip().split(" ")
        for c in l:
            if inte:
                symbols[c]='integer'
                inte = False
            if flo:
                symbols[c]='float'
                flo = False
            if c == 'i':
                inte = True
            elif c == 'f':
                flo = True
            
            tokens.append(c)
    #print(tokens)

def parser():
    l = len(tokens)
    i = 0
    assign = False
    flo = False
    temp = Node("")
    while i < l:
        if tokens[i] == "f":
            temp = Node("floatdcl "+str(tokens[i+1]))
            pTree.insertNode(temp)
            i+=2
        elif tokens[i] == "i":
            temp = Node("intdcl "+str(tokens[i+1]))
            pTree.insertNode(temp)
            i+=2
        elif tokens[i] == "p":
            temp = Node("print "+str(tokens[i+1]))
            pTree.insertNode(temp)
            i+=2
        elif tokens[i] == "=":
            if i+2 < l:
                if tokens[i+2] == "+" or tokens[i+2] == "-":
                    assign=False
                else:
                    assign=True
            temp = Node("assign")
            flo=False
            if symbols[tokens[i-1]] == "float":
                flo = True
            temp.insertData("id "+str(tokens[i-1]))
            pTree.insertNode(temp)
            i+=1
        elif tokens[i] == "+":
            temp1 = Node("plus")
            if i+2 < l:
                if tokens[i+2] == "+" or tokens[i+2] == "-":
                    assign=False
                else:
                    assign=True
            if tokens[i-1] in symbols.keys():
                if symbols[tokens[i-1]] == "float":
                    flo = True
                temp1.insertData("id "+str(tokens[i-1]))
                temp.insertNode(temp1)
                temp=temp1
            else:
                if "." in tokens[i-1]:
                    temp1.insertData("fnum "+str(tokens[i-1]))
                    temp.insertNode(temp1)
                    temp=temp1
                    flo = False
                else:
                    if flo:
                        temp1.insertData("fnum "+str(tokens[i-1]))
                        temp.insertNode(temp1)
                        temp=temp1
                        flo=False
                    else:
                        temp1.insertData("inum "+str(tokens[i-1]))
                        temp.insertNode(temp1)
                        temp=temp1
                        flo=False
            i+=1
        elif tokens[i] == "-":
            temp1 = Node("minus")
            if i+2 < l:
                if tokens[i+2] == "+" or tokens[i+2] == "-":
                    assign=False
                else:
                    assign=True
            if tokens[i-1] in symbols.keys():
                if symbols[tokens[i-1]] == "float":
                    flo = True
                temp1.insertData("id "+str(tokens[i-1]))
                temp.insertNode(temp1)
                temp=temp1
            else:
                if "." in tokens[i-1]:
                    temp1.insertData("fnum "+str(tokens[i-1]))
                    temp.insertNode(temp1)
                    temp=temp1
                    flo=False
                else:
                    if flo:
                        temp1.insertData("fnum "+str(tokens[i-1]))
                        temp.insertNode(temp1)
                        temp=temp1
                        flo=False
                    else:
                        temp1.insertData("inum "+str(tokens[i-1]))
                        temp.insertNode(temp1)
                        temp=temp1
                        flo=False
            i+=1
        else:
            if assign:
                if tokens[i] in symbols.keys():
                    temp.insertData("id "+str(tokens[i]))
                else:
                    if "." in tokens[i]:
                        temp.insertData("fnum "+str(tokens[i]))
                        flo=False
                    else:
                        if flo:
                            temp.insertData("fnum "+str(tokens[i]))
                            flo=False
                        else:
                            temp.insertData("inum "+str(tokens[i]))
                            flo=False
                assign=False
            i+=1

def checkFloat(node):
    nodeL = node.children[0]
    nodeR = node.children[1]
    if "inum" in nodeL.data:
        val = nodeL.data
        nodeL.data = "int2float"
        nodeL.insertData(val)
    elif "id" in nodeL.data:
        if symbols[nodeL.data.split(" ")[1]] == "integer":
            val = nodeL.data
            nodeL.data = "int2float"
            nodeL.insertData(val)
    elif "plus" in nodeL.data or "minus" in nodeL.data:
        checkFloat(nodeL)
    if "inum" in nodeR.data:
        val = nodeR.data
        nodeR.data = "int2float"
        nodeR.insertData(val)
    elif "id" in nodeR.data:
        if symbols[nodeR.data.split(" ")[1]] == "integer":
            val = nodeR.data
            nodeR.data = "int2float"
            nodeR.insertData(val)
    elif "plus" in nodeR.data or "minus" in nodeR.data:
        checkFloat(nodeR)

def checkInt(node):
    nodeL = node.children[0]
    nodeR = node.children[1]
    if "fnum" in nodeL.data:
        return True
    elif "id" in nodeL.data:
        if symbols[nodeL.data.split(" ")[1]] == "float":
            return True
    elif "plus" in nodeL.data or "minus" in nodeL.data:
        checkInt(nodeL)
    if "fnum" in nodeR.data:
        return True
    elif "id" in nodeR.data:
        if symbols[nodeR.data.split(" ")[1]] == "float":
            return True
    elif "plus" in nodeR.data or "minus" in nodeR.data:
        return checkInt(nodeR)
    else:
        return False

def typeChecker():
    nodes = pTree.children
    for n in nodes:
        if n.data == "assign":
            var = n.children[0].data.split(" ")[1]
            sTreeR = n.children[1]
            if symbols[var] == "float":
                if "inum" in sTreeR.data:
                    val = sTreeR.data
                    sTreeR.data = "int2float"
                    sTreeR.insertData(val)
                elif "id" in sTreeR.data:
                    if symbols[sTreeR.data.spli(" ")[1]] == "integer":
                        val = sTreeR.data
                        sTreeR.data = "int2float"
                        sTreeR.insertData(val)
                elif "plus" in sTreeR.data or "minus" in sTreeR.data:
                    checkFloat(sTreeR)
            else:
                if "fnum" in sTreeR.data:
                    return True
                elif "id" in sTreeR.data:
                    if symbols[sTreeR.data.spli(" ")[1]] == "float":
                        return True
                elif "plus" in sTreeR.data or "minus" in sTreeR.data:
                    error = checkInt(sTreeR)
                    if error:
                        return True

    return False

def intermCodeGenerator(error):
    file = open("output.txt","w")
    auxs = 1
    if error:
        file.write("Error")
        file.close()
        return "error"
    else:
        for n in pTree.children:
            if "intdcl" in n.data:
                file.write("DeclareInt "+str(n.data.split(" ")[1])+"\n")
            elif "floatdcl" in n.data:
                file.write("DeclareFloat "+str(n.data.split(" ")[1])+"\n")
            elif "print" in n.data:
                file.write("Print "+str(n.data.split(" ")[1])+"\n")
            elif n.data == "assign":
                inst = ""
                inst+=n.children[0].data.split(" ")[1]
                if n.children[1].data == "int2float":
                    file.write("R"+str(auxs)+" = int2float "+str(n.children[1].children[0].data)+"\n")
                    file.write(inst+" = R"+str(auxs)+"\n")
                    auxs+=1
                elif n.children[1].data == "plus" or n.children[1].data == "minus":
                    values = []
                    operations = []
                    n.genLists(n,values,operations)
                    operations.reverse()
                    i=1
                    values.append("end")
                    while values[i] != "end":
                        if values[i] == "int2float":
                            file.write("R"+str(auxs)+" = int2float "+values[i-1].split(" ")[1]+"\n")
                            values[i-1] = "R"+str(auxs)
                            values.pop(i)
                            auxs+=1
                        else:
                            i+=1
                    values.pop()
                    if operations[1]=="plus":
                        file.write("R"+str(auxs)+" = ")
                        if "R" in values[1]:
                            file.write(values[1]+" + ")
                        else:
                            file.write(values[1].split(" ")[1]+" + ")
                        if "R" in values[2]:
                            file.write(values[2]+"\n")
                        else:
                            file.write(values[2].split(" ")[1]+"\n")
                        auxs+=1
                    else:
                        file.write("R"+str(auxs)+" = ")
                        if "R" in values[1]:
                            file.write(values[1]+" - ")
                        else:
                            file.write(values[1].split(" ")[1]+" - ")
                        if "R" in values[2]:
                            file.write(values[2]+"\n")
                        else:
                            file.write(values[2].split(" ")[1]+"\n")
                        auxs+=1
                    i=2
                    while i<len(operations):
                        if operations[i]=="plus":
                            if "R" in values[i+1]:
                                file.write("R"+str(auxs)+" = R"+str(auxs-1)+" + "+values[i+1]+"\n")
                            else:
                                file.write("R"+str(auxs)+" = R"+str(auxs-1)+" + "+values[i+1].split(" ")[1]+"\n")
                        else:
                            if "R" in values[i+1]:
                                file.write("R"+str(auxs)+" = R"+str(auxs-1)+" - "+values[i+1]+"\n")
                            else:
                                file.write("R"+str(auxs)+" = R"+str(auxs-1)+" - "+values[i+1].split(" ")[1]+"\n")
                        auxs+=1
                        i+=1
                    file.write(values[0].split(" ")[1]+" = R"+str(auxs-1)+"\n")
                else:
                    file.write(inst+" = "+n.children[1].data.split(" ")[1]+"\n")
        file.close()
        return 0

print("Enter the file to analyze:")
name = input()
scanner(name)
parser()
casterror=typeChecker()
intermCodeGenerator(casterror)
print("Finish. Generated output.txt")
