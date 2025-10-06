# animals_web_generator.py
import json
from html import escape
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATA_PATH = BASE / "animals_data.json"
TPL_PATH  = BASE / "animals_template.html"
OUT_PATH  = BASE / "animals.html"
PLACEHOLDER = "__REPLACE_ANIMALS_INFO__"

def load_data(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_animals_html(data) -> str:
    """Erzeugt <li>-Einträge pro Tier; nur vorhandene Felder werden ausgegeben."""
    items = []
    for item in data:
        lines = []

        name = item.get("name")
        if name:
            lines.append(f"Name: {name}")

        ch = item.get("characteristics", {}) or {}
        diet = ch.get("diet")
        if diet:
            lines.append(f"Diet: {diet}")

        locs = item.get("locations") or []
        if locs:
            lines.append(f"Location: {locs[0]}")

        t = ch.get("type")
        if t:
            lines.append(f"Type: {t}")

        if lines:
            # HTML-sicher + Zeilenumbrüche als <br>
            safe = [escape(s) for s in lines]
            items.append("<li>" + "<br>".join(safe) + "</li>")

    return "\n".join(items)

def fill_template(template_path: Path, animals_html: str, out_path: Path):
    tpl = template_path.read_text(encoding="utf-8")
    if PLACEHOLDER not in tpl:
        raise RuntimeError(f"Platzhalter {PLACEHOLDER} fehlt in {template_path.name}")
    out = tpl.replace(PLACEHOLDER, animals_html)
    out_path.write_text(out, encoding="utf-8")

if __name__ == "__main__":
    data = load_data(DATA_PATH)
    animals_html = build_animals_html(data)
    fill_template(TPL_PATH, animals_html, OUT_PATH)
    print(f"OK → {OUT_PATH.name} mit {animals_html.count('<li>')} Einträgen geschrieben.")