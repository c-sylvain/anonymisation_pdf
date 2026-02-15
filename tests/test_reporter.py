import csv
from anonymisation_pdf.reporter import write_report_csv


def test_write_report_csv(tmp_path):
    rows = [
        {
            "champ": "name",
            "valeur": "Alice",
            "found_in_metadata": ["Author"],
            "found_in_content": True,
            "occurrences_total": 2,
            "pages": [1, 3],
        }
    ]
    out = tmp_path / "report.csv"
    write_report_csv(rows, str(out), mode="dry-run")
    # verify file exists and header
    with open(out, encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        assert "champ" in reader.fieldnames
        data = list(reader)
        assert len(data) == 1
        assert data[0]["champ"] == "name"
