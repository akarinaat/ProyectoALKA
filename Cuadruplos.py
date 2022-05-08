from dataclasses import dataclass
from typing import List
from analizadorSemanticoALKA import AnalizadorSemantico
from lark import Token, Tree


@dataclass
class Cuadruplo:

    operacion: str
    op1: str
    op2: str
    temporal: str


class GeneracionCuadruplos:

    def __init__(self, programa):
        # Aquí se le hace appende de los cuadruplos generados
        self.listaCuadruplos: List[Cuadruplo] = []
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

    def generar_cuadruplo_nuevo(self, operacion, operando_izq, operando_der, direccion=None):
        if direccion is None:
            temporal_actual = "t" + str(self.get_temporal())
            cuadruplo = Cuadruplo(operacion, operando_izq,
                                  operando_der, temporal_actual)
            self.listaCuadruplos.append(cuadruplo)
            return temporal_actual
        else:
            cuadruplo = Cuadruplo(operacion, operando_izq,
                                  operando_der, direccion)
            self.listaCuadruplos.append(cuadruplo)
            return direccion

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

    def generar_cuadruplos_main(self, subtree: Tree):

        for child in subtree.children:
            if child.data == "decvars":
                # Generar cuádruplos
                self.generar_cuadruplos_decvars(child)
            elif child.data == "estatutos":
                self.generar_cuadruplos_estatutos(child)
                pass

    def generar_cuadruplos_estatutos(self, estatutos:Tree):
        # (asignacion | llamadafuncion | expresion | if | while | forloop | return) ";"

        for estatuto in estatutos.children:

            if estatuto.children[0].data == "expresion":
                self.generar_cuadruplos_expresion(estatuto.children[0])

            elif estatuto.children[0].data == "asignacion":
                self.generar_cuadruplos_asignacion(estatuto.children[0])

            elif estatuto.children[0].data == "llamadafuncion":
                self.generar_cuadruplos_llamadafuncion(estatuto.children[0])

            elif estatuto.children[0].data == "if":
                self.generar_cuadruplos_if(estatuto.children[0])

            elif estatuto.children[0].data == "while":
                self.generar_cuadruplos_while(estatuto.children[0])

            elif estatuto.children[0].data == "forloop":
                self.generar_cuadruplos_forloop(estatuto.children[0])

            elif estatuto.children[0].data == "return":
                self.generar_cuadruplos_return(estatuto.children[0])

    def generar_cuadruplos_llamadafuncion(self):
        pass


############### EXPRESION ##################


    def generar_cuadruplos_expresion(self, expresion: Tree):

        if len(expresion.children) == 1:
            exp = expresion.children[0]
            return self.generar_cuadruplos_exp(exp)

        else:
            exp_izq = expresion.children[0]
            operacion = expresion.children[1]
            exp_der = expresion.children[2]
            operando_izq = self.generar_cuadruplos_exp(exp_izq)
            operando_der = self.generar_cuadruplos_exp(exp_der)

            # Generar cuadruplo
            return self.generar_cuadruplo_nuevo(operacion, operando_izq, operando_der)

    def generar_cuadruplos_exp(self, exp):
        lista_terminos = exp.children[::2].copy()
        lista_operaciones = exp.children[1::2].copy()

        arbol_termino_izq = lista_terminos.pop(0)
        valor_termino_izq = self.generar_cuadruplos_termino(arbol_termino_izq)

        while len(lista_operaciones) > 0:

            operacion = lista_operaciones.pop(0)
            termino_der = lista_terminos.pop(0)
            operando_der = self.generar_cuadruplos_termino(termino_der)
            valor_termino_izq = self.generar_cuadruplo_nuevo(
                operacion, valor_termino_izq, operando_der)

            # insertar resultado en stack
        return valor_termino_izq

    def generar_cuadruplos_termino(self, termino):

        lista_factores = termino.children[::2].copy()
        lista_operaciones = termino.children[1::2].copy()
        arbol_factor_izq = lista_factores.pop(0)
        valor_factor_izq = self.generar_cuadruplos_factor(arbol_factor_izq)

        while len(lista_operaciones) > 0:
            operacion = lista_operaciones.pop(0)
            arbol_termino_der = lista_factores.pop(0)
            valor_factor_der = self.generar_cuadruplos_factor(
                arbol_termino_der)
            valor_factor_izq = self.generar_cuadruplo_nuevo(
                operacion, valor_factor_izq, valor_factor_der)
        return valor_factor_izq

    # factor "(" expresion ")" | (PLUS | MINUS)? atomo
    def generar_cuadruplos_factor(self, arbol_factor: Tree):
        if len(arbol_factor.children) == 1:
            expresion = arbol_factor.children[0]
            if expresion.data == "expresion":
                return self.generar_cuadruplos_expresion(expresion)
            else:
                return self.generar_cuadruplos_atomo(expresion)
        elif len(arbol_factor.children) == 2:
            atomo = arbol_factor.children[1]
            valor_atomo = self.generar_cuadruplos_atomo(atomo)
            operacion = arbol_factor.children[0]

            return self.generar_cuadruplo_nuevo(operacion, valor_atomo, "")

    # atomo : llamadavariable | CTEF | CTESTR | CTEI | llamadafuncion | funcionesespeciales
    def generar_cuadruplos_atomo(self, atomo):

        atomo = atomo.children[0]
        if isinstance(atomo, Token):
            if atomo.type == "CTEI":
                return int(atomo)
            elif atomo.type == "CTEF":
                return float(atomo)
            elif atomo.type == "CTESTR":
                return atomo
        else:  # Es un arbol, no token.
            print("atomo child:", atomo.pretty())

            if atomo.data == 'llamadavariable':
                return atomo.children[0].children[0]
                # Como se ponen las variables con dimensiones en cuadruplos?
                # A[2+f(3)][3] + 3;
                # lo que regresa generar cuadruplos llamvar : "(a,[2,3])"
                # + (a,[2,3]) 3 t0
                # TODO FALTA TODO LO DE DIMENSIONES
            elif atomo.data == "llamadafuncion":
                pass
            elif atomo.data == "funcionesespeciales":
                pass

