import requests

token = "sbp_230d8596bc1893ab4f32b3b2121a74024c0fbbd8"
project_ref = "fsdtrbbyzfxlnwlmgzwr"

sql = """
CREATE OR REPLACE FUNCTION get_parroquias_geojson()
RETURNS json AS $$
BEGIN
    RETURN (
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', COALESCE(json_agg(ST_AsGeoJSON(t.*)::json), '[]'::json)
        )
        FROM (SELECT * FROM v_parroquias LIMIT 50) t
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
"""

url = f"https://api.supabase.com/v1/projects/{project_ref}/database/query"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

print(f"Inyectando función SQL en {project_ref}...")

try:
    res = requests.post(url, headers=headers, json={"query": sql})
    if res.status_code == 201 or res.status_code == 200:
        print("✅ Función SQL creada con éxito.")
    else:
        print(f"❌ Error: {res.status_code} - {res.text}")
except Exception as e:
    print(f"Error: {e}")
