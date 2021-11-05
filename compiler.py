import ply.yacc as yacc
import ply.lex as lex



literals = ['=', '+', '-', '*', '/', '(', ')','"', ';']
reserved = { 
    'int' : 'INTDEC',
    'float' : 'FLOATDEC',
    'print' : 'PRINT',
    'boolean' : 'BOOLDEC',
    'string' : 'STRINGDEC'
 }

tokens = [
    'INUMBER', 'FNUMBER', 'NAME', 'STRING', 'BOOLEAN'
] + list(reserved.values())


# Tokens

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

def t_BOOLEAN(t):
    r'false | true'

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
abstractTree = []

class Node:
    childrens=[]
    val=''
    type=''
    def __init__(self, val, type, childrens=[]):
        self.val=val
        self.type=type
        self.childrens=childrens

def p_statement_declare_int(p):
    '''statement : INTDEC NAME is_assing ';'
    '''
    if type(p[3])==float:
        print("no se puede asignar flotantes a enteros")
    else:
        names[p[2]] = { "type": "INT", "value":p[3].val}
        varname = Node(p[2],'INT',[])
        n = Node(p[3],'=', [varname, p[3]])
        abstractTree.append(n)
        #names[p[2]] = { "type": "INT", "value":p[3]}

def p_statement_declare_float(p):
    '''statement : FLOATDEC NAME is_assing ';' '''
    names[p[2]] = { "type": "FLOAT", "value":p[3].val}
    varname = Node(p[2],'FLOAT',[])
    n = Node(p[3],'=', [varname, p[3]])
    abstractTree.append(n)
    #print(p)

def p_is_assing(p):
    '''is_assing : "=" expression 
                | '''
    #p[0] = 0
    p[0] = Node(0, 'INT',[])
    if len(p)>2:
        p[0].type = p[2].type
        p[0].val = p[2].val
        p[0].childrens = [p[2]]
        #p[0] = p[2]

def p_statement_declare_string(p):
    '''statement : STRINGDEC NAME is_assign_s ';' '''
    names[p[2]] = { "type": "STRING", "value":p[3].val}
    varname = Node(p[2],'STRING',[])
    n = Node(p[3],'=', [varname, p[3]])
    abstractTree.append(n)

def p_is_assing_s(p):
    '''is_assign_s : "=" expression_s
                    | '''
    p[0] = Node("", 'STRING')
    if len(p)>2:
        p[0].type = p[2].type
        p[0].val = p[2].val
        p[0].childrens = [p[2]]

def p_statement_print(p):
    '''statement : PRINT '(' expression ')' ';' '''
    n = Node(p[3],'PRINT', [p[3]])
    abstractTree.append(n)
    print(p[3].val)

def p_statement_assign(p):
    'statement : NAME "=" expression'
    if p[1] not in names:
        print ( "You must declare a variable before using it")
    names[p[1]]["value"] = p[3]


def p_statement_expr(p):
    '''statement : expression
                  | expression_s'''
    # print(p[1])


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


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = Node(-p[2].val,p[2].type,p[2].childrens)
    #p[0] = -p[2]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = Node(p[2].val,p[2].type,p[2].children)


def p_expression_inumber(p):
    "expression : INUMBER"
    #p[0] = p[1]
    p[0] = Node(p[1], 'INT')


def p_expression_fnumber(p):
    "expression : FNUMBER"
    #p[0] = p[1]
    p[0] = Node(p[1], 'FLOAT')


def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]["value"]
        p[0] = Node(p[1],"ID")
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0

def p_expression_s_multiple(p):
    '''expression_s : expression_s '+' expression_s'''
    p[0] = Node('+','CONCATENACION',[p[1],p[3]])

def p_expression_s_string(p):
    'expression_s : STRING'
    p[0] = Node(p[1],'STRING')

def p_expression_s_name(p):
    "expression_s : NAME"
    try:
        p[0] = names[p[1]]["value"]
        p[0] = Node(p[1],"ID")
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
    line = file.readline()
    while(line):
        yacc.parse(line)
        line=file.readline()