# 🆕 NewCoin Tracker — Telegram + X

Μόλις βγαίνει καινούργιο crypto project στο DexScreener, το μαθαίνεις αμέσως.

Φίλτρο: κρατάει ΜΟΝΟ όσα έχουν **Telegram + X (Twitter)**. Τα άλλα τα αγνοεί.

## Γρήγορα
1. Φτιάξε bot από @BotFather → πάρε `BOT_TOKEN`
2. Στείλε μήνυμα στο bot σου, βρες το chat id (`ALERT_CHAT_ID`)
3. `cp .env.example .env` και γέμισέ τα
4. `python3 tracker.py` ή `./run.sh`

## Deploy στο Render
- Blueprint: `render.yaml` (worker tracker + web health)
- Βάλε στο Dashboard: `BOT_TOKEN`, `ALERT_CHAT_ID`

## Πηγές
- DexScreener latest profiles (χωρίς key, δωρεάν)
- DexScreener pair detail (τιμή / liq / fdv / socials)

## X auto-post
Προαιρετικό. Αν βάλεις X keys, ποστάρει κι εκεί, αλλιώς στέλνει μόνο Telegram.
