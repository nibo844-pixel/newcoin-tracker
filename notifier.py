import json
import urllib.request
import urllib.parse
import config

def tg_send(text):
    if not config.BOT_TOKEN or not config.ALERT_CHAT_ID:
        print("[DRY-TELEGRAM]\n" + text + "\n")
        return False
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
    data = {"chat_id": config.ALERT_CHAT_ID, "text": text, "disable_web_page_preview": False}
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())

def format_alert(p, d):
    lines = [
        "🆕 Νέο crypto project!",
        f"⛓ {p.get('chain')} | 📜 {p.get('address')}",
    ]
    if p.get("description"):
        lines.append(f"📝 {p['description'][:300]}")
    if d.get("price"):
        lines.append(f"💵 Price: ${d['price']}")
    if d.get("liquidity"):
        lines.append(f"💧 Liq: ${d['liquidity']:,.0f}")
    if d.get("fdv"):
        lines.append(f"📊 FDV: ${d['fdv']:,.0f}")
    if d.get("dex"):
        lines.append(f"🔄 DEX: {d['dex']}")
    if p.get("tg_url"):
        lines.append(f"✈️ Telegram: {p['tg_url']}")
    if p.get("x_url"):
        lines.append(f"𝕏 X/Twitter: {p['x_url']}")
    if p.get("web_url"):
        lines.append(f"🌐 Site: {p['web_url']}")
    if d.get("pair_url"):
        lines.append(f"📈 Chart: {d['pair_url']}")
    return "\n".join(lines)

def post_to_x(text):
    if not (config.X_API_KEY and config.X_ACCESS_TOKEN):
        print("[SKIP-X] λείπουν X keys, μόνο Telegram.")
        return False
    print("[X] X-posting θέλει OAuth1.0a — βάλε keys και ενεργοποίησέ το.")
    return False
