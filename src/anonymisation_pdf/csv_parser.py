import csv


def parse_csv(path):
    entries = []
    with open(path, encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        # headers must be exactly 'champ' and 'valeur'
        expected = ["champ", "valeur"]
        if reader.fieldnames is None:
            raise ValueError("CSV vide ou mal formé: pas d'en-têtes")
        if [h.strip() for h in reader.fieldnames] != expected:
            raise ValueError(f"En-têtes CSV invalides, attendu: {expected}, trouvé: {reader.fieldnames}")
        for row in reader:
            entries.append({"champ": row["champ"], "valeur": row["valeur"]})
    return entries
