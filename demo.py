import requests

retour = requests.get("http://10.0.0.36:5000/bonjour")
print(retour.json())

