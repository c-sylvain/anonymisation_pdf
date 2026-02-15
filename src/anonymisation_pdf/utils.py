def normalize_value(s):
    if s is None:
        return ""
    return s.casefold().strip()


def hash_mask(n):
    try:
        n = int(n)
    except Exception:
        n = 0
    return "#" * max(0, n)
