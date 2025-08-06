# Olivia - AutoGreen's Agent :leaves:
Powered by **Google's Gemini 1.5 Flash** LLM, Olivia is a chatbot that helps you manage your greenhouse like anything.

Introducing **Olivia**, the intelligent greenhouse manager. :robot:

Backed by a Supabase database and decorated by a beautiful React-based frontend, Olivia is all you need to take care of your greenhouse :zap:

## Capabilities:
- Natural conversation with users :speech_balloon:
- Ability to command greenhouse IoT systems to water regions accordingly upon command :droplet:
- Fetch reports of regions upon command :chart:
- Fallback on irrelevant requests :x:

## Setup
### Database Tables:
- Run the following in the SQL Editor after starting a new project in Supabase:
```sql
create table public.greenhouse (
  section varchar(5) primary key,
  is_watered boolean not null default false,
  last_watered timestamp default current_timestamp
);

insert into public.greenhouse(section) values (0),(1),(2),(3);
```

### Agent
- `git clone https://github.com/Coder-X15/AutoGreen -b agent`
- `cd AutoGreen` (**NB**: make sure to either rename this or clone the frontend to a different location in order to avoid conflict)
- Add a `.env` file containing the following to the repo root:
```
GEMINI_API_KEY= <YOUR_GEMINI_API_KEY>
SUPABASE_URL = <YOUR_SUPABASE_URL>
SUPABASE_KEY = <YOUR_SUPABASE_ANON_KEY>
```
- `virtualenv ./venv/ && ./venv/bin/activate && pip install -r requirements.txt` - on Linux (the Windows command is supposed to be similar tbh, but you can put them in a single line like this)
- `python app.py`