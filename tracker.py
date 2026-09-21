import time
import config
import storage
import sources
import notifier

def passes_filters(p, d):
    if config.REQUIRE_TELEGRAM and not (p.get("has_telegram") or d.get("has_telegram_detail")):
        return False, "no-telegram"
    if config.REQUIRE_X and not (p.get("has_x") or d.get("has_x_detail")):
        return False, "no-x"
    if d.get("liquidity", 0) and d["liquidity"] < config.MIN_LIQUIDITY_USD:
        return False, "low-liq"
    if d.get("fdv", 0) and d["fdv"] < config.MIN_FDV_USD:
        return False, "low-fdv"
    return True, "ok"

def scan_once(limit=30):
    c = storage.db()
    try:
        items = sources.dexscreener_latest()[:limit]
        print(f"scan: {len(items)} latest profiles")
        news = 0
        for t in items:
            p = sources.normalize_profile(t)
            if not p["id"] or p["id"] == "@":
                continue
            if not storage.is_new(c, p["id"]):
                continue
            if config.REQUIRE_TELEGRAM and not p.get("has_telegram"):
                storage.mark(c, p["id"], int(time.time()))
                print(f"skip {p['id']} (no-tg-prof)", flush=True)
                continue
            if config.REQUIRE_X and not p.get("has_x"):
                storage.mark(c, p["id"], int(time.time()))
                print(f"skip {p['id']} (no-x-prof)", flush=True)
                continue
            d = sources.pair_detail(p["chain"], p["address"])
            ok, reason = passes_filters(p, d)
            storage.mark(c, p["id"], int(time.time()))
            if not ok:
                print(f"skip {p['id']} ({reason})")
                continue
            msg = notifier.format_alert(p, d)
            notifier.tg_send(msg)
            notifier.post_to_x(msg[:260])
            news += 1
            print(f"alert {p['id']}")
        print(f"done: {news} νέα alerts")
        return news
    finally:
        c.close()

def main():
    print(f"Tracker start, interval={config.CHECK_INTERVAL}s, req TG={config.REQUIRE_TELEGRAM} X={config.REQUIRE_X}")
    if not config.BOT_TOKEN or not config.ALERT_CHAT_ID:
        print("ΠΡΟΣΟΧΗ: βάλε BOT_TOKEN και ALERT_CHAT_ID αλλιώς τρέχει σε dry-run.")
    while True:
        try:
            scan_once()
        except Exception as e:
            print("scan err:", str(e)[:200])
        time.sleep(config.CHECK_INTERVAL)

if __name__ == "__main__":
    main()
