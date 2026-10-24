# Corrected full-corpus split

```bash
python -m unittest discover -s tests -v
python scripts/safe_split.py --input clean --output split_data_corrected --seed 42
python scripts/verify_split.py --input clean --output split_data_corrected
```

Python 3.11, standard library only. Reads exactly Dataset_1.txt through Dataset_10.txt; deliberately excludes the combined Dataset_All.txt to avoid double counting. Supports explicit pandas index,sentence,intent headers and ordinary sentence,intent CSV. Repeated headers and empty fields are counted and excluded. Invalid UTF-8, malformed CSV and invalid indexed rows abort rather than silently dropping data. Output must be new/empty; original files are never overwritten.

Groups use NFKC, casefold and whitespace collapse. Whole groups, including conflicting labels, are assigned deterministically to approximately 60/20/20 partitions with seed 42. Stable sorted keys precede seeded shuffling. Only training is oversampled to its largest class. Original sentence values, labels and source IDs are preserved in held-out CSVs.

Verified full-data result: 257,590 CSV records; 10 headers and 4 empty rows excluded; 257,576 usable records; 233,305 groups. Before oversampling: 154,545 train, 51,516 validation, 51,515 test. After: 410,000 train; held-out counts unchanged. All three normalized-exact overlap counts are zero. See [AUDIT_FINDINGS.md](AUDIT_FINDINGS.md) for distributions, source overlap, conflicts and limitations.

The independent verifier reloads input and serialized output, verifies record conservation, unchanged held-out multisets, training-only replication, conflicting-group confinement, counts and pairwise overlap. CI executes the complete pipeline twice and compares byte hashes/content, then checks aggregate reports against committed results. Only audit.json and verification.json are uploaded as artifacts (30 days); aggregate copies persist in reports/. Generated CSVs are ignored and not published pending rights review.

This is not a source-held-out or semantic-leakage-free benchmark. There are 2,727 conflicting-label groups and residual punctuation-insensitive overlap candidates (27/29/7). Do not reuse historical oversample-before-split performance as validation of this corrected split. Original notebooks and historical results remain unchanged.
