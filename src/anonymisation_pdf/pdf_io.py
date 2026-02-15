def extract_metadata(pdf_path):
    try:
        import pikepdf
    except Exception:
        # pikepdf absent: retourner métadonnées vides
        return {}

    try:
        with pikepdf.Pdf.open(pdf_path) as pdf:
            info = {}
            docinfo = pdf.docinfo
            for k, v in docinfo.items():
                # keys like /Title -> strip leading '/'
                key = k.lstrip("/")
                try:
                    info[key] = str(v)
                except Exception:
                    info[key] = ""
            return info
    except Exception:
        return {}


def extract_text_by_page(pdf_path):
    try:
        import fitz
    except Exception:
        raise ImportError("PyMuPDF (fitz) requis pour extraire le texte")

    doc = fitz.open(pdf_path)
    pages = []
    for p in doc:
        pages.append(p.get_text("text"))
    return pages
