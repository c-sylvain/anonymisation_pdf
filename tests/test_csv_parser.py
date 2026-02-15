from anonymisation_pdf.csv_parser import parse_csv


def test_parse_csv(tmp_path):
    p = tmp_path / "data.csv"
    p.write_text("champ,valeur\nname,Alice\n", encoding="utf-8")
    entries = parse_csv(str(p))
    assert isinstance(entries, list)
    assert len(entries) == 1
    assert entries[0]["champ"] == "name"
    assert entries[0]["valeur"] == "Alice"
