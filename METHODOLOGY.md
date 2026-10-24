# Methodology and limitations

## Historical MSc corpus (2025)
The dissertation documents ten-source integration, label harmonisation, text cleaning, tokenisation, balancing and Subjectivity Space neural experiments. The historical notebooks, original split files and reported performance remain intact. Its upstream count (2,187,310) and historical processed counts describe different stages. Historical model results **must not** be represented as evaluations of the corrected 2026 split.

## Audited 2026 split
The standard-library Python 3.11 workflow reads ten cleaned CSV exports, excludes ten headers and four empty records, and groups normalized-identical sentences using NFKC, casefolding and whitespace collapse. It deterministically assigns complete groups to approximately 60/20/20 partitions with seed 42. Conflicting labels remain within their groups. Only training is oversampled to its largest class; validation and test retain original records and multiplicities. Original files are not overwritten.

Verified: **257,576 usable records**, **233,305 normalized groups**, **154,545 / 51,516 / 51,515** train/validation/test before balancing, **410,000** training after balancing (41,000 per class), and **0 / 0 / 0** normalized-exact cross-split overlap. Six regression tests and two byte-identical full executions passed. See [CORRECTED_SPLIT.md](CORRECTED_SPLIT.md), [AUDIT_FINDINGS.md](AUDIT_FINDINGS.md) and [REPRODUCIBILITY.md](REPRODUCIBILITY.md).

## Limitations and next experiments
- The corrected partition is **not source-held-out or class-stratified**; all ten sources occur in all three partitions. Source-aware generalisation remains untested.
- Normalized-exact overlap is eliminated across partitions, but semantic, author, thread and temporal leakage are **not** ruled out. Punctuation-insensitive diagnostic candidate overlaps remain: 27 / 29 / 7.
- There are **2,727 conflicting-label groups**, **12,615 repeated groups**, and **913 cross-source groups**. Annotation schemas are heterogeneous and cannot be presumed interchangeable.
- Oversampling replicates training records rather than adding independent evidence. Within-partition duplicates, including held-out duplicates, remain.
- Historical stopword removal, stemming and punctuation stripping may change negation, meaning or identity/context cues; historical notebooks have not been rerun in a pinned clean environment.
- Numbered source collections may overlap or combine publications. Source-specific attribution and licence evidence remain partly unresolved; uncertainty is not a finding of prohibited reuse.
- No new model training, predictive performance, calibration, robustness or fairness result is claimed.

## Research integrity
Preserve the original dissertation outputs separately from corrected experiments. For future evaluations, report the source-aware protocol, label crosswalk, seed, environment, data hashes, duplication policy and per-source performance. Do not overwrite historical figures.
