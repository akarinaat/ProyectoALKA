from alkaparser import ALKA_parser

from lark import tree

# decvars
# print(
#     ALKA_parser.parse("""var int : num ;
#                      var float : a, b;
#                      main(){} """).pretty())

# tree.pydot__tree_to_png(
#     ALKA_parser.parse("""var int : num ;
#                      var float : a, b;
#                      main(){} """), "test.png")

# decfunc
# print(
#     ALKA_parser.parse(""" func int foo (a int) returns int {


#     }
#       main(){} """).pretty()
# )

# asignacion
# print(
#     ALKA_parser.parse(""" var int: a
#                           main(){} """).pretty()
# )

# forloop
print(
    ALKA_parser.parse(""" 
    main(){
        for a = i to (a < b) {
        boo = t;
    };
    }""").pretty()
)


# todo
# Crear diccionario de variables
# Crear diccionario de funciones
# Crear funciones getter y setters
# Crear la clase de analizador semántico que va a contener los diccionarios

# TODO EXPRESION ESTÁ MAL
