import sources

SUSPICIOUS_CONTRACTS = [
    "mint", "pause", "blacklist", "freeze", "upgrade",
    "owner", "authority", "proxy", "selfdestruct"
]

def analyze_token(chain, address):
    flags = []
    risk = "LOW"
    
    d = sources.pair_detail(chain, address)
    
    liq = d.get("liquidity", 0)
    fdv = d.get("fdv", 0)
    socials = d.get("socials", [])
    
    # Liquidity checks
    if liq == 0:
        flags.append("❌ ΜΗΔΕΝΙΚΗ LIQUIDITY")
        risk = "CRITICAL"
    elif liq < 5000:
        flags.append(f"⚠️ LOW LIQUIDITY: ${liq:,.0f}")
        risk = "HIGH"
    elif liq < 20000:
        flags.append(f"⚠️ MEDIUM LIQUIDITY: ${liq:,.0f}")
        if risk != "CRITICAL":
            risk = "MEDIUM"
    
    # FDV vs Liquidity ratio
    if fdv > 0 and liq > 0:
        ratio = fdv / liq
        if ratio > 100:
            flags.append(f"🚨 HIGH FDV/LIQ RATIO: {ratio:.0f}x")
            risk = "CRITICAL"
        elif ratio > 50:
            flags.append(f"⚠️ HIGH FDV/LIQ RATIO: {ratio:.0f}x")
            if risk not in ("CRITICAL",):
                risk = "HIGH"
    
    # Social presence
    tg = d.get("has_telegram_detail", False)
    x = d.get("has_x_detail", False)
    if not tg and not x:
        flags.append("❌ NO SOCIALS (Telegram + X)")
        risk = "HIGH"
    elif not tg:
        flags.append("⚠️ NO TELEGRAM")
    elif not x:
        flags.append("⚠️ NO X/TWITTER")
    
    # Websites
    websites = d.get("websites", [])
    if not websites:
        flags.append("⚠️ NO WEBSITE")
    
    # Dex check
    dex = d.get("dex", "")
    if dex in ("moonshot", "pump.fun"):
        flags.append(f"⚠️ NEW LAUNCHPAD: {dex}")
        if risk not in ("CRITICAL",):
            risk = "MEDIUM"
    
    # Socials count
    if len(socials) < 2:
        flags.append("⚠️ LOW SOCIAL PRESENCE")
    
    return {
        "risk": risk,
        "flags": flags,
        "liquidity": liq,
        "fdv": fdv,
        "dex": dex,
        "pair_url": d.get("pair_url", ""),
        "price": d.get("price", "")
    }

def format_rug_report(address, analysis):
    risk_emoji = {
        "LOW": "🟢",
        "MEDIUM": "🟡",
        "HIGH": "🟠",
        "CRITICAL": "🔴"
    }
    
    lines = [
        f"{risk_emoji.get(analysis['risk'], '⚪')} RISK: {analysis['risk']}",
        f"📜 {address[:20]}...",
        f"💧 Liq: ${analysis['liquidity']:,.0f}",
        f"📊 FDV: ${analysis['fdv']:,.0f}",
        f"🔄 DEX: {analysis['dex']}"
    ]
    
    if analysis['price']:
        lines.append(f"💵 Price: ${analysis['price']}")
    
    if analysis['flags']:
        lines.append("\n🚨 RED FLAGS:")
        for f in analysis['flags']:
            lines.append(f"  • {f}")
    else:
        lines.append("\n✅ NO RED FLAGS DETECTED")
    
    if analysis['pair_url']:
        lines.append(f"\n📈 Chart: {analysis['pair_url']}")
    
    return "\n".join(lines)
