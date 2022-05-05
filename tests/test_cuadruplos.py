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
        b+3;
    }"""
    generador = GeneracionCuadruplos(programa)
    generador.generar_cuadruplos()
    assert len(generador.listaCuadruplos) == 2
    assert generador.listaCuadruplos[1].op1 == "b"
