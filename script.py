import os
import sqlite3
from google import genai
import feedparser
import requests

# 1. Configuración de la Nueva API de Google
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 2. Configuración WordPress (Dejalos así hasta que pongas los Secrets)
WP_URL = "https://TU-SITIO.com/wp-json/wp/v2/posts"
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
    
    # Probamos con un feed estable
    feed = feedparser.parse("https://hipertextual.com/feed")
    
    if feed.entries:
        entry = feed.entries[0]
        print(f"\n🚀 PROCESANDO: {entry.title}")
        
        try:
            # Nueva forma de llamar a Gemini 1.5 Flash
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=f"Escribe un post SEO profesional en español sobre: {entry.title}. Usa HTML (h2, p)."
            )
            
            articulo_html = response.text
            
            print("\n" + "="*50)
            print("📝 ARTÍCULO GENERADO:")
            print("="*50)
            print(articulo_html)
            print("="*50 + "\n")
            
        except Exception as e:
            print(f"❌ Error al generar con la nueva API: {e}")

    conn.close()

if __name__ == "__main__":
    ejecutar()
