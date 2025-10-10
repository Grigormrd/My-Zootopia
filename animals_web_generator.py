import sys
from html import escape
from typing import List, Dict, Any
import data_fetcher

PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"
TEMPLATE_PATH = "animals_template.html"
OUTPUT_PATH = "animals.html"

def serialize_animal_item(item: Dict[str, Any]) -> str:
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

    details = f'\n  <p class="card__text">\n      ' + "\n      ".join(rows) + "\n  </p>" if rows else ""
    return (
        '<li class="cards__item">\n'
        f'  <div class="card__title">{name}</div>'
        f'{details}\n'
        '</li>'
    )

def build_animals_html(items: List[Dict[str, Any]]) -> str:
    return "\n".join(serialize_animal_item(x) for x in items if isinstance(x, dict))

def render_empty_message(query: str) -> str:
    q = escape(query)
    return (
        '<li class="cards__item">'
        f'<div class="card__title">No results</div>'
        f'<p class="card__text">The animal &quot;{q}&quot; doesn’t exist or couldn’t be fetched.</p>'
        '</li>'
    )

def fill_template(template_path: str, injected_html: str, output_html_path: str) -> None:
    with open(template_path, "r", encoding="utf-8") as f:
        tpl = f.read()
    if PLACEHOLDER not in tpl:
        raise RuntimeError(f"Placeholder {PLACEHOLDER} missing in {template_path}")
    html = tpl.replace(PLACEHOLDER, injected_html)
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else ""
    if not query:
        try:
            query = input("Please enter an animal: ").strip()
        except EOFError:
            query = "Fox"

    data = data_fetcher.fetch_data(query or "Fox")
    injected = build_animals_html(data) if data else render_empty_message(query or "Fox")
    fill_template(TEMPLATE_PATH, injected, OUTPUT_PATH)
    print(f"Website was successfully generated to the file {OUTPUT_PATH}.")