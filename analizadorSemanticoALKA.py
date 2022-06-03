from ctypes import Union
from pickle import FALSE
from typing import Dict, List
from alkaparser import ALKA_parser
from lark import Token, Tree, tree
from dataclasses import dataclass
from enum import Enum


class SemanticError(Exception):
    pass


class Tipo(Enum):
    Float = "float"
    Int = "int"
    String = "string"
    Bool = "bool"
    Void = "void"


@dataclass  # son para guardar información
class Variable:

    tipo: Tipo
    nombre: str
    dimensiones: int


@dataclass
class Funcion:
    tipo: Tipo
    nombre: str
    parametros: List[Tipo]


class AnalizadorSemantico:

    def __init__(self, input) -> None:
        # Directorio de variables, en lista para poder analizar las globales y las locales
        #List[Dict[str,Variable]] = [{}]
        # Dict[str,Funcion]
        # Se declaran así osd directorios para saber de qué tipo es la info que contiene
        # Si no lo pongo, habrá un error de :
        # error: Need type annotation for "directoriosVariables"
        # error: Need type annotation for "directorioFunciones"

        self.directoriosVariables: List[Dict[str, Variable]] = [
            {}]  # Lista de directorio de variables
        # Se usa una lista por lo de las variables
        # locales de cada función (esas serían el dir2)
        # Directorio de funciones
        self.directorioFunciones: Dict[str, Funcion] = {}
        self.arbol: Tree = ALKA_parser.parse(input)  # Se define el árbol

    def analizarArbol(self):
        for subtree in self.arbol.children:

            if subtree.data == "decvars":
                self.analizar_decvars(subtree)
            elif subtree.data == "decfuncs":
                self.analizar_decfuncs(subtree)
            elif subtree.data == "main":
                self.analizar_main(subtree)

    def analizar_main(self, arbol_main: Tree):
        # main : "main" "(" ")" "{" decvars estatutos "}"
        arbol_decvars_main = arbol_main.children[0]
        arbol_estatutos_main = arbol_main.children[1]

        self.analizar_decvars(arbol_decvars_main)
        self.analizar_estatutos(arbol_estatutos_main.children)

    def analizar_decvars(self, subtree: Tree) -> None:
        for decvar in subtree.children:
            self.analizar_decvar(decvar)

    def analizar_decfuncs(self, subtree: Tree) -> None:
        for decfunc in subtree.children:
            self.analizar_decfunc(decfunc)

    def analizar_decvar(self, subtree: Tree) -> None:
        tipo = subtree.children[0].children[0]
        variables = subtree.children[1:]

        for variable in variables:
            nombre = variable.children[0].children[0]
            # Encontrar con cuantas dimensiones tiene la variable
            len_dimensiones = len(variable.children[1:])
            self.declarar_variable(nombre, Tipo(tipo), len_dimensiones)

    def declarar_variable(self, nombre, tipo: Tipo, dimensiones: int):

        if tipo == Tipo.Void:
            raise SemanticError("Una variable no puede ser void")
        # checar si ya existe la variable en la lista de directorios
        for directorio in self.directoriosVariables:
            if nombre in directorio:
                raise SemanticError("ID ya existe")
        # Si no existe declararlo en el último directorio (-1)
        self.directoriosVariables[-1][str(nombre)
                                      ] = Variable(tipo, str(nombre), dimensiones)

    def analizar_decfunc(self, subtree: Tree) -> None:

        self.directoriosVariables.append({})
        tipo = Tipo(subtree.children[0].children[0])
        nombre = str(subtree.children[1].children[0])
        if nombre in self.directorioFunciones:
            raise SemanticError("funcion ya existe")

        arbol_parametros = subtree.children[2]
        lista_parametros = []
        # declarar los argumentos

        for parametro in arbol_parametros.children:
            nombre_parametro = parametro.children[0].children[0]
            tipo_parametro = Tipo(parametro.children[1].children[0])
            lista_parametros.append(tipo_parametro)
            self.declarar_variable(nombre_parametro, tipo_parametro, 0)

        decvars = subtree.children[-2]
        estatutos = subtree.children[-1].children

        for decvar in decvars.children:
            self.analizar_decvar(decvar)

        self.directorioFunciones[nombre] = Funcion(
            tipo, nombre, lista_parametros)

        # analizar el cuerpo de la función
        lista_tipos_return = self.analizar_estatutos(estatutos)

        if tipo == Tipo.Void and len(lista_tipos_return) != 0:
            raise SemanticError("Una funcion void no puede regresar nada")

        for tipo_return in lista_tipos_return:
            if tipo_return != tipo:
                raise SemanticError(
                    "No se puede regresar un tipo diferente a la función")
        # Cuando acabo de analizar las variables locales
        # las borro, por eso el pop
        self.directoriosVariables.pop()


