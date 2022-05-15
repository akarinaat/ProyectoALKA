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
    # Cuadruplos
    # 1. Declara variable a
    # 2. Declara variable b
    # 3. > a b t0
    # 4. gotof t0  _
    # 5. + 3 2 t1
    # 6. goto 7 _

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


def test_for():
    programa = """main(){
        var int: a;
        for a = 0 to 10 {

            4+5;
        };
    }"""
    # Convertir como a while
    # var int a
    # a= 0;
    # while (a < 10){
    #   Cuerpo While
    #   a = a +1;
    # }

    # cuadruplos esperados:
    # dec a
    # = 0   a
    # < a 10 t0   -> generar condicion y guardar su lugar
    # gotof t0 _ -> generar gotof
    # + 4 5 t1
    # + a 1 t2  -> incermentar la variable de control
    # = t2  a
    # goto condicion -> hacer goto a la posicion de la condicion
    generador = GeneracionCuadruplos(programa)
    generador.generar_cuadruplos()
    assert len(generador.listaCuadruplos) == 8


def test_llamadafuncion():
    programa = """ 
    func int foo(a int, b int){
        a+b;
    }
    main(){
        foo(2*3,5+4);
    }"""
    generador = GeneracionCuadruplos(programa)
    generador.generar_cuadruplos()
    assert len(generador.listaCuadruplos) > 8


def test_decfunc():
    programa = """ 
    func int foo(a int, b int){
        a+b;
    }
    main(){
        
    }"""
    generador = GeneracionCuadruplos(programa)
    generador.generar_cuadruplos()
    print(generador.listaCuadruplos)
    assert len(generador.listaCuadruplos) == 5
