import requests

project_ref = "fsdtrbbyzfxlnwlmgrzw"
anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZzZHRyYmJ5emZ4bG53bG1nendyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY3MDk1NzIsImV4cCI6MjA4MjI4NTU3Mn0.hAQkrjZZwm2_1XXMirAvF5-BvJ8Wf0yAN2BJgy-OnBE"

url = f"https://{project_ref}.supabase.co/rest/v1/"
headers = {
    "apikey": anon_key,
    "Authorization": f"Bearer {anon_key}"
}

try:
    # Intentamos obtener la especificación OpenAPI para ver las tablas disponibles
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        schema = response.json()
        tables = schema.get('definitions', {}).keys()
        print("Tablas encontradas en 'public':")
        for table in tables:
            print(f"- {table}")
    else:
        print(f"Error al conectar: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
