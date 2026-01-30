import os
import sqlite3
import google.generativeai as genai
import feedparser
import requests

# Forzamos la configuración base
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def ejecutar():
    print("🔍 Buscando modelos disponibles para tu API Key...")
    
    # 1. LISTAR MODELOS DISPONIBLES
    modelo_a_usar = None
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # Priorizamos Flash o Pro si aparecen
            if '1.5' in m.name:
                modelo_a_usar = m.name
                break
            modelo_a_usar = m.name # Si no, cualquiera que genere contenido
    
    if not modelo_a_usar:
        print("❌ No se encontraron modelos compatibles con esta API Key.")
        return

    print(f"✅ Usando modelo encontrado: {modelo_a_usar}")
    model = genai.GenerativeModel(modelo_a_usar)

    # 2. PROCESAR NOTICIA
    feed = feedparser.parse("https://hipertextual.com/feed")
    if feed.entries:
        entry = feed.entries[0]
        print(f"🚀 REDACTANDO: {entry.title}")
        
        try:
            response = model.generate_content(
                f"Escribe un post SEO corto en español sobre: {entry.title}. Usa HTML."
            )
            
            print("\n" + "X"*50)
            print("📝 ARTÍCULO GENERADO:")
            print("X"*50)
            print(response.text)
            print("X"*50 + "\n")
            
        except Exception as e:
            print(f"❌ Error en generación: {e}")

if __name__ == "__main__":
    ejecutar()
