import os
import sqlite3
import google.generativeai as genai
import feedparser
import requests

# FORZAMOS LA VERSIÓN ESTABLE DE LA API
genai.configure(api_key=os.environ["GEMINI_API_KEY"], transport='rest')

def iniciar_db():
    conn = sqlite3.connect('historial.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS publicados (link TEXT PRIMARY KEY)''')
    conn.commit()
    return conn

def ejecutar():
    conn = iniciar_db()
    c = conn.cursor()
    
    # Mantenemos el feed de noticias
    feed = feedparser.parse("https://hipertextual.com/feed")
    
    if feed.entries:
        entry = feed.entries[0]
        print(f"\n🚀 INTENTO FINAL CON: {entry.title}")
        
        # Usamos el nombre de modelo más básico posible
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        try:
            response = model.generate_content(
                f"Escribe un post SEO corto en español sobre: {entry.title}. Usa HTML."
            )
            
            print("\n" + "="*50)
            print("📝 ARTÍCULO GENERADO:")
            print("="*50)
            print(response.text)
            print("="*50 + "\n")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Si esto falla, el problema es la región de tu API Key en Google AI Studio.")

    conn.close()

if __name__ == "__main__":
    ejecutar()
