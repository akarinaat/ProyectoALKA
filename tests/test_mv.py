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
    

def test_while():
    programa = """
    main(){
        var int: a;
        a = 1;
        while(a<5){
           a = a+1;
        };
        return a;
    } """

    res = compilar_y_correr(programa)
    assert res == 5

def test_forloop():
    programa = """main(){
        var int: a;
        for a = 0 to 10 {      
          4+5;
        };
        return a;
    }"""

    res = compilar_y_correr(programa)
    assert res == 10

def test_if_():
    programa = """main(){
        var int: a,b;
        a = 6;
        b = 3;
        if(a>b){
          return 5;
        };
        
    } """

    res = compilar_y_correr(programa)
    assert res == 5
    
def test_if_false():
    programa = """main(){
        var int: a,b;
        a = 6;
        b = 3;
        if(a>b){
          3+2;
        };
        return a;
    } """

    res = compilar_y_correr(programa)
    assert res == 6

def test_if_else():

     programa = """main(){
        var int: a,b ;
        a = 8;
        b= 4;
        if(a>b){
           return 3+2;
        }else{
           return 5+6;
        };
      

    } """

     res = compilar_y_correr(programa)
     assert res == 5

def test_prueba_asignacion():

    programa = """ main(){
                var int: a;
                a = 3;
                return a;
                } """

    res = compilar_y_correr(programa)
    assert res == 3

def test_prueba_promedio():

    programa = """ main(){
    var int: a[7];
    var int: x;

    a[0] = 7;
    a[1] = 2;
    a[2] = 8;
    a[3] = 2;
    a[4] = 4;
    a[5] = 5;
    a[6] = 7;
    return mean(a);

    
} """

    res = compilar_y_correr(programa)
    assert res == 5

def test_prueba_moda():

    programa = """ main(){
    var int: a[7];
    var int: x;

    a[0] = 7;
    a[1] = 2;
    a[2] = 8;
    a[3] = 2;
    a[4] = 4;
    a[5] = 7;
    a[6] = 7;
    return mode(a);

    
} """

    res = compilar_y_correr(programa)
    assert res == 7


