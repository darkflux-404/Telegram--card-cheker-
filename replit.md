# Telegram Card Checker Bot

A Telegram bot built with Pyrogram that checks credit/debit cards against various payment gateways.

## Project Structure

```
telegram-card-checker-bot-main/
├── main.py              # Entry point — initializes Pyrogram client, loads plugins
├── requirements.txt     # Python dependencies
├── gates/               # Payment gate implementations (30+ gates)
├── plugins/             # Pyrogram plugin handlers
│   ├── admin/           # Admin commands (ban/unban, premium, keys, etc.)
│   ├── gates_cmds/      # Commands for each gate
│   ├── handlers/        # Message/callback event handlers
│   └── users/           # User-facing commands (bin lookup, generator, plan, etc.)
├── utilsdf/             # Utility modules
│   ├── db.py            # SQLite database (users, keys, groups)
│   ├── vars.py          # Bot configuration constants
│   ├── functions.py     # Helper functions
│   └── ...
└── assets/              # Static data files
    ├── db_bot.db        # SQLite database (auto-created)
    ├── banned_bins.json
    ├── countrys.json
    ├── gates.json
    └── responses.json
```

## Tech Stack

- **Language**: Python 3.12
- **Bot Framework**: Pyrogram 2.0.106 + pyromod 3.1.6
- **Database**: SQLite (via `utilsdf/db.py`)
- **Crypto**: TgCrypto 1.2.5 (fast Pyrogram encryption)

## Environment Variables / Secrets

All credentials are stored as Replit Secrets:

| Secret | Description |
|--------|-------------|
| `TELEGRAM_API_ID` | API ID from https://my.telegram.org |
| `TELEGRAM_API_HASH` | API Hash from https://my.telegram.org |
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather |
| `TELEGRAM_CHANNEL_LOGS` | (Optional) Channel ID for logging |

## Running

The workflow `Start application` runs:
```
cd telegram-card-checker-bot-main && python main.py
```

This is a console-type workflow (no web frontend).

## Database

SQLite database auto-created at `telegram-card-checker-bot-main/assets/db_bot.db` on first run. Tables:
- `bot` — user records (rank, membership, credits, etc.)
- `bot_keys` — premium activation keys
- `groups` — authorized group chats
