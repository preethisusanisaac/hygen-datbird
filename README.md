# Hygen Real Estate MVP1

WhatsApp-based lead management system for real estate projects.

## Features

- 🤖 WhatsApp chatbot for lead qualification
- 📊 Streamlit dashboard for lead management
- 💬 Automated conversation flow
- 📅 Site visit scheduling
- 🏢 Multi-project support

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Frontend**: Streamlit
- **Messaging**: WhatsApp Cloud API
- **Deployment**: Render.com

## Local Development

### Prerequisites

- Python 3.12+
- PostgreSQL 16+
- Virtual environment

### Setup

1. **Clone the repository**:
```bash
git clone https://github.com/YOUR_USERNAME/hygen_re_mvp1.git
cd hygen_re_mvp1
```

2. **Create virtual environment**:
```bash
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
Create a `.env` file:
```env
DATABASE_URL=postgresql+psycopg2://hygen_user:Hygen123@localhost:5432/HYGEN?options=-csearch_path=hygen_re
WHATSAPP_VERIFY_TOKEN=your_verify_token
WHATSAPP_ACCESS_TOKEN=your_access_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
DEFAULT_PROJECT_ID=1
```

5. **Run database migrations** (if schema not created):
```bash
psql -U postgres -d HYGEN -f schema.sql
```

6. **Start FastAPI backend**:
```bash
uvicorn app.main:app --reload
```

7. **Start Streamlit dashboard** (in another terminal):
```bash
streamlit run dashboard/dashboard.py
```

## Project Structure

```
hygen_re_mvp1/
├── app/
│   ├── api/
│   │   ├── health.py          # Health check endpoint
│   │   └── whatsapp.py        # WhatsApp webhook
│   ├── models/
│   │   ├── builder.py         # Builder model
│   │   ├── project.py         # Project model
│   │   ├── lead.py            # Lead model
│   │   └── db.py              # Database setup
│   ├── services/
│   │   ├── conversation.py    # Conversation engine
│   │   └── lead_service.py    # Lead management
│   ├── schemas/               # Pydantic schemas
│   ├── config.py              # Configuration
│   └── main.py                # FastAPI app
├── dashboard/
│   └── dashboard.py           # Streamlit dashboard
├── requirements.txt           # Python dependencies
├── render.yaml               # Render.com config
└── .env                      # Environment variables (not in git)
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions to Render.com.

## API Endpoints

- `GET /health` - Health check
- `GET /webhook/whatsapp` - WhatsApp webhook verification
- `POST /webhook/whatsapp` - Receive WhatsApp messages
- `GET /docs` - Interactive API documentation

## Database Schema

- **builders** - Real estate builders/developers
- **projects** - Real estate projects
- **leads** - Customer leads
- **conversations** - Lead conversations
- **messages** - Individual messages

## License

Proprietary
