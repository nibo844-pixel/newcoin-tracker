import json
import time
import urllib.request

def fetch_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "newcoin-tracker/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def get_volume_alerts(min_volume=100000):
    try:
        data = fetch_json("https://api.dexscreener.com/latest/dex/tokens")
        pairs = data.get("pairs", [])
        alerts = []
        for p in pairs:
            vol = p.get("volume", {}).get("h24", 0) or 0
            if vol >= min_volume:
                alerts.append({
                    "name": p.get("baseToken", {}).get("name", ""),
                    "symbol": p.get("baseToken", {}).get("symbol", ""),
                    "volume": vol,
                    "price": p.get("priceUsd", "0"),
                    "change_24h": p.get("priceChange", {}).get("h24", 0),
                    "chain": p.get("chainId", ""),
                    "dex": p.get("dexId", ""),
                    "url": p.get("url", "")
                })
        alerts.sort(key=lambda x: x["volume"], reverse=True)
        return alerts[:10]
    except Exception as e:
        print("volume err:", str(e)[:150])
        return []

def format_volume_alert(alerts):
    if not alerts:
        return "📊 Δεν υπάρχουν τεράστια volume αυτή τη στιγμή."
    lines = ["📊 VOLUME ALERTS:\n"]
    for a in alerts[:5]:
        emoji = "🟢" if a["change_24h"] > 0 else "🔴"
        lines.append(f"{emoji} {a['symbol']} ({a['chain']})")
        lines.append(f"   💰 Volume: ${a['volume']:,.0f}")
        lines.append(f"   💵 Price: ${a['price']}")
        lines.append(f"   📈 24h: {a['change_24h']}%")
        lines.append(f"   🔄 {a['dex']}")
        lines.append(f"   🔗 {a['url']}\n")
    return "\n".join(lines)
