def anonymize_metadata(input_pdf, entries, output_pdf, dry_run=True):
    try:
        import pikepdf
    except Exception:
        raise ImportError("pikepdf est requis pour anonymiser les métadonnées")

    # Construire mapping valeur.casefold() -> valeur original
    targets = {e.get("valeur", "").casefold(): e.get("valeur", "") for e in entries}
    changes = {}

    with pikepdf.Pdf.open(input_pdf) as pdf:
        info = pdf.docinfo
        for k, v in list(info.items()):
            sval = str(v)
            key_display = k.lstrip("/")
            if sval.casefold() in targets:
                masked = "#" * len(sval)
                changes[key_display] = masked
                if not dry_run:
                    info[k] = masked

        if not dry_run:
            pdf.save(output_pdf)

    return changes
