# V.I.R.G.I.L / D.I.A.N.A_002 Standalone Telegram Bot

## Description

This standalone Python Telegram bot implements the V.I.R.G.I.L / D.I.A.N.A_002 idea development 7-step workflow.

It is intended to be run separately on the VPS so as not to interfere with your existing OpenClaw bot.

## Requirements

- Python 3.9+
- python-telegram-bot package
- python-dotenv package

## Installation

```bash
cd virgildiana_bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and add your Telegram bot token:

```
cp .env.example .env
# Edit .env to add your token
```

## Running the Bot

```bash
source venv/bin/activate
python bot.py
```

## Systemd Service

Template and instructions are provided below to enable this bot as a systemd service on your VPS.

## Commands Supported

- `/start` - Show welcome message.
- `/virgildiana` - Start idea workflow.
- `/virgildiana_report` - Generate and show current report.
- `/virgildiana_restart` - Restart workflow.
- `/virgildiana_cancel` - Cancel workflow.

## Notes

- The bot uses polling for simplicity and easy setup.
- Session state is per-user in memory.
- Report is generated in Telegram HTML format.
