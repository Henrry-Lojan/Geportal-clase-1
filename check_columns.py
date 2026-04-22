import requests

token = "sbp_230d8596bc1893ab4f32b3b2121a74024c0fbbd8"
project_ref = "fsdtrbbyzfxlnwlmgzwr"
service_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZzZHRyYmJ5emZ4bG53bG1nendyIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjcwOTU3MiwiZXhwIjoyMDgyIjg1NTcyfQ.cd-ZSC7HnrNdVe6m0un3VjvxS9v_kM1gkGsfEDI35ts"

url = f"https://{project_ref}.supabase.co/rest/v1/v_red_tuberias?limit=1" # v_red_tuberias es una vista, probemos vialidad
url = f"https://{project_ref}.supabase.co/rest/v1/vialidad?limit=1"

headers = {
    "apikey": service_key,
    "Authorization": f"Bearer {service_key}"
}

try:
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        data = res.json()
        if data:
            print(f"Columnas en 'vialidad': {data[0].keys()}")
        else:
            print("La tabla 'vialidad' está vacía.")
    else:
        print(f"Error: {res.status_code} - {res.text}")
except Exception as e:
    print(f"Error: {e}")
