import pytest
from Cuadruplos import GeneracionCuadruplos


def test_prueba_basica():
    programa = """ main(){2+-3;} """
    generador = GeneracionCuadruplos(programa)
    generador.generar_cuadruplos()
    print(generador.listaCuadruplos)
    assert len(generador.listaCuadruplos) == 2


def test_prueba_asignacion():
    programa = """ main(){
                var int: a;
                a = 3;
                } """
    generador = GeneracionCuadruplos(programa)
    generador.generar_cuadruplos()
    assert len(generador.listaCuadruplos) == 2


def test_prueba_decvar():
    programa = """main(){
        var float: b;
    }"""
    generador = GeneracionCuadruplos(programa)
    generador.generar_cuadruplos()
    assert len(generador.listaCuadruplos) == 1


def test_expresion_llamada_var():
    programa = """main(){
        var float: b;
        b+3.2;
    }"""
    generador = GeneracionCuadruplos(programa)
    generador.generar_cuadruplos()
    assert len(generador.listaCuadruplos) == 2
    assert generador.listaCuadruplos[1].op1 == "b"



def test_if():
    #Cuadruplos
    #1. Declara variable a
    #2. Declara variable b
    #3. > a b t0
    #4. gotof t0  _
    #5. + 3 2 t1
    #6. goto 7 _
    
    

    programa = """main(){
        var int: a,b;
        if(a>b){
            3+2;
        };
    } """
    generador = GeneracionCuadruplos(programa)
    generador.generar_cuadruplos()
    assert len(generador.listaCuadruplos) == 6

def test_while():
    programa = """main(){
        var int: a;
        while(a>5){
            2+1;
        };
    } """
    generador = GeneracionCuadruplos(programa)
    generador.generar_cuadruplos()
    assert len(generador.listaCuadruplos) == 5
    