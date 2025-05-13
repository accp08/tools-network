from flask import Flask, render_template, request, jsonify
import subprocess
import socket
import requests
import nmap
import re
import speedtest

app = Flask(__name__)

# ----------------- Herramientas Auxiliares -----------------

def get_mac_table():
    result = subprocess.run(['arp', '-a'], stdout=subprocess.PIPE)
    output = result.stdout.decode()
    macs = {}
    for line in output.splitlines():
        match = re.search(r'\(([\d\.]+)\) at ([\w:]+)', line)
        if match:
            ip = match.group(1)
            mac = match.group(2)
            macs[ip] = mac
    return macs

def get_vendor(mac):
    try:
        r = requests.get(f"https://api.macvendors.com/{mac}", timeout=3)
        return r.text if r.status_code == 200 else "Desconocido"
    except:
        return "Desconocido"

def get_latency(ip):
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '1', ip],
                                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        output = result.stdout.decode()
        match = re.search(r'time=(\d+\.\d+)', output)
        return f"{match.group(1)} ms" if match else "Sin respuesta"
    except:
        return "Error"

def get_ttl(ip):
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '1', ip],
                                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        output = result.stdout.decode()
        match = re.search(r'ttl=(\d+)', output)
        if match:
            ttl = int(match.group(1))
            if ttl >= 128:
                return f"{ttl} (Windows)"
            elif ttl >= 64:
                return f"{ttl} (Linux/macOS)"
            else:
                return f"{ttl} (Prob. Unix/IoT)"
        return "Desconocido"
    except:
        return "Error"

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Desconocido"

def get_open_ports(ip, top_ports=[22, 80, 443, 8080]):
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=ip, arguments='-Pn -T4 -p ' + ','.join(map(str, top_ports)))
        ports = nm[ip].get('tcp', {})
        return sorted([str(p) for p in ports.keys()])
    except:
        return []

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=2).text
    except:
        return "Desconocida"

# ----------------- Escaneo Principal -----------------

def scan_network(ip_range="192.168.1.0/24"):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, arguments='-sn')
    arp_table = get_mac_table()
    results = []

    for host in nm.all_hosts():
        ip = host
        mac = arp_table.get(ip, "N/A")
        vendor = get_vendor(mac) if mac != "N/A" else "Desconocido"
        latency = get_latency(ip)
        ttl = get_ttl(ip)
        hostname = get_hostname(ip)
        open_ports = get_open_ports(ip)

        results.append({
            "ip": ip,
            "mac": mac,
            "hostname": hostname,
            "vendor": vendor,
            "latencia": latency,
            "ttl": ttl,
            "open_ports": ', '.join(open_ports) if open_ports else "Ninguno",
            "os": "Estimación por TTL"
        })

    return results

# ----------------- Endpoints -----------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/localip")
def api_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "No detectada"
    finally:
        s.close()
    return jsonify({"ip": ip})

@app.route("/api/publicip")
def api_public_ip():
    return jsonify({"ip": get_public_ip()})

@app.route("/api/scan")
def api_scan():
    ip_range = request.args.get('range', '192.168.1.0/24')
    return jsonify(scan_network(ip_range))

@app.route("/api/speedtest")
def api_speedtest():
    s = speedtest.Speedtest()
    s.get_best_server()
    return jsonify({
        "download": round(s.download() / 1_000_000, 2),
        "upload": round(s.upload() / 1_000_000, 2),
        "ping": s.results.ping
    })

@app.route("/api/traceroute")
def api_traceroute():
    target = request.args.get("target", "8.8.8.8")
    try:
        result = subprocess.run(['traceroute', '-n', '-m', '15', target],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        salida = result.stdout.decode(errors="ignore") or result.stderr.decode(errors="ignore")
    except subprocess.TimeoutExpired:
        salida = "❌ Timeout: El traceroute tardó demasiado."
    except Exception as e:
        salida = f"❌ Error: {str(e)}"
    return jsonify({"trace": salida})

@app.route("/api/dns")
def api_dns():
    domain = request.args.get("domain", "google.com")
    try:
        ip = socket.gethostbyname(domain)
        return jsonify({"domain": domain, "ip": ip})
    except socket.gaierror:
        return jsonify({"domain": domain, "ip": "No encontrado"})

@app.route("/api/whois")
def api_whois():
    domain = request.args.get("domain", "google.com")
    result = subprocess.run(['whois', domain], stdout=subprocess.PIPE)
    return jsonify({"whois": result.stdout.decode()})

# ----------------- Ejecutar -----------------

if __name__ == "__main__":
    app.run(debug=True)
