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
        """ func int foo () {}
        main(){}""")  # Creo que está mal y el returns va dentro de los brackets --> faltan los parametros y los parámetros


def test_asignacion():

    ALKA_parser.parse(""" var int: a;
                          main(){
                              a = 3;
                          } """)


def test_forloop():
    ALKA_parser.parse(""" main(){
        for a = i to (a < b) {
        boo = t;
    };
    }""")


def test_while():
    ALKA_parser.parse(""" main() {
        while( a == b){
            a = 3;
        };
    } """)


def test_if():
    ALKA_parser.parse(""" main(){
        if(a<b){
            a=6;
        };
    } """)


def test_else():
    ALKA_parser.parse("""
    main(){
        if(a){
            a = 3;
        }
        else{

        };
    }
    """)


def test_exp():
    ALKA_parser.parse("""main(){ a + b;} """)


def test_llamada_funcion():
    ALKA_parser.parse(""" main(){
        read(a);
        write(a);
        hist(a);
        }
    """)
