# V.I.R.G.I.L / D.I.A.N.A_002 HTTP API Service

This is a minimal FastAPI-powered HTTP API for the V.I.R.G.I.L / D.I.A.N.A_002 7-step idea workflow.

## Setup

1. Install Python 3.9+ and required packages:

```bash
cd virgildiana_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run the API:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

- POST `/start` with JSON `{"session_id": "unique_user_or_chat_id"}` — to start a new workflow session.
- POST `/answer` with JSON `{"session_id": "id", "answer": "your answer"}` — submit answer and receive next question.
- POST `/report` with JSON `{"session_id": "id"}` — get the final report HTML.
- POST `/restart` — restart the workflow for a session.
- POST `/cancel` — cancel the workflow for a session.


## Integration

Your existing Telegram bot can call this HTTP API to implement the conversational workflow.


## Systemd Service

See `virgildiana_api.service` for example systemd unit.

Enable persistent running with:

```bash
sudo cp virgildiana_api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable virgildiana_api
sudo systemctl start virgildiana_api
sudo systemctl status virgildiana_api
```


## Notes

- Store session state externally or persistently as needed.
- Session ID should be unique per Telegram user or chat.
- API currently uses in-memory store; not persistent over restarts.
