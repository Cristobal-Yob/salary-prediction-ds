import requests

url = "http://127.0.0.1:5000/predict"  # Cambia si tu servidor está en otra dirección
test_data = {
    "python": "yes",
    "excel": "no",
    "sql": "yes",
    "aws": "no",
    "grouped_rating": "3_to_3.5",
    "group_title": "data_scientist",
    "group_sector": "it"
}

response = requests.post(url, json=test_data)
print(response.json())