######################### ANALIZAR ESTATUTOS #######################
# A cada función de analizar le llega el arbol que le corresponde
# Se asigna una a variable al valor de los nodos
#    Se analizan los valores


    def analizar_estatutos(self, estatutos: List[Tree]) -> List[Tipo]:
        results: List[Tipo] = []
        for estatuto in estatutos:
            tipo_resultado = self.analizar_estatuto(estatuto)
            results = results + tipo_resultado if tipo_resultado is not None else results
        return results

    def analizar_estatuto(self, estatuto: Tree):
        # (asignacion | expresion | if | while | forloop | return) ";"
        # El unico que regresa un valor es el return

        if estatuto.children[0].data == "expresion":
            self.analizar_expresion(estatuto.children[0])

        elif estatuto.children[0].data == "asignacion":
            self.analizar_asignacion(estatuto.children[0])

        elif estatuto.children[0].data == "if":
            return self.analizar_if(estatuto.children[0])

        elif estatuto.children[0].data == "return":
            return self.analizar_return(estatuto.children[0])

        elif estatuto.children[0].data == "forloop":
            return self.analizar_for(estatuto.children[0])

        elif estatuto.children[0].data == "while":
            return self.analizar_while(estatuto.children[0])

    def analizar_asignacion(self, arbol_asignacion: Tree) -> Tipo:
        # llamadavariable "=" expresion

        arbol_llamada_variable = arbol_asignacion.children[0]
        arbol_expresion = arbol_asignacion.children[1]

        tipo_llamada_variable = self.analizar_llamadavariable(
            arbol_llamada_variable)
        tipo_expresion = self.checar_void(
            self.analizar_expresion(arbol_expresion))

        # Comparar los tipos
        if tipo_llamada_variable != tipo_expresion:
            raise SemanticError("Tipos incompatibles")
        return tipo_expresion

