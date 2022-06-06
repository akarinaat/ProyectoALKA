from lark import Lark
from dataclasses import dataclass
from lark import Lark, ast_utils, Transformer, v_args
from lark.tree import Meta
from typing import List
import sys


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
    NOTEQ : "!="
    EQ: "=="
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
    CTEBOOL : "True" | "False"
    COLON : ":"
    VAR : "var"
    IF : "if"
    FLOAT : "float"
    INT : "int"
    ELSE : "else"
    TO : "to"
    WHILE : "while"
    STRING : "string"
    BOOL : "bool"
    VOID : "void"
    READ : "read"
    HIST : "hist"
    MODE : "mode"
    WRITE : "write"
    MEAN : "mean"
    VARIANCE : "variance"
    RETURNS : "returns"
    FUNC : "func"
    FOR : "for"
    MAIN : "main"
   
    COMMENT: "#" /[^\n]/*
    %ignore COMMENT 

    id : ID

    programa : decvars decfuncs main

    main : "main" "(" ")" "{" decvars estatutos "}"

    decvars : decvar*

    decvar:  "var" tipo ":" iddecvar ("," iddecvar)* ";"

    iddecvar: id ("[" CTEI "]" )*

    decfuncs : decfunc*

    decfunc : "func" tipo id  "(" parametros ")"  "{" decvars estatutos "}"

    parametros :  (parametro ("," parametro)*)?

    parametro : id tipo

    asignacion : llamadavariable "=" expresion

    forloop : "for" asignacion "to" expresion "{" estatutos "}"

    while : "while" "(" expresion ")" "{" estatutos "}"

    if : "if" "(" expresion ")" "{" estatutos "}" else

    else : ("else" "{" estatutos "}")?

    estatutos : estatuto*

    estatuto : (return| asignacion |  expresion | if | while | forloop  ) ";" 

    return : "return" expresion

    expresion : exp ((GT | LT | NOTEQ | EQ ) exp )?

    exp : termino ((PLUS | MINUS ) termino )*

    termino : factor (( TIMES | DIVIDE ) factor )*

    factor : "(" expresion ")" | (PLUS | MINUS)? atomo

    atomo : llamadavariable | CTEF | CTESTR | CTEI | CTEBOOL  | funcionesespeciales | llamadafuncion 

    llamadafuncion :  id "(" (expresion  ("," expresion)*)? ")"

    llamadavariable : id ("[" expresion "]" )*

    tipo : INT | STRING | FLOAT | BOOL | VOID

    read : "read" "(" llamadavariable "," CTESTR ")"

    write : "write" "(" expresion ( "," expresion )* ")"

    funcionesespeciales : read | write | hist | mean | mode |  variance

    hist : "hist" "(" llamadavariable ")"

    mean: "mean" "(" llamadavariable ")"

    mode: "mode" "(" llamadavariable  ")"

    variance: "variance" "(" llamadavariable ")"

    ''',
    start='programa'
)
