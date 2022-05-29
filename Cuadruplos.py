from audioop import reverse
from dataclasses import dataclass
from enum import Enum, auto
from functools import reduce
from typing import Any, Dict, List, Tuple
from Memoria import Memoria
from analizadorSemanticoALKA import AnalizadorSemantico, SemanticError
from lark import Token, Tree
import sys


string_ops = "* / + - decfunc decvar < > != = param goto gotof gosub".split()
Operaciones = dict(zip(string_ops, range(len(string_ops))))
# {'*': 0, '/': 1, '+': 2, '-': 3, 'decfunc': 4, 'decvar': 5, '<': 6, '>': 7, '!=': 8, '=': 9, 'param': 10, 'goto': 11, 'gotof': 12, 'call': 13}


class Alcance(Enum):
    alcance_global = auto()
    alcance_local = auto()
    alcance_constante = auto()


@dataclass
class Cuadruplo:

    operacion: str
    op1: str
    op2: str
    temporal: str
    # cuando use la funcion str en un cuadruplo
    # para cuadno lo mande al archivo de abajo

    def __str__(self) -> str:
        return f"{self.operacion},{self.op1},{self.op2},{self.temporal}\n"


@dataclass
class Funcion:

    tamaño: int
    nombre: str
    direccion_inicio: int
    directorio_variables: dict[str, str]
    lista_nombres_parametros: list[str]


