import os
import google.generativeai as genai
import feedparser

# Forzamos la configuración
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

def ejecutar():
    print("\n" + "!"*60)
    print("INICIANDO DEBUG DE MODELOS")
    print("!"*60)
    
    try:
        # Listamos TODO lo que tu API Key puede ver
        modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        print(f"Modelos encontrados: {modelos}")
        
        if not modelos:
            print("❌ No hay modelos disponibles. Revisa tu API Key en Google AI Studio.")
            return

        # Usamos el primero de la lista (el que Google te asigne por región)
        modelo_nombre = modelos[0]
        print(f"✅ Seleccionado automáticamente: {modelo_nombre}")
        
        model = genai.GenerativeModel(modelo_nombre)
        
        feed = feedparser.parse("https://hipertextual.com/feed")
        if feed.entries:
            entry = feed.entries[0]
            print(f"🚀 REDACTANDO SOBRE: {entry.title}")
            
            response = model.generate_content(f"Escribe un post SEO corto en español sobre: {entry.title}. Usa HTML.")
            
            print("\n" + "X"*60)
            print("👇 ARTÍCULO GENERADO 👇")
            print(response.text)
            print("X"*60 + "\n")
            
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")

if __name__ == "__main__":
    ejecutar()
