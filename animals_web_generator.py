import json
from html import escape

PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"

def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def serialize_animal_item(item) -> str:
    """Serialisiert ein Tier als <li class="cards__item"> mit Titel & Infozeilen."""
    name = escape(str(item.get("name", "Unknown")))
    ch = item.get("characteristics", {}) or {}

    diet = ch.get("diet")
    locs = item.get("locations") or item.get("locations")  # robust, falls Struktur variiert
    first_loc = (item.get("locations") or [])
    first_loc = first_loc[0] if first_loc else None
    t = ch.get("type")

    rows = []
    if diet:
        rows.append(f"<strong>Diet:</strong> {escape(str(diet))}<br/>")
    if first_loc:
        rows.append(f"<strong>Location:</strong> {escape(str(first_loc))}<br/>")
    if t:
        rows.append(f"<strong>Type:</strong> {escape(str(t))}<br/>")

    # p-Block nur, wenn es wenigstens eine Zeile gibt
    details = f'\n  <p class="card__text">\n      ' + "\n      ".join(rows) + '\n  </p>' if rows else ""

    return (
        '<li class="cards__item">\n'
        f'  <div class="card__title">{name}</div>'
        f'{details}\n'
        '</li>'
    )
def build_animals_html(data) -> str:
    return "\n".join(filter(None, (serialize_animal_item(a) for a in data)))

def fill_template(template_path, animals_html, output_html_path):
    with open(template_path, "r", encoding="utf-8") as f:
        tpl = f.read()
    html = tpl.replace(PLACEHOLDER, animals_html)
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    data = load_data("animals_data.json")
    animals_html = build_animals_html(data)
    fill_template("animals_template.html", animals_html, "animals.html")
    print(f"OK: animals.html written with {animals_html.count('<li class=\"cards__item\">')} items.")