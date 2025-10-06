import json

def load_data(file_path):
    """ Loads a JSON file """
    with open(file_path, "r", encoding="utf-8") as handle:
        return json.load(handle)

def print_animals(data):
    """Iterates animals and prints selected fields if present."""
    for item in data:
        lines = []

        name = item.get("name")
        if name:
            lines.append(f"Name: {name}")

        characteristics = item.get("characteristics", {}) or {}
        diet = characteristics.get("diet")
        if diet:
            lines.append(f"Diet: {diet}")

        locations = item.get("locations") or []
        first_location = locations[0] if locations else None
        if first_location:
            lines.append(f"Location: {first_location}")

        type_ = characteristics.get("type")
        if type_:
            lines.append(f"Type: {type_}")

        if lines:
            print("\n".join(lines))
            print()  # Leerzeile zwischen den Tieren

if __name__ == "__main__":
    animals_data = load_data("animals_data.json")
    print_animals(animals_data)