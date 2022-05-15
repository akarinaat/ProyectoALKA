
from Cuadruplos import GeneracionCuadruplos
from analizadorSemanticoALKA import AnalizadorSemantico
from lark import tree

programa = """
        var int:a;
        func int foo (h int, b int) {
            var float: c;
        }
        main(){}"""

analizador = AnalizadorSemantico(programa)
analizador.analizarArbol()

tree.pydot__tree_to_png(analizador.arbol,"test_conParametros.png")

