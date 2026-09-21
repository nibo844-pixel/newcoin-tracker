import json
import time
import urllib.request

def fetch_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "newcoin-tracker/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def get_daily_summary():
    try:
        profiles = fetch_json("https://api.dexscreener.com/token-profiles/latest/v1")
        top = []
        for p in profiles[:30]:
            addr = p.get("tokenAddress", "")
            chain = p.get("chainId", "")
            try:
                data = fetch_json(f"https://api.dexscreener.com/latest/dex/tokens/{addr}")
                pair = (data.get("pairs") or [{}])[0] if data.get("pairs") else {}
                vol = pair.get("volume", {}).get("h24", 0) or 0
                liq = pair.get("liquidity", {}).get("usd", 0) or 0
                top.append({
                    "name": p.get("description", "")[:80],
                    "chain": chain,
                    "volume": vol,
                    "liquidity": liq,
                    "url": pair.get("url", "")
                })
            except:
                continue
        top.sort(key=lambda x: x["volume"], reverse=True)
        return top[:5]
    except Exception as e:
        print("summary err:", str(e)[:150])
        return []

def format_daily_summary(tokens):
    if not tokens:
        return "📋 Δεν υπάρχουν δεδομένα για σήμερα."
    lines = ["📋 DAILY TOP 5 TOKENS:\n"]
    for i, t in enumerate(tokens[:5], 1):
        lines.append(f"{i}. {t['name'][:50]}")
        lines.append(f"   ⛓ {t['chain']} | 💰 Vol: ${t['volume']:,.0f} | 💧 Liq: ${t['liquidity']:,.0f}")
        if t['url']:
            lines.append(f"   🔗 {t['url']}")
        lines.append("")
    return "\n".join(lines)
