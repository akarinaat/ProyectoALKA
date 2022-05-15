
from Cuadruplos import GeneracionCuadruplos
from analizadorSemanticoALKA import AnalizadorSemantico
from lark import tree

programa = """
        var int:a;
        func int foo () {
            var float: c;
        }
        main(){}"""

analizador = AnalizadorSemantico(programa)
analizador.analizarArbol()

tree.pydot__tree_to_png(analizador.arbol,"test2.png")

