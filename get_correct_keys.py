import requests

token = "sbp_230d8596bc1893ab4f32b3b2121a74024c0fbbd8"
project_ref = "fsdtrbbyzfxlnwlmgzwr"

# Obtener las llaves del proyecto correcto desde el Management API
url = f"https://api.supabase.com/v1/projects/{project_ref}/api-keys"
headers = {"Authorization": f"Bearer {token}"}

try:
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        keys = res.json()
        print("--- LLAVES ENCONTRADAS ---")
        for k in keys:
            print(f"{k['name']}: {k['api_key']}")
    else:
        print(f"Error: {res.status_code} - {res.text}")
except Exception as e:
    print(f"Error: {e}")
