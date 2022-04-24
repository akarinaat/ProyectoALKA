En esta primera fase, lo que se entrega es el analizador sintáctico del lenguaje ALKA.

Este incluye las gramáticas del lenguaje para poder analizar las entradas y saber si son válidas de acuerdo a las reglas del lenguaje.

Este parser también incluye (por default) un analizador léxico y es lo que se utiliza para la tokenización del input.

Ejemplo:

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

Fecha de entrega: Abril 13 2022


En esta segunda fase se entrega lo siguiente:

Un analizador semántico que contiene:

 - El directorio de variables
 - El directorio de funciones
 - El cubo semántico

 Se analizan las reglas decvars, decfuncs, decvar, decfunc, estatutos, estatuto, exp, expresion, término, factor y átomo.

 También agregué pruebas para comprobar la funcionalidad del analizador.

Ejemplo de una prueba:

def test_variable_no_declarada():
    programa = """
        func int foo (a int) {

            (b)+2+3-2+1;
        }
        main(){}"""

    analizador = AnalizadorSemantico(programa)

    with pytest.raises(SemanticError):
        analizador.analizarArbol()

 Fecha de entrega: Abril 24 del 2022