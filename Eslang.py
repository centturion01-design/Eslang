import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Cargar el prompt
with open("prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

def traducir(orden_usuario):
    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": orden_usuario}
        ],
        temperature=0.1  # Muy bajo para que sea predecible
    )
    return respuesta.choices[0].message.content

# Bucle principal
while True:
    orden = input(">>> ")
    if orden.lower() in ["salir", "exit", "quit"]:
        break
    codigo = traducir(orden)
    print("\n[Código generado]")
    print(codigo)
    print("\n[Ejecutando...]")
    try:
        exec(codigo)
    except Exception as e:
        print(f"Error: {e}")