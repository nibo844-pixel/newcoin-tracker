import json, time, urllib.request, urllib.parse, os
import config, rugcheck, notifier, alerts, daily_summary

def tok():
    lines = open(".env").read().splitlines()
    for l in lines:
        if l.startswith("BOT_TOKEN="):
            return l.split("=", 1)[1].strip()
    return os.environ.get("BOT_TOKEN", "")

def api(method, data=None):
    t = tok()
    url = f"https://api.telegram.org/bot{t}/{method}"
    body = json.dumps(data or {}).encode() if data else None
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode())

def save_chat(cid):
    lines = [l for l in open(".env").read().splitlines() if not l.startswith("ALERT_CHAT_ID=")]
    lines.append(f"ALERT_CHAT_ID={cid}")
    open(".env", "w").write("\n".join(lines) + "\n")

def handle_rug(chat_id, address):
    api("sendMessage", {"chat_id": chat_id, "text": f"🔍 Checking {address[:30]}..."})
    try:
        analysis = rugcheck.analyze_token("solana", address)
        report = rugcheck.format_rug_report(address, analysis)
        api("sendMessage", {"chat_id": chat_id, "text": report, "disable_web_page_preview": False})
    except Exception as e:
        api("sendMessage", {"chat_id": chat_id, "text": f"❌ Error: {str(e)[:200]}"})

def handle_volume(chat_id):
    api("sendMessage", {"chat_id": chat_id, "text": "📊 Scanning volume..."})
    try:
        vol_alerts = alerts.get_volume_alerts(min_volume=50000)
        report = alerts.format_volume_alert(vol_alerts)
        api("sendMessage", {"chat_id": chat_id, "text": report})
    except Exception as e:
        api("sendMessage", {"chat_id": chat_id, "text": f"❌ Error: {str(e)[:200]}"})

def handle_summary(chat_id):
    api("sendMessage", {"chat_id": chat_id, "text": "📋 Generating daily summary..."})
    try:
        summary = daily_summary.get_daily_summary()
        report = daily_summary.format_daily_summary(summary)
        api("sendMessage", {"chat_id": chat_id, "text": report})
    except Exception as e:
        api("sendMessage", {"chat_id": chat_id, "text": f"❌ Error: {str(e)[:200]}"})

HELP_TEXT = """🤖 NewCoin Tracker Bot

/rug <address> - Check if token is safe
/volume - Top volume alerts
/summary - Daily top 5 tokens
/start - Start bot

💡 Auto alerts: new tokens with Telegram + X
🛡️ Rug detection: liquidity, socials, ratio"""

off = 0
print("bot polling with all features...", flush=True)
while True:
    try:
        res = api(f"getUpdates?offset={off}&timeout=20")
        for up in res.get("result", []):
            off = up["update_id"] + 1
            m = up.get("message", {})
            cid = (m.get("chat") or {}).get("id")
            text = m.get("text", "").strip()

            if not cid:
                continue

            save_chat(cid)

            if text.startswith("/rug"):
                parts = text.split()
                if len(parts) < 2:
                    api("sendMessage", {"chat_id": cid, "text": "Usage: /rug <token_address>"})
                else:
                    handle_rug(cid, parts[1])
            elif text == "/volume":
                handle_volume(cid)
            elif text == "/summary":
                handle_summary(cid)
            elif text in ("/start", "start"):
                api("sendMessage", {"chat_id": cid, "text": HELP_TEXT})
            elif text in ("/help", "help"):
                api("sendMessage", {"chat_id": cid, "text": HELP_TEXT})
    except Exception as e:
        print("poll err", str(e)[:150], flush=True)
        time.sleep(3)
