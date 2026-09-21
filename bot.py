import json, time, urllib.request, urllib.parse, os
import config, rugcheck, notifier

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
    print(f"saved ALERT_CHAT_ID={cid}", flush=True)

def handle_rug(chat_id, address):
    api("sendMessage", {"chat_id": chat_id, "text": f"🔍 Checking {address[:30]}..."})
    try:
        analysis = rugcheck.analyze_token("solana", address)
        report = rugcheck.format_rug_report(address, analysis)
        api("sendMessage", {"chat_id": chat_id, "text": report, "disable_web_page_preview": False})
    except Exception as e:
        api("sendMessage", {"chat_id": chat_id, "text": f"❌ Error: {str(e)[:200]}"})

off = 0
print("bot polling with /rug support...", flush=True)
while True:
    try:
        res = api(f"getUpdates?offset={off}&timeout=20")
        for up in res.get("result", []):
            off = up["update_id"] + 1
            m = up.get("message", {})
            chat = m.get("chat", {})
            cid = chat.get("id")
            text = m.get("text", "")

            if cid:
                save_chat(cid)

            if text.startswith("/rug"):
                parts = text.split()
                if len(parts) < 2:
                    api("sendMessage", {"chat_id": cid, "text": "Usage: /rug <token_address>\nExample: /rug CDiRFiVsxARw23uAsNtTxaMhYpnFLfQCcBKS6u8bfXL"})
                else:
                    handle_rug(cid, parts[1])
            elif text in ("/start", "start"):
                api("sendMessage", {"chat_id": cid, "text": "✅ NewCoin Tracker Bot\n\nCommands:\n/rug <address> - Check if token is safe"})
    except Exception as e:
        print("poll err", str(e)[:150], flush=True)
        time.sleep(3)
