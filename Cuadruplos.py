from dataclasses import dataclass
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
        self.listaCuadruplos = []  # Aquí se le hace appende de los cuadruplos generados
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

    def generar_cuadruplos_estatutos(self, estatutos):
        # (asignacion | llamadafuncion | expresion | if | while | forloop | return) ";"

        for estatuto in estatutos.children:

            if estatuto.children[0].data == "expresion":
                self.generar_cuadruplos_expresion(estatuto.children[0])

            elif estatuto.children[0].data == "asignacion":
                self.generar_cuadruplos_asignacion(estatuto.children[0])

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

        print(exp)
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

    # Lega el arbol de la regla de asignacion
    def generar_cuadruplos_asignacion(self, asignacion: Tree):
        # asignacion : llamadavariable "=" expresion
        llamada_var_asig = asignacion.children[0]

        print(llamada_var_asig)
        pass

    def generar_cuadruplos_decvars(self, decvars: Tree):

        for decvar in decvars.children:
            self.generar_cuadruplos_decvar(decvar)

    def generar_cuadruplos_decvar(self, decvar: Tree):
        # cuadruplo de decvar:
        # decvar tipo dimensiones nombre
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
            self.generar_cuadruplo_nuevo("decvar", tipo,dimensiones_str,str(nombre))

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
        print(arbol_factor)
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
        print(atomo.data)

        atomo = atomo.children[0]
        if isinstance(atomo, Token):
            print(atomo.type)
            if atomo.type == "CTEI":
                return int(atomo)
            elif atomo.type == "CTEF":
                return float(atomo)
            elif atomo.type == "CTESTR":
                return atomo
        else:
            print("no es token")
