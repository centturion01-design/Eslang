import openai
import os
import hashlib
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# === CARGAR EL PROMPT ===
with open("prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# === INICIALIZAR MEMORIA ===
# Modelo de embeddings (corre en local, sin API)
modelo_embedding = SentenceTransformer('all-MiniLM-L6-v2')

# Cliente de ChromaDB (memoria persistente)
cliente_chroma = chromadb.PersistentClient(
    path="./memoria",
    settings=Settings(anonymized_telemetry=False)
)

# Crear o recuperar la colección de memorias
try:
    coleccion = cliente_chroma.get_collection("eslang_memory")
except:
    coleccion = cliente_chroma.create_collection("eslang_memory")

# === ESTADO DE LA CONVERSACIÓN ===
contexto = {
    "orden_pendiente": None,
    "esperando_respuesta": False
}

# === FUNCIONES DE MEMORIA ===

def generar_embedding(texto):
    """Genera un vector numérico para un texto."""
    return modelo_embedding.encode(texto).tolist()

def buscar_en_memoria(orden_usuario, umbral=0.85):
    """
    Busca en la memoria si ya existe una orden similar.
    Retorna (codigo, similitud) o (None, 0) si no hay.
    """
    embedding = generar_embedding(orden_usuario)
    
    resultados = coleccion.query(
        query_embeddings=[embedding],
        n_results=1
    )
    
    if resultados['distances'] and resultados['distances'][0]:
        distancia = resultados['distances'][0][0]  # distancia coseno (0 = idéntico)
        similitud = 1 - distancia  # convertimos a similitud (1 = idéntico)
        
        if similitud >= umbral:
            codigo = resultados['metadatas'][0][0]['codigo']
            return codigo, similitud
    
    return None, 0

def guardar_en_memoria(orden_usuario, codigo_generado):
    """Guarda una nueva orden y su código en la memoria."""
    embedding = generar_embedding(orden_usuario)
    id_unico = hashlib.md5(orden_usuario.encode()).hexdigest()
    
    coleccion.add(
        ids=[id_unico],
        embeddings=[embedding],
        metadatas=[{
            "orden": orden_usuario,
            "codigo": codigo_generado
        }]
    )
    print(f"🧠 Memoria actualizada con nueva orden.")

# === FUNCIONES DE TRADUCCIÓN ===

def traducir(mensaje_usuario):
    """Llama a la API para traducir español a Python."""
    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": mensaje_usuario}
        ],
        temperature=0.1
    )
    return respuesta.choices[0].message.content

def contiene_pregunta(codigo):
    return "#PREGUNTA:" in codigo

def extraer_orden_sin_pregunta(codigo):
    lineas = codigo.split("\n")
    lineas_limpias = [l for l in lineas if not l.startswith("#PREGUNTA:")]
    return "\n".join(lineas_limpias)

# === BUCLE PRINCIPAL ===

print("🧠 Eslang v0.3 — La Memoria")
print("Escribe 'salir' para terminar.")
print(f"📚 Memoria actual: {coleccion.count()} órdenes almacenadas.\n")

while True:
    entrada = input(">>> ").strip()
    
    if entrada.lower() in ["salir", "exit", "quit"]:
        print("¡Hasta la próxima, capitán! ⛵")
        break
    
    # === MODO PREGUNTA (como en v0.2) ===
    if contexto["esperando_respuesta"]:
        orden_original = contexto["orden_pendiente"]
        mensaje_completo = f"{orden_original}\n\nRespuesta del usuario: {entrada}"
        contexto["esperando_respuesta"] = False
        contexto["orden_pendiente"] = None
        
        print("\n🔄 Generando código con tu respuesta...")
        codigo_final = traducir(mensaje_completo)
        
        print("\n[Código generado]")
        print(codigo_final)
        print("\n[Ejecutando...]")
        try:
            exec(codigo_final)
            # Guardar en memoria después de ejecutar correctamente
            guardar_en_memoria(orden_original, codigo_final)
        except Exception as e:
            print(f"❌ Error: {e}")
        continue
    
    # === BUSCAR EN MEMORIA PRIMERO ===
    print("🔍 Buscando en memoria...")
    codigo_memoria, similitud = buscar_en_memoria(entrada)
    
    if codigo_memoria:
        print(f"✅ ¡Memoria encontrada! (Similitud: {similitud*100:.1f}%)")
        print("\n[Código recuperado de memoria]")
        print(codigo_memoria)
        print("\n[Ejecutando...]")
        try:
            exec(codigo_memoria)
        except Exception as e:
            print(f"❌ Error: {e}")
        continue
    
    # === NO ESTÁ EN MEMORIA: TRADUCIR ===
    print("🆕 Orden nueva. Traduciendo con IA...")
    codigo_generado = traducir(entrada)
    
    if contiene_pregunta(codigo_generado):
        print("\n🤔 Eslang necesita más información:")
        for linea in codigo_generado.split("\n"):
            if linea.startswith("#PREGUNTA:"):
                print(f"   {linea.replace('#PREGUNTA:', '').strip()}")
        
        contexto["esperando_respuesta"] = True
        contexto["orden_pendiente"] = entrada
        
        codigo_limpio = extraer_orden_sin_pregunta(codigo_generado)
        if codigo_limpio.strip():
            print("\n[Código parcial generado]")
            print(codigo_limpio)
    else:
        print("\n[Código generado]")
        print(codigo_generado)
        print("\n[Ejecutando...]")
        try:
            exec(codigo_generado)
            # Guardar en memoria si se ejecutó bien
            guardar_en_memoria(entrada, codigo_generado)
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "-" * 50 + "\n")
