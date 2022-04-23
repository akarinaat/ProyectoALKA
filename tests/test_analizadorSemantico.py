import pytest

from analizadorSemanticoALKA import AnalizadorSemantico


def test_analisis_decvar():
    programa = """var int : num, b ;
						  
						 main(){}"""

    analizador = AnalizadorSemantico(programa)
    analizador.analizarArbol()

    assert "num" in analizador.directorioVariables
    print(analizador.directorioVariables["num"])
    assert analizador.directorioVariables["num"].tipo == "int"
    assert "b" in analizador.directorioVariables
    assert analizador.directorioVariables["b"].tipo == "int"


def test_analisis_decfunc():
    programa = """func int foo () {}
        main(){}"""

    analizador = AnalizadorSemantico(programa)

    analizador.analizarArbol()

    assert "foo" in analizador.directorioFunciones
    assert analizador.directorioFunciones["foo"].tipo == "int"
