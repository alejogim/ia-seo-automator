import os
import sqlite3
import google.generativeai as genai
import feedparser
import requests
import warnings

# Desactivar avisos visuales de advertencia en el log para leer mejor
warnings.filterwarnings("ignore", category=FutureWarning)

# 1. CONFIGURACIÓN DE IA (Google Gemini)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. CONFIGURACIÓN DE WORDPRESS (Para el paso final)
# Si aún no tienes estas variables en Secrets, el script solo imprimirá el texto
WP_URL = "https://TU-SITIO-WEB.com/wp-json/wp/v2/posts" 
WP_USER = os.environ.get("WP_USER", "usuario_ejemplo")
WP_PASS = os.environ.get("WP_APP_PASSWORD", "pass_ejemplo")

# 3. BASE DE DATOS LOCAL
def iniciar_db():
    conn = sqlite3.connect('historial.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS publicados (link TEXT PRIMARY KEY)''')
    conn.commit()
    return conn

# 4. FUNCIÓN PARA PUBLICAR
def publicar_wp(titulo, contenido):
    if "TU-SITIO-WEB" in WP_URL:
        print("⚠️ Salteando publicación: No se configuró una URL real de WordPress.")
        return
    
    payload = {"title": titulo, "content": contenido, "status": "publish"}
    response = requests.post(WP_URL, json=payload, auth=(WP_USER, WP_PASS))
    if response.status_code == 201:
        print("✅ ¡Publicado en WordPress con éxito!")
    else:
        print(f"❌ Error WP: {response.status_code}")

# 5. LÓGICA PRINCIPAL
def ejecutar():
    conn = iniciar_db()
    c = conn.cursor()
    
    # Usamos un feed de tecnología en español para la prueba
    feed = feedparser.parse("https://hipertextual.com/feed")
    
    if feed.entries:
        entry = feed.entries[0]
        
        # Consultamos si ya existe
        c.execute("SELECT * FROM publicados WHERE link=?", (entry.link,))
        if not c.fetchone():
            print(f"\n🚀 PROCESANDO NOTICIA: {entry.title}")
            
            prompt = f"""
            Escribe un artículo de blog SEO en español. 
            Tema: {entry.title}
            Referencia: {entry.link}
            Usa formato HTML (h2, p, strong).
            """
            
            response = model.generate_content(prompt)
            articulo_html = response.text
            
            # ESTO ES LO QUE BUSCAS EN EL LOG:
            print("\n" + "X"*60)
            print("👇 AQUÍ ESTÁ TU ARTÍCULO GENERADO 👇")
            print("X"*60)
            print(articulo_html)
            print("X"*60 + "\n")
            
            # Intento de publicación
            publicar_wp(entry.title, articulo_html)
            
            # Guardar para no repetir
            c.execute("INSERT INTO publicados VALUES (?)", (entry.link,))
            conn.commit()
        else:
            print(f"\n😴 La noticia '{entry.title}' ya fue procesada anteriormente.")
    
    conn.close()

if __name__ == "__main__":
    ejecutar()
