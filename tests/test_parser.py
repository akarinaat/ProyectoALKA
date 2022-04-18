import pytest
from alkaparser import ALKA_parser


def test_main():
    ALKA_parser.parse("main(){}")


def test_declaracion_variables():
    ALKA_parser.parse("""var int : num ;
                         var float : a, b;   
                         main(){} """)


def test_declaracion_funciones():
    ALKA_parser.parse(
        """ func int foo () returns int {}
        main(){}""")  # Creo que está mal y el returns va dentro de los brackets --> faltan los parametros y los parámetros


# def test_asigmacion():
#     ALKA_parser.parse("""  """)
# print(
#     ALKA_parser.parse(""" var int: a
#                           main(){} """).pretty()
# )

def test_forloop():
    ALKA_parser.parse(""" main(){
        for a = i to (a < b) {
        boo = t;
    };
    }""")
