import requests
import streamlit as st
from bs4 import BeautifulSoup
from ddgs import DDGS
from google import genai
from google.genai import types

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# The app tries each model in order. Add new names here if Google changes them.
MODELS = ["gemini-3-flash-preview", "gemini-2.5-flash"]


def search_web(query: str) -> str:
    """Search the web. Return titles, links, and short text."""
    results = DDGS().text(query, max_results=5)
    return "\n".join(f"{r['title']} | {r['href']} | {r['body']}" for r in results)


def read_page(url: str) -> str:
    """Read a web page. Return the first 3000 characters of text."""
    try:
        html = requests.get(
            url, timeout=10, headers={"User-Agent": "Mozilla/5.0"}
        ).text
        return BeautifulSoup(html, "html.parser").get_text(" ", strip=True)[:3000]
    except Exception as e:
        return f"Error: {e}"


SYSTEM = """You are a lead research agent for a freelance developer.
When the user gives a company name:
1. Use search_web to find the company website.
2. Use read_page to read the website.
3. Find: what the company does, and one problem a freelance developer can solve.
4. Write a cold email. Use 80 words or fewer. Use one clear offer.
Use only facts from the tools. Cite the URL for each fact.
If you do not find a fact, say so.
Output: a 3-line summary, then the email."""

st.title("Lead Research Agent")
company = st.text_input("Company name")

if st.button("Research") and company:
    with st.spinner("The agent is working..."):
        for name in MODELS:
            try:
                response = client.models.generate_content(
                    model=name,
                    contents=f"Research {company} and write a cold email.",
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM,
                        tools=[search_web, read_page],
                    ),
                )
                st.markdown(response.text)
                break
            except Exception as e:
                st.error(f"{name} failed: {e}")
