import os
import sqlite3
import google.generativeai as genai
import feedparser
import requests

# 1. CONFIGURACIÓN DE IA (Google Gemini)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. CONFIGURACIÓN DE WORDPRESS (Del cliente)
WP_URL = "https://TU-SITIO-WEB.com/wp-json/wp/v2/posts" # <-- CAMBIA ESTO
WP_USER = os.environ.get("WP_USER")
WP_PASS = os.environ.get("WP_APP_PASSWORD")

# 3. BASE DE DATOS LOCAL (Persistencia con SQLite)
def iniciar_db():
    conn = sqlite3.connect('historial.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS publicados (link TEXT PRIMARY KEY)''')
    conn.commit()
    return conn

# 4. FUNCIÓN PARA PUBLICAR EN WORDPRESS
def publicar_wp(titulo, contenido):
    payload = {
        "title": titulo,
        "content": contenido,
        "status": "publish" # Cambia a "draft" si quieres revisarlo antes
    }
    response = requests.post(WP_URL, json=payload, auth=(WP_USER, WP_PASS))
    if response.status_code == 201:
        print("✅ ¡Artículo publicado exitosamente en WordPress!")
    else:
        print(f"❌ Error al publicar: {response.status_code} - {response.text}")

# 5. LÓGICA PRINCIPAL
def ejecutar_seo_automator():
    conn = iniciar_db()
    c = conn.cursor()
    
    # RSS de noticias (Ejemplo: Noticias de SEO/Tech)
    feed = feedparser.parse("https://www.searchenginelane.com/feed/")
    
    # Procesamos solo la noticia más reciente
    if feed.entries:
        entry = feed.entries[0]
        c.execute("SELECT * FROM publicados WHERE link=?", (entry.link,))
        
        if not c.fetchone():
            print(f"🚀 Procesando nueva noticia: {entry.title}")
            
            # Prompt optimizado para Gemini
            prompt = f"""
            Actúa como un experto en SEO y redacción para blogs. 
            Escribe un artículo completo en español basado en la siguiente noticia: {entry.title}
            Usa el link como referencia: {entry.link}
            
            REGLAS:
            1. Usa formato HTML (h2, p, strong, ul, li). No uses etiquetas html/body/head.
            2. El tono debe ser profesional y útil para el lector.
            3. Estructura el post con una introducción, 2 subtítulos y una conclusión.
            4. Optimiza para la palabra clave principal del título.
            """
            
            response = model.generate_content(prompt)
            articulo_html = response.text
            
            # Mostramos el resultado en el log para control
            print("\n--- ARTÍCULO GENERADO ---")
            print(articulo_html)
            print("-------------------------\n")
            
            # Publicamos en el WordPress del cliente
            publicar_wp(entry.title, articulo_html)
            
            # Guardamos en la memoria local para no repetir mañana
            c.execute("INSERT INTO publicados VALUES (?)", (entry.link,))
            conn.commit()
        else:
            print("😴 No hay noticias nuevas. La última ya fue publicada.")
    
    conn.close()

if __name__ == "__main__":
    ejecutar_seo_automator()
