import argparse
import os
from .csv_parser import parse_csv
from .pdf_io import extract_metadata, extract_text_by_page
from .matcher import match_all
from .reporter import write_report_csv


def build_parser():
    p = argparse.ArgumentParser(
        prog="anonymisation_pdf",
        description="CLI pour anonymisation de PDF"
    )
    p.add_argument("--input", required=True, help="fichier PDF d'entrée")
    p.add_argument("--csv", required=True, help="fichier CSV champ;valeur")
    p.add_argument("--output-dir", default="data/out", help="répertoire de sortie")
    p.add_argument("--report", default=None, help="chemin du rapport (CSV/JSON)")
    p.add_argument("--dry-run", action="store_true", help="ne modifie rien")
    p.add_argument("--verbose", action="store_true", help="mode verbeux")
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    run(args)


def run(args):
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Fichier input introuvable: {args.input}")
    entries = parse_csv(args.csv)
    metadata = extract_metadata(args.input)
    pages = extract_text_by_page(args.input)

    # Résumé basique pour le moment (dry-run affiche ce qui serait fait)
    summary = {
        "input": args.input,
        "n_entries": len(entries),
        "n_pages": len(pages),
        "metadata_keys": list(metadata.keys()),
        "dry_run": bool(args.dry_run),
    }

    # Matching
    rows = match_all(entries, pages, metadata)

    # Report path par défaut
    if args.report:
        report_path = args.report
    else:
        base = os.path.basename(args.input)
        name = os.path.splitext(base)[0]
        report_path = os.path.join(args.output_dir, f"{name}-report.csv")

    mode = "dry-run" if args.dry_run else "apply"
    write_report_csv(rows, report_path, mode=mode)

    if args.dry_run:
        print(f"Dry-run: rapport écrit -> {report_path}")
    else:
        print(f"Rapport écrit -> {report_path} (mode apply)\nAnonymisation à appliquer dans l'étape suivante")

    return summary