class GeneracionCuadruplos:

    def __init__(self, programa):  # el programa que le llega de pruebas
        # Aquí se le hace appende de los cuadruplos generados
        # En el paso de la mv, necesito procesar estos a str

        # se inicializa con el cuadruplo de goto main
        self.listaCuadruplos: List[Cuadruplo] = [Cuadruplo("goto", "", "", "")]
        # Necesito un directorio que teniendo el nombre,
        # me diga cual es su dirección
        # Puede ser una lista de directorios
        # Y necesito otro para que me diga en qué
        # línea está la función
        # Directorio de funciones:
        self.diccionarioFunciones: Dict[str,
                                        Funcion] = {}  # tipos parametricos

        self.diccionarioConstates = {}
        self.contadorConstantes = {
            "int": 0,
            "float": 0,
            "str": 0,
            "bool": 0
        }
        # Lista de variables de funciones
        self.programa = programa
        self.temporal_actual = 0

        # Esta es para pasar de los nombres a direcciones
        # recibe un str y nos regresa un int (la dirección)
        self.directorio_variables_globales: Dict[str, Tuple[int, List[int]]] = {
        }

        # Cuando se llama una funcion, se mete un directorio nuevo
        # Cuando termina la funcion, se saca un directorio
        # le das el nombre de una variable, y te regresa su ( direccion , lista dimensiones)
        # Cuando se llama una funcion, se agrega un directorio nuevo
        self.directorio_variables_locales: List[Dict[str, Tuple[int, List[int]]]] = [
            {}]

        # el programa que le llega de pruebas (o del usuario) se va al analizador semántico
        self.analizador = AnalizadorSemantico(programa)
        # En analizador semántico genera un árbol
        self.analizador.analizarArbol()
        # guarda el arbol
        self.arbol = self.analizador.arbol

        # Para saber direcciones y cantidades de variables globales,
        self.memoria_global = Memoria()

        # Para saber direcciones / cantidades variables locales
        self.memoria_stack: List[Memoria] = [Memoria()]

    def get_temporal(self):
        """Para saber en qué temporal voy"""
        temporal_actual = self.temporal_actual
        self.temporal_actual += 1
        return temporal_actual

    def generar_cuadruplo_nuevo(self, operacion: Operaciones, operando_izq: str, operando_der: str, direccion: str = None):
        if direccion is None:
            temporal_actual = "2" + str(self.get_temporal()).zfill(4)
            cuadruplo = Cuadruplo(operacion, operando_izq,
                                  operando_der, temporal_actual)
            self.listaCuadruplos.append(cuadruplo)
            return temporal_actual
        else:
            cuadruplo = Cuadruplo(operacion, operando_izq,
                                  operando_der, direccion)
            self.listaCuadruplos.append(cuadruplo)
            return direccion

    def generar_cuadruplos_programa(self):

        for subtree in self.arbol.children:
            if subtree.data == "decvars":
                self.generar_cuadruplos_decvars(
                    subtree, Alcance.alcance_global)  # decvars globales
            elif subtree.data == "decfuncs":
                self.generar_cuadruplos_decfuncs(subtree)
            elif subtree.data == "main":
                self.generar_cuadruplos_main(subtree)
                pass

    def generar_cuadruplos_main(self, subtree: Tree):
        posicion_main = len(self.listaCuadruplos)

        self.listaCuadruplos[0].op1 = posicion_main
        for child in subtree.children:

            if child.data == "decvars":
                # Generar cuádruplos
                self.generar_cuadruplos_decvars(child, Alcance.alcance_local)
            elif child.data == "estatutos":
                self.generar_cuadruplos_estatutos(child)

    def generar_cuadruplos_estatutos(self, estatutos: Tree):
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
                self.generar_cuadruplos_for(estatuto.children[0])

            elif estatuto.children[0].data == "return":
                self.generar_cuadruplos_return(estatuto.children[0])

    # llamadafuncion :  id "(" (expresion  ("," expresion)*)? ")"
    def generar_cuadruplos_llamadafuncion(self, arbol_llamadafuncion: Tree):

        # LLAMADA FUNCION SOLO ACEPTA VALORES UNIDIMENSIONALES - AUN NO ARREGLOS

        nombre_funcion = arbol_llamadafuncion.children[0].children[0]
        lista_expresiones_argumentos = arbol_llamadafuncion.children[1:]

        self.generar_cuadruplo_nuevo("ERA", nombre_funcion, "", "")

        # conseguir la direccin de la funcion, lo hago con el nombre de la misma
        funcion_actual = self.diccionarioFunciones[nombre_funcion]

        direccion_funcion = funcion_actual.direccion_inicio

        # foo(2+3,a*5)
        # + 2 3 t0
        # * a 5 t1
        # param 0 t0
        # param 1 t1
        # call foo 2 t2 ---> AHORA SERÁ CALL LA DIRECCIÓN DE FOO

        # Encontrar el valor de todos los argumentos (donde se va a guardar el resultado)
        # lista_resultados_expresiones = []
        # for expresion in lista_expresion_llamadafuncion:
        #     res = self.generar_cuadruplos_expresion(expresion)
        #     lista_resultados_expresiones.append(res)

        # 1. Conseguir la dirección de los resultados de los argumentos
        # func(2+3,5)
        # + 2 3 t1
        # t1 --> La direccion de este temporal es el que estoy consiguiedo

        lista_resultados_expresiones = [
            self.generar_cuadruplos_expresion(expresion)
            for expresion in lista_expresiones_argumentos
        ]

        # 2.  Meter el argumento en el espacio del parametro
        #
        for (index, direccion_resultado_argumento) in enumerate(lista_resultados_expresiones):

            # Tengo que definir la direccion virtual del parametro

            # agarro el nombre del parametro correspondiente, y consigo su direccion virtual
            # le digo a la mv, que guarde el valor del argumento (resultado), en la direccion (espacio) del parametro
            nombre_parametro = funcion_actual.lista_nombres_parametros[index]

            direccion_parametro = funcion_actual.directorio_variables[nombre_parametro]

            self.generar_cuadruplo_nuevo(
                "param", direccion_resultado_argumento, "", direccion_parametro)

        # 3. Generar el cuadruplo llamada funcion
        direccion_resultado_llamada = self.generar_cuadruplo_nuevo(
            "gosub", direccion_funcion,"")  # antes estaba el nombre
       
        # rergresar el valor que regresa la funcion
        return direccion_resultado_llamada

    # decfunc : "func" tipo id  "(" parameters ")"  "{" decvars estatutos "}"
    # parameters : (id tipo ("," id tipo)*)?
    def generar_cuadruplos_decfuncs(self, arbol_decfuncs: Tree):
        for arbol_decfunc in arbol_decfuncs.children:
            self.generar_cuadruplos_decfunc(arbol_decfunc)

    def generar_cuadruplos_decfunc(self, arbol_decfunc: Tree):
        tipo_decfunc = arbol_decfunc.children[0]
        nombre_decfunc = arbol_decfunc.children[1].children[0]
        arbol_parametros = arbol_decfunc.children[2]
        arbol_decvars = arbol_decfunc.children[3]
        arbol_estatutos = arbol_decfunc.children[4]

        # decfunc tipo nombre  ERA (para la MV)
        # TODO FALTA ERA
        # self.generar_cuadruplo_nuevo(
        #     "decfunc", tipo_decfunc, nombre_decfunc, "")

        # Para saber en qué cuadruplo voy
        posicion_inicio = len(self.listaCuadruplos)

        self.directorio_variables_locales.append({})
        self.memoria_stack.append(Memoria())

        # Asignar espacio a parametros
        lista_nombres_parametros = self.asignar_espacio_parametros(
            arbol_parametros)

        

        # librar memoria del stack

        self.memoria_stack.pop()

        self.generar_cuadruplos_decvars(
            arbol_decvars, Alcance.alcance_local)  # dentro de funcion es local

        self.generar_cuadruplos_estatutos(arbol_estatutos)


        # generar el objeto de la funcion

        funcion = Funcion(0, nombre_decfunc, posicion_inicio,
                          self.directorio_variables_locales.pop(), lista_nombres_parametros)

        # meter funcion a diccionario funciones
        self.diccionarioFunciones[nombre_decfunc] = funcion

        self.generar_cuadruplo_nuevo("ENDFunc", "", "", "")


    def asignar_espacio_parametros(self, arbol_parametros: Tree) -> list[str]:
        lista_nombres = []
        for parametro in arbol_parametros.children:
            nombre_parametro = str(parametro.children[0].children[0])
            lista_nombres.append(nombre_parametro)
            tipo_parametro = parametro.children[1].children[0]
            self.declarar_variable_local(
                tipo_parametro, 1, nombre_parametro, [])
        return lista_nombres

    # return : "return" expresion
    def generar_cuadruplos_return(self, arbol_return: Tree):
        direccion_valor_return = self.generar_cuadruplos_expresion(
            arbol_return.children[0])
        self.generar_cuadruplo_nuevo("return", "", "", direccion_valor_return)


