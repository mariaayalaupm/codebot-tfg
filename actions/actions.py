from typing import Any, Text, Dict, List
import json
import os
from datetime import datetime
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction


MINITESTS = {
    "tema0": [
        {
            "pregunta": (
                "Vamos a hacer un minitest del Tema 0: Introducción a la programación.\n\n"
                "Responde a las preguntas con a, b o c. \n\n"
                "Pregunta 1:\n"
                "¿Qué es un programa?\n\n"
                "a) Un lenguaje de programación\n"
                "b) Un conjunto de instrucciones que ejecuta el ordenador\n"
                "c) Un compilador"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. Un programa es un conjunto de instrucciones que ejecuta el ordenador para realizar una tarea concreta. Es decir, el ordenador no actúa por sí solo, sino que sigue las instrucciones que el programador ha escrito.",
            "feedback_incorrecto": "No es correcto. La respuesta correcta era b) Un conjunto de instrucciones que ejecuta el ordenador. Un lenguaje de programación sirve para escribir programas, y un compilador sirve para traducirlos, pero el programa en sí es el conjunto de instrucciones.",
        },
        {
            "pregunta": (
                "Pregunta 2:\n"
                "¿Qué hace la función main() en C?\n\n"
                "a) Marca el comienzo de la ejecución del programa\n"
                "b) Sirve para escribir comentarios\n"
                "c) Sirve para incluir librerías"
            ),
            "correcta": "a",
            "feedback_correcto": "Correcto. La función main() marca el punto de inicio de la ejecución de un programa en C. Cuando se ejecuta el programa, el ordenador empieza siguiendo las instrucciones que aparecen dentro de main().",
            "feedback_incorrecto": "No es correcto. La respuesta correcta era a) Marca el comienzo de la ejecución del programa. Los comentarios sirven para aclarar el código y las librerías se incluyen con #include, pero main() indica por dónde empieza a ejecutarse el programa.",
        },
        {
            "pregunta": (
                "Pregunta 3:\n"
                "¿Para qué sirve #include?\n\n"
                "a) Para repetir instrucciones\n"
                "b) Para incluir librerías o archivos de cabecera\n"
                "c) Para declarar variables"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. #include sirve para incluir librerías o archivos de cabecera. Esto permite usar funciones ya definidas, como printf o scanf cuando se incluye stdio.h.",
            "feedback_incorrecto": "No es correcto. La respuesta correcta era b) Para incluir librerías o archivos de cabecera. #include no repite instrucciones ni declara variables, sino que añade al programa código o funciones externas que se van a utilizar.",
        },
    ],
    "tema1": [
        {
            "pregunta": (
                "Vamos a hacer un minitest del Tema 1: Variables y tipos de datos.\n\n"
                "Responde a las preguntas con a, b o c. \n\n"
                "Pregunta 1:\n"
                "¿Qué es una variable?\n\n"
                "a) Un valor fijo que no cambia\n"
                "b) Un espacio de memoria donde se almacena un dato\n"
                "c) Un operador lógico"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. Una variable es un espacio de memoria donde se almacena un dato. Gracias a las variables podemos guardar información y utilizarla o modificarla posteriormente durante la ejecución del programa.",
            "feedback_incorrecto": "No es correcto. La respuesta correcta era b) Un espacio de memoria donde se almacena un dato. Una variable no es un valor fijo, ya que su contenido puede cambiar durante la ejecución del programa.",
        },
        {
            "pregunta": (
                "Pregunta 2:\n"
                "¿Cuál de estos es un tipo de dato entero en C?\n\n"
                "a) int\n"
                "b) float\n"
                "c) char*"
            ),
            "correcta": "a",
            "feedback_correcto": "Correcto. int es el tipo de dato utilizado para almacenar números enteros, es decir, números sin parte decimal.",
            "feedback_incorrecto": "No es correcto. La respuesta correcta era a) int. El tipo float se utiliza para números con decimales y char* suele emplearse para trabajar con cadenas de caracteres.",
        },
        {
            "pregunta": (
                "Pregunta 3:\n"
                "¿Qué significa asignar un valor a una variable?\n\n"
                "a) Compararla con otra\n"
                "b) Guardar un dato en ella\n"
                "c) Borrarla"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. Asignar un valor consiste en guardar un dato dentro de una variable para poder utilizarlo posteriormente en el programa.",
            "feedback_incorrecto": "No es correcto. La respuesta correcta era b) Guardar un dato en ella. La asignación permite almacenar información en una variable mediante el operador =.",
        },
    ],
    "tema2": [
        {
            "pregunta": (
                "Vamos a hacer un minitest del Tema 2: Entrada y salida.\n\n"
                "Responde a las preguntas con a, b o c. \n\n"
                "Pregunta 1:\n"
                "¿Para qué sirve printf?\n\n"
                "a) Para leer datos del usuario\n"
                "b) Para mostrar información por pantalla\n"
                "c) Para declarar variables"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. printf se utiliza para mostrar información por pantalla. Es una de las funciones más utilizadas en C para comunicar resultados o mensajes al usuario.",
            "feedback_incorrecto": "No es correcto. La respuesta correcta era b) Para mostrar información por pantalla. La función printf permite enviar texto, variables y resultados a la salida estándar, normalmente la pantalla.",
        },
        {
            "pregunta": (
                "Pregunta 2:\n"
                "¿Para qué sirve scanf?\n\n"
                "a) Para imprimir datos\n"
                "b) Para leer datos del usuario\n"
                "c) Para hacer operaciones"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. scanf se utiliza para leer datos introducidos por el usuario y almacenarlos en variables del programa.",
            "feedback_incorrecto": "No es correcto. La respuesta correcta era b) Para leer datos del usuario. scanf permite que el programa reciba información desde el teclado para trabajar posteriormente con ella.",
        },
        {
            "pregunta": (
                "Pregunta 3:\n"
                "¿Qué especificador se usa en printf para un entero?\n\n"
                "a) %f\n"
                "b) %c\n"
                "c) %d"
            ),
            "correcta": "c",
            "feedback_correcto": "Correcto. %d se usa para enteros.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era c) %d. El especificador %f se usa para números con decimales y %c para caracteres.",
        },
    ],
    "tema3": [
        {
            "pregunta": (
                "Vamos a hacer un minitest del Tema 3: Operadores.\n\n"
                "Responde a las preguntas con a, b o c. \n\n"
                "Pregunta 1:\n"
                "¿Qué operador se usa para obtener el resto de una división entre enteros?\n\n"
                "a) /\n"
                "b) %\n"
                "c) *"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. El operador % devuelve el resto de una división entre enteros. Por ejemplo, 7 % 3 devuelve 1 porque al dividir 7 entre 3 sobra 1.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era b) %. El operador % permite obtener el resto de una división entre enteros, mientras que / realiza la división y * la multiplicación.",
        },
        {
            "pregunta": (
                "Pregunta 2:\n"
                "¿Qué operador lógico devuelve verdadero solo si ambas condiciones son verdaderas?\n\n"
                "a) ||\n"
                "b) !\n"
                "c) &&"
            ),
            "correcta": "c",
            "feedback_correcto": "Correcto. && es el operador AND lógico. Una expresión que utiliza && solo será verdadera cuando todas las condiciones sean verdaderas.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era c) &&. El operador && representa el AND lógico, mientras que || significa OR y ! se utiliza para negar una condición.",
        },
        {
            "pregunta": (
                "Pregunta 3:\n"
                "¿Qué diferencia hay entre = y == en C?\n\n"
                "a) = compara y == asigna\n"
                "b) = asigna y == compara\n"
                "c) los dos comparan"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. = asigna un valor y == compara si dos valores son iguales.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era b) = asigna y == compara.",
        },
    ],
    "tema4": [
        {
            "pregunta": (
                "Vamos a hacer un minitest del Tema 4: Condicionales.\n\n"
                "Responde a las preguntas con a, b o c. \n\n"
                "Pregunta 1:\n"
                "¿Qué estructura se usa para ejecutar un bloque solo si se cumple una condición?\n\n"
                "a) for\n"
                "b) if\n"
                "c) switch"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. La respuesta buena es b) if. La estructura if permite ejecutar un bloque de instrucciones únicamente cuando se cumple una determinada condición.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era b) if. La estructura if sirve para ejecutar un bloque solo si se cumple una condición. for no es un bucle que repite instrucciones, y switch se usa para comparar una expresión con varios valores posibles.",
        },
        {
            "pregunta": (
                "Pregunta 2:\n"
                "¿Qué parte de una estructura if-else se ejecuta cuando la condición es falsa?\n\n"
                "a) if\n"
                "b) else\n"
                "c) case"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. La respuesta buena es b) else.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era b) else. El bloque else se ejecuta cuando la condición del if es falsa. La opción if corresponde al bloque que se ejecuta cuando la condición es verdadera, mientras que case se utiliza dentro de una estructura switch.",
        },
        {
            "pregunta": (
                "Pregunta 3:\n"
                "¿Qué sentencia se usa cuando quieres comparar una expresión con varios valores?\n\n"
                "a) switch\n"
                "b) while\n"
                "c) printf"
            ),
            "correcta": "a",
            "feedback_correcto": "Correcto. La respuesta buena es a) switch.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era a) switch. La estructura switch se utiliza cuando queremos comparar una expresión con varios valores posibles. while es un bucle que repite instrucciones mientras se cumpla una condición y printf se utiliza para mostrar información por pantalla.",
        },
    ],
    "tema5": [
        {
            "pregunta": (
                "Vamos a hacer un minitest del Tema 5: Bucles.\n\n"
                "Responde a las preguntas con a, b o c. \n\n"
                "Pregunta 1:\n"
                "¿Qué bucle se usa normalmente cuando sabes cuántas repeticiones quieres hacer?\n\n"
                "a) for\n"
                "b) while\n"
                "c) if"
            ),
            "correcta": "a",
            "feedback_correcto": "Correcto. El bucle for se usa normalmente cuando sabes cuántas repeticiones quieres hacer.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era a) for. El bucle for suele utilizarse cuando conocemos el número de repeticiones que queremos realizar. El bucle while se emplea cuando la repetición depende de una condición y no necesariamente sabemos cuántas veces se ejecutará. La estructura if no es un bucle, sino una estructura condicional.",
        },
        {
            "pregunta": (
                "Pregunta 2:\n"
                "¿Qué bucle garantiza que el bloque se ejecuta al menos una vez?\n\n"
                "a) while\n"
                "b) do while\n"
                "c) for"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. El bucle do while comprueba la condición al final de cada iteración, por lo que el bloque de instrucciones se ejecuta al menos una vez.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era b) do while. Este bucle evalúa la condición después de ejecutar el bloque de instrucciones, garantizando al menos una ejecución. En cambio, while y for comprueban la condición antes de ejecutar el bloque, por lo que podrían no ejecutarse ninguna vez.",
        },
        {
            "pregunta": (
                "Pregunta 3:\n"
                "¿Para qué sirve break dentro de un bucle?\n\n"
                "a) Para volver al inicio del programa\n"
                "b) Para salir inmediatamente del bucle\n"
                "c) Para repetir la iteración actual"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. break sirve para salir inmediatamente del bucle.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era b) break, para salir inmediatamente del bucle. La instrucción break finaliza la ejecución del bucle en ese momento. No sirve para volver al inicio del programa ni para repetir la iteración actual.",
        },
    ],
    "tema6": [
        {
            "pregunta": (
                "Vamos a hacer un minitest del Tema 6: Funciones.\n\n"
                "Responde a las preguntas con a, b o c. \n\n"
                "Pregunta 1:\n"
                "¿Qué es un prototipo de función en C?\n\n"
                "a) La llamada a una función dentro del main\n"
                "b) Una declaración previa que indica cómo es la función\n"
                "c) Una variable local"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. Un prototipo es una declaración previa que indica el nombre de la función, el tipo de dato que devuelve y los parámetros que recibe.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era b) Una declaración previa que indica cómo es la función.  La llamada a una función dentro de main es simplemente su utilización, y una variable local es una variable que solo existe dentro de una función o bloque concreto.",
        },
        {
            "pregunta": (
                "Pregunta 2:\n"
                "¿Qué significa que una función tenga tipo de retorno void?\n\n"
                "a) No recibe parámetros\n"
                "b) No devuelve ningún valor\n"
                "c) No puede ejecutarse"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. Una función void no devuelve ningún valor.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era b) No devuelve ningún valor. Una función void puede recibir parámetros si se definen en su cabecera, y también puede ejecutarse normalmente. Lo único que indica void es que la función no devuelve ningún resultado.",
        },
        {
            "pregunta": (
                "Pregunta 3:\n"
                "Si una función recibe una variable por valor y modifica el parámetro dentro de la función, ¿qué ocurre con la variable original?\n\n"
                "a) También se modifica\n"
                "b) Permanece igual\n"
                "c) Se elimina"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. Cuando una variable se pasa por valor, la función trabaja con una copia. Por ello, los cambios realizados dentro de la función no afectan a la variable original.",
            "feedback_incorrecto": "No es correcto. La respuesta correcta era b) Permanece igual. Cuando una variable se pasa por valor, la función recibe una copia y cualquier modificación afecta únicamente a esa copia. La variable original conserva su valor, ni se modifica ni se elimina.",
        },
    ],
    "tema7": [
        {
            "pregunta": (
                "Vamos a hacer un minitest del Tema 7: Arrays.\n\n"
                "Responde a las preguntas con a, b o c. \n\n"
                "Pregunta 1:\n"
                "¿Qué es un array?\n\n"
                "a) Una estructura que almacena varios valores del mismo tipo\n"
                "b) Una función especial de C\n"
                "c) Un operador lógico"
            ),
            "correcta": "a",
            "feedback_correcto": "Correcto. Un array permite almacenar varios valores del mismo tipo bajo un mismo nombre.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era a) Una estructura que almacena varios valores del mismo tipo. Un array sirve para guardar varios datos relacionados en posiciones consecutivas de memoria. No es una función especial de C ni un operador lógico utilizado en expresiones.",
        },
        {
            "pregunta": (
                "Pregunta 2:\n"
                "¿En qué índice empieza un array en C?\n\n"
                "a) En 1\n"
                "b) En 0\n"
                "c) Depende del array"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. En C los arrays empiezan en el índice 0.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era b) En 0.",
        },
        {
            "pregunta": (
                "Pregunta 3:\n"
                "¿Qué problema puede ocurrir si accedes a una posición fuera del array?\n\n"
                "a) Ninguno, el programa corrige el índice\n"
                "b) Se repite el último valor\n"
                "c) Puede haber errores o resultados inesperados"
            ),
            "correcta": "c",
            "feedback_correcto": "Correcto. Acceder fuera del array puede provocar errores o resultados inesperados.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era c). Por ejemplo, si un array tiene 5 elementos, sus posiciones van de 0 a 4. Si intentas acceder a la posición 10, el programa intentará leer una zona de memoria que no pertenece al array. Por eso pueden aparecer errores o valores extraños. El programa no corrige automáticamente el índice ni repite el último valor.",
        },
    ],
    "tema8": [
        {
            "pregunta": (
                "Vamos a hacer un minitest del Tema 8: Strings.\n\n"
                "Responde a las preguntas con a, b o c. \n\n"
                "Pregunta 1:\n"
                "¿Qué es una cadena en C?\n\n"
                "a) Un número entero especial\n"
                "b) Un array de caracteres\n"
                "c) Un tipo de bucle"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. Una cadena en C es un array de caracteres terminado en '\\0'.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era b) Un array de caracteres. Una cadena se utiliza para almacenar texto, por lo que está formada por varios caracteres guardados en posiciones consecutivas de memoria. No es un número entero ni una estructura de control como un bucle.",
        },
        {
            "pregunta": (
                "Pregunta 2:\n"
                "¿Qué función se usa para calcular la longitud de una cadena?\n\n"
                "a) strcpy\n"
                "b) strcat\n"
                "c) strlen"
            ),
            "correcta": "c",
            "feedback_correcto": "Correcto. strlen se usa para calcular la longitud de una cadena.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era c) strlen. Esta función cuenta el número de caracteres de una cadena. strcpy se utiliza para copiar cadenas y strcat para concatenarlas, es decir, unir una cadena al final de otra.",
        },
        {
            "pregunta": (
                "Pregunta 3:\n"
                "¿Qué representa el carácter '\\0' en una cadena?\n\n"
                "a) El inicio de la cadena\n"
                "b) El final de la cadena\n"
                "c) Un espacio en blanco"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. '\\0' indica el final de la cadena.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era b) El final de la cadena. Cuando el programa encuentra '\\0', sabe que ya no quedan más caracteres. No representa el inicio de la cadena ni un espacio en blanco.",
        },
    ],
    "tema9": [
        {
            "pregunta": (
                "Vamos a hacer un minitest del Tema 9: Punteros.\n\n"
                "Responde a las preguntas con a, b o c. \n\n"
                "Pregunta 1:\n"
                "¿Qué es un puntero?\n\n"
                "a) Una variable que almacena un número entero\n"
                "b) Una variable que almacena la dirección de memoria de otra variable\n"
                "c) Una función especial de C"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. Un puntero almacena la dirección de memoria de otra variable.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era b) Una variable que almacena la dirección de memoria de otra variable. Mientras que una variable normal almacena un dato como un número o un carácter, un puntero almacena la dirección donde se encuentra ese dato en memoria. Tampoco es una función especial de C.",
        },
        {
            "pregunta": (
                "Pregunta 2:\n"
                "¿Qué operador se usa para obtener la dirección de una variable?\n\n"
                "a) *\n"
                "b) &\n"
                "c) %"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. El operador & se usa para obtener la dirección de memoria de una variable.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era b) &. Por ejemplo, si tenemos una variable llamada edad, la expresión &edad devuelve la dirección de memoria donde está almacenada. El operador * se utiliza para acceder al valor apuntado por un puntero y % se utiliza, entre otras cosas, para obtener el resto de una división entre enteros.",
        },
        {
            "pregunta": (
                "Pregunta 3:\n"
                "¿Qué hace el operador * aplicado a un puntero?\n\n"
                "a) Obtiene la dirección de memoria\n"
                "b) Accede al valor almacenado en la dirección\n"
                "c) Declara una variable nueva"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. El operador * permite acceder al valor al que apunta el puntero.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era b) Accede al valor almacenado en la dirección. Si un puntero apunta a una variable que contiene el valor 5, al utilizar * sobre ese puntero obtenemos ese 5. La dirección de memoria se obtiene con &, y * no sirve para declarar una variable nueva.",
        },
    ],
    "tema10": [
        {
            "pregunta": (
                "Vamos a hacer un minitest del Tema 10: Structs.\n\n"
                "Responde a las preguntas con a, b o c. \n\n"
                "Pregunta 1:\n"
                "¿Para qué sirve un struct en C?\n\n"
                "a) Para agrupar varias variables de distintos tipos bajo un mismo nombre\n"
                "b) Para repetir instrucciones\n"
                "c) Para comparar valores lógicos"
            ),
            "correcta": "a",
            "feedback_correcto": "Correcto. Un struct sirve para agrupar varias variables de distintos tipos bajo un mismo nombre.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era a) Para agrupar varias variables de distintos tipos bajo un mismo nombre. Un struct se utiliza para organizar datos relacionados en una única estructura. No sirve para repetir instrucciones como los bucles ni para realizar comparaciones lógicas.",
        },
        {
            "pregunta": (
                "Pregunta 2:\n"
                "¿Qué operador se usa para acceder a un campo de una variable struct?\n\n"
                "a) ->\n"
                "b) .\n"
                "c) &"
            ),
            "correcta": "b",
            "feedback_correcto": "Correcto. El operador punto se usa para acceder a campos de una variable struct.",
            "feedback_incorrecto": "No es correcto. La respuesta buena era b). . Por ejemplo, si persona es una variable de tipo struct, persona.edad permite acceder al campo edad. El operador -> se utiliza cuando trabajamos con un puntero a struct y & sirve para obtener direcciones de memoria.",
        },
        {
            "pregunta": (
                "Pregunta 3:\n"
                "¿Qué operador se utiliza para acceder al campo edad si p es un puntero que apunta a una estructura Persona?\n\n\n\n"
                "a) p.edad\n"
                "b) *p.edad\n"
                "c) p->edad"
            ),
            "correcta": "c",
            "feedback_correcto": "Correcto.",
            "feedback_incorrecto": "No es correcto. La respuesta correcta era c) p->edad. Cuando p es un puntero a una estructura, se utiliza el operador -> para acceder a sus campos. La expresión p.edad solo sería válida si p fuera una variable struct normal y no un puntero.",
        },
    ],
}


def texto_a_tema(texto: Text) -> Text | None:
    if not texto:
        return None

    t = texto.lower().strip()

    # Detectar formato "tema X"
    if t.startswith("tema "):
        numero = t.replace("tema ", "").strip()
        if numero.isdigit():
            return f"tema{numero}"

    mapa = {

        "introduccion": "tema0",
        "introducción": "tema0",
        "introduccion a la programacion": "tema0",
        "introducción a la programación": "tema0",

        "variables": "tema1",
        "variables y tipos": "tema1",
        "variables y tipos de datos": "tema1",

        "entrada y salida": "tema2",
        "entrada salida": "tema2",
        "printf y scanf": "tema2",

        "operadores": "tema3",
        "operadores aritmeticos": "tema3",
        "operadores aritméticos": "tema3",
        "tema de operadores": "tema3",

        "condicionales": "tema4",
        "tema condicionales": "tema4",

        "bucles": "tema5",
        "tema de bucles": "tema5",
        "loops": "tema5",

        "funciones": "tema6",
        "función": "tema6",
        "tema de funciones": "tema6",

        "arrays": "tema7",
        "array": "tema7",
        "vectores": "tema7",
        "tema de arrays": "tema7",

        "strings": "tema8",
        "string": "tema8",
        "cadenas": "tema8",
        "cadenas de caracteres": "tema8",
        "tema de strings": "tema8",

        "punteros": "tema9",
        "puntero": "tema9",
        "direcciones de memoria": "tema9",
        "tema de punteros": "tema9",

        "structs": "tema10",
        "struct": "tema10",
        "estructuras": "tema10",
        "tema de structs": "tema10",
    }

    return mapa.get(t)


def intent_a_respuesta(intent_name: Text) -> Text | None:
    mapa = {
        "respuesta_a": "a",
        "respuesta_b": "b",
        "respuesta_c": "c",
    }
    return mapa.get(intent_name)

def guardar_resultado_minitest(
    user_id: Text,
    tema: Text,
    indice_pregunta: int,
    es_correcta: bool,
    respuesta_usuario: Text,
    respuesta_correcta: Text,
    username: Text = None,
    first_name: Text = None,
    last_name: Text = None,
) -> None:
    """
    Guarda el resultado de una respuesta del minitest en un archivo JSON local.
    Esta primera versión sirve como prototipo de seguimiento del progreso del alumno.
    """

    ruta_archivo = "progreso_alumnos.json"

    nuevo_registro = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "tema": tema,
        "pregunta": indice_pregunta + 1,
        "correcta": es_correcta,
        "respuesta_usuario": respuesta_usuario,
        "respuesta_correcta": respuesta_correcta,
        "fecha": datetime.now().isoformat(timespec="seconds"),
    }

    if os.path.exists(ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except json.JSONDecodeError:
            datos = []
    else:
        datos = []

    datos.append(nuevo_registro)

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

def guardar_intento_minitest(
    user_id: Text,
    tema: Text,
    puntuacion: int,
    total_preguntas: int,
    respuestas: List[Dict[Text, Any]],
    username: Text = None,
    first_name: Text = None,
    last_name: Text = None,
) -> None:
    """
    Guarda un intento completo de minitest como una única entrada en el archivo JSON.
    """

    ruta_archivo = "progreso_alumnos.json"

    nuevo_registro = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "tema": tema,
        "puntuacion": puntuacion,
        "total_preguntas": total_preguntas,
        "porcentaje_acierto": round((puntuacion / total_preguntas) * 100, 2),
        "respuestas": respuestas,
        "fecha": datetime.now().isoformat(timespec="seconds"),
    }

    if os.path.exists(ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except json.JSONDecodeError:
            datos = []
    else:
        datos = []

    datos.append(nuevo_registro)

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

def guardar_consulta_ejercicio_guiado(
    user_id: Text,
    ejercicio_id: Text,
    ejercicio_titulo: Text,
    tema: Text,
    username: Text = None,
    first_name: Text = None,
    last_name: Text = None,
) -> None:
    """
    Guarda en un archivo JSON cada consulta realizada a un ejercicio guiado.
    """

    ruta_archivo = "progreso_ejercicios_guiados.json"

    nuevo_registro = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "tipo_actividad": "ejercicio_guiado",
        "ejercicio_id": ejercicio_id,
        "ejercicio_titulo": ejercicio_titulo,
        "tema": tema,
        "fecha": datetime.now().isoformat(timespec="seconds"),
    }

    if os.path.exists(ruta_archivo):
        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except json.JSONDecodeError:
            datos = []
    else:
        datos = []

    datos.append(nuevo_registro)

    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

def recomendar_ejercicio_por_tema(tema: Text) -> Text:
    """
    Devuelve una recomendación de ejercicio guiado en función del tema del minitest.
    """

    recomendaciones = {
        "tema1": "Te recomiendo revisar el Ejercicio guiado 1: Variables y operadores, porque te ayudará a reforzar el uso de variables, fórmulas y operaciones básicas.",
        "tema3": "Te recomiendo revisar el Ejercicio guiado 1: Variables y operadores, porque también trabaja operaciones y expresiones en C.",
        "tema4": "Te recomiendo revisar el Ejercicio guiado 2: Condicionales, porque está relacionado con el uso de if, else if y condiciones compuestas.",
        "tema5": "Te recomiendo revisar el Ejercicio guiado 3: Bucles, porque te ayudará a practicar la repetición de instrucciones y el uso de while.",
        "tema6": "Te recomiendo revisar el Ejercicio guiado 4: Funciones, porque trabaja la definición de funciones, parámetros y valor de retorno.",
        "tema7": "Te recomiendo revisar el Ejercicio guiado 5: Arrays, porque te ayudará a practicar el recorrido de arrays con bucles.",
        "tema8": "Te recomiendo revisar el Ejercicio guiado 6: Strings, porque trabaja el recorrido de cadenas carácter a carácter.",
        "tema9": "Te recomiendo revisar el Ejercicio guiado 7: Punteros, porque está relacionado con direcciones de memoria y paso por referencia.",
        "tema10": "Te recomiendo revisar el Ejercicio guiado 8: Structs, porque te ayudará a practicar el acceso a campos de una estructura.",
    }

    return recomendaciones.get(
        tema,
        "Te recomiendo volver a la teoría de este tema antes de repetir el minitest."
    )

def nombre_tema(tema: Text) -> Text:
    nombres = {
        "tema0": "Tema 0 - Introducción a la programación",
        "tema1": "Tema 1 - Variables y tipos de datos",
        "tema2": "Tema 2 - Entrada y salida",
        "tema3": "Tema 3 - Operadores",
        "tema4": "Tema 4 - Condicionales",
        "tema5": "Tema 5 - Bucles",
        "tema6": "Tema 6 - Funciones",
        "tema7": "Tema 7 - Arrays",
        "tema8": "Tema 8 - Strings",
        "tema9": "Tema 9 - Punteros",
        "tema10": "Tema 10 - Structs",
    }

    return nombres.get(tema, tema)

def generar_feedback_adaptativo(puntuacion: int, total_preguntas: int, tema: Text) -> Text:
    """
    Genera un mensaje final adaptado al rendimiento del alumno.
    """

    recomendacion = recomendar_ejercicio_por_tema(tema)

    if puntuacion == total_preguntas:
        return (
            "Resultado excelente. Parece que dominas bastante bien este tema. "
            "Puedes seguir practicando con otros bloques del temario."
        )

    if puntuacion >= total_preguntas - 1:
        return (
            "Buen resultado. Tienes una base bastante sólida, aunque te recomiendo repasar "
            "la pregunta que has fallado para afianzar el concepto.\n\n"
            f"{recomendacion}"
        )

    if puntuacion == 1:
        return (
            "Te recomiendo repasar este tema antes de continuar. Has acertado una pregunta, "
            "pero todavía hay conceptos importantes que conviene reforzar.\n\n"
            f"{recomendacion}"
        )

    return (
        "Te recomiendo volver a la teoría de este tema antes de repetir el minitest. "
        "Parece que necesitas reforzar los conceptos básicos.\n\n"
        f"{recomendacion}"
    )

class ActionPedirTemaMinitest(Action):
    def name(self) -> Text:
        return "action_pedir_tema_minitest"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text=(
                "Claro. ¿De qué tema quieres hacer el minitest?\n\n"
                "Respóndeme con uno de estos temas:\n"
                "- 0. introducción\n"
                "- 1. variables y tipos de datos\n"
                "- 2. entrada y salida\n"
                "- 3. operadores\n"
                "- 4. condicionales\n"
                "- 5. bucles\n"
                "- 6. funciones\n"
                "- 7. arrays\n"
                "- 8. strings\n"
                "- 9. punteros\n"
                "- 10. structs\n"
                "Puedes elegir diciendo tema x, el nombre del tema, o pulsando el botón del tema correspondiente"
            )
        )

        return [ SlotSet("minitest_activo", "esperando_tema"),
                SlotSet("modo_conversacion", "minitest"),]


class ActionIniciarMinitest(Action):
    def name(self) -> Text:
        return "action_iniciar_minitest"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        texto_usuario = tracker.latest_message.get("text", "")
        tema = texto_a_tema(texto_usuario)

        if tema is None or tema not in MINITESTS:
            dispatcher.utter_message(
                text=(
                    "No he podido identificar el tema del minitest.\n\n"
                    "Respóndeme con el nombre del tema, por ejemplo:\n"
                    "- Introducción a la programación\n"
                    "- Variables y tipos de datos\n"
                    "- Entrada y salida\n"
                    "- Operadores\n"
                    "- Condicionales\n"
                    "- Bucles\n"
                    "- Funciones\n"
                    "- Arrays\n"
                    "- Strings\n"
                    "- Punteros\n"
                    "- Structs"
                )
            )
            return [SlotSet("minitest_activo", "esperando_tema"),
                    SlotSet("modo_conversacion", "minitest"),]

        primera_pregunta = MINITESTS[tema][0]["pregunta"]
        dispatcher.utter_message(text=primera_pregunta)

        return [
            SlotSet("minitest_activo", "en_curso"),
            SlotSet("modo_conversacion", "minitest"),
            SlotSet("tema_minitest", tema),
            SlotSet("pregunta_actual", "0"),
            SlotSet("puntuacion_minitest", 0),
            SlotSet("respuestas_minitest", []),
        ]


class ActionProcesarRespuestaMinitest(Action):
    def name(self) -> Text:
        return "action_procesar_respuesta_minitest"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        tema = tracker.get_slot("tema_minitest")
        pregunta_actual = tracker.get_slot("pregunta_actual")
        puntuacion = tracker.get_slot("puntuacion_minitest")
        respuestas_minitest = tracker.get_slot("respuestas_minitest")

        if respuestas_minitest is None:
            respuestas_minitest = []

        if puntuacion is None:
            puntuacion = 0

        if tema is None or tema not in MINITESTS or pregunta_actual is None:
            dispatcher.utter_message(text="Ahora mismo no hay ningún minitest activo.")
            return []

        try:
            indice = int(pregunta_actual)
        except ValueError:
            dispatcher.utter_message(text="Ha habido un problema con el estado del minitest.")
            return []

        ultimo_intent = tracker.latest_message.get("intent", {}).get("name")
        respuesta_usuario = intent_a_respuesta(ultimo_intent)

        if respuesta_usuario is None:
            dispatcher.utter_message(text="No he entendido tu respuesta. Contesta con a, b o c.")
            return []

        pregunta = MINITESTS[tema][indice]
        es_correcta = respuesta_usuario == pregunta["correcta"]

        if es_correcta:
            dispatcher.utter_message(text=pregunta["feedback_correcto"])
            puntuacion += 1
        else:
            dispatcher.utter_message(text=pregunta["feedback_incorrecto"])

        metadata = tracker.latest_message.get("metadata", {})

        # guardar_resultado_minitest(
        #     user_id=tracker.sender_id,
        #     username=metadata.get("username"),
        #     first_name=metadata.get("first_name"),
        #     last_name=metadata.get("last_name"),
        #     tema=tema,
        #     indice_pregunta=indice,
        #     es_correcta=es_correcta,
        #     respuesta_usuario=respuesta_usuario,
        #     respuesta_correcta=pregunta["correcta"],
        # )
        siguiente_indice = indice + 1

        respuestas_minitest.append(
            {
                "pregunta": indice + 1,
                "respuesta_usuario": respuesta_usuario,
                "respuesta_correcta": pregunta["correcta"],
                "correcta": es_correcta,
            }
        )

        if siguiente_indice < len(MINITESTS[tema]):
            dispatcher.utter_message(text=MINITESTS[tema][siguiente_indice]["pregunta"])
            return [
                SlotSet("pregunta_actual", str(siguiente_indice)),
                SlotSet("puntuacion_minitest", puntuacion),
                SlotSet("respuestas_minitest", respuestas_minitest),
            ]

        guardar_intento_minitest(
            user_id=tracker.sender_id,
            username=metadata.get("username"),
            first_name=metadata.get("first_name"),
            last_name=metadata.get("last_name"),
            tema=tema,
            puntuacion=puntuacion,
            total_preguntas=len(MINITESTS[tema]),
            respuestas=respuestas_minitest,
        )
        feedback_final = generar_feedback_adaptativo(
            puntuacion=puntuacion,
            total_preguntas=len(MINITESTS[tema]),
            tema=tema,
        )

        dispatcher.utter_message(
            text=(
                f"Has completado el minitest. Tu puntuación ha sido "
                f"{puntuacion} de {len(MINITESTS[tema])}.\n\n"
                f"{feedback_final}"
            )
        )
        return [
            SlotSet("minitest_activo", None),
            SlotSet("tema_minitest", None),
            SlotSet("pregunta_actual", None),
            SlotSet("puntuacion_minitest", None),
            SlotSet("respuestas_minitest", None),
            SlotSet("modo_conversacion", "general"),
            SlotSet("numero_tema", None),
            FollowupAction("action_listen"),
        ]
    
class ActionRespuestaInvalidaMinitest(Action):
    def name(self) -> Text:
        return "action_respuesta_invalida_minitest"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        if tracker.get_slot("minitest_activo") == "en_curso":
            dispatcher.utter_message(
                text="En el minitest solo puedes responder con a, b o c."
            )
        else:
            dispatcher.utter_message(
                text=" No estoy seguro de haber entendido tu pregunta. Por favor, reformúlala. Estoy aquí para ayudarte"
            )

        return []
    
class ActionMostrarTema(Action):

    def name(self) -> Text:
        return "action_mostrar_tema"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        tema = tracker.get_slot("numero_tema")

        if tema == "0":
            dispatcher.utter_message(response="utter_tema_introduccion")

        elif tema == "1":
            dispatcher.utter_message(response="utter_tema_variables_tipos")

        elif tema == "2":
            dispatcher.utter_message(response="utter_tema_entrada_salida")

        elif tema == "3":
            dispatcher.utter_message(response="utter_tema_operadores")

        elif tema == "4":
            dispatcher.utter_message(response="utter_tema_condicionales")

        elif tema == "5":
            dispatcher.utter_message(response="utter_tema_bucles")

        elif tema == "6":
            dispatcher.utter_message(response="utter_tema_funciones")

        elif tema == "7":
            dispatcher.utter_message(response="utter_tema_arrays")

        elif tema == "8":
            dispatcher.utter_message(response="utter_tema_strings")

        elif tema == "9":
            dispatcher.utter_message(response="utter_tema_punteros")

        elif tema == "10":
            dispatcher.utter_message(response="utter_tema_structs")

        else:
            dispatcher.utter_message(text="No he reconocido ese tema. Prueba con 'tema 0', 'tema 1', etc.")

        return [ SlotSet("modo_conversacion", "general"),
                    SlotSet("minitest_activo", None),]
    

class ActionGestionarEleccionTema(Action):
    def name(self) -> Text:
        return "action_gestionar_eleccion_tema"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        modo = tracker.get_slot("modo_conversacion")
        minitest_activo = tracker.get_slot("minitest_activo")
        texto_usuario = tracker.latest_message.get("text", "")
        numero_tema = tracker.get_slot("numero_tema")

        # Caso 1: estamos esperando el tema de un minitest
        if modo == "minitest" and minitest_activo == "esperando_tema":
            tema = texto_a_tema(texto_usuario)

            if tema is None or tema not in MINITESTS:
                dispatcher.utter_message(
                    text=(
                        "No he podido identificar el tema del minitest.\n\n"
                        "Respóndeme con el nombre del tema o con un formato como 'tema 1'."
                    )
                )
                return [
                    SlotSet("minitest_activo", "esperando_tema"),
                    SlotSet("modo_conversacion", "minitest"),
                ]

            primera_pregunta = MINITESTS[tema][0]["pregunta"]
            dispatcher.utter_message(text=primera_pregunta)

            return [
                SlotSet("minitest_activo", "en_curso"),
                SlotSet("modo_conversacion", "minitest"),
                SlotSet("tema_minitest", tema),
                SlotSet("pregunta_actual", "0"),
                SlotSet("puntuacion_minitest", 0),
                SlotSet("respuestas_minitest", []),
            ]

        # Caso 2: modo general -> mostrar teoría
        # Si el usuario ha escrito "tema 9", usamos el slot numero_tema.
        # Si ha escrito "punteros", "strings", "arrays", etc., lo convertimos con texto_a_tema().
        tema_por_texto = texto_a_tema(texto_usuario)

        if numero_tema is None and tema_por_texto is not None:
            numero_tema = tema_por_texto.replace("tema", "")


        if numero_tema == "0":
            dispatcher.utter_message(response="utter_tema_introduccion")
        elif numero_tema == "1":
            dispatcher.utter_message(response="utter_tema_variables_tipos")
        elif numero_tema == "2":
            dispatcher.utter_message(response="utter_tema_entrada_salida")
        elif numero_tema == "3":
            dispatcher.utter_message(response="utter_tema_operadores")
        elif numero_tema == "4":
            dispatcher.utter_message(response="utter_tema_condicionales")
        elif numero_tema == "5":
            dispatcher.utter_message(response="utter_tema_bucles")
        elif numero_tema == "6":
            dispatcher.utter_message(response="utter_tema_funciones")
        elif numero_tema == "7":
            dispatcher.utter_message(response="utter_tema_arrays")
        elif numero_tema == "8":
            dispatcher.utter_message(response="utter_tema_strings")
        elif numero_tema == "9":
            dispatcher.utter_message(response="utter_tema_punteros")
        elif numero_tema == "10":
            dispatcher.utter_message(response="utter_tema_structs")
        else:
            dispatcher.utter_message(
                text="No he reconocido ese tema. Prueba con 'tema 0', 'tema 1', etc."
            )

        return [
            SlotSet("modo_conversacion", "general"),
            SlotSet("minitest_activo", None),
            SlotSet("numero_tema", None),
        ]
    

EJERCICIOS_GUIADOS = {
    "ejercicio1": {
        "titulo": "Variables y operadores: superficie de una esfera",
        "tema": "Tema 1 - Variables y operadores",
        "texto": (
            "Ejercicio guiado 1: Variables y operadores\n"
            "Superficie de una esfera\n\n"
            "1. Enunciado del problema\n"
            "Escribir un programa en C que solicite al usuario el radio de una esfera "
            "y calcule su superficie.\n\n"
            "La fórmula de la superficie de una esfera es:\n"
            "S = 4 * PI * radio * radio\n\n"
            "2. ¿Qué nos piden?\n"
            "Nos piden construir un programa que:\n"
            "- Lea el valor del radio.\n"
            "- Calcule la superficie aplicando la fórmula.\n"
            "- Muestre el resultado por pantalla.\n\n"
            "3. Variables que necesitamos\n"
            "Necesitamos una variable para guardar el radio y otra para guardar la superficie:\n\n"
            "float radio;\n"
            "float superficie;\n\n"
            "También usamos una constante para PI:\n\n"
            "#define PI 3.1416\n\n"
            "4. Estrategia para resolverlo\n"
            "Primero pedimos el radio al usuario. Después calculamos la superficie usando "
            "la fórmula. Por último, mostramos el resultado con printf.\n\n"
            "5. Construcción del código paso a paso\n"
            "Incluimos la librería:\n\n"
            "#include <stdio.h>\n\n"
            "Definimos PI:\n\n"
            "#define PI 3.1416\n\n"
            "Declaramos las variables:\n\n"
            "float radio;\n"
            "float superficie;\n\n"
            "Pedimos el radio:\n\n"
            "printf(\"Introduce el radio: \");\n"
            "scanf(\"%f\", &radio);\n\n"
            "Calculamos la superficie:\n\n"
            "superficie = 4 * PI * radio * radio;\n\n"
            "Mostramos el resultado:\n\n"
            "printf(\"La superficie de la esfera es: %.2f\", superficie);\n\n"
            "6. Código completo\n\n"
            "#include <stdio.h>\n\n"
            "#define PI 3.1416\n\n"
            "int main() {\n"
            "    float radio;\n"
            "    float superficie;\n\n"
            "    printf(\"Introduce el radio: \");\n"
            "    scanf(\"%f\", &radio);\n\n"
            "    superficie = 4 * PI * radio * radio;\n\n"
            "    printf(\"La superficie de la esfera es: %.2f\", superficie);\n\n"
            "    return 0;\n"
            "}\n\n"
            "7. Ejemplo de ejecución\n"
            "Si el usuario introduce 2, el cálculo sería:\n\n"
            "superficie = 4 * 3.1416 * 2 * 2;\n"
            "superficie = 50.2656;\n\n"
            "8. Resultado\n"
            "La superficie de la esfera es: 50.27"
        ),
    },

    "ejercicio2": {
        "titulo": "Condicionales: valor central de tres números",
        "tema": "Tema 4 - Condicionales",
        "texto": """Ejercicio guiado 2: Condicionales
            Valor central de tres números

            1. Enunciado del problema
            Escribir un programa en C que lea tres números reales distintos y muestre cuál es el valor central, es decir, el que no es ni el mayor ni el menor.

            2. ¿Qué nos piden?
            Nos piden identificar el número que queda en medio de tres valores.

            Por ejemplo, si los números son:
            4, 9, 6

            El valor central es:
            6

            porque 4 es el menor y 9 es el mayor.

            3. Variables que necesitamos
            float a, b, c;
            float central;

            4. Estrategia para resolverlo
            Para que a sea el valor central, debe estar entre b y c.

            Eso se comprueba así:
            (a > b && a < c) || (a < b && a > c)

            La misma idea se aplica a b. Si ni a ni b son el valor central, entonces lo será c.

            5. Construcción del código paso a paso
            Leemos los tres números:

            scanf("%f", &a);
            scanf("%f", &b);
            scanf("%f", &c);

            Comprobamos si a está entre b y c:

            if ((a > b && a < c) || (a < b && a > c)) {
                central = a;
            }

            Si no, comprobamos si b está entre a y c:

            else if ((b > a && b < c) || (b < a && b > c)) {
                central = b;
            }

            Si no se cumple ninguno de los casos anteriores, el valor central será c:

            else {
                central = c;
            }

            6. Código completo

            #include <stdio.h>

            int main() {
                float a, b, c;
                float central;

                printf("Introduce el primer numero: ");
                scanf("%f", &a);

                printf("Introduce el segundo numero: ");
                scanf("%f", &b);

                printf("Introduce el tercer numero: ");
                scanf("%f", &c);

                if ((a > b && a < c) || (a < b && a > c)) {
                    central = a;
                } else if ((b > a && b < c) || (b < a && b > c)) {
                    central = b;
                } else {
                    central = c;
                }

                printf("El valor central es: %.2f", central);

                return 0;
            }

            7. Ejemplo de ejecución
            Si el usuario introduce:
            4
            9
            6

            El programa compara:
            - 4 no está entre 9 y 6.
            - 9 no está entre 4 y 6.
            - Por tanto, el valor central es 6.

            8. Resultado
            El valor central es: 6.00"""
        
        
    },

    "ejercicio3": {
        "titulo": "Bucles: contar cifras impares",
        "tema": "Tema 5 - Bucles",
        "texto": """Ejercicio guiado 3: Bucles
            Contar cifras impares de un número

            1. Enunciado del problema
            Escribir un programa en C que lea un número entero positivo y cuente cuántas de sus cifras son impares.

            2. ¿Qué nos piden?
            Nos piden recorrer las cifras de un número y contar cuántas son impares.

            Por ejemplo, en el número:
            305827

            Las cifras impares son:
            3, 5, 7

            Por tanto, el resultado sería:
            3

            3. Variables que necesitamos
            int n;
            int cifra;
            int contador = 0;

            4. Estrategia para resolverlo
            Para obtener la última cifra usamos el operador módulo:

            cifra = n % 10;

            Para eliminar la última cifra usamos división entera entre 10:

            n = n / 10;

            Repetimos este proceso mientras n sea mayor que 0.

            Para comprobar si una cifra es impar usamos:

            cifra % 2 != 0

            5. Construcción del código paso a paso
            Leemos el número:

            scanf("%d", &n);

            Repetimos mientras queden cifras:

            while (n > 0) {

            Extraemos la última cifra:

            cifra = n % 10;

            Comprobamos si es impar:

            if (cifra % 2 != 0) {
                contador++;
            }

            Eliminamos la última cifra:

            n = n / 10;

            6. Código completo

            #include <stdio.h>

            int main() {
                int n;
                int cifra;
                int contador = 0;

                printf("Introduce un numero entero positivo: ");
                scanf("%d", &n);

                while (n > 0) {
                    cifra = n % 10;

                    if (cifra % 2 != 0) {
                        contador++;
                    }

                    n = n / 10;
                }

                printf("El numero tiene %d cifras impares", contador);

                return 0;
            }

            7. Ejemplo de ejecución
            Si el usuario introduce:
            305827

            El programa analiza las cifras de derecha a izquierda:
            7 -> impar
            2 -> par
            8 -> par
            5 -> impar
            0 -> par
            3 -> impar

            8. Resultado
            El numero tiene 3 cifras impares"""
    },

    "ejercicio4": {
        "titulo": "Funciones: comprobar divisibilidad",
        "tema": "Tema 6 - Funciones",
        "texto": """Ejercicio guiado 4: Funciones
            Comprobar si un número es divisible por otro

            1. Enunciado del problema
            Escribir una función en C que reciba dos números enteros y devuelva 1 si el primero es divisible por el segundo, y 0 en caso contrario.

            2. ¿Qué nos piden?
            Nos piden crear una función que compruebe si una división es exacta.

            Un número a es divisible por b si el resto de dividir a entre b es 0:

            a % b == 0

            3. Variables que necesitamos
            La función recibirá dos parámetros:

            int a;
            int b;

            Y devolverá:
            1 si a es divisible por b
            0 si no lo es

            4. Estrategia para resolverlo
            Creamos una función llamada esDivisible.

            Dentro de la función comprobamos si:

            a % b == 0

            Si se cumple, devolvemos 1. Si no se cumple, devolvemos 0.

            5. Construcción del código paso a paso
            Declaramos la función:

            int esDivisible(int a, int b)

            Comprobamos si el resto es 0:

            if (a % b == 0)

            Si lo es, devolvemos 1:

            return 1;

            Si no lo es, devolvemos 0:

            return 0;

            6. Código completo

            #include <stdio.h>

            int esDivisible(int a, int b) {
                if (a % b == 0) {
                    return 1;
                } else {
                    return 0;
                }
            }

            int main() {
                int a, b;
                int resultado;

                printf("Introduce el primer numero: ");
                scanf("%d", &a);

                printf("Introduce el segundo numero: ");
                scanf("%d", &b);

                resultado = esDivisible(a, b);

                if (resultado == 1) {
                    printf("%d es divisible por %d", a, b);
                } else {
                    printf("%d no es divisible por %d", a, b);
                }

                return 0;
            }

            7. Ejemplo de ejecución
            Si el usuario introduce:
            20
            5

            La función calcula:

            20 % 5 == 0

            Como el resto es 0, devuelve 1.

            8. Resultado
            20 es divisible por 5"""
    },

    "ejercicio5": {
        "titulo": "Arrays: sumar elementos pares",
        "tema": "Tema 7 - Arrays",
        "texto": """Ejercicio guiado 5: Arrays
            Sumar los elementos pares de un array

            1. Enunciado del problema
            Escribir un programa en C que recorra un array de enteros y calcule la suma de los elementos pares.

            2. ¿Qué nos piden?
            Nos piden recorrer un array elemento a elemento y acumular solamente los valores que sean pares.

            Por ejemplo, si el array es:
            {3, 2, 8, 1, 5}

            Los valores pares son:
            2 y 8

            Por tanto, la suma será:
            10

            3. Variables que necesitamos
            int v[5] = {3, 2, 8, 1, 5};
            int i;
            int suma = 0;

            4. Estrategia para resolverlo
            Usamos un bucle for para recorrer el array desde la posición 0 hasta la última posición.

            En cada posición comprobamos si el elemento es par:

            v[i] % 2 == 0

            Si lo es, lo sumamos:

            suma = suma + v[i];

            5. Construcción del código paso a paso
            Declaramos el array:

            int v[5] = {3, 2, 8, 1, 5};

            Inicializamos la suma:

            int suma = 0;

            Recorremos el array:

            for (i = 0; i < 5; i++) {

            Comprobamos si el elemento es par:

            if (v[i] % 2 == 0) {

            Si es par, lo sumamos:

            suma = suma + v[i];

            6. Código completo

            #include <stdio.h>

            int main() {
                int v[5] = {3, 2, 8, 1, 5};
                int i;
                int suma = 0;

                for (i = 0; i < 5; i++) {
                    if (v[i] % 2 == 0) {
                        suma = suma + v[i];
                    }
                }

                printf("La suma de los elementos pares es: %d", suma);

                return 0;
            }

            7. Ejemplo de ejecución
            El array es:
            {3, 2, 8, 1, 5}

            El programa analiza:
            3 -> impar, no se suma
            2 -> par, suma = 2
            8 -> par, suma = 10
            1 -> impar, no se suma
            5 -> impar, no se suma

            8. Resultado
            La suma de los elementos pares es: 10"""
    },

    "ejercicio6": {
        "titulo": "Strings: sumar dígitos de una cadena",
        "tema": "Tema 8 - Strings",
        "texto": """Ejercicio guiado 6: Strings
            Sumar los dígitos de una cadena

            1. Enunciado del problema
            Escribir un programa en C que reciba una cadena formada por dígitos y calcule la suma de esos dígitos.

            Por ejemplo, para la cadena:
            "2046"

            El resultado debe ser:
            12

            porque:
            2 + 0 + 4 + 6 = 12

            2. ¿Qué nos piden?
            Nos piden recorrer una cadena carácter a carácter y convertir cada carácter numérico en su valor entero.

            3. Variables que necesitamos
            char s[] = "2046";
            int i;
            int suma = 0;

            4. Estrategia para resolverlo
            En C, los caracteres numéricos no son directamente enteros.

            Por ejemplo, el carácter '2' no es lo mismo que el número 2.

            Para convertir un carácter numérico en su valor entero, restamos el carácter '0':

            s[i] - '0'

            Así:
            '2' - '0' = 2

            Recorremos la cadena hasta encontrar el carácter final '\\0'.

            5. Construcción del código paso a paso
            Declaramos la cadena:

            char s[] = "2046";

            Inicializamos la suma:

            int suma = 0;

            Recorremos la cadena:

            for (i = 0; s[i] != '\\0'; i++) {

            Convertimos cada carácter a número y lo sumamos:

            suma = suma + s[i] - '0';

            6. Código completo

            #include <stdio.h>

            int main() {
                char s[] = "2046";
                int i;
                int suma = 0;

                for (i = 0; s[i] != '\\0'; i++) {
                    suma = suma + s[i] - '0';
                }

                printf("La suma de los digitos es: %d", suma);

                return 0;
            }

            7. Ejemplo de ejecución
            La cadena es:
            "2046"

            El programa recorre:
            '2' -> 2
            '0' -> 0
            '4' -> 4
            '6' -> 6

            Y calcula:
            2 + 0 + 4 + 6 = 12

            8. Resultado
            La suma de los digitos es: 12"""
    },

    "ejercicio7": {
        "titulo": "Punteros: intercambio de dos variables",
        "tema": "Tema 9 - Punteros",
        "texto": """Ejercicio guiado 7: Punteros
            Intercambio de dos variables

            1. Enunciado del problema
            Escribir una función en C que intercambie los valores de dos variables enteras utilizando punteros.

            2. ¿Qué nos piden?
            Nos piden modificar dos variables declaradas en main desde una función.

            Para poder modificar variables externas a una función, no basta con pasar sus valores. Hay que pasar sus direcciones de memoria usando punteros.

            3. Variables que necesitamos
            En main tendremos:

            int a;
            int b;

            En la función necesitaremos dos punteros:

            int *x;
            int *y;

            Y una variable auxiliar:

            int aux;

            4. Estrategia para resolverlo
            Si queremos intercambiar a y b, no podemos hacer directamente:

            a = b;
            b = a;

            porque al hacer a = b, el valor original de a se pierde.

            Por eso usamos una variable auxiliar:

            aux = *x;
            *x = *y;
            *y = aux;

            Los operadores importantes son:
            &a -> dirección de memoria de a
            *x -> valor almacenado en la dirección a la que apunta x

            5. Construcción del código paso a paso
            Declaramos la función:

            void intercambiar(int *x, int *y)

            Guardamos el valor de la primera variable:

            aux = *x;

            Copiamos el valor de la segunda variable en la primera:

            *x = *y;

            Recuperamos el valor original de la primera variable:

            *y = aux;

            En main llamamos a la función pasando las direcciones:

            intercambiar(&a, &b);

            6. Código completo

            #include <stdio.h>

            void intercambiar(int *x, int *y) {
                int aux;

                aux = *x;
                *x = *y;
                *y = aux;
            }

            int main() {
                int a = 5;
                int b = 9;

                printf("Antes del intercambio: a = %d, b = %d\\n", a, b);

                intercambiar(&a, &b);

                printf("Despues del intercambio: a = %d, b = %d\\n", a, b);

                return 0;
            }

            7. Ejemplo de ejecución
            Inicialmente:
            a = 5
            b = 9

            Dentro de la función:
            aux = 5
            *x = 9
            *y = 5

            Como x apunta a a e y apunta a b, los valores reales de a y b cambian.

            8. Resultado
            Antes del intercambio: a = 5, b = 9
            Despues del intercambio: a = 9, b = 5"""
    },

    "ejercicio8": {
        "titulo": "Structs: almacenar y mostrar datos de un alumno",
        "tema": "Tema 10 - Structs",
        "texto": """Ejercicio guiado 8: Structs
            Almacenar y mostrar datos de un alumno

            1. Enunciado del problema
            Definir una estructura Alumno que almacene la matrícula de un estudiante y tres notas. Después, crear una variable de ese tipo y mostrar sus datos por pantalla.

            2. ¿Qué nos piden?
            Nos piden trabajar con una estructura, es decir, agrupar varios datos relacionados bajo un mismo tipo.

            En este caso, un alumno tendrá:
            - Una matrícula.
            - Tres notas.

            3. Variables que necesitamos
            Primero definimos el tipo struct:

            struct Alumno {
                int matricula;
                float notas[3];
            };

            Después declaramos una variable de ese tipo:

            struct Alumno a;

            4. Estrategia para resolverlo
            Una estructura permite guardar información relacionada dentro de una misma variable.

            Para acceder a sus campos usamos el operador punto:

            a.matricula
            a.notas[0]
            a.notas[1]
            a.notas[2]

            Como las notas están en un array, podemos recorrerlas con un bucle for.

            5. Construcción del código paso a paso
            Definimos la estructura:

            struct Alumno {
                int matricula;
                float notas[3];
            };

            Declaramos e inicializamos una variable:

            struct Alumno a = {21013, {7.5, 8.0, 6.5}};

            Mostramos la matrícula:

            printf("Matricula: %d\\n", a.matricula);

            Recorremos las notas:

            for (i = 0; i < 3; i++) {
                printf("Nota %d: %.2f\\n", i + 1, a.notas[i]);
            }

            6. Código completo

            #include <stdio.h>

            struct Alumno {
                int matricula;
                float notas[3];
            };

            int main() {
                struct Alumno a = {21013, {7.5, 8.0, 6.5}};
                int i;

                printf("Matricula: %d\\n", a.matricula);

                for (i = 0; i < 3; i++) {
                    printf("Nota %d: %.2f\\n", i + 1, a.notas[i]);
                }

                return 0;
            }

            7. Ejemplo de ejecución
            La variable a contiene:

            matricula = 21013
            notas = {7.5, 8.0, 6.5}

            El programa primero muestra la matrícula y después recorre el array de notas.

            8. Resultado
            Matricula: 21013
            Nota 1: 7.50
            Nota 2: 8.00
            Nota 3: 6.50"""
    }

}


def texto_a_ejercicio_guiado(texto: Text) -> Text | None:
    if not texto:
        return None

    t = texto.lower().strip()

    mapa = {
        "ejercicio 1": "ejercicio1",
        "ejercicio guiado 1": "ejercicio1",
        "quiero el ejercicio 1": "ejercicio1",
        "quiero ver el ejercicio 1": "ejercicio1",

        "ejercicio 2": "ejercicio2",
        "ejercicio guiado 2": "ejercicio2",
        "quiero el ejercicio 2": "ejercicio2",
        "quiero ver el ejercicio 2": "ejercicio2",

        "ejercicio 3": "ejercicio3",
        "ejercicio guiado 3": "ejercicio3",
        "quiero el ejercicio 3": "ejercicio3",
        "quiero ver el ejercicio 3": "ejercicio3",

        "ejercicio 4": "ejercicio4",
        "ejercicio guiado 4": "ejercicio4",
        "quiero el ejercicio 4": "ejercicio4",
        "quiero ver el ejercicio 4": "ejercicio4",

        "ejercicio 5": "ejercicio5",
        "ejercicio guiado 5": "ejercicio5",
        "quiero el ejercicio 5": "ejercicio5",
        "quiero ver el ejercicio 5": "ejercicio5",

        "ejercicio 6": "ejercicio6",
        "ejercicio guiado 6": "ejercicio6",
        "quiero el ejercicio 6": "ejercicio6",
        "quiero ver el ejercicio 6": "ejercicio6",

        "ejercicio 7": "ejercicio7",
        "ejercicio guiado 7": "ejercicio7",
        "quiero el ejercicio 7": "ejercicio7",
        "quiero ver el ejercicio 7": "ejercicio7",

        "ejercicio 8": "ejercicio8",
        "ejercicio guiado 8": "ejercicio8",
        "quiero el ejercicio 8": "ejercicio8",
        "quiero ver el ejercicio 8": "ejercicio8",
        
    }

    return mapa.get(t)


class ActionPedirEjercicioGuiado(Action):
    def name(self) -> Text:
        return "action_pedir_ejercicio_guiado"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text=(
                "Claro. ¿Qué ejercicio guiado quieres ver?\n\n"
                "1. Variables y operadores: superficie de una esfera\n"
                "2. Condicionales: valor central de tres números\n"
                "3. Bucles: contar cifras impares\n"
                "4. Funciones: comprobar divisibilidad\n"
                "5. Arrays: sumar elementos pares\n"
                "6. Strings: sumar dígitos de una cadena\n"
                "7. Punteros: intercambio de dos variables\n"
                "8. Structs: datos de un alumno\n\n"
                "Elige uno y escribe: ejercicio 1, ejercicio 2..., ejercicio 8"
            )
        )

        return [
            SlotSet("ejercicio_guiado_activo", "esperando_ejercicio"),
            SlotSet("modo_conversacion", "ejercicio_guiado"),
            SlotSet("minitest_activo", None),
        ]


class ActionMostrarEjercicioGuiado(Action):
    def name(self) -> Text:
        return "action_mostrar_ejercicio_guiado"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        texto_usuario = tracker.latest_message.get("text", "")
        ejercicio = texto_a_ejercicio_guiado(texto_usuario)

        if ejercicio is None or ejercicio not in EJERCICIOS_GUIADOS:
            dispatcher.utter_message(
                text=(
                    "No he reconocido ese ejercicio guiado.\n\n"
                    "Escribe exactamente ejercicio x, con x entre 1 y 8."
                )
            )
            return [
                SlotSet("ejercicio_guiado_activo", "esperando_ejercicio"),
                SlotSet("modo_conversacion", "ejercicio_guiado"),
            ]

        metadata = tracker.latest_message.get("metadata", {})

        guardar_consulta_ejercicio_guiado(
            user_id=tracker.sender_id,
            username=metadata.get("username"),
            first_name=metadata.get("first_name"),
            last_name=metadata.get("last_name"),
            ejercicio_id=ejercicio,
            ejercicio_titulo=EJERCICIOS_GUIADOS[ejercicio]["titulo"],
            tema=EJERCICIOS_GUIADOS[ejercicio]["tema"],
        )

        dispatcher.utter_message(text=EJERCICIOS_GUIADOS[ejercicio]["texto"])

        return [
            SlotSet("ejercicio_guiado_activo", None),
            SlotSet("modo_conversacion", "general"),
            SlotSet("minitest_activo", None),
            FollowupAction("action_listen"),
        ]
    

class ActionVerProgreso(Action):
    def name(self) -> Text:
        return "action_ver_progreso"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        ruta_archivo = "progreso_alumnos.json"
        user_id_actual = str(tracker.sender_id)

        if not os.path.exists(ruta_archivo):
            dispatcher.utter_message(
                text=(
                    "Todavía no tengo datos de progreso guardados.\n\n"
                    "Haz algún minitest primero y después podré mostrarte tu evolución."
                )
            )
            return []

        try:
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
        except json.JSONDecodeError:
            dispatcher.utter_message(
                text="No he podido leer correctamente el archivo de progreso."
            )
            return []

        intentos_usuario = [
            registro for registro in datos
            if str(registro.get("user_id")) == user_id_actual
            and "puntuacion" in registro
            and "total_preguntas" in registro
            and "porcentaje_acierto" in registro
        ]

        if not intentos_usuario:
            dispatcher.utter_message(
                text=(
                    "Todavía no tengo minitests registrados para tu usuario.\n\n"
                    "Haz primero un minitest y después podré mostrarte tu progreso."
                )
            )
            return []

        total_intentos = len(intentos_usuario)

        media_acierto = sum(
            intento["porcentaje_acierto"] for intento in intentos_usuario
        ) / total_intentos

        resumen_por_tema = {}

        for intento in intentos_usuario:
            tema = intento["tema"]

            if tema not in resumen_por_tema:
                resumen_por_tema[tema] = {
                    "intentos": 0,
                    "suma_porcentaje": 0,
                    "mejor_porcentaje": 0,
                    "ultima_puntuacion": intento["puntuacion"],
                    "total_preguntas": intento["total_preguntas"],
                }

            resumen_por_tema[tema]["intentos"] += 1
            resumen_por_tema[tema]["suma_porcentaje"] += intento["porcentaje_acierto"]
            resumen_por_tema[tema]["mejor_porcentaje"] = max(
                resumen_por_tema[tema]["mejor_porcentaje"],
                intento["porcentaje_acierto"],
            )
            resumen_por_tema[tema]["ultima_puntuacion"] = intento["puntuacion"]
            resumen_por_tema[tema]["total_preguntas"] = intento["total_preguntas"]

        for tema, datos_tema in resumen_por_tema.items():
            datos_tema["media"] = datos_tema["suma_porcentaje"] / datos_tema["intentos"]

        mejor_tema = max(
            resumen_por_tema,
            key=lambda tema: resumen_por_tema[tema]["media"]
        )

        tema_mejora = min(
            resumen_por_tema,
            key=lambda tema: resumen_por_tema[tema]["media"]
        )

        lineas_temas = []

        for tema, datos_tema in resumen_por_tema.items():
            lineas_temas.append(
                f"- {nombre_tema(tema)}: media {datos_tema['media']:.2f}% "
                f"({datos_tema['intentos']} intento/s)"
            )

        recomendacion = recomendar_ejercicio_por_tema(tema_mejora)

        mensaje = (
            "📊 Resumen de tu progreso\n\n"
            f"Has realizado {total_intentos} minitest(s).\n"
            f"Media global de aciertos: {media_acierto:.2f}%\n\n"
            "Resultados por tema:\n"
            + "\n".join(lineas_temas)
            + "\n\n"
            f"Mejor tema: {nombre_tema(mejor_tema)} "
            f"({resumen_por_tema[mejor_tema]['media']:.2f}%).\n\n"
            f"Tema con más margen de mejora: {nombre_tema(tema_mejora)} "
            f"({resumen_por_tema[tema_mejora]['media']:.2f}%).\n\n"
            f"{recomendacion}"
        )

        dispatcher.utter_message(text=mensaje)

        return [
            SlotSet("modo_conversacion", "general"),
            SlotSet("minitest_activo", None),
        ]