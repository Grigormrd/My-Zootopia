# Animals Web Generator

Generate a simple, styled website that lists animals fetched from the [API Ninjas Animals API](https://api-ninjas.com/api/animals).  
The app asks for an animal name (e.g., `Fox`), fetches matching entries, and renders them as cards in `animals.html`.

## Features

- 🔌 **Decoupled architecture**: 
  - `data_fetcher.py` → fetches data (API Ninjas)
  - `animals_web_generator.py` → generates the website from given data
- 🖼️ **Template-based** rendering (`animals_template.html`) with a placeholder
- 🧩 **“Like A Pro” serialization** (title + info lines inside each card)
- 🧯 **Graceful empty-state** when no results are returned
- 🧪 **Easy to swap data source** (JSON/API/other) as long as output format stays the same

## Project Structure

.
├─ animals_web_generator.py # website generator (HTML rendering, CLI)
├─ data_fetcher.py # data fetching from API Ninjas
├─ animals_template.html # HTML template (contains REPLACE_ANIMALS_INFO)
├─ requirements.txt # Python dependencies (requests)
└─ README.md

## Requirements

- Python 3.10+
- API key from API Ninjas (free tier is fine)

Install dependencies:
```bash
pip install -r requirements.txt
Configuration
Set your API key as environment variable API_NINJAS_KEY.

macOS/Linux (bash/zsh):

export API_NINJAS_KEY="YOUR_API_KEY"
Windows PowerShell:

setx API_NINJAS_KEY "YOUR_API_KEY"
Alternatively, hardcode it in data_fetcher.py by setting API_KEY (not recommended for real projects).

Usage
Interactive prompt (asks for the animal name):

python animals_web_generator.py
# Please enter an animal: Fox
# → Generates animals.html
Direct argument:

python animals_web_generator.py Fox
Open the result:

animals.html in your browser (double-click or use your IDE’s “Preview Static”)

How It Works
animals_web_generator.py asks for an animal name (or reads CLI args).

It calls data_fetcher.fetch_data(animal_name).

The returned list of animal dictionaries is serialized as:

<li class="cards__item">
  <div class="card__title">Wire Fox Terrier</div>
  <p class="card__text">
    <strong>Diet:</strong> Carnivore<br/>
    <strong>Location:</strong> North-America and Canada<br/>
    <strong>Type:</strong> mamal<br/>
  </p>
</li>
The HTML gets injected into animals_template.html (placeholder __REPLACE_ANIMALS_INFO__) and written to animals.html.

Troubleshooting
Empty page / “No results” card: The API returned no items for that query.

No output / error: Check that API_NINJAS_KEY is set and that your network allows outbound requests.

Styling looks plain: Ensure your template contains the card CSS and the placeholder __REPLACE_ANIMALS_INFO__.

Credits
Animal data: API Ninjas — https://api-ninjas.com/api/animals
