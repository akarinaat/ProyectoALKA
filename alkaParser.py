from lark import Lark

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

    
    programa : decvars decfuncs main

    main : MAIN "(" ")" "{" decvars estatutos "}"

    decvars : (decvar)*

    decvar:  VAR tipo COLON ID (COMMA ID)* SEMICOLON

    decfuncs : (decfunc)*

    decfunc : FUNC tipo ID  LPAREN (ID tipo (COMMA ID tipo)*)? RPAREN RETURNS tipo LCURLYBRACKET  decvars estatutos RCURLYBRACKET

    asignacion : llamadavariable ASSIGN expresion

    forloop : FOR ID ASSIGN expresion TO expresion LCURLYBRACKET estatutos "}"

    while : WHILE "(" expresion ")" "{" estatutos "}"

    if : IF "(" expresion ")" "{" estatutos "}" else

    else : (ELSE "{" estatutos "}")?

    estatutos : (estatuto)*

    estatuto : (asignacion | llamadafuncion | expresion | if | while | forloop) SEMICOLON 

    expresion : exp ((">" | "<" | "!=" ) exp )?

    exp : termino (("+" | "-" ) termino )*

    termino : factor (("*" | "/") factor )*

    factor : "(" expresion ")" | ("+" | "-")? atomo

    atomo : ID | CTEF | CTEI | CTESTR | llamadafuncion | funcionesespeciales

    llamadafuncion :  ID "(" (expresion  ("," expresion)*)? ")"

    llamadavariable : ID ("[" expresion "]" )*

    tipo : INT | STRING | FLOAT | BOOL

    read : READ "(" llamadavariable ")"

    write : WRITE "(" expresion ( COMMA expresion )* ")"

    funcionesespeciales : READ | WRITE | HIST | MEAN | MODE | AVG | VARIANCE


    ''',
    start='programa'
)
