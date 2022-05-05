
from Cuadruplos import GeneracionCuadruplos
from analizadorSemanticoALKA import AnalizadorSemantico

programa = """main(){
        var float: b;
        b+3;
    }"""
generador = GeneracionCuadruplos(programa)
generador.generar_cuadruplos()
assert len(generador.listaCuadruplos) == 2
print(generador.listaCuadruplos)