# regresa booleano si es > o < else el tipo de la exp

    def analizar_expresion(self, expresion: Tree) -> Tipo:

        if len(expresion.children) == 1:
            exp = expresion.children[0]
            tipo = self.analizar_exp(exp)
            expresion.tipo = tipo
            return tipo
            # si es una comoparación
        elif len(expresion.children) == 3:
            exp1 = expresion.children[0]
            exp2 = expresion.children[2]
            tipo_exp1 = self.checar_void(self.analizar_exp(exp1))
            tipo_exp2 = self.checar_void(self.analizar_exp(exp2))

            if tipo_exp1 == tipo_exp2:
                expresion.tipo = Tipo.Bool
                return Tipo.Bool
                # return Tipo("bool")
            else:
                raise SemanticError("No se pueden comparar")

        else:
            raise SemanticError("Expresion mal formada")

    def analizar_exp(self, exp: Tree):
        return self.analizar_operacion_binaria(exp, self.analizar_termino)

    def analizar_termino(self, termino: Tree):
        return self.analizar_operacion_binaria(termino, self.analizar_factor)

    def analizar_factor(self, factor: Tree):
        if len(factor.children) == 1:
            expresion = factor.children[0]
            if expresion.data == "expresion":
                return self.analizar_expresion(expresion)
            else:
                return self.analizar_atomo(expresion)
        elif len(factor.children) == 2:
            atomo = factor.children[1]
            return self.checar_void(self.analizar_atomo(atomo))

        else:
            raise SemanticError("Factor mal formado")

    def analizar_atomo(self, atomo: Tree) -> Tipo:
        atomo = atomo.children[0]
        if isinstance(atomo, Token):

            if atomo.type == "CTEI":
                return Tipo.Int
            elif atomo.type == "CTEF":
                return Tipo.Float
            elif atomo.type == "CTESTR":
                return Tipo.String
            elif atomo.type == "CTEBOOL":
                return Tipo.Bool
        else:
            if atomo.data == "llamadavariable":
               # print(atomo.pretty())
                return self.analizar_llamadavariable(atomo)
                # que efectivamente si tenga las 2 dimensiones
            elif atomo.data == "funcionesespeciales":
                # Checar que se llame con el tipo correcto
                return self.analizar_funcionesespeciales(atomo)

            elif atomo.data == "llamadafuncion":
                # Checar que la función esté declarada
                # Que tiene la cantidad correcta de argumentos
                # Checar que los argumentos tengan el tipo correcto
                return self.analizar_llamadafuncion(atomo)
    
    def checar_que_exista_variable(self, arbol_llamada_variable:Tree)-> Variable:
        nombre_variable = str(arbol_llamada_variable.children[0].children[0])
        # Checar que esté declarada
        variable = None
        for directorio in self.directoriosVariables:
            if nombre_variable in directorio:
                variable = directorio[nombre_variable]
                break

        if variable is None:
            raise SemanticError("Error, la variable no esta declarada")
        
        return variable

    def analizar_llamadavariable(self, arbol_llamada_variable: Tree) -> Tipo:
        variable = self.checar_que_exista_variable(arbol_llamada_variable)
        # Checar que se llame con la cantidad de dimensiones correcta (por ejemplo si es una matriz de dos dimensiones)
        len_dimensiones = len(arbol_llamada_variable.children[1:])
        if len_dimensiones != variable.dimensiones:
            raise SemanticError("Dimensiones incorrectas")
        else:
            # Tengo que confirmar que son del mismo tipo, ejemplo 2+2 = int+int
            # Es lo último que se verifica (en la gramática)
            return variable.tipo

    # llamadafuncion :  id "(" (expresion  ("," expresion)*)? ")"
    def analizar_llamadafuncion(self, arbol_llamada_funcion: Tree) -> Tipo:
        nombre_funcion = arbol_llamada_funcion.children[0].children[0]

        lista_de_arboles_argumentos = arbol_llamada_funcion.children[1:]

        # 1. Checar que la funcion exista
        if nombre_funcion not in self.directorioFunciones:
            raise SemanticError("Función no declarada")

        funcion_declarada = self.directorioFunciones[nombre_funcion]

        # 2. checar que tenemos la cantidad correcta de argumentos
        cantidad_argumentos = len(lista_de_arboles_argumentos)
        cantidad_parametros = len(funcion_declarada.parametros)

        if cantidad_argumentos != cantidad_parametros:
            raise SemanticError("Cantidad incorrecta de argumentos")

        # 3. Checar que los argumentos sean del tipo correcto
        for (argumento, tipo_parametro) in zip(lista_de_arboles_argumentos, funcion_declarada.parametros):
            tipo_argumento = self.checar_void(
                self.analizar_expresion(argumento))
            if tipo_argumento != tipo_parametro:
                raise SemanticError(
                    f"Tipos no on iguales: {tipo_argumento} != {tipo_parametro}")

        return funcion_declarada.tipo

    def analizar_operacion_binaria(self, operacion: Tree, funcion):
        lista_operandos = operacion.children[::2]
        tipo = funcion(lista_operandos[0])
        # para que no se cheque el primero dos veces
        for operando in lista_operandos[1:]:
            if self.checar_void(funcion(operando)) != tipo:
                raise SemanticError("Tipos incompatibles")

        return tipo

    # if : "if" "(" expresion ")" "{" estatutos "}" else
    def analizar_if(self, arbol_if: Tree) -> List[Tipo]:
        arbol_expresion = arbol_if.children[0]
        arbol_estatutos = arbol_if.children[1]
        arbol_else = arbol_if.children[2]

        tipo_arbol_expresion = self.analizar_expresion(arbol_expresion)
        if tipo_arbol_expresion != Tipo.Bool:
            raise SemanticError("Tipo no booleano")

        lista_tipos_return_if = self.analizar_estatutos(
            arbol_estatutos.children)
        lista_tipos_return_else = self.analizar_else(arbol_else)

        # esto es para analizar los tipos de expresiones return dentro de los estatutos
        return lista_tipos_return_if + lista_tipos_return_else

    def analizar_else(self, arbol_else: Tree) -> List[Tipo]:
        if arbol_else.children:
            return self.analizar_estatutos(arbol_else.children[0].children)
        return []

    def analizar_return(self, arbol_return: Tree) -> List[Tipo]:
        expresion = arbol_return.children[0]
        # Regresa un tipo
        return [self.checar_void(self.analizar_expresion(expresion))]

    # while : "while" "(" expresion ")" "{" estatutos "}"
    def analizar_while(self, arbol_while: Tree) -> List[Tipo]:
        arbol_expresion_while = arbol_while.children[0]
        arbol_estatutos_while = arbol_while.children[1]

        tipo_expresion_while = self.analizar_expresion(arbol_expresion_while)
        lista_tipos_return = self.analizar_estatutos(
            arbol_estatutos_while.children)

        if tipo_expresion_while != Tipo.Bool:
            raise SemanticError("Tipo no booleano")

        return lista_tipos_return

    # forloop : "for" asignacion "to" expresion "{" estatutos "}"
    def analizar_for(self, arbol_forloop: Tree) -> List[Tipo]:
        arbol_asignacion_for = arbol_forloop.children[0]
        arbbol_expresion_for = arbol_forloop.children[1]
        arbol_estaturos_for = arbol_forloop.children[2]

        tipo_asig_for = self.analizar_asignacion(arbol_asignacion_for)
        if tipo_asig_for != Tipo.Int:
            raise SemanticError("Variable tiene que ser entero")

        tipo_expresion_for = self.analizar_expresion(arbbol_expresion_for)
        if tipo_expresion_for != Tipo.Int:
            raise SemanticError("Variable tiene que ser entero")

        return self.analizar_estatutos(arbol_estaturos_for.children)

    def analizar_funcionesespeciales(self, arbol_funcionesespeciales: Tree) -> Tipo:
        #funcionesespeciales : read | write | hist | mean | mode | avg | variance | print

        if arbol_funcionesespeciales.children[0].data == "read":
            self.analizar_funcion_especial(
                arbol_funcionesespeciales.children[0])
            return Tipo.Void

        elif arbol_funcionesespeciales.children[0].data == "write":
            self.analizar_write(arbol_funcionesespeciales.children[0])
            return Tipo.Void

        elif arbol_funcionesespeciales.children[0].data == "hist":
            self.analizar_hist(
                arbol_funcionesespeciales.children[0])
            return Tipo.Void

        elif arbol_funcionesespeciales.children[0].data == "mean":
            self.analizar_funcion_especial(
                arbol_funcionesespeciales.children[0], True)
            return Tipo.Float

        elif arbol_funcionesespeciales.children[0].data == "mode":
            self.analizar_funcion_especial(
                arbol_funcionesespeciales.children[0], True)
            return Tipo.Float

        elif arbol_funcionesespeciales.children[0].data == "variance":
            self.analizar_funcion_especial(
                arbol_funcionesespeciales.children[0], True)
            return Tipo.Float

    def analizar_write(self, arbol_print: Tree):

        for expresion in arbol_print.children:
            self.analizar_expresion(expresion)

    def analizar_funcion_especial(self, arbol_funcEsp: Tree, isNum=False):

        arbol_llamada_variable = arbol_funcEsp.children[0]
        variable = self.checar_que_exista_variable(
            arbol_llamada_variable)

        if len(variable.dimensiones) == 0: # --> Para ver si el valor de la dimension es mayor 0, entonces es arreglo
            raise SemanticError ("No se puede llamar a funcion especial con variable escalar")

        if isNum:
            if variable.tipo != Tipo.Int and variable.tipo != Tipo.Float:
                raise SemanticError(
                    "Esta función especial no se puede llamar con una variable NO numérica")

    def analizar_hist(self, arbol_hist:Tree) -> None:
        llamada_variable = arbol_hist.children[0]

        variable = self.checar_que_exista_variable(llamada_variable)

        if len(variable.dimensiones) != 2: # porque a fuerza tiene que ser una matriz
            raise SemanticError("Hist solo acepta variables de dos dimensiones")

        if variable.tipo != Tipo.Int and variable.tipo != Tipo.Float:
                raise SemanticError(
                    "Histo solo se puede llamar con variable numérica")
        

    def checar_void(self, tipo):

        if tipo == Tipo.Void:
            raise SemanticError(
                "No se puede completar una operación con tipo void")
        return tipo


def get_token(subtree: Tree, token_type: str):
    return [token.value for token in filter(lambda t: t.type == token_type,
                                            subtree.scan_values(
                                                lambda v: isinstance(v, Token))  # Los tokens del subtree
                                            )]


def chunker(seq, size):
    return (seq[pos: pos + size] for pos in range(0, len(seq), size))
