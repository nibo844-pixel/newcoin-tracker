import json
import time
import urllib.request

def fetch_json(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": "newcoin-tracker/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def dexscreener_latest():
    try:
        data = fetch_json("https://api.dexscreener.com/token-profiles/latest/v1")
        return data if isinstance(data, list) else []
    except Exception as e:
        print("dex latest err:", str(e)[:150])
        return []

def dexscreener_boosts():
    try:
        data = fetch_json("https://api.dexscreener.com/token-boosts/top/v1")
        return data if isinstance(data, list) else []
    except Exception as e:
        print("dex boosts err:", str(e)[:150])
        return []

def normalize_profile(t):
    links = t.get("links") or []
    has_tg = any((l.get("type") or "").lower() == "telegram" for l in links)
    has_x = any((l.get("type") or "").lower() in ("twitter", "x") for l in links)
    tg_url = next((l.get("url", "") for l in links if (l.get("type") or "").lower() == "telegram"), "")
    x_url = next((l.get("url", "") for l in links if (l.get("type") or "").lower() in ("twitter", "x")), "")
    web_url = next((l.get("url", "") for l in links if (l.get("type") or "").lower() == "website"), t.get("url", ""))
    return {
        "id": t.get("tokenAddress", "") + "@" + t.get("chainId", ""),
        "address": t.get("tokenAddress", ""),
        "chain": t.get("chainId", ""),
        "description": (t.get("description") or "")[:500],
        "has_telegram": has_tg,
        "has_x": has_x,
        "tg_url": tg_url,
        "x_url": x_url,
        "web_url": web_url,
        "icon": t.get("icon", ""),
        "source": "dexscreener",
    }

def pair_detail(chain, address):
    try:
        data = fetch_json(f"https://api.dexscreener.com/latest/dex/tokens/{address}")
        pairs = (data or {}).get("pairs") or []
        if not pairs:
            return {}
        pairs = [p for p in pairs if p.get("chainId") == chain] or pairs
        best = max(pairs, key=lambda p: (p.get("liquidity") or {}).get("usd") or 0)
        info = best.get("info") or {}
        socials = info.get("socials") or []
        websites = info.get("websites") or []
        has_tg = any((s.get("type") or "").lower() == "telegram" for s in socials)
        has_x = any((s.get("type") or "").lower() in ("twitter", "x") for s in socials)
        return {
            "price": best.get("priceUsd", ""),
            "liquidity": ((best.get("liquidity") or {}).get("usd") or 0),
            "fdv": best.get("fdv") or 0,
            "dex": best.get("dexId", ""),
            "pair_url": best.get("url", ""),
            "websites": websites,
            "socials": socials,
            "has_telegram_detail": has_tg,
            "has_x_detail": has_x,
        }
    except Exception as e:
        print("pair detail err:", str(e)[:120])
        return {}
