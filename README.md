# Olivia - AutoGreen's Agent (Frontend) :leaves:
Powered by **Google's Gemini 1.5 Flash** LLM, Olivia is a chatbot that helps you manage your greenhouse like anything.

Introducing **Olivia**, the intelligent greenhouse manager. :robot:

Backed by a Supabase database and decorated by a beautiful React-based frontend, Olivia is all you need to take care of your greenhouse :zap:

## Capabilities:
- Natural conversation with users :speech_balloon:
- Ability to command greenhouse IoT systems to water regions accordingly upon command :droplet:
- Fetch reports of regions upon command :chart:
- Fallback on irrelevant requests :x:

## Setup (Frontend)
- `git clone https://github.com/Coder-X15/AutoGreen -b frontend`
- `cd AutoGreen` (**NB**: make sure to either rename this or clone the frontend to a different location in order to avoid conflict)
- You may have to edit the port number in `.env`, note that.
- `npm install` to install dependencies
- `npm run dev` to start the frontend after starting the agent in the `agent` branch