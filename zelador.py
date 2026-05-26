#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import ipaddress
from scapy.all import *

conf.verb = 0

# ─────────────────────────────────────────────
#  CORES ANSI
# ─────────────────────────────────────────────
R  = "\033[0m"
G1 = "\033[92m"
G2 = "\033[32m"
G3 = "\033[2;32m"
CY = "\033[96m"
WH = "\033[97m"
YW = "\033[93m"
RD = "\033[91m"
PU = "\033[95m"
DM = "\033[2;32m"
BT = "\033[1;97m"
GR = "\033[90m"

# ─────────────────────────────────────────────
#  BANNER
# ─────────────────────────────────────────────
def banner():
    print(f"""
{G3}                    .                         .   
              .           .       .     .          
        .  .       .   .    .   .    .    .   .    
{G2}     .    .    .     .   .    .   .   .     .      
   .   .    .    .    .   .    .    .   .    .  .  
  .  .   .    .    .    .   .    .    .   .    .   
{G1}  ______     _           _                        
 |___  /    | |         | |                       
    / / ___ | | __ _  __| | ___  _ __             
   / / / _ \| |/ _` |/ _` |/ _ \| '__|            
  / /_|  __/| | (_| | (_| | (_) | |               
{G2} /_____\___||_|\__,_|\__,_|\___/|_|               
{R}
{CY}       =[ {BT}Zelador v2.0.0{R}{CY} - Python Network Scanner  ]={R}
{WH}  + -- --=[ {G1}varredura de portas{R}{WH}  |  {YW}TCP SYN stealth scan{R}{WH}   ]=--
{WH}  + -- --=[ {G1}varredura de hosts{R}{WH}   |  {YW}ICMP ping sweep / CIDR{R}{WH} ]=--
{WH}  + -- --=[ {PU}mascara de subrede{R}{WH}   |  {RD}ex: 192.168.1.0/24{R}{WH}     ]=--
{GR}  + -- --=[ use com responsabilidade | apenas redes autorizadas ]=--{R}
""")

# ─────────────────────────────────────────────
#  VARREDURA DE PORTAS
# ─────────────────────────────────────────────
def scan_portas(ip: str):
    print(f"\n{CY}[*]{R} Iniciando varredura de portas em {YW}{ip}{R}")
    print(f"{CY}[*]{R} Escaneando portas 1–65535...\n")

    abertas = []
    try:
        for porta in range(1, 65536):
            pacote = IP(dst=ip) / TCP(dport=porta, flags="S")
            resp = sr1(pacote, timeout=0.01, verbose=False)
            if resp and resp.haslayer(TCP) and resp[TCP].flags == "SA":
                abertas.append(porta)
                print(f"  {G1}[+]{R} Porta {BT}{porta}{R} {G1}ABERTA{R}")
    except KeyboardInterrupt:
        print(f"\n{YW}[!]{R} Varredura interrompida pelo usuário.")

    print(f"\n{CY}[*]{R} Varredura concluída. {G1}{len(abertas)}{R} porta(s) abertas encontradas.")
    if abertas:
        print(f"{GR}     Portas: {', '.join(map(str, abertas))}{R}")

# ─────────────────────────────────────────────
#  VARREDURA DE HOSTS (CIDR)
# ─────────────────────────────────────────────
def scan_hosts(rede_cidr: str):
    try:
        rede = ipaddress.IPv4Network(rede_cidr, strict=False)
    except ValueError as e:
        print(f"{RD}[!]{R} Endereço inválido: {e}")
        print(f"{YW}    Formato esperado: 192.168.1.0/24{R}")
        return

    mascara    = str(rede.netmask)
    prefixo    = rede.prefixlen
    total      = rede.num_addresses - 2
    hosts_list = list(rede.hosts())

    print(f"\n{CY}[*]{R} Rede alvo   : {YW}{rede.network_address}/{prefixo}{R}")
    print(f"{CY}[*]{R} Mascara     : {YW}{mascara}{R}")
    print(f"{CY}[*]{R} Broadcast   : {YW}{rede.broadcast_address}{R}")
    print(f"{CY}[*]{R} Hosts totais: {YW}{total}{R}")
    print(f"{CY}[*]{R} Iniciando ping sweep...\n")

    ativos = []
    try:
        for host in hosts_list:
            ip_str = str(host)
            pacote = IP(dst=ip_str) / ICMP()
            resp   = sr1(pacote, timeout=0.05, verbose=False)
            if resp:
                ativos.append(ip_str)
                print(f"  {G1}[+]{R} Host {BT}{ip_str}{R} {G1}ATIVO{R}")
    except KeyboardInterrupt:
        print(f"\n{YW}[!]{R} Varredura interrompida pelo usuário.")

    print(f"\n{CY}[*]{R} Varredura concluída.")
    print(f"{CY}[*]{R} {G1}{len(ativos)}{R} host(s) ativos em {YW}{rede_cidr}{R}")
    if ativos:
        print(f"{GR}     Hosts: {', '.join(ativos)}{R}")

# ─────────────────────────────────────────────
#  MENU PRINCIPAL
# ─────────────────────────────────────────────
def menu():
    banner()
    while True:
        print(f"{WH}  {'─'*48}{R}")
        print(f"  {G1}[1]{R} Varredura de Portas  (TCP SYN)")
        print(f"  {G1}[2]{R} Varredura de Hosts   (ICMP / CIDR)")
        print(f"  {RD}[0]{R} Sair")
        print(f"{WH}  {'─'*48}{R}")

        try:
            opcao = input(f"\n{G2}  zelador{R}{GR}(alvo){R}{WH} > {R}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{YW}[!]{R} Saindo...\n")
            sys.exit(0)

        if opcao == "0":
            print(f"\n{G2}[*]{R} Encerrando o Zelador. Até logo!\n")
            sys.exit(0)

        elif opcao == "1":
            ip = input(f"  {CY}IP alvo{R} (ex: 192.168.1.1) > ").strip()
            if not ip:
                print(f"{RD}[!]{R} IP inválido.\n")
                continue
            scan_portas(ip)

        elif opcao == "2":
            rede = input(f"  {CY}Rede alvo{R} (ex: 192.168.1.0/24) > ").strip()
            if "/" not in rede:
                print(f"{RD}[!]{R} Informe a mascara CIDR. Ex: 192.168.1.0/24\n")
                continue
            octetos = rede.split("/")[0].split(".")
            if octetos[-1] != "0":
                print(f"{YW}[!]{R} Dica: o último octeto deve ser 0 (ex: 192.168.1.0/24)")
                confirmar = input(f"  Continuar mesmo assim? {WH}[s/N]{R} > ").strip().lower()
                if confirmar != "s":
                    continue
            scan_hosts(rede)

        else:
            print(f"{RD}[!]{R} Opção inválida. Use 0, 1 ou 2.\n")

        print()

# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    menu()
