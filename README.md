# JobMail Assistant

Persönlicher KI-Assistent, der meine E-Mail-Postfächer überwacht, mich bei neuen Mails per Telegram benachrichtigt und alle Jobbewerbungen automatisch erkennt, zuordnet und statistisch auswertet (Absagen, Zusagen, Interview-Einladungen).

## Features

- **Postfächer überwachen**: Gmail, IMAP (GMX, web.de, etc.), optional Outlook
- **Telegram Benachrichtigungen**: Sofortige Benachrichtigung bei neuen Mails mit KI-Zusammenfassung
- **Bewerbungsanalyse**: Automatische Klassifizierung und Status-Tracking
- **Statistiken**: Funnel-Analyse, Quoten, Antwortzeiten
- **Backfill**: Rückwirkende Analyse vergangener Mails

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL + SQLAlchemy 2.0
- Anthropic Claude API
- Telegram Bot
- Streamlit Dashboard
- Docker

## Quick Start

1. **Clone and setup:**
   ```bash
   git clone https://github.com/khusanovich/EMail-Assistant.git
   cd EMail-Assistant
   cp .env.example .env
   # Edit .env with your credentials
   ```

2. **Start database:**
   ```bash
   docker compose up -d db
   ```

3. **Install dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Start application:**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Start dashboard:**
   ```bash
   streamlit run dashboard/streamlit_app.py
   ```

## Development Status

### Phase 0 - Setup ✅
- [x] Project structure
- [x] Database models
- [x] Docker setup
- [x] Configuration

### Phase 1 - Gmail Ingestion (In Progress)
- [ ] OAuth authentication
- [ ] Gmail connector
- [ ] Email ingestion

### Phase 2 - Telegram Notifications (Pending)
### Phase 3 - Classification & Matching (Pending)
### Phase 4 - Statistics & Dashboard (Pending)
### Phase 5 - Backfill & Real-time (Pending)
### Phase 6 - Additional Mail Providers (Pending)
### Phase 7 - Deployment (Pending)

## License

Private project

## Author

Khusanovich
