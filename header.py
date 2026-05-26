import requests, sys

url = sys.argv[1]

try:
    r = requests.head(url, timeout=5)
    for chave, valor in r.headers.items():
        print(f"{chave}: {valor}")
except requests.exceptions.RequestException as e:
    print(f"Erro: {e}")
    
