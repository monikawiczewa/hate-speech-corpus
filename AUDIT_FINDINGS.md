# Full-corpus audit — 24 October 2026

Completed locally using all ten `clean/Dataset_1.txt` through `Dataset_10.txt` files. Input SHA-256 hashes and full aggregate results are in [audit.json](reports/audit.json); independent serialized-file checks are in [verification.json](reports/verification.json). No generated corpus text is committed or uploaded as an artifact.

## Initial failure and fix

[Initial Actions run](https://github.com/monikawiczewa/hate-speech-corpus/actions/runs/40120534486) failed with `expected 2 CSV fields, got 3`. All ten inputs are pandas exports with an index column. The loader now explicitly recognizes that schema and the two-column format; malformed records and invalid UTF-8 fail closed. Sentence values are preserved, with normalization only used for grouping.

## Recomputed counts

| Measure | Count |
|---|---:|
| Raw CSV records, including headers | 257,590 |
| Header rows excluded | 10 |
| Empty sentence/label rows excluded | 4 |
| Malformed records | 0 |
| Usable input records | 257,576 |
| Unique normalized sentence groups | 233,305 |
| Repeated normalized groups | 12,615 |
| Duplicate records beyond first per group | 24,271 |
| Conflicting-label groups | 2,727 |
| Records in conflicting-label groups | 8,964 |
| Groups appearing in multiple sources | 913 |

| Partition | Before oversampling | After oversampling |
|---|---:|---:|
| train | 154,545 | 410,000 |
| val | 51,516 | 51,516 |
| test | 51,515 | 51,515 |

## Per-class distribution

| Label | Input | Train before | Train after | Validation | Test |
|---|---:|---:|---:|---:|---:|
| Cyberbullying | 7,601 | 4,540 | 41,000 | 1,490 | 1,571 |
| Hate | 36,807 | 21,927 | 41,000 | 7,457 | 7,423 |
| Neither | 21,065 | 12,544 | 41,000 | 4,328 | 4,193 |
| No Hate | 59,712 | 36,119 | 41,000 | 11,842 | 11,751 |
| Normal | 8,208 | 4,862 | 41,000 | 1,613 | 1,733 |
| Not cyberbullying | 7,790 | 4,739 | 41,000 | 1,535 | 1,516 |
| Not offensive | 45,513 | 27,208 | 41,000 | 9,095 | 9,210 |
| Offensive | 68,219 | 41,000 | 41,000 | 13,611 | 13,608 |
| Racism | 945 | 595 | 41,000 | 176 | 174 |
| Sexism | 1,716 | 1,011 | 41,000 | 369 | 336 |

## Per-source integrity

| File | Raw rows | Headers | Empty | Usable |
|---|---:|---:|---:|---:|
| Dataset_1.txt | 24,763 | 1 | 0 | 24,762 |
| Dataset_2.txt | 14,506 | 1 | 0 | 14,505 |
| Dataset_3.txt | 76,498 | 1 | 0 | 76,497 |
| Dataset_4.txt | 20,149 | 1 | 1 | 20,147 |
| Dataset_5.txt | 10,555 | 1 | 0 | 10,554 |
| Dataset_6.txt | 19,571 | 1 | 0 | 19,570 |
| Dataset_7.txt | 40,624 | 1 | 1 | 40,622 |
| Dataset_8.txt | 31,443 | 1 | 0 | 31,442 |
| Dataset_9.txt | 15,392 | 1 | 0 | 15,391 |
| Dataset_10.txt | 4,089 | 1 | 2 | 4,086 |

## Leakage and reproducibility checks

- Train–validation, train–test and validation–test normalized-exact overlaps: **0 / 0 / 0** (checked after reading emitted CSVs).
- Conflicting labels are retained, and every normalized group is confined to one partition. No relabelling or conflict adjudication is performed.
- Independent multiset comparisons verify that validation/test retain all their original records and multiplicities; training contains only replications of training originals.
- Six unit/regression tests pass, including indexed CSV, Unicode conflicts, malformed input, deterministic output, overwrite refusal and detection of altered holdout records.
- Two full executions with seed 42 produce byte-identical train/validation/test CSVs and audit JSON. CI repeats these checks and compares committed aggregate reports.

## Historical figures and limitations

The historical 257,590 concatenated count matches the current ten-file raw CSV record total, including ten headers. Removing headers yields 257,580; four empty records yield 257,576 usable records. Historical 682,190 oversampled and 409,314/136,438/136,438 split counts are not targets. The corrected pipeline splits first and balances only training to 41,000 records per class. The historical original-source count 2,187,310 is not independently revalidated by this cleaned-file audit. Historical notebook outputs and datasets are unchanged.

The split is group-aware but not class-stratified or source-held-out. All ten source IDs occur in all three partitions. There are 913 cross-source normalized duplicate groups; the largest pairwise source overlap is Dataset 6–9 (447 groups). Pairwise overlaps are non-additive because groups can occur in more than two sources. These findings warrant provenance review rather than assuming each source is independent.

A limited near-duplicate diagnostic removes all non-alphanumeric characters from normalized text: train–validation **27**, train–test **29**, validation–test **7** common keys remain. These are lexical candidates, not verified semantic duplicates; the transform can conflate distinct text. No exhaustive edit-distance, paraphrase, author/thread/time leakage or semantic audit was performed. Normalized-exact safety must not be described as elimination of all leakage.

Within-partition duplicates remain, including in held-out sets, and may affect weighting. Label conflicts and different annotation schemes require research review. Upstream licences, redistribution rights and source attribution remain unverified. This is a verified split implementation, not a licence clearance, model-performance validation or benchmark release.

## CI evidence

The final successful run and commit are recorded below after GitHub execution.
