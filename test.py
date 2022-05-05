
from Cuadruplos import GeneracionCuadruplos
from analizadorSemanticoALKA import AnalizadorSemantico

programa = """main(){
    var float: b[2];
}"""
generador = GeneracionCuadruplos(programa)
generador.generar_cuadruplos()
assert len(generador.listaCuadruplos) == 1

print(generador.listaCuadruplos)