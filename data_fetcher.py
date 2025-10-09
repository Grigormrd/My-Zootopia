import os
from typing import List, Dict, Any
import requests

# ====== Konfiguration (als Konstanten) ======
API_URL: str = "https://api.api-ninjas.com/v1/animals?name={q}"
API_KEY: str = os.getenv("API_NINJAS_KEY", "YOUR_API_KEY_HERE")  # trage deinen Key ein / per Env-Var setzen
HEADERS = {"X-Api-Key": API_KEY}
TIMEOUT_SEC = 15

def fetch_data(animal_name: str) -> List[Dict[str, Any]]:
    """
    Fetches the animals data for the animal 'animal_name'.
    Returns: a list of animals, each a dictionary with keys:
      'name', 'taxonomy', 'locations', 'characteristics', ...
    """
    q = (animal_name or "").strip()
    if not q:
        return []

    if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
        # Keine Exception werfen – der Website-Generator kann einen freundlichen
        # Hinweis rendern, wenn die Liste leer ist.
        return []

    try:
        resp = requests.get(API_URL.format(q=q), headers=HEADERS, timeout=TIMEOUT_SEC)
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else []
    except requests.RequestException:
        # Bei Fehlern geben wir eine leere Liste zurück; der Generator zeigt dann den Empty-State.
        return []