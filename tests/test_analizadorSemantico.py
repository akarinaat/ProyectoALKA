import pytest

from analizadorSemanticoALKA import AnalizadorSemantico

def test_analisis_decvar():
    programa = """var int : num, b ;
						  
						 main(){}"""

    analizador = AnalizadorSemantico(programa)

    analizador.analizarArbol()
