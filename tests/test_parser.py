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
        """ func int foo () returns int {} """)  # Creo que está mal y el returns va dentro de los brackets --> faltan los parametros y los parámetros
