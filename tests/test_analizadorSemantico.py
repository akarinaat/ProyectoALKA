import pytest

from analizadorSemanticoALKA import AnalizadorSemantico, SemanticError, Tipo


def test_analisis_decvar():
    programa = """var int : num , b ;
						  
						 main(){}"""

    analizador = AnalizadorSemantico(programa)
    analizador.analizarArbol()
    print(analizador.directoriosVariables)
    assert analizador.directoriosVariables[0]["num"].tipo == Tipo.Int
    assert analizador.directoriosVariables[0]["b"].tipo == Tipo.Int


def test_analisis_decvar_dimensiones():
    programa = """var int : num[2][3], b ;
						  
						 main(){}"""

    analizador = AnalizadorSemantico(programa)
    analizador.analizarArbol()
    print(analizador.directoriosVariables)
    assert analizador.directoriosVariables[0]["num"].tipo == Tipo.Int
    assert analizador.directoriosVariables[0]["b"].tipo == Tipo.Int


def test_analisis_decfunc():
    programa = """func int foo () {}
        main(){}"""

    analizador = AnalizadorSemantico(programa)

    analizador.analizarArbol()

    assert "foo" in analizador.directorioFunciones
    assert analizador.directorioFunciones["foo"].tipo == Tipo.Int


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


def test_variable_dimensiones_incorrectas():
    programa = """
        func int foo (a int) {

            var int: i[2][3];
            i[1][3][2];
        }
        main(){}"""

    analizador = AnalizadorSemantico(programa)

    with pytest.raises(SemanticError):
        analizador.analizarArbol()

def test_if():

    programa = """main(){
        var int: a,b;
        if(a>b){
            3+2;
        };
    } """

    analizador = AnalizadorSemantico(programa)

    analizador.analizarArbol()

def test_while():
    programa = """main(){
        var int: a,b;
        while(a<b){
            3+2;
        };
    }"""
    analizador = AnalizadorSemantico(programa)

    analizador.analizarArbol()

def test_else():
    programa = """main(){
        var int: a,b;
        if(a>b){
            2+3+4;
        }else{
            2+2;
        };
    }"""
    analizador = AnalizadorSemantico(programa)

    analizador.analizarArbol()

def test_return():
    programa = """main(){
        var int: a,b;
        if(a>b){
            2+3+4;
        }else{
            2+2;
        };
        return 5.3*3.2;
    }"""
    analizador = AnalizadorSemantico(programa)

    analizador.analizarArbol()

def test_for():
    programa = """main(){
        var int: i;
        for  i = 0 to  10{
            2+4;
        };
    }"""
    analizador = AnalizadorSemantico(programa)

    analizador.analizarArbol()

def test_for_error():
    programa = """main(){
        for  i = 0 to  10{
            2+4;
        };
    }"""
    analizador = AnalizadorSemantico(programa)
    with pytest.raises(SemanticError):
        analizador.analizarArbol()
        print(analizador.directoriosVariables)


def test_llamadafuncion_error():
    programa = """
    
    main(){
    foo();    
    }"""
    analizador = AnalizadorSemantico(programa)
    with pytest.raises(SemanticError):
        analizador.analizarArbol()
        print(analizador.directoriosVariables)


def test_llamadafuncion():
    programa = """
    func int foo (a int){
        a + 8;
        return 3;
    }
    main(){
    foo(3);    
    }"""
    analizador = AnalizadorSemantico(programa)
    analizador.analizarArbol()
    print(analizador.directoriosVariables)