############### EXPRESION ##################


    def generar_cuadruplos_expresion(self, expresion: Tree) -> str:
        # regresa la dirección de donde se guardó el resultado de la expresión

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
            print("TOKEN!", atomo, atomo.type)
            if atomo.type == "CTEI":
                print("INT")
                if int(atomo) in self.diccionarioConstates:
                    return self.diccionarioConstates[int(atomo)]
                else:
                    direccion = "00" + \
                        str(self.contadorConstantes["int"]).zfill(3)
                    self.contadorConstantes["int"] += 1

                    self.diccionarioConstates[int(atomo)] = direccion

                    return direccion
            elif atomo.type == "CTEF":

                if float(atomo) in self.diccionarioConstates:
                    return self.diccionarioConstates[float(atomo)]
                else:
                    direccion = "01" + \
                        str(self.contadorConstantes["float"]).zfill(3)
                    self.contadorConstantes["float"] += 1

                    self.diccionarioConstates[float(atomo)] = direccion
                    return direccion
            elif atomo.type == "CTESTR":
                if str(atomo) in self.diccionarioConstates:
                    return self.diccionarioConstates[str(atomo)]
                else:
                    direccion = "02" + \
                        str(self.contadorConstantes["str"]).zfill(3)
                    self.contadorConstantes["str"] += 1
                    self.diccionarioConstates[str(atomo)] = direccion

                    return direccion
            elif atomo.type == "CTEBOOL":
                valor = atomo.value == 'True'
                if valor in self.diccionarioConstates:
                    return self.diccionarioConstates[valor]
                else:
                    direccion = "03" + \
                        str(self.contadorConstantes["bool"]).zfill(3)
                    self.contadorConstantes["bool"] += 1

                    self.diccionarioConstates[valor] = direccion

                    return direccion
        else:  # Es un arbol, no token.
            # print("atomo child:", atomo.pretty())

            if atomo.data == 'llamadavariable':
                direccion, lista_dims = self.generar_cuadruplos_llamadavariable(
                    atomo)
                return direccion
                # Como se ponen las variables con dimensiones en cuadruplos?
                # A[2+f(3)][3] + 3;
                # lo que regresa generar cuadruplos llamvar : "(a,[2,3])"
                # + (a,[2,3]) 3 t0
                # TODO FALTA TODO LO DE DIMENSIONES
            elif atomo.data == "llamadafuncion":
                return self.generar_cuadruplos_llamadafuncion(atomo)

            elif atomo.data == "funcionesespeciales":
                pass

