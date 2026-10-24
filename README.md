# Hate Speech Corpus from Ten Datasets

**Dataset engineering for the Subjectivity Space NLP research project**

This repository contains a corpus created by integrating, cleaning and preprocessing **ten existing hate-speech datasets** for my MSc research at the University of Sheffield.

The resource was developed for **Subjectivity Space**, a neural-network approach to modelling ambiguity in subjective language using continuous multidimensional representations.

## Project Motivation

Subjective-language research is complicated by differences in dataset structure, annotation schemes, class definitions and preprocessing conventions.

Rather than relying on a single source, this project combines data from ten datasets into a larger experimental resource suitable for neural sequence modelling and cross-category research.

## What This Repository Contains

The project includes:

- integration of ten hate-speech datasets;
- cleaned and preprocessed text;
- tokenized and untokenized corpus versions;
- data-cleaning notebooks;
- preprocessing pipelines;
- dataset splitting and preparation; and
- data used in the Subjectivity Space experiments.

## Research Context

The corpus forms the data-engineering component of my MSc dissertation:

**Subjectivity Spaces in Natural Language Processing**

University of Sheffield  
MSc Computer Science (Artificial Intelligence: Speech & Language Processing) — Distinction

The wider research investigates whether ambiguity and disagreement in subjective language can be represented as meaningful continuous structure rather than reduced entirely to discrete classification labels.

## Related Project

The neural-network experiments and evaluation are available in the companion repository:

**[Subjectivity Space](https://github.com/monikawiczewa/subjectivity-space)**

That project includes RNN experiments, limited-data conditions, unseen-category evaluation, model-stability work and human evaluation.

## Author

**Monika Wiczewa**  
Creative Technologist | AI/ML | NLP & Human-Centred AI | Music Technology

[LinkedIn](https://www.linkedin.com/in/monika-wiczewa-9771771a3/)

## Historical MSc corpus and improved research workflow

**Historical (2025).** The original MSc dissertation, notebooks, integrated corpus and reported model results are preserved as the historical research record. The dissertation reports 2,187,310 upstream sentences before preprocessing and 257,580 post-processing records. Those figures describe different stages; historical model performance must not be attributed to the corrected pipeline.

**Audited workflow (2026).** A separate, reproducible group-aware split uses the ten cleaned source files, assigns normalized-identical sentences to the same partition, and oversamples training only. The verified input has 257,576 usable records (257,590 CSV rows including ten headers and four empty records). Its partitions contain 154,545 training, 51,516 validation and 51,515 test records before balancing; training is then expanded to 410,000. The three normalized-exact cross-split overlap counts are zero. These are **data-integrity results, not new model-performance results**.

Start with [CORRECTED_SPLIT.md](CORRECTED_SPLIT.md), [AUDIT_FINDINGS.md](AUDIT_FINDINGS.md) and [REPRODUCIBILITY.md](REPRODUCIBILITY.md). Source identifications and licence evidence, including unresolved questions, are tracked in [SOURCES.md](SOURCES.md). Publicly accessible source data should not be mistaken for a verified uniform licence across all ten upstream collections.

The improved split does **not** establish semantic near-duplicate freedom, source-held-out generalisation, class stratification or compatibility of all source annotation schemes. The original data and notebooks are not overwritten by the corrected workflow.
