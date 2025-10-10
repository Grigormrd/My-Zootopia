import os
from typing import List, Dict, Any
import requests

API_URL = "https://api.api-ninjas.com/v1/animals?name={q}"
API_KEY = os.getenv("API_NINJAS_KEY")  # setze deinen Key als Env-Var
HEADERS = {"X-Api-Key": API_KEY} if API_KEY else {}
TIMEOUT_SEC = 15

def fetch_data(animal_name: str) -> List[Dict[str, Any]]:
    """
    Fetches the animals data for 'animal_name' from API Ninjas.
    Returns a list of animal dicts. Bei Fehlern oder fehlendem Key: leere Liste.
    """
    q = (animal_name or "").strip()
    if not q:
        return []
    if not API_KEY:
        # Kein Key gesetzt -> leere Liste; der Generator zeigt dann eine freundliche Meldung.
        return []
    try:
        resp = requests.get(API_URL.format(q=q), headers=HEADERS, timeout=TIMEOUT_SEC)
        resp.raise_for_status()
        data = resp.json()
        return data if isinstance(data, list) else []
    except requests.RequestException:
        return []