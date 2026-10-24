# Corpus of Hate Speech from Ten Datasets — Dataset Card

**Curator:** Monika Wiczewa. **Academic context:** *Subjectivity Spaces in Natural Language Processing*, University of Sheffield, MSc dissertation (submitted 8 September 2025; Distinction).

## Scope and intended use
A research corpus assembled and transformed from ten existing dataset collections for studying subjective, offensive and hate-related language. The contribution is source integration, category harmonisation, preprocessing and experimental preparation, not new independent annotation. Intended for research on subjectivity, classification, annotation disagreement, domain shift and data integrity; not validated for automated moderation or consequential decisions.

## Two research records
**Historical MSc corpus (2025):** Original `DataSets/`, `clean/`, `tokenize/`, `split_data/` and notebooks are retained as the dissertation research record. Chapter 4 reports 2,187,310 upstream sentences before preprocessing, and historical cleaned and oversampled counts. The original neural-model results belong to that historical experiment, **not** to the corrected split.

**Audited workflow (2026):** `scripts/safe_split.py` and `scripts/verify_split.py` produce and verify a separate group-aware partition of the ten cleaned files, with training-only oversampling. Original data and notebooks are not overwritten.

## Verified 2026 composition
The ten cleaned CSV exports contain 257,590 records including ten headers and four empty rows, leaving **257,576 usable records**. They form 233,305 normalized-exact sentence groups; 12,615 groups have repeated records, 24,271 records are duplicates beyond the first, 2,727 groups contain conflicting labels (8,964 records), and 913 groups appear in multiple sources. See [AUDIT_FINDINGS.md](AUDIT_FINDINGS.md) for per-class and per-source tables.

The corrected pre-oversampling partitions contain 154,545 training, 51,516 validation and 51,515 test records. Training-only oversampling expands training to 410,000 (41,000 per class). Normalized-exact cross-partition overlap is zero in all three pairwise comparisons. These are **data-validation findings, not model accuracy measurements**.

## Processing and provenance
Dissertation Chapter 4 describes lowercasing, removal of URLs, HTML, digits, hashtags, mentions, punctuation and stopwords, Snowball stemming and label harmonisation. The notebooks, rather than the prose description, remain the authoritative historical implementation. The corrected pipeline groups by Unicode NFKC normalization, casefolding and whitespace collapse, then deterministically assigns whole groups to approximately 60/20/20 partitions (seed 42) before balancing training.

Files include `DataSets/` (source material), `clean/Dataset_1.txt`–`Dataset_10.txt` (corrected pipeline inputs), `tokenize/` (historical tokenized material), `split_data/` (historical splits), `data_cleaning.ipynb` and `data_preprocessing.ipynb` (historical notebooks), and `reports/` (aggregate audit evidence). The corrected output is written separately to `split_data_corrected/` and ignored by Git.

## Known limitations
The ten numbered collections are not necessarily ten independent originating publications. Dataset 5's bundled README identifies de Gibert et al. (2018), whereas the dissertation appendix lists Figea et al. Dataset 1/7 provenance overlaps and Dataset 3/4/9 mappings require further reconciliation; see [SOURCES.md](SOURCES.md) and [BIBLIOGRAPHY.md](BIBLIOGRAPHY.md).

The corrected split is neither source-held-out nor class-stratified; all ten source IDs occur in every partition. Normalized-exact deduplication does not rule out semantic or punctuation-only near-duplicates (diagnostic candidate overlaps 27/29/7), author/thread leakage, annotation bias or label-schema incompatibility. Conflicting labels are retained. Repeated examples remain within partitions, including held-out partitions. Original cleaning may remove negation or identity/context cues. Source texts may include harmful language and personal references.

## Availability and reuse
The historical corpus has been openly published as a research resource. Its constituent sources have differing attribution and licence evidence: public availability does not establish one uniform licence for every upstream text. This dataset card does **not** assert that redistribution is prohibited; it records which permissions have or have not been independently verified. The bundled Dataset 5 licence is CC BY-SA 3.0 Spain. Consult [SOURCES.md](SOURCES.md) for individual source details. Preserve attribution and applicable source terms when reusing material.

## Reproducibility status
The corrected Python 3.11 standard-library split, independent verification, six tests and two byte-identical full executions passed in GitHub Actions; see [REPRODUCIBILITY.md](REPRODUCIBILITY.md), [CORRECTED_SPLIT.md](CORRECTED_SPLIT.md), and [AUDIT_FINDINGS.md](AUDIT_FINDINGS.md). A clean end-to-end rerun of the historical notebooks and new model-training results are **not** claimed.
