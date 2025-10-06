import json
from html import escape

PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"

def load_data(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def serialize_animal_item(item) -> str:
    parts = []
    name = item.get("name")
    if name:
        parts.append(f"Name: {escape(str(name))}<br/>")

    ch = item.get("characteristics", {}) or {}
    diet = ch.get("diet")
    if diet:
        parts.append(f"Diet: {escape(str(diet))}<br/>")

    locs = item.get("locations") or []
    if locs:
        parts.append(f"Location: {escape(str(locs[0]))}<br/>")

    t = ch.get("type")
    if t:
        parts.append(f"Type: {escape(str(t))}<br/>")

    if not parts:
        return ""
    return '<li class="cards__item">' + "\n    ".join(parts) + "</li>"

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