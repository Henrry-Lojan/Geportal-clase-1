import requests
import json

token = "sbp_230d8596bc1893ab4f32b3b2121a74024c0fbbd8"
project_ref = "fsdtrbbyzfxlnwlmgrzw"
service_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZzZHRyYmJ5emZ4bG53bG1nendyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjcwOTU3MiwiZXhwIjoyMDgyIjg1NTcyfQ.cd-ZSC7HnrNdVe6m0un3VjvxS9v_kM1gkGsfEDI35ts"

# URL para obtener GeoJSON directamente de PostgREST
url = f"https://{project_ref}.supabase.co/rest/v1/v_parroquias"

headers = {
    "apikey": service_key,
    "Authorization": f"Bearer {service_key}",
    "Accept": "application/geo+json" # Esto le pide a Supabase que devuelva GeoJSON puro
}

print("Extrayendo parroquias de Supabase...")

try:
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        with open("parroquias_loja.json", "w", encoding="utf-8") as f:
            f.write(res.text)
        print("✅ Archivo 'parroquias_loja.json' creado con éxito.")
    else:
        print(f"❌ Error al extraer: {res.status_code}")
        # Intento alternativo como JSON normal si GeoJSON falla
        res = requests.get(url, headers={"apikey": service_key, "Authorization": f"Bearer {service_key}"})
        if res.status_code == 200:
            data = res.json()
            # Envolver en FeatureCollection si es necesario
            with open("parroquias_loja.json", "w", encoding="utf-8") as f:
                json.dump(data, f)
            print("✅ Archivo creado como JSON plano (revisar geometría).")
except Exception as e:
    print(f"Error: {e}")
