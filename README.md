## Primera entrega

Lo que se entrega es el analizador sintáctico del lenguaje ALKA.

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


## Segunda entrega:

Un analizador semántico que contiene:

 - El directorio de variables
 - El directorio de funciones
 - El cubo semántico

 Análisis semántico de:
 * decvars
 * decfuncs 
 * decvar
 * decfunc
 * estatutos
 * estatuto
 * exp
 * expresion
 * termino
 * factor

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

## Tercera entrega:

 - Generación de cuadruplos
 - Generación de cuadruplos main
 - Generación cuadruplos expresion
 - Generación cuadruplos estatutos en progreso
 - Agregué variables multidimiensionales : a[][]
 - Análisis semántico de atomo

 Falta la generación de cuadruplos estatutos:
 - asignacion, llamadafuncion, if, while, forloop, return
 Faltan atomos especiales como:
 - funciones especiales, llamadafuncion, llamadavariable

 Fecha de entrega: Mayo 1 del 2022

 ## Cuarta entrega
 En el archivo de Analizador Semántico:

- Agregué en enumerador tipo para tener mejor organizados los tipos
- Agregué análisis semántico de asignación
- Mejoré el análisis semántico de llamadavariable
- Agregué análisis de if

En el archivo de Cuádruplos

- Agregué tipos a algunas variables
- Mejoré cuádruplos de llamadavariable
- Empecé a generar cuádruplos de asignación
- Agregué comentarios
En el archivo de pruebas de analizador semántico

- Actualicé las pruebas al nuevo sistema de tipos

En el archivo de prueba de cuádruplos

- Agregué una prueba


- Analicé while y else
- Le cambie el id del for asignación	(porque era lo mismo) REFACTORING

Con mypy:

Pip install mypy
Mypy 

- Generation cuadruplos while
- Generation cuádruplos if y else

- Terminé análisis del for
- Terminé cuádruplos del for
- Arreglé análisis y cuádruplos de llamada variable (que regresara la variable que se le asignó)

Fecha de entrega Mayo 8 2022

## Quinta entrega:

- Se cambió la gramática de decfuncs, hice un arbol parametros 
- Generación de cuádruplos de decfuncs (no al 100% todavía, pero sí los genera)
- Agregé pruebas de generar cuadruplos decfunc
- Agregué prueba de generar cuadruplo llamada función
- Análisis de llamadafuncion
- Generación cuadruplos llamadafuncion
- Generé .png para tener una referencia visual
- Falta la parte de ERA pero lo veo en Maquina Virtual

Fecha de entrega: Mayo 16 2022

## Sexta entrega

- Cambié nombres de funciones por direcciones
- Arreglé análisis semántico para estatuto return dentro funciones y estatutos de control
- Generé cuádruplos return
- Generé cuadruplo ERA (no al 100% pero si lo genera)
- Arreglé el stack en generación de código (le agregué stack de variables locales para el main)
- Cambié gramatica de decvar, le quite llamada variable y agregué iddecvar que tiene una CTEI en vez de expresion
- Arreglé direcciones virtuales globales
- Ya puedo pedir memoria de arreglos
- **Mapa de memoria en ejecución ya funciona**

Falta: Ejecución de Expresiones y Estatutos Secuenciales.
       Temporales

Fecha de entrega: Mayo 24 2022





