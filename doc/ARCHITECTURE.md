Proposition d'architecture - anonymisation_pdf

But: application CLI modulaire pour anonymiser des PDF (texte natif).

Packages/modules proposés (sous `src/anonymisation_pdf/`):

- `__main__.py` : point d'entrée (appelé par `python -m anonymisation_pdf`), parse args et orchestre.
- `cli.py` : définition de l'interface CLI (argparse) et validation d'entrée.
- `csv_parser.py` : lecture et validation du CSV (champ,valeur). Retourne liste d'objets.
- `pdf_io.py` : lecture/écriture PDF :
  - extraction métadonnées via `pikepdf`;
  - lecture texte par page via `PyMuPDF` (fitz) et localisation d'occurrences.
- `matcher.py` : matching exact case-insensitive (casefold) d'une valeur dans un texte; utilities pour compter occurrences et pages.
- `reporter.py` : construction et écriture du rapport (CSV/JSON) avec les champs demandés.
- `anonymizer_metadata.py` : modification des métadonnées via `pikepdf` (remplacer valeurs trouvées par '#'*len).
- `anonymizer_content.py` : anonymisation du contenu page par page via PyMuPDF redaction + overlay si nécessaire.
- `utils.py` : fonctions utilitaires (normalisation, générer chaîne '#', logging simple).

Tests (sous `tests/`):
- `test_csv_parser.py`
- `test_matcher.py`
- `test_reporter.py`
- `test_anonymize_metadata.py` (avec PDF minimal de test)

Dépendances (à ajouter dans `pyproject.toml` / `requirements.txt`):
- pikepdf
- PyMuPDF
- pytest

Workflow par étape (correspond aux étapes A→F):
A) proposer architecture (ce document)
B) implémenter squelette + CLI + extraction (dry-run possible)
C) implémenter matching + reporting
D) anonymisation metadata via pikepdf
E) anonymisation contenu via PyMuPDF (redaction & overlay)
F) tests + README

Notes:
- Conserver modularité et API testable par fonction.
- Chaque étape livrée avec commit Git atomique et message en français.
