import csv
import os


def write_report_csv(rows, path, mode="dry-run"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    headers = [
        "champ",
        "valeur",
        "found_in_metadata",
        "found_in_content",
        "occurrences_total",
        "pages",
        "mode",
    ]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers)
        writer.writeheader()
        for r in rows:
            writer.writerow({
                "champ": r.get("champ", ""),
                "valeur": r.get("valeur", ""),
                "found_in_metadata": ";".join(r.get("found_in_metadata", [])),
                "found_in_content": str(bool(r.get("found_in_content", False))),
                "occurrences_total": r.get("occurrences_total", 0),
                "pages": ";".join(str(p) for p in r.get("pages", [])),
                "mode": mode,
            })
