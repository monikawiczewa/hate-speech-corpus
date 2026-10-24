# Corpus of Hate Speech from Ten Datasets

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23624421.svg)](https://doi.org/10.5281/zenodo.23624421)

**Historical MSc research corpus and audited reproducibility workflow**  
**Author:** Monika Wiczewa · University of Sheffield · MSc dissertation, 2025  
**Citable release:** [v1.0.0 on Zenodo](https://doi.org/10.5281/zenodo.23624421) · [GitHub release](https://github.com/monikawiczewa/hate-speech-corpus/releases/tag/v1.0.0)

A research corpus integrating ten existing hate-speech and related subjective-language datasets, developed for *Subjectivity Spaces in Natural Language Processing*. The repository preserves the historical MSc materials and provides a separately verified, group-aware 2026 splitting workflow. It is **not** a newly independently annotated dataset, and the 2026 audit does **not** report new model accuracy.

## Cite this dataset

> Wiczewa, M. (2026). *Corpus of Hate Speech from Ten Datasets: Historical MSc Corpus and Audited Research Workflow* (v1.0.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.23624421

Use the **version-specific DOI** above when citing the archived v1.0.0 materials. Cite the relevant upstream dataset publications as well; see [BIBLIOGRAPHY.md](BIBLIOGRAPHY.md) and [SOURCES.md](SOURCES.md). The `CITATION.cff` file supplies machine-readable citation metadata.

**Version note:** Zenodo v1.0.0 is a fixed archived snapshot. Changes committed to GitHub after the release are not automatically included in that archived version; publish a subsequent GitHub release to archive them.

## Research context

This corpus is the data-engineering component of the University of Sheffield MSc dissertation *Subjectivity Spaces in Natural Language Processing* (submitted 2025; MSc awarded with Distinction). It supports investigations into ambiguity, annotation disagreement and continuous representations of subjective language. The companion [Subjectivity Space repository](https://github.com/monikawiczewa/subjectivity-space) contains neural-model experiments and evaluation.

## Historical versus improved workflow

| | Historical MSc research (2025) | Audited workflow (2026) |
|---|---|---|
| Purpose | Original dissertation experiments | Reproducible data-integrity improvement |
| Data | Integrated source files, historical cleaned/tokenized files and splits | Same ten cleaned inputs, processed into a separate corrected split |
| Reported size | 2,187,310 upstream examples before preprocessing; historical cleaned count 257,580 | 257,576 usable cleaned records after excluding 10 headers and 4 empty rows |
| Partitioning | Historical notebook-generated experimental splits | Normalized-exact group-aware split, then training-only oversampling |
| Model accuracy | Historical dissertation/companion repository results | **No new model training or accuracy claimed** |
| Preservation | Original files and notebooks retained | New outputs kept separate; originals not overwritten |

### Verified corrected-split results

| Measure | Verified count |
|---|---:|
| Usable cleaned input records | 257,576 |
| Normalized sentence groups | 233,305 |
| Groups with conflicting labels | 2,727 |
| Groups occurring in multiple source files | 913 |
| Training before oversampling | 154,545 |
| Validation | 51,516 |
| Test | 51,515 |
| Training after oversampling | 410,000 |
| Normalized-exact cross-split overlap (train/val, train/test, val/test) | 0 / 0 / 0 |

The independent verifier checks serialized outputs, record conservation, held-out integrity and group confinement. Six unit/regression tests and two byte-identical full executions passed. [GitHub Actions verification](https://github.com/monikawiczewa/hate-speech-corpus/actions/runs/40123093049) succeeded for the v1.0.0 release commit.

## Reproduce the audited split

Use **Python 3.11** from the repository root. The corrected workflow uses the Python standard library.

```bash
python -m unittest discover -s tests -v
python scripts/safe_split.py --input clean --output split_data_corrected --seed 42
python scripts/verify_split.py --input clean --output split_data_corrected
```

The output directory must be new or empty. The pipeline reads `clean/Dataset_1.txt` through `Dataset_10.txt`, excludes the combined `Dataset_All.txt` to prevent double counting, groups normalized-identical sentences together and oversamples **training only**. The historical files remain unchanged. Full details: [REPRODUCIBILITY.md](REPRODUCIBILITY.md) and [CORRECTED_SPLIT.md](CORRECTED_SPLIT.md).

## Repository guide

| Path | Contents |
|---|---|
| `DataSets/` | Original source-dataset materials retained with the research |
| `clean/` | Historical cleaned corpus; ten numbered inputs for the corrected workflow |
| `tokenize/` | Historical tokenized data |
| `split_data/` | Historical experimental splits |
| `data_cleaning.ipynb`, `data_preprocessing.ipynb` | Original notebooks |
| `scripts/`, `tests/` | Audited split and verification implementation |
| `reports/` | Aggregate audit and verification reports |
| [DATASET_CARD.md](DATASET_CARD.md) | Scope, provenance, intended use and risks |
| [METHODOLOGY.md](METHODOLOGY.md) | Historical and corrected methods; limitations |
| [AUDIT_FINDINGS.md](AUDIT_FINDINGS.md) | Full-data counts, overlap and CI evidence |
| [SOURCES.md](SOURCES.md) | Source-by-source attribution and open questions |
| [BIBLIOGRAPHY.md](BIBLIOGRAPHY.md) | Upstream references and citation guidance |

## Limitations and responsible reuse

- **Not source-held-out:** all ten source IDs occur in each partition, so performance on unseen source datasets is not established.
- **Not free of all leakage:** normalized-exact cross-split overlap is zero, but punctuation-insensitive candidate overlaps remain (27 / 29 / 7); semantic, author, thread and temporal leakage have not been exhaustively tested.
- **Annotation heterogeneity:** conflicting labels and incompatible source annotation schemes remain; repeated records may influence weighting.
- **No new predictive claims:** the corrected split has not been used here to rerun the dissertation models or establish updated accuracy, fairness or robustness.
- **Provenance and permissions:** the historical corpus was openly published; the component datasets have different origins and source-specific terms. [SOURCES.md](SOURCES.md) records verified evidence and unresolved mappings without presuming that uncertain permissions mean prohibited reuse. No blanket licence is asserted over all third-party text.

This resource contains offensive and potentially harmful language. It is intended for research, not deployment-ready moderation or decisions about individuals.

## Author

**Monika Wiczewa** — AI/ML, NLP and Creative Technology  
[LinkedIn](https://www.linkedin.com/in/monika-wiczewa-9771771a3/)
