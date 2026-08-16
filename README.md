# Telegram Bot Deployer — Phase 1 (Core Skeleton)

এটি পুরো প্রজেক্টের **Phase 1**: bot boot হয়, `/start` কাজ করে, main menu দেখায়, এবং
Plans database থেকে load হয় (এখনো খালি, কারণ Plan CRUD আসবে Phase 2-তে)।

## এই Phase-এ যা আছে
- ✅ aiogram 3.x bot boots, polling mode-এ চলে
- ✅ `/start` → user DB-তে save হয় (get-or-create) + banned-check
- ✅ Main menu: 🚀 Deploy Bot | 🤖 My Bots | 📋 Plans | 🖥 Server Status | 🎟 Support
- ✅ SQLAlchemy 2.x async models — পুরো schema (users, plans, payments, bots,
  deployments, bot_versions, backups, environment_variables, workers, jobs,
  system_logs, broadcasts, bans) সংজ্ঞায়িত, যাতে পরের phase-এ migration ভাঙতে না হয়
- ✅ SQLite (dev) / PostgreSQL (prod) — শুধু `DATABASE_URL` বদলালেই চলবে
- 🔜 Deploy Bot, My Bots, Server Status বাটনে এখন শুধু "coming soon" placeholder —
  আসল ফাংশনালিটি আসবে Phase 2 (Plans+Admin) থেকে শুরু করে পরবর্তী phase-গুলোতে

## 1. Installation

```bash
python3.12 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Environment Variables

```bash
cp .env.example .env
```

`.env` ফাইলে পূরণ করুন:

| Variable | বর্ণনা |
|---|---|
| `BOT_TOKEN` | BotFather থেকে পাওয়া main bot-এর token |
| `ADMIN_IDS` | কমা দিয়ে আলাদা করা Telegram user ID (admin panel পরের phase-এ) |
| `DATABASE_URL` | ডিফল্ট SQLite; production-এ PostgreSQL URL দিন |
| `SUPPORT_USERNAME` | Support বাটনে যে username দেখাবে |

## 3. Telegram Bot Setup

1. Telegram-এ [@BotFather](https://t.me/BotFather)-কে `/newbot` পাঠান
2. পাওয়া token টি `.env`-এ `BOT_TOKEN=` এর পরে বসান
3. Token কখনো কারো সাথে শেয়ার করবেন না — এটি logs/messages-এ কখনো দেখানো হয় না

## 4. Database Setup

Phase 1-এ `main.py` চালু হলে টেবিলগুলো নিজে থেকেই তৈরি হয়ে যায় (`init_db()`)।
Production-এ Alembic migration ব্যবহার হবে — সেটি Phase 2-তে যুক্ত হবে।

## 5. Run Locally

```bash
python main.py
```

Telegram-এ bot-কে `/start` পাঠান — main menu আসা উচিত।

## 6. Docker

```bash
docker build -t deployer-bot .
docker run --env-file .env deployer-bot
```

## 7. Railway Deployment

- এই repo Railway-তে connect করুন
- Environment variables (উপরের টেবিল অনুযায়ী) Railway dashboard-এ সেট করুন
- Railway স্বয়ংক্রিয়ভাবে `Dockerfile` detect করে build করবে
- Start command: `python main.py` (Dockerfile CMD-তে already সেট করা আছে)
- Database: Railway-এর PostgreSQL addon যোগ করে `DATABASE_URL` সেট করুন

## Checklist (Phase 1 scope)

- [x] Bot starts
- [x] `/start` works
- [x] Main menu renders, all 5 buttons respond
- [x] Plans load from DB (empty state handled)
- [ ] Admin panel (Phase 2)
- [ ] Payment flow (Phase 3)
- [ ] ZIP upload/extraction (Phase 4)
- [ ] Worker/deployment queue (Phase 5)
- [ ] My Bots management (Phase 6)

## Common Errors

| Error | কারণ / সমাধান |
|---|---|
| `pydantic_core.ValidationError: BOT_TOKEN` | `.env` ফাইলে `BOT_TOKEN` সেট করা হয়নি |
| `TelegramUnauthorizedError` | Token ভুল অথবা revoke হয়ে গেছে — BotFather থেকে নতুন token নিন |
| `sqlite3.OperationalError: unable to open database file` | `UPLOAD_DIR`/working directory-তে write permission নেই |

---
**Next:** Phase 2 — Plan CRUD + Admin panel (`/admin`)।
