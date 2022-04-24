import pytest

from analizadorSemanticoALKA import AnalizadorSemantico, SemanticError


def test_analisis_decvar():
    programa = """var int : num, b ;
						  
						 main(){}"""

    analizador = AnalizadorSemantico(programa)
    analizador.analizarArbol()
    print(analizador.directoriosVariables)
    assert analizador.directoriosVariables[0]["num"].tipo == "int"
    assert analizador.directoriosVariables[0]["b"].tipo == "int"


def test_analisis_decfunc():
    programa = """func int foo () {}
        main(){}"""

    analizador = AnalizadorSemantico(programa)

    analizador.analizarArbol()

    assert "foo" in analizador.directorioFunciones
    assert analizador.directorioFunciones["foo"].tipo == "int"


def test_analisis_decfunc_error():
    programa = """
        var int:a;
        func int foo (a int,b float) {
            var float: c;
        }
        main(){}"""

    analizador = AnalizadorSemantico(programa)

    with pytest.raises(SemanticError):
        analizador.analizarArbol()

    programa = """
        var int:a;
        func int foo () {
            var int:a;
        }
        main(){}"""

    analizador = AnalizadorSemantico(programa)

    with pytest.raises(SemanticError):
        analizador.analizarArbol()

    programa = """
        func int foo (a int) {
            var int:a;
        }
        main(){}"""

    analizador = AnalizadorSemantico(programa)

    with pytest.raises(SemanticError):
        analizador.analizarArbol()


def test_variable_no_declarada():
    programa = """
        func int foo (a int) {

            (b)+2+3-2+1;
        }
        main(){}"""

    analizador = AnalizadorSemantico(programa)

    with pytest.raises(SemanticError):
        analizador.analizarArbol()
