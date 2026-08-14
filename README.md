# anonymisation_pdf

Fonctionnement pas très concluant, je ne sais plus exactement ce que ce projet fait réelement

Outil CLI pour anonymiser des PDF (texte natif).

Installation (recommandé dans un venv) :

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Exemples :

Dry-run (ne modifie rien, écrit un rapport) :

```bash
python -m anonymisation_pdf --input data/in/XXX.pdf --csv data/in/donnees_a_detecter.csv --dry-run
```

Exécution (apply) :

```bash
python -m anonymisation_pdf --input data/in/XXX.pdf --csv data/in/donnees_a_detecter.csv
```

Le PDF de sortie sera écrit dans `data/out/` avec le suffixe `-anonymise.pdf`.
