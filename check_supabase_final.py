import requests

token = "sbp_230d8596bc1893ab4f32b3b2121a74024c0fbbd8"
project_ref = "fsdtrbbyzfxlnwlmgzwr"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 1. Verificar el proyecto
print(f"--- Investigando Proyecto: {project_ref} ---")

# Para listar tablas necesitamos usar la API de administración o consultar vía SQL si tenemos service_role
# Pero con el Access Token podemos usar la API de Management de Supabase
# Vamos a intentar listar las tablas mediante una consulta SQL a través de la API (si es posible)
# O mejor, usamos el token para obtener info del proyecto

try:
    # Obtener detalles del proyecto
    res = requests.get(f"https://api.supabase.com/v1/projects/{project_ref}", headers=headers)
    if res.status_code == 200:
        print("Conexión exitosa al Management API.")
        print(f"Proyecto: {res.json().get('name')}")
    else:
        print(f"Error Management API: {res.status_code} - {res.text}")

    # Ahora vamos a intentar ver qué tablas hay. 
    # Como no hay un endpoint de 'list tables' directo en el Management API que sea fácil de usar sin SQL,
    # voy a intentar una consulta REST básica para ver si 'puntos' existe.
    
    url_rest = f"https://{project_ref}.supabase.co/rest/v1/"
    rest_headers = {
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZzZHRyYmJ5emZ4bG53bG1nendyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjcwOTU3MiwiZXhwIjoyMDgyMjg1NTcyfQ.cd-ZSC7HnrNdVe6m0un3VjvxS9v_kM1gkGsfEDI35ts", # service role de antes
        "Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZzZHRyYmJ5emZ4bG53bG1nendyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjcwOTU3MiwiZXhwIjoyMDgyMjg1NTcyfQ.cd-ZSC7HnrNdVe6m0un3VjvxS9v_kM1gkGsfEDI35ts"
    }
    
    # Consultar el esquema (OpenAPI) para listar tablas
    res_schema = requests.get(url_rest, headers=rest_headers)
    if res_schema.status_code == 200:
        tables = res_schema.json().get('definitions', {}).keys()
        print("\nTablas encontradas:")
        for t in tables:
            print(f"- {t}")
    else:
        print(f"\nError al listar tablas: {res_schema.status_code}")

except Exception as e:
    print(f"Error: {e}")
