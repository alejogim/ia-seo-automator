import os
import google.generativeai as genai
import feedparser
from datetime import datetime

# Forzamos la configuración usando la variable de entorno
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def ejecutar():
    print("\n" + "!"*60)
    print("INICIANDO GENERADOR DE POSTS")
    print("!"*60)
    
    try:
        # Es mucho más seguro y rápido definir el modelo directamente
        modelo_nombre = "models/gemini-1.5-flash"
        print(f"✅ Seleccionado el modelo: {modelo_nombre}")
        
        model = genai.GenerativeModel(modelo_nombre)
        
        # Leer el feed RSS de Hipertextual
        feed = feedparser.parse("https://hipertextual.com/feed")
        if feed.entries:
            entry = feed.entries[0]
            print(f"🚀 REDACTANDO SOBRE: {entry.title}")
            
            # Generar contenido con la IA
            prompt = f"Escribe un post SEO corto en español sobre: {entry.title}. Usa HTML para estructurarlo (h2, p, strong)."
            response = model.generate_content(prompt)
            
            # Guardar el resultado en un archivo HTML
            nombre_archivo = "ultimo_post.html"
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                f.write(f"\n")
                f.write(f"<h1>{entry.title}</h1>\n")
                f.write(response.text)
            
            print("\n" + "X"*60)
            print(f"✅ ¡Éxito! Artículo guardado en {nombre_archivo}")
            print("X"*60 + "\n")
            
        else:
            print("⚠️ No se encontraron entradas en el feed RSS.")
            
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")

if __name__ == "__main__":
    ejecutar()