################## ASIGNACION ##########################
    # Lega el arbol de la regla de asignacion
    # Cuadruplo de asignacion: = valor_expresion _ variable
    def generar_cuadruplos_asignacion(self, asignacion: Tree):
        # asignacion : llamadavariable "=" expresion
        llamada_var_asig = asignacion.children[0]
        arbol_expresion = asignacion.children[1]
        valor_expresion = self.generar_cuadruplos_expresion(arbol_expresion)
        # Generar llamada variable

############### LLAMADAVARIABLE #######################
   # llamadavariable : id ("[" expresion "]" )*
    def generar_cuadruplos_llamadavariable(self, llamadavariable: Tree):
        id_var = llamadavariable.children[0]
        print(id_var, "el nombre de llamada variable")

    def generar_cuadruplos_decvars(self, decvars: Tree):

        for decvar in decvars.children:
            self.generar_cuadruplos_decvar(decvar)

    def generar_cuadruplos_decvar(self, decvar: Tree):
        # cuadruplo de decvar:
        # decvar tipo dimensiones nombre
        # 3???????este porque no está dentro del for?
        tipo = decvar.children[0].children[0]
        variables = decvar.children[1:]
        for variable in variables:
            nombre = variable.children[0].children[0]

            expresiones_dimensiones = variable.children[1:]
            temporales_dimensiones = [
                self.generar_cuadruplos_expresion(expresion)
                for expresion in expresiones_dimensiones
            ]

            dimensiones_str = str(temporales_dimensiones)
            # generar los cuádruplos de las expresiones de las dimensiones
            self.generar_cuadruplo_nuevo(
                "decvar", tipo, dimensiones_str, str(nombre))

    # while : "while" "(" expresion ")" "{" estatutos "}"
    def generar_cuadruplos_while(self, arbol_while:Tree):
        arbol_expresion_while = arbol_while.children[0]
        arbol_estatutos_while = arbol_while.children[1] #Aqui ya no le pongo el .children porque generar 
                                                        #generar_cuadruplos_estatutos ya recibe el arbol y
                                                        #en el for, ya loopeo en el .children
        posicion_dela_condicion = len(self.listaCuadruplos)
        resultado_expresion = self.generar_cuadruplos_expresion(arbol_expresion_while)
        #goto
        self.generar_cuadruplo_nuevo("gotof", resultado_expresion, "", "")
        posicion_goto = len(self.listaCuadruplos) - 1
        self.generar_cuadruplos_estatutos(arbol_estatutos_while)
        self.generar_cuadruplo_nuevo("goto","","",posicion_dela_condicion)
        posicion_acabando_while = len(self.listaCuadruplos)
        self.listaCuadruplos[posicion_goto].temporal = posicion_acabando_while

    # if : "if" "(" expresion ")" "{" estatutos "}" else
    def generar_cuadruplos_if(self, arbol_if: Tree):
          #Cuadruplos
          #1. Declara variable a
          #2. Declara variable b
          #3. > a b t0
          #4. gotof t0  _
          #5. + 3 2 t1
          #6. goto 7 _

        arbol_expresion_if = arbol_if.children[0]
        arbol_estatutos_if = arbol_if.children[1]
        arbol_else_if = arbol_if.children[2]

        #1. Generar cuadruplos de la condicion
        resultado_expresion_if = self.generar_cuadruplos_expresion(arbol_expresion_if)

        #2. gotof de la condición (4)
        self.generar_cuadruplo_nuevo("gotof",resultado_expresion_if, "", "")
        #La posicion es el ultimo elmento de la lista de cuadruplos
        posicion_gotof = len(self.listaCuadruplos) - 1 

        #3. Generamos los cuadruplos del cuerpo del if
        self.generar_cuadruplos_estatutos(arbol_estatutos_if)

        #4. GOTO para saltar el else
        self.generar_cuadruplo_nuevo("goto","","","")
        posicion_goto_saltar_else = len(self.listaCuadruplos) - 1 

        #La posición justo después del if
        posicion_terminando_if = len(self.listaCuadruplos)

        #5. Ponerle al gotof la posicion después del if
        #Al gotof le tengo que poner la posición de a donde brincar despues del cuerpo del if
        self.listaCuadruplos[posicion_gotof].temporal = posicion_terminando_if
       
        #6. Generar cuadruplos del else
        self.generar_cuadruplos_else(arbol_else_if)


      #else : ("else" "{" estatutos "}")?  
    def generar_cuadruplos_else(self, arbol_else:Tree):
        if len(arbol_else.children) > 0:
            self.generar_cuadruplos_estatutos(arbol_else.children[0])
        

        