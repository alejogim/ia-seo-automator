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
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

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
    try:
        feed = feedparser.parse("https://hipertextual.com/feed")
        if feed.entries:
            entry = feed.entries[0]
            print(f"\n🚀 INTENTANDO REDACTAR: {entry.title}")
            
            prompt = f"Escribe un post SEO profesional en español sobre: {entry.title}. Usa HTML."
            
            # Intento de generación con manejo de errores
            try:
                response = model.generate_content(prompt)
                articulo_html = response.text
                
                print("\n" + "="*50)
                print("📝 ¡LO LOGRAMOS! AQUÍ ESTÁ EL ARTÍCULO:")
                print("="*50)
                print(articulo_html)
                print("="*50 + "\n")
            except Exception as e:
                print(f"❌ Error de Gemini: {e}")
                print("Prueba cambiar el nombre del modelo a 'gemini-pro' si persiste.")
    finally:
        conn.close()

if __name__ == "__main__":
    ejecutar()
