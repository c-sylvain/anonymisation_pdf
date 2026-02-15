Tu es un agent de développement autonome (Python). Tu travailles DANS CE REPO et tu respectes strictement la structure existante:
- code dans src/anonymisation_pdf/
- data/in/ contient les PDF d’entrée
- data/out/ contient les PDF sortis
- tests/ contient les tests
- point d’entrée: python -m anonymisation_pdf

Objectif: construire une application CLI modulaire d’anonymisation de PDF (PDF texte natif, pas d’OCR).

Données à anonymiser:
- CSV séparé par ';' avec entêtes EXACTES: champ;valeur
- On anonymise en recherchant les VALEURS (colonne "valeur"). La colonne "champ" sert au reporting.

Matching:
- Matching EXACT (égalité) mais insensible à la casse (casefold).
- Pas de regex. Pas de matching partiel.

Fonctionnement:
1) Charger le CSV champ/valeur et valider format/encodage.
2) Lire:
   - Métadonnées du PDF
   - Texte du PDF par page
3) Pour chaque "valeur" du CSV:
   - Si trouvée dans une métadonnée: remplacer par une chaîne de '#' de même longueur (en conservant le reste).
   - Si trouvée dans le contenu:
        - anonymiser chaque occurrence avec des '#' visibles de même longueur.
        - Si remplacement direct du texte n’est pas fiable, utiliser redaction + overlay (masquer puis écrire '#'*len(valeur)).
4) Générer:
   - PDF de sortie dans data/out/ (même nom + suffixe -anonymise.pdf), sauf si --dry-run.
   - Rapport (CSV ou JSON) listant pour chaque ligne du CSV:
        champ, valeur, found_in_metadata (liste des champs metadata), found_in_content (bool),
        occurrences_total, pages (liste), mode (dry-run ou apply)

CLI (argparse) obligatoire:
- --input (fichier PDF)
- --csv (fichier champ;valeur)
- --output-dir (défaut data/out)
- --report (chemin fichier rapport, défaut: <output-dir>/<input>-report.csv)
- --dry-run (ne modifie rien, ne produit pas de PDF de sortie)
- --case-insensitive est implicite (toujours actif)
- --verbose

Contraintes d’implémentation:
- Code modulaire (un module par responsabilité) dans src/anonymisation_pdf/
- Tests unitaires pytest:
   - parsing/validation CSV
   - matching case-insensitive exact
   - génération du rapport
   - anonymisation metadata (sur PDF minimal de test si possible)
- Documentation dans README: installation, usage, exemples
- Un commit Git minimum par fonctionnalité (petits commits, messages explicites)

À CHAQUE fonctionnalité livrée, tu expliques en FRANÇAIS très précisément:
- fichiers créés/modifiés
- fonctions/classes ajoutées
- commandes pour exécuter et tester
- limites connues

Dépendances:
- PyMuPDF (fitz) pour lire texte, localiser occurrences, redactions/overlay, écrire PDF.
- pikepdf pour lire/écrire métadonnées proprement.
- csv (stdlib) ou pandas pour lecture CSV (choisis le plus simple).
- pytest pour tests.
Mettre les deps dans pyproject.toml.

Plan:
A) inspecter repo et proposer architecture de modules
B) implémenter squelette + CLI + dry-run + extraction (texte+metadata)
C) implémenter matching + reporting
D) implémenter anonymisation metadata
E) implémenter anonymisation contenu via redaction/overlay
F) tests + README
