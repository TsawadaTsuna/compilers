import re
import ply.yacc as yacc
import ply.lex as lex

literals = ['=', '+', '-', '*', '/', '(', ')','"', ';','<','>','{','}','!']
reserved = { 
    'int' : 'INTDEC',
    'float' : 'FLOATDEC',
    'print' : 'PRINT',
    'boolean' : 'BOOLDEC',
    'string' : 'STRINGDEC',
    'and' : 'AND',
    'or' : 'OR',
    'if' : 'IF',
    'elif' : 'ELIF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR'
 }

tokens = [
    'INUMBER', 'FNUMBER', 'NAME', 'STRING', 'BOOLEAN'
] + list(reserved.values())


# Tokens

def t_BOOLEAN(t):
    r'false | true'

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

def t_FNUMBER(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'".*"'
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# dictionary of names
names = {}
nodes=[]

class Node:
    childrens=[]
    val=''
    type=''
    def __init__(self, val, type, childrens=[]):
        self.val=val
        self.type=type
        self.childrens=childrens

    def __str__(self):
        return "val: " +str(self.val)+" type: "+str(self.type)
    
    def printTree(self, node, lv):
        if lv<4:
            print(" "*lv + str(node))
        #print(lv)
        l = node.childrens.copy()
        if l:
            for n in l:
                self.printTree(n,lv+1)
    
    def addToList(self, node, lv, lis):
        if lv<10:
            print(" "*lv + str(node.val))
            lis.append(str(lv) +": "+node.val)
        #print(lv)
        l = node.childrens.copy()
        for n in l:
            self.addToList(n,lv+1,lis)

abstractTree = Node("inicio","inicio")

def p_statement(p):
    'statement : state states'
    abstractTree.childrens.append(p[1])

def p_statement_declare_int(p):
    '''stmt : INTDEC NAME is_assing ';'
    '''
    if type(p[3])==float:
        print("no se puede asignar flotantes a enteros")
    else:
        names[p[2]] = { "type": "INT", "value":p[3].val}
        varname = Node(p[2],'INT')
        n = Node('assign','=', [varname, p[3]])
        #abstractTree.childrens.append(n)
        p[0]=n
        #print(n)
        #print("int assign")
        #names[p[2]] = { "type": "INT", "value":p[3]}

def p_statement_declare_float(p):
    '''stmt : FLOATDEC NAME is_assing ';' '''
    names[p[2]] = { "type": "FLOAT", "value":p[3].val}
    varname = Node(p[2],'FLOAT')
    #print(varname)
    n = Node('assign','=', [varname, p[3]])
    #abstractTree.childrens.append(n)
    p[0]=n
    #print(n)
    #print("float assign")
    #print(p)

def p_is_assing(p):
    '''is_assing : "=" expression 
                | '''
    #p[0] = 0
    p[0] = Node(0, 'INT')
    if len(p)>2:
        p[0].type = p[2].type
        p[0].val = p[2].val
        p[0].childrens = p[2].childrens
        #p[0] = p[2]
    #print(p[0])

def p_statement_declare_string(p):
    '''stmt : STRINGDEC NAME is_assign_s ';' '''
    names[p[2]] = { "type": "STRING", "value":p[3].val}
    varname = Node(p[2],'STRING')
    n = Node('assign','=', [varname, p[3]])
    #abstractTree.childrens.append(n)
    p[0]=n
    #print(n)
    #print("string assign")

def p_is_assing_s(p):
    '''is_assign_s : "=" expression_s
                    | '''
    p[0] = Node("", 'STRING')
    if len(p)>2:
        p[0].type = p[2].type
        p[0].val = p[2].val
        p[0].childrens = [p[2]]
    #print(p[0])

def p_statement_declare_boolean(p):
    '''stmt : BOOLDEC NAME is_assign_b ';' '''
    names[p[2]] = { "type": "BOOLEAN", "value":p[3].val}
    varname = Node(p[2],'BOOLEAN')
    n = Node('assign','=', [varname, p[3]])
    #abstractTree.childrens.append(n)
    p[0]=n
    #print(n)
    #print("boolean assign")

def p_is_assing_b(p):
    '''is_assign_b : "=" expression_b
                    | "=" num
                    | '''
    p[0] = Node("false", 'BOOLEAN')
    if len(p)>2:
        p[0].type = p[2].type
        p[0].val = p[2].val
        p[0].childrens = [p[2]]
    #print(p[0])

def p_statement_print(p):
    '''stmt : PRINT '(' expression ')' ';' '''
    n = Node('PRINT','PRINT', [p[3]])
    #abstractTree.childrens.append(n)
    p[0]=n
    #print(n)
    #print("print finish")
    #print(p[3].val)

def p_statement_printstring(p):
    '''stmt : PRINT '(' expression_s ')' ';' '''
    n = Node('PRINT','PRINT', [p[3]])
    #abstractTree.childrens.append(n)
    p[0]=n
    #print(n)
    #print("print finish")
    #print(p[3].val)

def p_statement_printbool(p):
    '''stmt : PRINT '(' expression_b ')' ';' '''
    n = Node('PRINT','PRINT', [p[3]])
    #abstractTree.childrens.append(n)
    p[0]=n
    #print(n)
    #print("print finish")
    #print(p[3].val)

def p_statement_assign(p):
    '''stmt : NAME "=" expression ';' '''
    if p[1] not in names:
        print ( "You must declare a variable before using it")
    names[p[1]]["value"] = p[3]
    if names[p[1]]["type"] != "FLOAT" or names[p[1]]["type"]!="INT":
        id = Node(p[1],'ID')
        n = Node('=','ASSIGN',[id,p[3]])
        #abstractTree.childrens.append(n)
        p[0]=n
        #print(n)
        #print("number assign")
    else:
        print("type missmatch")

def p_statement_assign_string(p):
    '''stmt : NAME "=" expression_s ';' '''
    if p[1] not in names:
        print ( "You must declare a variable before using it")
    names[p[1]]["value"] = p[3]
    if names[p[1]]["type"] != "STRING":
        id = Node(p[1],'ID')
        n = Node('=','ASSIGN',[id,p[3]])
        #abstractTree.childrens.append(n)
        p[0]=n
        #print(n)
        #print("string assign")
    else:
        print("type missmatch")

def p_statement_assign_boolean(p):
    '''stmt : NAME "=" expression_b ';' '''
    if p[1] not in names:
        print ( "You must declare a variable before using it")
    names[p[1]]["value"] = p[3]
    if names[p[1]]["type"]!="BOOLEAN":
        id = Node(p[1],names[p[1]]["type"])
        n = Node('=','ASSIGN',[id,p[3]])
        #abstractTree.childrens.append(n)
        p[0]=n
        #print(n)
        #print("boolean assign")
    else:
        print("type missmatch")

def p_statement_expr(p):
    '''stmt : expression ';'
                  | expression_s ';' 
                  | expression_b ';' '''
    #abstractTree.childrens.append(p[1])
    p[0]=p[1]
    #print(p[1])

def p_statement_if(p):
    '''stmt : IF "(" expression_b ")" "{" state states "}" elif else'''
    ifblock = Node("bloque","if",[p[6],p[7]])
    n = Node("if","IF",[p[3],ifblock,p[9],p[10]])
    #abstractTree.childrens.append(n)
    #print(ifblock)
    p[0]=n
    #print(n)
    #print("IF-ELIF-ELSE block")

def p_elif(p):
    '''elif : ELIF "(" expression_b ")" "{" state states "}"
            | '''
    elifbck = Node("bloque","elif",[p[6],p[7]])
    n = Node("elif","ELIF",[p[3],elifbck])
    p[0]=n
    #print(elifbck)
    #print(n)

def p_else(p):
    '''else : ELSE "{" state states "}"
            | '''
    elsebck=Node("bloque","else",[p[3],p[4]])
    n=Node("else","ELSE",[elsebck])
    p[0]=n
    #print(elsebck)
    #print(n)

def p_while(p):
    '''stmt : WHILE "(" expression_b ")" "{" state states "}" '''
    whilebck = Node("bloque","while",[p[6],p[7]])
    n=Node("while","WHILE",[p[3],whilebck])
    p[0]=n
    #print(whilebck)
    #print(n)
    #print("WHILE block")

def p_for(p):
    '''stmt : FOR "(" NAME "=" num ";" expression_b ";" step ")" "{" state states "}" '''
    try:
        if names[p[3]]["type"] == "INT"  or names[p[3]]["type"] == "FLOAT":
            forbck = Node("bloque","for",[p[12],p[13]])
            assign = Node("assign","=",[p[3],p[5]])
            n=Node("for","FOR",[assign,p[7],p[9],forbck])
            #print(assign)
            #print(forbck)
            #print(n)
            p[0]=n
            #print("FOR block")
        else:
            print("missmatch types")
    except:
        print("Undefined name '%s'" % p[3])


def p_step(p):
    '''step : NAME "+" "=" num
            | NAME "-" "=" num
            | NAME "*" "=" num
            | NAME "/" "=" num
            | NAME "+" "+"
            | NAME "-" "-" '''
    if len(p)==4:
        if p[2] == '+':
            p[0] = Node("+","step",[p[1],Node("1","INT")])
        else:
            p[0] = Node("-","step",[p[1],Node("1","INT")])
    else:
        if p[2] == '+':
            p[0]=Node("+","step",[p[1],p[4]])
        elif p[2] == '-':
            p[0]=Node("-","step",[p[1],p[4]])
        elif p[2] == '*':
            p[0]=Node("*","step",[p[1],p[4]])
        elif p[2] == '/':
            p[0]=Node("/","step",[p[1],p[4]])
    #print(p[0])

def p_state(p):
    '''state : stmt state
            | '''
    if len(p) >2:
        if not p[1]==None: 
            p[0]=Node(p[1].val,p[1].type,p[1].childrens.append(p[2]))
    #print(p[0])

def p_states(p):
    '''states : state
                | '''
    p[0]=p[1]
    #print(p[0])

def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '^' expression'''
    if p[2] == '+':
        p[0] = Node('+','OPERATION',[p[1],p[3]])
        #p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = Node('-','OPERATION',[p[1],p[3]])
        #p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = Node('*','OPERATION',[p[1],p[3]])
        #p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = Node('/','OPERATION',[p[1],p[3]])
        #p[0] = p[1] / p[3]
    elif p[2] == '^':
        p[0] = Node('^','OPERATION',[p[1],p[3]])
        #p[0] = p[1] ** p[3]
    #print(p[0])


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = Node(-p[2].val,p[2].type,p[2].childrens)
    #print(p[0])
    #p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]
    #print(p[0])


def p_expression_inumber(p):
    "expression : INUMBER"
    #p[0] = p[1]
    p[0] = Node(p[1], 'INT')
    #print(p[0])


def p_expression_fnumber(p):
    "expression : FNUMBER"
    #p[0] = p[1]
    p[0] = Node(p[1], 'FLOAT')
    #print(p[0])


def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]["value"]
        p[0] = Node(p[1],"ID")
        #print(p[0])
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_expression_b_multiple(p):
    '''expression_b : expression_b AND expression_b
                    | expression_b OR expression_b'''
    if p[2] == 'and':
        p[0] = Node('and','OPERATION',[p[1],p[3]])
        #p[0] = p[1] + p[3]
    elif p[2] == 'or':
        p[0] = Node('or','OPERATION',[p[1],p[3]])
        #p[0] = p[1] - p[3]
    #print(p[0])

def p_expression_b_bool(p):
    '''expression_b : BOOLEAN'''
    p[0] = Node(p[1],'BOOLEAN')
    #print(p[0])

def p_expression_b_boolnum(p):
    '''expression_b : num'''
    p[0]=p[1]

def p_expression_b_boolcompnums(p):
    '''expression_b : num "<" num
                    | num ">" num
                    | num "=" "=" num
                    | num "!" "=" num
                    | num "<" "=" num
                    | num ">" "=" num '''
    if p[2] == '<':
        if p[3] == '=':
            p[0] = Node('<=','OPERATION',[p[1],p[4]])
        else:
            p[0] = Node('<','OPERATION',[p[1],p[3]])
        #p[0] = p[1] + p[3]
    elif p[2] == '>':
        if p[3] == '=':
            p[0] = Node('>=','OPERATION',[p[1],p[4]])
        else:
            p[0] = Node('>','OPERATION',[p[1],p[3]])
        #p[0] = p[1] - p[3]
    elif p[2] == '=':
        p[0] = Node('==','OPERATION',[p[1],p[4]])
        #p[0] = p[1] * p[3]
    elif p[2] == '!':
        p[0] = Node('!=','OPERATION',[p[1],p[4]])
        #p[0] = p[1] / p[3]
    
    #print(p[0])
    
def p_numint(p):
    '''num : INUMBER'''
    p[0] = Node(p[1],'INT')
    #print(p[0])

def p_numfloat(p):
    '''num : FNUMBER'''
    p[0] = Node(p[1],'FLOAT')
    #print(p[0])

def p_numname(p):
    '''num : NAME'''
    try:
        p[0] = Node(p[1],"ID")
    except:
        print("Undefined name '%s'" % p[1])
    #print(p[0])

def p_expression_b_name(p):
    '''expression_b : NAME'''
    try:
        p[0] = names[p[1]]["value"]
        p[0] = Node(p[1],"ID")
        #print(p[0])
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_expression_s_multiple(p):
    '''expression_s : expression_s '+' expression_s
                    | expression_s '+' expression
                    | expression_s '+' expression_b
                    | expression '+' expression_s
                    | expression_b '+' expression_s '''
    p[0] = Node('+','CONCATENACION',[p[1],p[3]])
    #print(p[0])

def p_expression_s_string(p):
    'expression_s : STRING'
    p[0] = Node(p[1],'STRING')
    #print(p[0])

def p_expression_s_name(p):
    "expression_s : NAME"
    try:
        p[0] = names[p[1]]["value"]
        p[0] = Node(p[1],"ID")
        #print(p[0])
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_error(p):
    if p:
        print(p)
        print("Syntax error at line '%s' character '%s'" % (p.lineno, p.lexpos) )
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

def parsefile(inputfile):
    try:
        #s = input('Nombre de archivo:\n ')
        file = open(inputfile,"r")
    except EOFError:
        return False
    if not inputfile:
        return False
    source = ""
    line = file.readline()
    while(line):
        source=source+line
        line=file.readline()
    try:
        yacc.parse(source)
        return True
    except:
        return False
#print(parsefile("code.txt"))
#print("end")
'''
i=0
while i<1:
    i=i+1
    try:
        s = input('Nombre de archivo:\n ')
        file = open(s,"r")
    except EOFError:
        break
    if not s:
        continue
    source = ""
    line = file.readline()
    while(line):
        source=source+line
        line=file.readline()
    yacc.parse(source)
    i=i+1
#abstractTree.printTree(abstractTree,0)
    #abstractTree.addToList(abstractTree,0,nodes)
    #print(nodes)
    '''
