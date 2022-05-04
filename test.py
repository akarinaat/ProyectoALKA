
from analizadorSemanticoALKA import AnalizadorSemantico

programa = """
    func int foo (a int) {

        (b)+2+3-2+1;
    }
    main(){}"""

analizador = AnalizadorSemantico(programa)

analizador.analizarArbol()