################## ASIGNACION ##########################
    # Lega el arbol de la regla de asignacion
    # Cuadruplo de asignacion: = valor_expresion _ variable
    def generar_cuadruplos_asignacion(self, asignacion: Tree) -> Any:
        # asignacion : llamadavariable "=" expresion
        llamada_var_asig = asignacion.children[0]
        arbol_expresion = asignacion.children[1]
        valor_expresion = self.generar_cuadruplos_expresion(arbol_expresion)
        # Generar llamada variable
        direccion_variable, lista_dims = self.generar_cuadruplos_llamadavariable(
            llamada_var_asig)
        self.generar_cuadruplo_nuevo(
            "=", valor_expresion, "", direccion_variable)
        return direccion_variable

############### LLAMADAVARIABLE #######################
   # llamadavariable : id ("[" expresion "]" )*
    def generar_cuadruplos_llamadavariable(self, arbol_llamadavariable: Tree):

        id_var = arbol_llamadavariable.children[0].children[0]
        if id_var in self.directorio_variables_locales[-1]:
            direccion_variable, lista_dimensiones = self.directorio_variables_locales[-1][id_var]
        elif id_var in self.directorio_variables_globales:
            direccion_variable, lista_dimensiones = self.directorio_variables_globales[id_var]
        else:
            raise SemanticError("Error al compilar")

        # checar si es valor unidimensional
        if len(lista_dimensiones) == 0:
            return direccion_variable, []

        # guardo direccion como constante

        direccion_constante_base = self.obtener_direccion_constante(
            direccion_variable)

        # M empieza en uno, porque empiezo por la ultima dimension
        direccion_m_inicial = self.obtener_direccion_constante(1)
        direccion_m_temporal = self.generar_cuadruplo_nuevo(
            "=", direccion_m_inicial, "")

        direccion_indice_inicial = self.obtener_direccion_constante(0)
        direccion_indice_final_temporal = self.generar_cuadruplo_nuevo(
            "=", direccion_indice_inicial, "")

        lista_arboles_expresiones = arbol_llamadavariable.children[1:]

        for expresion_index, dimension in reversed(list(zip(lista_arboles_expresiones, lista_dimensiones))):
            direccion_indice_temporal = self.generar_cuadruplos_expresion(
                expresion_index)

            direccion_dimension_constante = self.obtener_direccion_constante(
                dimension)

            # calcular posicion indice

            aux1 = self.generar_cuadruplo_nuevo(
                "*", direccion_m_temporal, direccion_indice_temporal
            )

            self.generar_cuadruplo_nuevo(
                "+", direccion_indice_final_temporal, aux1, direccion_indice_final_temporal)

            # calcular M
            self.generar_cuadruplo_nuevo(
                "*", direccion_m_temporal, direccion_dimension_constante, direccion_m_temporal)

            self.generar_cuadruplo_nuevo(
                "ver", direccion_indice_temporal, dimension, "")
        # print(id_var, "el nombre de llamada variable")

        # agregar el indice a la direccion base
        return self.generar_cuadruplo_nuevo("+", direccion_constante_base, direccion_indice_final_temporal), lista_dimensiones

    def obtener_direccion_constante(self, constante: str):
        if int(constante) in self.diccionarioConstates:
            return self.diccionarioConstates[int(
                constante)]
        else:
            direccion = "00" + \
                str(self.contadorConstantes["int"]).zfill(3)
            self.contadorConstantes["int"] += 1

            self.diccionarioConstates[int(constante)] = direccion

            return direccion

    def generar_cuadruplos_decvars(self, decvars: Tree, alcance: Alcance):

        for decvar in decvars.children:
            self.generar_cuadruplos_decvar(decvar, alcance)

    def generar_cuadruplos_decvar(self, decvar: Tree, alcance: Alcance):
        # cuadruplo de decvar:
        # decvar tipo dimensiones nombre

        tipo = decvar.children[0].children[0]

        variables = decvar.children[1:]

        for variable in variables:

            nombre = variable.children[0].children[0]
            lista_CTEIs_dimensiones: List[Token] = variable.children[1:]
            lista_dimensiones = [] if len(
                lista_CTEIs_dimensiones) == 0 else [int(str(dim)) for dim in lista_CTEIs_dimensiones]

            tamano = reduce(lambda x, y: x*y, lista_dimensiones, 1)
            print(tamano)
            cantidad_expresiones = len(lista_CTEIs_dimensiones)

            # Conseguir la direccion de la variable
            direccion_variable = 0
            if alcance == Alcance.alcance_global:

                # Direccion base del tipo, mas cuantos de ese tipo hay
                direccion_variable = self.memoria_global.direcciones_base[tipo] + \
                    self.memoria_global.contadores_tipo_variables[tipo]

                direccion_variable = str(direccion_variable).zfill(4)
                # incrementar el contador de variables de su tipo.
                self.memoria_global.contadores_tipo_variables[tipo] += tamano
                # Prefijo variables globales es "1"
                self.directorio_variables_globales[nombre] = ("1" +
                                                              str(direccion_variable), lista_dimensiones)
            elif alcance == Alcance.alcance_local:

                self.declarar_variable_local(
                    tipo, tamano, nombre, lista_dimensiones)

            else:
                raise SemanticError("Error al compilar, alcance no definido")

            # generar los cuádruplos de las expresiones de las dimensiones
            # temporales_dimensiones = [
            #     self.generar_cuadruplos_expresion(expresion)
            #     for expresion in lista_CTEIs_dimensiones
            # ]

            # dimensiones_str = str(temporales_dimensiones)
            # self.generar_cuadruplo_nuevo(
            #     "decvar", tipo, dimensiones_str, str(nombre))

    # while : "while" "(" expresion ")" "{" estatutos "}"

    def declarar_variable_local(self, tipo, tamano, nombre, lista_dimensiones):
        direccion_variable = self.memoria_stack[-1].direcciones_base[tipo] + \
            self.memoria_stack[-1].contadores_tipo_variables[tipo]

        direccion_variable = str(direccion_variable).zfill(4)

        # incrementar el contador de variables de su tipo.
        self.memoria_stack[-1].contadores_tipo_variables[tipo] += tamano
        # Prefijo variables locales es "2"
        self.directorio_variables_locales[-1][nombre] = ("2" +
                                                         str(direccion_variable), lista_dimensiones)

    def generar_cuadruplos_while(self, arbol_while: Tree):
        arbol_expresion_while = arbol_while.children[0]
        # Aqui ya no le pongo el .children porque generar
        arbol_estatutos_while = arbol_while.children[1]
        # generar_cuadruplos_estatutos ya recibe el arbol y
        # en el for, ya loopeo en el .children
        posicion_dela_condicion = len(self.listaCuadruplos)
        resultado_expresion = self.generar_cuadruplos_expresion(
            arbol_expresion_while)
        # goto
        self.generar_cuadruplo_nuevo("gotof", resultado_expresion, "", "")
        posicion_goto = len(self.listaCuadruplos) - 1
        self.generar_cuadruplos_estatutos(arbol_estatutos_while)
        self.generar_cuadruplo_nuevo("goto", "", "", posicion_dela_condicion)
        posicion_acabando_while = len(self.listaCuadruplos)
        self.listaCuadruplos[posicion_goto].temporal = posicion_acabando_while

    # if : "if" "(" expresion ")" "{" estatutos "}" else
    def generar_cuadruplos_if(self, arbol_if: Tree):
        # Cuadruplos
        # 1. Declara variable a
        # 2. Declara variable b
        # 3. > a b t0
        # 4. gotof t0  _
        # 5. + 3 2 t1
        # 6. goto 7 _

        arbol_expresion_if = arbol_if.children[0]
        arbol_estatutos_if = arbol_if.children[1]
        arbol_else_if = arbol_if.children[2]

        # 1. Generar cuadruplos de la condicion
        resultado_expresion_if = self.generar_cuadruplos_expresion(
            arbol_expresion_if)

        # 2. gotof de la condición (4)
        self.generar_cuadruplo_nuevo("gotof", resultado_expresion_if, "", "")
        # La posicion es el ultimo elmento de la lista de cuadruplos
        posicion_gotof = len(self.listaCuadruplos) - 1

        # 3. Generamos los cuadruplos del cuerpo del if
        self.generar_cuadruplos_estatutos(arbol_estatutos_if)

        # 4. GOTO para saltar el else
        self.generar_cuadruplo_nuevo("goto", "", "", "")
        posicion_goto_saltar_else = len(self.listaCuadruplos) - 1

        # La posición justo después del if
        posicion_terminando_if = len(self.listaCuadruplos)

        # 5. Ponerle al gotof la posicion después del if
        # Al gotof le tengo que poner la posición de a donde brincar despues del cuerpo del if
        self.listaCuadruplos[posicion_gotof].temporal = posicion_terminando_if

        # 6. Generar cuadruplos del else
        self.generar_cuadruplos_else(arbol_else_if)

        posicion_despues_else = len(self.listaCuadruplos)

        # 7. Ponerle la posicion al goto de saltar else

        self.listaCuadruplos[posicion_goto_saltar_else].temporal = posicion_despues_else

      # else : ("else" "{" estatutos "}")?

    def generar_cuadruplos_else(self, arbol_else: Tree):
        if len(arbol_else.children) > 0:
            self.generar_cuadruplos_estatutos(arbol_else.children[0])

    # forloop : "for" asignacion "to" expresion "{" estatutos "}"
    def generar_cuadruplos_for(self, arbol_for: Tree):
        # cuadruplos esperados:
        # dec a
        # = 0   a
        # < a 10 t0   -> generar condicion y guardar su lugar
        # gotof t0 _ -> generar gotof
        # + 4 5 t1
        # + a 1 t2  -> incermentar la variable de control
        # = t2  a
        # goto condicion -> hacer goto a la posicion de la condicion

        arbol_asignacion_for = arbol_for.children[0]
        arbol_expresion_for = arbol_for.children[1]
        arbol_estatutos_for = arbol_for.children[2]

        self.generar_cuadruplos_asignacion(arbol_asignacion_for)
        variable = arbol_asignacion_for.children[0]
        resultado_expresion = self.generar_cuadruplos_expresion(
            arbol_expresion_for)

        # # < a 10 t0   -> generar condicion y guardar su lugar
        resultado_condicion = self.generar_cuadruplo_nuevo(
            "<", variable, resultado_expresion)
        posicion_condicion = len(self.listaCuadruplos) - 1

        # gotof t0 _ -> generar gotof y guardar su lugar
        self.generar_cuadruplo_nuevo("gotof", resultado_condicion, "", "")
        posicion_gotof = len(self.listaCuadruplos) - 1

        # generar el cuerpo del for
        self.generar_cuadruplos_estatutos(arbol_estatutos_for)

        # Incrementar la variable de control
        resultado_incremento = self.generar_cuadruplo_nuevo("+", variable, "1")
        self.generar_cuadruplo_nuevo("=", resultado_incremento, "", variable)

        # goto de regreso al a condicion
        self.generar_cuadruplo_nuevo("goto", "", "", posicion_condicion)

        # ponerle la direccion despues del for al gotof
        posicion_despues_for = len(self.listaCuadruplos)
        self.listaCuadruplos[posicion_gotof].temporal = posicion_despues_for

    def hacer_string_cuadruplos(self) -> List[str]:
        lista_string_cuadruplos = [str(cuadruplo)
                                   for cuadruplo in self.listaCuadruplos
                                   ]

        # 1 insert - tabla constantes

        lista_string_cuadruplos.append(repr(self.diccionarioConstates))

        return lista_string_cuadruplos


if __name__ == "__main__":

    # Voy a leer el archivo que contiene el código fuente
    # ArchivoIn tiene el string de lo que es el programa (tipo el string que hay en las pruebas, not exactly but like that)
    # archivoIn = sys.argv[1]
    archivoIn = "test.alka"
    # Es el que contiene el código intermedio
    # archivoOut = sys.argv[2]
    archivoOut = "test.out"
    # Abre y cierra sin el close
    with open(archivoIn, "r") as codigo:
        generador = GeneracionCuadruplos(codigo.read())
        generador.generar_cuadruplos_programa()  # genero lista de cuadruplos
        lista_strings = generador.hacer_string_cuadruplos()
        with open(archivoOut, "w") as cuadruplos:
            cuadruplos.writelines(lista_strings)
