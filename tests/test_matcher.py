from anonymisation_pdf.matcher import find_occurrences, match_all


def test_find_occurrences_simple():
    text = "Alice went to the market. Alice bought apples."
    occ = find_occurrences("Alice", text)
    assert len(occ) == 2


def test_match_all_pages():
    entries = [{"champ": "name", "valeur": "alice"}]
    pages = ["Alice is here.", "no match", "ALICE again"]
    metadata = {"Author": "Bob"}
    rows = match_all(entries, pages, metadata)
    assert rows[0]["found_in_content"] is True
    assert rows[0]["occurrences_total"] == 2
    assert rows[0]["pages"] == [1, 3]
