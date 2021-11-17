tokens = ['DIGIT']

literals = ['o']

# Tokens

def t_DIGIT(t): 
    r'\d'
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

def p_statement_octane(p):
    'statement : "o" octanes'
    print(p[2])

def p_statement_decimal(p):
    'statement : numbers'
    print(p[1])

def p_numbers(p):
    '''numbers : numbers number
                | number'''
    if len(p)>2:
        p[0] = int(p[1]) * 10 + int(p[2])
    else:
        p[0] = int(p[1])

def p_number(p):
    'number : DIGIT'
    p[0] = int(p[1])

def p_octanes(p):
    '''octanes : octanes octane
                | octane'''
    if len(p)>2:
        p[0] = int(p[1]) * 8 + int(p[2])
    else:
        p[0] = int(p[1])

def p_octane(p):
    'octane : DIGIT'
    val = int(p[1])
    if val >= 8:
        print("error non octane value")
        exit()
    else:
        p[0] = val

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
parser = yacc.yacc()


#num = input("Ingresa un numero:\n")
nums = ["123","o 123"]
for n in nums:
    yacc.parse(n)