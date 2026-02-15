from .utils import normalize_value


def _is_boundary(text, start, end):
    before = text[start - 1] if start > 0 else None
    after = text[end] if end < len(text) else None

    def is_alnum(c):
        return c is not None and c.isalnum()

    return not is_alnum(before) and not is_alnum(after)


def find_occurrences(value, text):
    if not value:
        return []
    nv = normalize_value(value)
    nt = text.casefold()
    results = []
    i = 0
    L = len(nv)
    while True:
        i = nt.find(nv, i)
        if i == -1:
            break
        end = i + L
        if _is_boundary(nt, i, end):
            results.append(i)
        i = end
    return results


def match_all(entries, pages, metadata):
    rows = []
    for e in entries:
        valeur = e.get("valeur", "")
        champ = e.get("champ", "")
        found_in_metadata = []
        nv = normalize_value(valeur)
        # metadata exact equality (case-insensitive)
        for k, v in (metadata or {}).items():
            if normalize_value(v) == nv:
                found_in_metadata.append(k)

        occurrences_total = 0
        pages_found = []
        for idx, page_text in enumerate(pages, start=1):
            occ = find_occurrences(valeur, page_text)
            if occ:
                occurrences_total += len(occ)
                pages_found.append(idx)

        rows.append({
            "champ": champ,
            "valeur": valeur,
            "found_in_metadata": found_in_metadata,
            "found_in_content": occurrences_total > 0,
            "occurrences_total": occurrences_total,
            "pages": pages_found,
        })
    return rows
