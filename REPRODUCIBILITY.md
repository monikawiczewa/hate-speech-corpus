# Reproducibility: historical MSc record and audited 2026 pipeline

## A. Historical dissertation workflow (2025)
The original `data_cleaning.ipynb`, `data_preprocessing.ipynb`, `DataSets/`, `clean/`, `tokenize/` and `split_data/` are preserved. Dissertation Chapter 4 reports 2,187,310 upstream sentences before preprocessing; its historical 257,580 cleaned rows and 682,190 oversampled rows are **not** the corrected workflow's targets. No clean-environment rerun of the historical notebooks or pinned historical environment is claimed. Do not replace historical results with new audit figures or attribute historical neural-model performance to the corrected split.

## B. Audited group-safe pipeline (2026)
**Environment:** Python 3.11; Python standard library for the corrected pipeline. From repository root:

```bash
python -m unittest discover -s tests -v
python scripts/safe_split.py --input clean --output split_data_corrected --seed 42
python scripts/verify_split.py --input clean --output split_data_corrected
```

Use a **new or empty** output directory; the pipeline refuses to overwrite existing output. It reads exactly `clean/Dataset_1.txt` through `Dataset_10.txt`, not `Dataset_All.txt`, avoiding double counting. Inputs may contain pandas index/sentence/intent columns or ordinary sentence/intent columns. Headers and empty rows are excluded; malformed CSV and invalid UTF-8 cause failure.

Sentence grouping uses Unicode NFKC, casefolding and whitespace collapse. Whole groups (including groups with conflicting labels) are deterministically assigned to approximately 60/20/20 train/validation/test using seed 42; **only training** is oversampled to the largest training class. This is not class-stratified or source-held-out.

The independent verifier checks conservation of records, original held-out record multiplicities, training-only replication, group confinement, output counts and zero normalized-exact cross-split overlap. Two full seed-42 executions were byte-identical. Six unit/regression tests passed. Aggregate evidence: [audit.json](reports/audit.json), [verification.json](reports/verification.json), [AUDIT_FINDINGS.md](AUDIT_FINDINGS.md). Successful [GitHub Actions run 40121243024](https://github.com/monikawiczewa/hate-speech-corpus/actions/runs/40121243024).

## Verified checkpoints
- Input: 257,590 CSV records including 10 headers and 4 empty rows; **257,576 usable**.
- Normalized groups: 233,305; conflicting-label groups: 2,727; cross-source groups: 913.
- Train/validation/test before oversampling: **154,545 / 51,516 / 51,515**.
- Training after oversampling: **410,000** (41,000 per class); held-out partitions unchanged.
- Pairwise normalized-exact train/validation, train/test, validation/test overlap: **0 / 0 / 0**.

## Scope and limitations
The audit does not establish semantic near-duplicate freedom, author/thread/time independence, source-held-out generalisation, annotation-schema equivalence or new model accuracy. Punctuation-insensitive overlap candidates remain (27 / 29 / 7). Existing held-out duplicates are retained. Hashes and detailed per-source/per-class counts are in the committed aggregate reports. Corrected output CSVs are ignored by Git; existing historical files remain unchanged.

## Outstanding historical replication work
Inventory original notebook dependencies and NLTK downloads; pin versions and seeds; execute notebooks in a clean environment to separate outputs; verify transformations and category mappings; reconcile source identities, licences and historical counts. These are **open tasks**, not completed checks.
