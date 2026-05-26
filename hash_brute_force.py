import hashlib, sys

senha = sys.argv[1]
lista = open(sys.argv[2])
tipo = sys.argv[3]

senha = senha.replace('"', '')

if tipo == 'md5':
    for palavra in lista:
        possivel_senha = hashlib.md5(palavra.strip().encode()).hexdigest()
        if possivel_senha == senha:
            print(f"{senha} --> {palavra}")
            break

