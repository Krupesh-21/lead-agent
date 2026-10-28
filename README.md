# Lead Research Agent

An AI agent for freelance outreach. Type a company name. The agent researches the company on the web and returns:

1. A 3-line company summary, with a source URL for each fact
2. A personalized cold email (80 words or fewer) with one clear offer

**Live demo:** https://lead-agent-6rr5rgplexwd5wtet4sect.streamlit.app/
<img width="1358" height="596" alt="image" src="https://github.com/user-attachments/assets/c6bb8d24-e38f-4b17-854c-5b3694564477" />
<img width="1362" height="554" alt="image" src="https://github.com/user-attachments/assets/4b8bbd73-1b5b-4208-9701-ed4e4c7fb4ae" />
<img width="1363" height="592" alt="image" src="https://github.com/user-attachments/assets/c4de7915-c25a-45a4-af61-0f2a93dbdc80" />

## How it works

The app uses **Gemini function calling**. The model decides which tool to call and when.

```
Company name
   │
   ▼
Gemini (system prompt + 2 tools)
   │
   ├── search_web(query)  → DuckDuckGo: top 5 results (title, link, snippet)
   │
   ├── read_page(url)     → requests + BeautifulSoup: first 3,000 chars of page text
   │
   ▼
Summary (with cited URLs) + cold email
```

1. The agent calls `search_web` to find the company's website.
2. The agent calls `read_page` to read the site.
3. It finds what the company does and one problem a freelance developer can solve.
4. It writes the summary and the email.

## Design choices

- **Grounded output:** the prompt tells the model to use only facts from the tools, cite a URL for each fact, and say when it cannot find a fact. This reduces made-up claims.
- **Model fallback:** the app tries `gemini-3-flash-preview` first, then `gemini-2.5-flash`. If one model fails or is removed, the app still works.
- **Bounded page reads:** each page read stops at 3,000 characters, with a 10-second timeout. This keeps token cost and latency low.
- **Free to run:** Gemini free tier, DuckDuckGo search (no API key), and Streamlit Community Cloud hosting.

## Tech stack

| Part | Tool |
|---|---|
| LLM + tool calling | Google Gemini (`google-genai` SDK) |
| Web search | DuckDuckGo (`ddgs`) |
| Page reading | `requests` + `beautifulsoup4` |
| UI + hosting | Streamlit, Streamlit Community Cloud |
| Language | Python |

## Run locally

```bash
git clone https://github.com/Krupesh-21/lead-agent.git
cd lead-agent
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-key-here"
```

Get a free key at https://aistudio.google.com/apikey. Then run:

```bash
streamlit run app.py
```

## Limits

- Results depend on what DuckDuckGo returns and on what the company site shows as plain text. Sites that load content only with JavaScript return little text.
- Check each email before you send it.

## Next steps

- Show each tool call in the UI (agent trace)
- Read more than one page (for example, About and Services pages)
- Export results to CSV for a lead list

## License

MIT
