import os
import requests
import time

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

if not TELEGRAM_TOKEN:
    raise RuntimeError(
        "No se ha definido la variable de entorno TELEGRAM_BOT_TOKEN."
    )

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
def teclado_inicio():
    return {
        "keyboard": [
            [{"text": "Ver temas"}, {"text": "Hacer minitest"}],
            [{"text": "Ejercicios guiados"}, {"text": "Ver progreso"}],
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False,
    }


def teclado_temas():
    return {
        "keyboard": [
            [{"text": "Tema 0"}, {"text": "Tema 1"}, {"text": "Tema 2"}],
            [{"text": "Tema 3"}, {"text": "Tema 4"}, {"text": "Tema 5"}],
            [{"text": "Tema 6"}, {"text": "Tema 7"}, {"text": "Tema 8"}],
            [{"text": "Tema 9"}, {"text": "Tema 10"}],
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False,
    }


def teclado_abc():
    return {
        "keyboard": [
            [{"text": "a"}, {"text": "b"}, {"text": "c"}]
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False,
    }

def teclado_ejercicios():
    return {
        "keyboard": [
            [{"text": "Ejercicio 1"}, {"text": "Ejercicio 2"}],
            [{"text": "Ejercicio 3"}, {"text": "Ejercicio 4"}],
            [{"text": "Ejercicio 5"}, {"text": "Ejercicio 6"}],
            [{"text": "Ejercicio 7"}, {"text": "Ejercicio 8"}],
        ],
        "resize_keyboard": True,
        "one_time_keyboard": False,
    }


def quitar_teclado():
    return {
        "remove_keyboard": True
    }


def enviar_mensaje(chat_id, texto, reply_markup=None):
    data = {
        "chat_id": chat_id,
        "text": texto,
    }

    if reply_markup is not None:
        data["reply_markup"] = reply_markup

    requests.post(f"{TELEGRAM_API_URL}/sendMessage", json=data)


def enviar_a_rasa(user_id, mensaje, username=None, first_name=None, last_name=None):
    respuesta = requests.post(
        RASA_URL,
        json={
            "sender": str(user_id),
            "message": mensaje,
            "metadata": {
                "telegram_user_id": str(user_id),
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            }
        }
    )

    if respuesta.status_code == 200:
        return respuesta.json()

    return []


def normalizar_boton(texto):
    mapa_botones = {
        "Ver temas": "temas",
        "Hacer minitest": "quiero un minitest",
        "Tema 0": "tema 0",
        "Tema 1": "tema 1",
        "Tema 2": "tema 2",
        "Tema 3": "tema 3",
        "Tema 4": "tema 4",
        "Tema 5": "tema 5",
        "Tema 6": "tema 6",
        "Tema 7": "tema 7",
        "Tema 8": "tema 8",
        "Tema 9": "tema 9",
        "Tema 10": "tema 10",
        "Ejercicios guiados": "quiero un ejercicio guiado",
        "Ver progreso": "ver progreso",
        "Ejercicio 1": "ejercicio 1",
        "Ejercicio 2": "ejercicio 2",
        "Ejercicio 3": "ejercicio 3",
        "Ejercicio 4": "ejercicio 4",
        "Ejercicio 5": "ejercicio 5",
        "Ejercicio 6": "ejercicio 6",
        "Ejercicio 7": "ejercicio 7",
        "Ejercicio 8": "ejercicio 8",
    }

    return mapa_botones.get(texto, texto)

def normalizar_operadores(texto):
    reemplazos = {
        "==": " doble igual ",
        "!=": " distinto de ",
        "%": " modulo ",
        "&&": " y logico ",
        "||": " o logico ",
        "=": " asignacion ",
        "+": " suma ",
        "!": " negacion ",
        "->": " flecha ",
        ".": " punto ",
        "*": " asterisco ",
        "&": " ampersand ",
    }

    for simbolo, palabra in reemplazos.items():
        texto = texto.replace(simbolo, palabra)

    return " ".join(texto.split())


def es_pregunta_minitest(texto):
    texto = texto.lower()

    return (
        "responde a las preguntas con a, b o c" in texto
        or "contesta con a, b o c" in texto
        or ("pregunta" in texto and "a)" in texto and "b)" in texto and "c)" in texto)
    )


def pide_tema_minitest(texto):
    texto = texto.lower()

    return (
        "de qué tema quieres hacer el minitest" in texto
        or "no he podido identificar el tema del minitest" in texto
    )


def termina_minitest(texto):
    texto = texto.lower()

    return "has completado el minitest" in texto

def muestra_menu_ejercicios(texto):
    texto = texto.lower()

    return (
        "qué ejercicio guiado quieres ver" in texto
        or "que ejercicio guiado quieres ver" in texto
        or "elige uno y escribe" in texto
        or ("ejercicio 1" in texto and "ejercicio 8" in texto)
    )


def main():
    print("Puente Telegram-Rasa iniciado...")
    offset = None

    while True:
        try:
            params = {"timeout": 30}
            if offset is not None:
                params["offset"] = offset

            updates = requests.get(
                f"{TELEGRAM_API_URL}/getUpdates",
                params=params
            ).json()

            for update in updates.get("result", []):
                offset = update["update_id"] + 1

                if "message" not in update:
                    continue

                message = update["message"]
                chat_id = message["chat"]["id"]
                user_id = message["from"]["id"]
                username = message["from"].get("username")
                first_name = message["from"].get("first_name")
                last_name = message["from"].get("last_name")
                texto = message.get("text", "")

                if not texto:
                    continue

                if texto.lower().strip() in [
                    "/start",
                    "hola",
                    "buenas",
                    "hey",
                    "qué puedo hacer",
                    "que puedo hacer",
                    "qué puedes hacer",
                    "que puedes hacer",
                    "ayuda",
                    "menu",
                    "menú"
                ]:
                    enviar_mensaje(
                        chat_id,
                        "¡Hola! Soy CodeBot 🤖\n\nElige una opción (o utiliza el teclado normal para hacer una pregunta):",
                        teclado_inicio()
                    )
                    continue

                texto_normalizado = normalizar_boton(texto)
                texto_normalizado = normalizar_operadores(texto_normalizado)

                respuestas_rasa = enviar_a_rasa(
                    user_id,
                    texto_normalizado,
                    username=username,
                    first_name=first_name,
                    last_name=last_name
                )

                if not respuestas_rasa:
                    enviar_mensaje(
                        chat_id,
                        "No he podido generar una respuesta.",
                        quitar_teclado()
                    )
                    continue

                for r in respuestas_rasa:
                    if "text" not in r:
                        continue

                    respuesta_texto = r["text"]

                    if pide_tema_minitest(respuesta_texto):
                        enviar_mensaje(chat_id, respuesta_texto, teclado_temas())
                    
                    elif muestra_menu_ejercicios(respuesta_texto):
                        enviar_mensaje(chat_id, respuesta_texto, teclado_ejercicios())

                    elif es_pregunta_minitest(respuesta_texto):
                        enviar_mensaje(chat_id, respuesta_texto, teclado_abc())

                    elif termina_minitest(respuesta_texto):
                        enviar_mensaje(chat_id, respuesta_texto, teclado_inicio())

                    else:
                         if texto_normalizado == "temas":
                            enviar_mensaje(chat_id, respuesta_texto, teclado_temas())
                         else:
                            enviar_mensaje(chat_id, respuesta_texto)

        except Exception as e:
            print("Error:", e)
            time.sleep(3)


if __name__ == "__main__":
    main()