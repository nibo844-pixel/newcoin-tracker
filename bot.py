import json, time, urllib.request, urllib.parse, os
def tok():
    return open(".env").read().split("BOT_TOKEN=")[1].splitlines()[0].strip()
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
    open(".env","w").write("\n".join(lines)+"\n")
    print(f"saved ALERT_CHAT_ID={cid}", flush=True)
off = 0
print("bot polling...", flush=True)
while True:
    try:
        res = api(f"getUpdates?offset={off}&timeout=20")
        for up in res.get("result", []):
            off = up["update_id"]+1
            m = up.get("message") or {}
            chat = m.get("chat") or {}
            cid = chat.get("id")
            text = m.get("text","")
            print(f"msg from {cid}: {text}", flush=True)
            if cid:
                save_chat(cid)
                try:
                    api("sendMessage", {"chat_id": cid, "text": "✅ Συνδέθηκες! Θα λαμβάνεις εδώ τα νέα crypto projects με Telegram + X. 🚀"})
                except Exception as e:
                    print("send fail", e, flush=True)
    except Exception as e:
        print("poll err", str(e)[:150], flush=True)
        time.sleep(3)
