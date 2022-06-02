import pytest
import Cuadruplos
from Cuadruplos import GeneracionCuadruplos
import mv

def compilar_y_correr(programa):
    generador = GeneracionCuadruplos(programa)
    generador.generar_cuadruplos_programa()

    cuadruplos = "".join(generador.hacer_string_cuadruplos())
    print(cuadruplos)
    maquina = mv.MaquinaVirtual(cuadruplos)
    return maquina.ejecutar_programa()

def test_recursividad():
    programa = """
    func int fibonacci(n int){

        if(n<2){
            return n;
        }else{
            return fibonacci(n-1) + fibonacci(n-2);
        };
    }

    func int factorial(f int){
     
     if (f == 0){
         return 1;
     } else {
         return f * factorial(f-1);
     };
}

     main (){
        return factorial(5);
    }
    """
    res= compilar_y_correr(programa)
    
    assert res == 120

def test_vars():
    programa = """
    var int: a;


     main (){
         a = 5;
        return  a;
    }
    """
    res= compilar_y_correr(programa)
    
    assert res == 5

def test_arreglos():
    programa = """
    var int: a[3];


     main (){
         a[2] = 5;
        return  a[2];
    }
    """
    res= compilar_y_correr(programa)
    
    assert res == 5

def test_arreglos2():
    programa = """
    var int: a[3][5];


     main (){
        a[2][3] = 55;
        return  a[2][3];
    }
    """
    res= compilar_y_correr(programa)
    
    assert res == 55
    
def test_arreglos():
    programa = """
    var int: a[3];


     main (){
         a[2] = 5;
        return  a[2];
    }
    """
    res= compilar_y_correr(programa)
    
    assert res == 5

