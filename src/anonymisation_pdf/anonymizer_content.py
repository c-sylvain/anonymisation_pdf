from .utils import normalize_value, hash_mask


def anonymize_content(input_pdf, entries, output_pdf, dry_run=True):
    try:
        import fitz
    except Exception:
        raise ImportError("PyMuPDF (fitz) est requis pour anonymiser le contenu")

    # Préparer valeurs normalisées et longueur
    targets = [(e.get("valeur", ""), normalize_value(e.get("valeur", ""))) for e in entries]
    changes = {t[0]: {"occurrences": 0, "pages": []} for t in targets}

    doc = fitz.open(input_pdf)
    for pno in range(len(doc)):
        page = doc[pno]
        words = page.get_text("words")  # list of tuples (x0, y0, x1, y1, "word", block, line, word_no)
        # sort by vertical/horizontal order
        words.sort(key=lambda w: (w[5], w[6], w[7]))
        word_texts = [w[4] for w in words]
        word_rects = [fitz.Rect(w[0], w[1], w[2], w[3]) for w in words]

        for original, normalized in targets:
            if not original:
                continue
            tokens = original.split()
            L = len(tokens)
            i = 0
            while i <= len(word_texts) - L:
                seq = " ".join(word_texts[i : i + L])
                if normalize_value(seq) == normalized:
                    # union rect
                    r = word_rects[i]
                    for j in range(i + 1, i + L):
                        r |= word_rects[j]
                    # add redaction annotation
                    page.add_redact_annot(r, fill=(1, 1, 1))
                    changes[original]["occurrences"] += 1
                    if (pno + 1) not in changes[original]["pages"]:
                        changes[original]["pages"].append(pno + 1)
                    i += L
                else:
                    i += 1

        # apply redactions for this page
        page.apply_redactions()

        # overlay masks (simple approach: write hashes over redacted areas)
        # collect redaction annots
        for ra in page.annots(types=[fitz.PDF_ANNOT_REDACT]) or []:
            r = ra.rect
            # approximate number of characters by width of rect / 6
            # prefer original lengths unknown here; write a visible mask
            mask = "#" * max(1, int(r.width // 6))
            fontsize = max(4, int(r.height * 0.8))
            page.insert_textbox(r, mask, fontsize=fontsize, align=1)

    if not dry_run:
        doc.save(output_pdf)
    doc.close()
    return changes
