import os
import sys
import json
from html import escape
from typing import List, Dict, Any
import requests

PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"
API_URL = "https://api.api-ninjas.com/v1/animals?name={q}"

def fetch_animals_from_api(query: str) -> List[Dict[str, Any]]:
    """Fetch animals via API Ninjas /v1/animals?name=..."""
    api_key = os.getenv("API_NINJAS_KEY") or os.getenv("X_API_KEY") or os.getenv("API_NINJAS_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing API key. Set env var API_NINJAS_KEY (Profile: https://api-ninjas.com/profile)"
        )

    resp = requests.get(
        API_URL.format(q=query),
        headers={"X-Api-Key": api_key},
        timeout=15,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"API error {resp.status_code}: {resp.text[:200]}")

    data = resp.json()
    if not isinstance(data, list):
        # API usually returns a list; be defensive
        return []
    return data

def serialize_animal_item(item: Dict[str, Any]) -> str:
    """Like A Pro: <li class='cards__item'><div class='card__title'>...</div><p class='card__text'>...</p></li>"""
    name = escape(str(item.get("name", "Unknown")))
    ch = item.get("characteristics", {}) or {}
    locs = item.get("locations") or []
    first_loc = locs[0] if locs else None

    rows = []
    diet = ch.get("diet")
    if diet:
        rows.append(f"<strong>Diet:</strong> {escape(str(diet))}<br/>")
    if first_loc:
        rows.append(f"<strong>Location:</strong> {escape(str(first_loc))}<br/>")
    t = ch.get("type")
    if t:
        rows.append(f"<strong>Type:</strong> {escape(str(t))}<br/>")

    detail_html = ""
    if rows:
        detail_html = '\n  <p class="card__text">\n      ' + "\n      ".join(rows) + "\n  </p>"

    return (
        '<li class="cards__item">\n'
        f'  <div class="card__title">{name}</div>'
        f'{detail_html}\n'
        '</li>'
    )

def build_animals_html(items: List[Dict[str, Any]]) -> str:
    return "\n".join(serialize_animal_item(x) for x in items if isinstance(x, dict))

def render_empty_message(query: str) -> str:
    """Milestone 3: freundliche Message als Card (valides HTML innerhalb des <ul>)."""
    q = escape(query)
    return (
        '<li class="cards__item">'
        f'<div class="card__title">No results</div>'
        f'<p class="card__text">The animal &quot;{q}&quot; doesn’t exist.</p>'
        '</li>'
    )

def fill_template(template_path: str, injected_html: str, output_html_path: str) -> None:
    with open(template_path, "r", encoding="utf-8") as f:
        tpl = f.read()
    html = tpl.replace(PLACEHOLDER, injected_html)
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    # Milestone 2: Name vom User (CLI-Arg priorisiert, sonst prompt)
    query = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else ""
    if not query:
        try:
            query = input("Enter a name of an animal: ").strip()
        except EOFError:
            query = "Fox"  # fallback for non-interactive

    try:
        data = fetch_animals_from_api(query or "Fox")
        injected = build_animals_html(data) if data else render_empty_message(query or "Fox")
        fill_template("animals_template.html", injected, "animals.html")
        print('Website was successfully generated to the file animals.html.')
        print(f'Query: "{query or "Fox"}", items: {injected.count("<li class=\"cards__item\">")}')
    except Exception as e:
        # Zeige Fehler im HTML statt im Terminal (für konsistente UX)
        injected = (
            '<li class="cards__item">'
            '<div class="card__title">Error</div>'
            f'<p class="card__text">{escape(str(e))}</p>'
            '</li>'
        )
        fill_template("animals_template.html", injected, "animals.html")
        print("animals.html generated with error message.")