# V.I.R.G.I.L / D.I.A.N.A_002 Telegram Client

This standalone Python Telegram bot client interfaces your Telegram messages with the V.I.R.G.I.L / D.I.A.N.A_002 FastAPI HTTP API backend.

## Setup

1. Install Python 3.9+ and required packages:

```bash
cd virgildiana_telegram_client
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Edit `bot.py` to update the `API_BASE_URL` if your API is hosted elsewhere.

## Running

```bash
source venv/bin/activate
python bot.py
```

## Systemd Service

Template provided to enable this client as a systemd service.

Enable persistent running with:

```bash
sudo cp virgildiana_telegram_client.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable virgildiana_telegram_client
sudo systemctl start virgildiana_telegram_client
sudo systemctl status virgildiana_telegram_client
```

## Usage

Use Telegram commands:
- `/start`
- `/virgildiana`
- `/virgildiana_report`
- `/virgildiana_restart`
- `/virgildiana_cancel`

