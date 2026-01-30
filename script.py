import os
import sqlite3
import google.generativeai as genai
import feedparser
import requests
import warnings

# Limpiamos advertencias visuales
warnings.filterwarnings("ignore")

# 1. IA
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. WP (Configuración segura)
WP_URL = "https://TU-SITIO-WEB.com/wp-json/wp/v2/posts"
WP_USER = os.environ.get("WP_USER")
WP_PASS = os.environ.get("WP_APP_PASSWORD")

def iniciar_db():
    conn = sqlite3.connect('historial.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS publicados (link TEXT PRIMARY KEY)''')
    conn.commit()
    return conn

def ejecutar():
    conn = iniciar_db()
    c = conn.cursor()
    
    # Cambiamos el feed para que encuentre algo nuevo sí o sí
    feed = feedparser.parse("https://hipertextual.com/feed")
    
    if feed.entries:
        entry = feed.entries[0]
        
        # Generamos siempre para esta prueba
        print(f"\n🚀 REDACTANDO ARTÍCULO SOBRE: {entry.title}")
        
        prompt = f"Escribe un post SEO profesional en español sobre: {entry.title}. Usa etiquetas HTML h2 y p."
        response = model.generate_content(prompt)
        articulo_html = response.text
        
        # ESTO ES LO QUE QUERÉS VER:
        print("\n" + "=".current_time_str * 50)
        print("📝 CONTENIDO GENERADO POR IA:")
        print("=".current_time_str * 50)
        print(articulo_html)
        print("=".current_time_str * 50 + "\n")
        
        # Intento de publicación (si falla, no corta el script)
        try:
            if WP_USER and WP_PASS:
                payload = {"title": entry.title, "content": articulo_html, "status": "publish"}
                requests.post(WP_URL, json=payload, auth=(WP_USER, WP_PASS), timeout=10)
                print("✅ Intento de envío a WordPress completado.")
            else:
                print("ℹ️ Modo lectura: No se detectaron credenciales de WordPress.")
        except:
            print("⚠️ Nota: WordPress no respondió, pero el artículo se generó arriba.")

    conn.close()

if __name__ == "__main__":
    ejecutar()
