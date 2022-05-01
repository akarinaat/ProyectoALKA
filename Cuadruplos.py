from dataclasses import dataclass
from analizadorSemanticoALKA import AnalizadorSemantico
from lark import Tree

@dataclass
class Cuadruplo:

    operacion : str
    op1 : str
    op2 : str
    temporal : str

class GeneracionCuadruplos:

    def __init__(self,programa):
        self.listaCuadruplos = [] # Aquí se le hace appende de los cuadruplos generados
        self.programa = programa
        self.temporal_actual = 0

        self.analizador = AnalizadorSemantico(programa)
        self.analizador.analizarArbol()
        
        self.arbol = self.analizador.arbol
    
    def get_temporal(self): 
        """Para saber en qué temporal voy"""
        temporal_actual = self.temporal_actual
        self.temporal_actual += 1
        return temporal_actual


    def generar_cuadruplo_nuevo(self,operacion,operando_izq,operando_der):
            temporal_actual = "t" + self.get_temporal()
            cuadruplo = Cuadruplo(operacion,operando_izq,operando_der,temporal_actual)
            self.listaCuadruplos.append(cuadruplo)
            return temporal_actual

    
    def generar_cuadruplos(self):
        print(self.arbol.pretty())
        for subtree in self.arbol.children:
            if subtree.data == "decvars":
                pass
                # self.analizar_decvars(subtree)
            elif subtree.data == "decfuncs":
                pass
                # self.analizar_decfuncs(subtree)
            elif subtree.data == "main":
                self.generar_cuadruplos_main(subtree)
                pass

    def generar_cuadruplos_main(self,subtree: Tree):
    
        for child in subtree.children:
            if child.data == "decvars":
                pass
            elif child.data == "estatutos":
                self.generar_cuadruplos_estatutos(child)
                pass    

    def generar_cuadruplos_estatutos(self, estatutos):
        #(asignacion | llamadafuncion | expresion | if | while | forloop | return) ";"

        for estatuto in estatutos.children:
            
            if estatuto.children[0].data == "expresion":
                self.generar_cuadruplos_expresion(estatuto.children[0])
                
            elif estatuto.children[0].data == "asignacion":
                pass
            elif estatuto.children[0].data == "llamadafuncion":
                pass
            elif estatuto.children[0].data == "if":
                pass
            elif estatuto.children[0].data == "while":
                pass
            elif estatuto.children[0].data == "forloop":
                pass
            elif estatuto.children[0].data == "return":
                pass


    def generar_cuadruplos_expresion(self, expresion: Tree):
        print(expresion.data)
        if len(expresion.children) == 1:
            exp = expresion.children[0]
            self.generar_cuadruplos_exp(exp)
        else:
            exp_izq = expresion.children[0]
            operacion = expresion.children[1]
            exp_der = expresion.children[2]
            operando_izq = self.generar_cuadruplos_exp(exp_izq)
            operando_der = self.generar_cuadruplos_exp(exp_der)

            #Generar cuadruplo
            self.generar_cuadruplo_nuevo(operacion, operando_izq,operando_der)

    def generar_cuadruplos_exp(self, exp):
        print(exp.pretty())
        lista_terminos = exp.children[::2].copy()
        lista_operaciones = exp.children[1::2].copy()

        while operacion := lista_operaciones.pop(0):
            termino_izq = lista_terminos.pop(0)
            termino_der = lista_terminos.pop(1)
            operando_izq = self.generar_cuadruplos_termino(termino_izq)
            operando_der = self.generar_cuadruplos_termino(termino_der)
            resultado = self.generar_cuadruplo_nuevo(operacion, operando_izq, operando_der)
            #insertar resultado en stack
            
    def generar_cuadruplos_termino(self, termino):

        pass

        # 1 + 2 + 3 + 4

    