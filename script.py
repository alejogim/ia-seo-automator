import os
import sqlite3
import google.generativeai as genai
import feedparser
import requests

# 1. Configuración de Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Configuración de Base de Datos Local (SQLite)
def iniciar_db():
    conn = sqlite3.connect('historial.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS publicados (link TEXT PRIMARY KEY)''')
    conn.commit()
    return conn

# 3. Lógica de generación
def ejecutar():
    conn = iniciar_db()
    c = conn.cursor()
    
    # Aquí puedes cambiar el RSS por uno del sector de tu cliente
    feed = feedparser.parse("https://www.searchenginelane.com/feed/") 
    
    for entry in feed.entries[:1]: # Solo toma la noticia más reciente
        c.execute("SELECT * FROM publicados WHERE link=?", (entry.link,))
        if not c.fetchone():
            print(f"Generando artículo para: {entry.title}")
            
            prompt = f"Actúa como experto en SEO. Escribe un artículo de blog en español basado en esta noticia: {entry.title}. Usa etiquetas HTML (h2, p, strong). No incluyas etiquetas html/body, solo el contenido."
            
            response = model.generate_content(prompt)
            articulo_html = response.text
            
            # TODO: Aquí agregaremos la función para enviar a WordPress en el siguiente paso
            print("Artículo generado con éxito:")
            print(articulo_html[:200] + "...") 

            # Guardar en la memoria local para no repetir mañana
            c.execute("INSERT INTO publicados VALUES (?)", (entry.link,))
            conn.commit()
        else:
            print("La noticia más reciente ya fue publicada.")
            
    conn.close()

if __name__ == "__main__":
    ejecutar()
