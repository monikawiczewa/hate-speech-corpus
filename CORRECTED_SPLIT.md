# Corrected split workflow (experimental)

Run from the repository root:

```bash
python -m unittest discover -s tests -v
python scripts/safe_split.py --input clean --output split_data_corrected --seed 42
```

This standard-library script reads the ten existing cleaned CSV-like text files, removes repeated `sentence,intent` headers, groups records by Unicode-normalized, casefolded, whitespace-normalized sentence, assigns each entire group to one split (approximately 60/20/20), and oversamples **training only**. It writes `train.csv`, `val.csv`, `test.csv` and `audit.json` to a new output directory. It refuses to overwrite existing nonempty output directories. Historical `split_data/` remains unchanged.

**Validation guarantee:** normalized-exact duplicate text cannot occur across the new train/validation/test sets, even if labels conflict. This does **not** rule out paraphrase/near-duplicate leakage, leakage via source datasets, or other evaluation biases. Splitting is group-aware but **not stratified**; class proportions may vary. Oversampling creates repeated records within training, intentionally.

**Important:** This workflow is a proposed correction, not a claim that the full corpus was executed or validated in this environment. Review `audit.json` after running, and verify class distributions, input provenance, licences, and any source-level leakage before a benchmark release. Existing notebooks are preserved for historical reproducibility.
