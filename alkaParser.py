from lark import Lark
from dataclasses import dataclass
from lark import Lark, ast_utils, Transformer, v_args
from lark.tree import Meta
from typing import List
import sys


this_module = sys.modules[__name__]
#


class _Ast(ast_utils.Ast):
    # This will be skipped by create_transformer(), because it starts with an underscore
    pass


class ToAst(Transformer):
    # Define extra transformation functions, for rules that don't correspond to an AST class.
    # def ID(self, s):
    #     return s
    # def STRING(self, s):
    #     # Remove quotation marks
    #     return s[1:-1]

    # # def DEC_NUMBER(self, n):
    # #     return int(n)

    # @v_args(inline=True)
    # def start(self, x):
    #     return x
    pass


@dataclass
class ID(_Ast):
    id: str


@dataclass
class Decvar(_Ast):
    tipo: str
    ids: List[ID]


@dataclass
class Decvars(_Ast, ast_utils.AsList):
    declaraciones: List[Decvar]


@dataclass
class Estatutos(_Ast):
    pass
#


@dataclass
class Decfunc(_Ast):
    pass
# FUNC tipo id  LPAREN (id tipo (COMMA id tipo)*)? RPAREN RETURNS tipo LCURLYBRACKET  decvars estatutos RCURLYBRACKET


@dataclass
class Decfuncs(_Ast, ast_utils.AsList):
    decfuncs: List[Decfunc]


@dataclass
class Main(_Ast):
    decvars: Decvars
    estatutos: Estatutos
# MAIN "(" ")" "{" decvars estatutos "}"


@dataclass
class Programa(_Ast):
    declaracion_variables: Decvars
    declaracion_funciones: Decfuncs
    main: Main


@dataclass
class Asignacion(_Ast):
    pass
# llamadavariable ASSIGN expresion


@dataclass
class Forloop(_Ast):
    pass


@dataclass
class While(_Ast):
    pass


@dataclass
class If(_Ast):
    pass


@dataclass
class Else(_Ast):
    pass


@dataclass
class Estatuto(_Ast):
    pass

# (asignacion | llamadafuncion | expresion | if | while | forloop) SEMICOLON


@dataclass
class Expresion(_Ast):
    pass


@dataclass
class Exp(_Ast):
    pass


@dataclass
class Termino(_Ast):
    pass


@dataclass
class Factor(_Ast):
    pass


@dataclass
class Atomo(_Ast):
    pass


@dataclass
class Llamadafuncion(_Ast):
    pass


@dataclass
class Llamadavariable(_Ast):
    pass


@dataclass
class Tipo(_Ast):
    pass


@dataclass
class Read(_Ast):
    pass


@dataclass
class Write(_Ast):
    pass


@dataclass
class Funcionesespeciales(_Ast):
    pass


ALKA_parser = Lark(


    r'''
    %import common.WS
    %ignore WS

    ID : /[a-zA-Z_][a-zA-Z_0-9]*/
    SEMICOLON : ";"
    COMMA : ","
    ASSIGN : "="
    LCURLYBRACKET : "{"
    RCURLYBRACKET : "}"
    LT : "<"
    GT : ">"
    NOTEQ : "<>"
    PLUS : "+"
    MINUS : "-"
    TIMES : "*"
    DIVIDE : "/"
    LPAREN : "("
    RPAREN : ")"
    LBRACE : "["
    RBRACE : "]"
    CTEI :  /[0-9]+/
    CTEF : /[0-9]+\.[0-9]+/
    CTESTR : /\"([^\\\n]|(\\.))*?\"/
    COLON : ":"
    VAR : "var"
    IF : "if"
    FLOAT : "float"
    INT : "int"
    PRINT : "print"
    ELSE : "else"
    TO : "to"
    WHILE : "while"
    STRING : "string"
    BOOL : "bool"
    READ : "read"
    HIST : "hist"
    MODE : "mode"
    WRITE : "write"
    MEAN : "mean"
    AVG : "avg"
    VARIANCE : "variance"
    RETURNS : "returns"
    FUNC : "func"
    FOR : "for"
    MAIN : "main"

    id : ID

    
    programa : decvars decfuncs main

    main : MAIN "(" ")" "{" decvars estatutos "}"

    decvars : decvar*

    decvar:  VAR tipo ":" id ("," id)* ";"

    decfuncs : decfunc*

    decfunc : FUNC tipo id  "(" (id tipo (COMMA id tipo)*)? ")) RETURNS tipo "{" decvars estatutos "}"

    asignacion : llamadavariable "=" expresion

    forloop : FOR id "=" expresion TO expresion "{" estatutos "}"

    while : WHILE "(" expresion ")" "{" estatutos "}"

    if : IF "(" expresion ")" "{" estatutos "}" else

    else : (ELSE "{" estatutos "}")?

    estatutos : estatuto*

    estatuto : (asignacion | llamadafuncion | expresion | if | while | forloop) ";" 

    expresion : exp ((">" | "<" | "!=" | "==" ) exp )?

    exp : termino (("+" | "-" ) termino )*

    termino : factor (("*" | "/") factor )*

    factor : "(" expresion ")" | ("+" | "-")? atomo

    atomo : id | CTEF | CTEI | CTESTR | llamadafuncion | funcionesespeciales

    llamadafuncion :  id "(" (expresion  ("," expresion)*)? ")"

    llamadavariable : id ("[" expresion "]" )*

    tipo : INT | STRING | FLOAT | BOOL

    read : READ "(" llamadavariable ")"

    write : WRITE "(" expresion ( "," expresion )* ")"

    funcionesespeciales : READ | WRITE | HIST | MEAN | MODE | AVG | VARIANCE


    ''',
    start='programa'
)


transformer = ast_utils.create_transformer(this_module, ToAst())


def parse(text):
    tree = ALKA_parser.parse(text)
    return transformer.transform(tree)
