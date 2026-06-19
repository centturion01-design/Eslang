# ⚡ Eslang🦜
> *"No programas. Conversas."*

**Eslang** es un intérprete experimental que traduce español coloquial a Python ejecutable. 
No es un lenguaje nuevo; es una **forma nueva de hablarle a la máquina**.


## 🚀 ¿Qué hace?

Escribes esto: ordena los números del 1 al 10 y quédate con los pares

Y Eslang ejecuta esto:

```python
numeros = list(range(1, 11))
pares = [n for n in numeros if n % 2 == 0]
print(pares)
# [2, 4, 6, 8, 10]
```

## 🧠 Filosofía

Eslang no busca reemplazar a Python. Busca reemplazar la fricción.
Si puedes decirlo en español, Eslang intentará hacerlo. Y si no puede, te preguntará.

(La bidireccionalidad llegará en la versión 0.2. Por ahora, solo obedece.)


El manifiesto de a bordo (para que quede claro)

    Nosotros, los de Eslang, declaramos:

    Que el código no debe ser un muro, sino un puente.

    Que la máquina debe aprender nuestro idioma, no nosotros el suyo.

    Que el primer paso es torpe, pero el segundo ya es firme.

    Que este barco no tiene puerto fijo; su destino es la próxima pregunta del humano.


## 📦 Instalación (2 minutos)

##### bash:

git clone https://github.com/centturion01-desing/eslang.git
cd eslang
pip install openai python-dotenv


    Crea un archivo .env:

##### text:

OPENAI_API_KEY=tu_api_key

    Ejecuta:

##### bash:

python eslang.py

    Empieza a hablar:

##### text

> crea un archivo llamado hola.txt con el texto "Bienvenido a Eslang"
> Archivo creado ✅



## 🧪 Ejemplos

##### Tu dices											Eslang hace

dime la hora actual							    	print(datetime.now())
crea una lista con los cuadrados del 1 al 10		  	[n**2 for n in range(1, 11)]
guarda este texto en un archivo (con texto previo)	      with open(...)
baja este JSON de esta URL						      requests.get(url).json()



## 🗺️ Hoja de ruta (nuestro viaje)

    Versión 0.1 — Traductor español → Python (el trampolín)
    
    Versión 0.2 — Sistema de preguntas (bidireccionalidad)
    
    Versión 0.3 — Memoria asociativa (aprende de ti)
    
    Versión 0.4 — Lógica difusa (preferencias y probabilidades)
    
    Versión 1.0 — Compilador generativo (CogniLang)



## 🫡 Contribuye

Este barco es pequeño, pero tiene espacio para tripulación valiente.
Abre un issue, haz un fork, o simplemente úsalo y maldícelo en voz alta.
Todo eso es combustible.



## 📜 Licencia

MIT. Porque la libertad también es un lenguaje universal.

Hecho con café, rebeldía y la certeza de que el código también puede ser poesía.




---

