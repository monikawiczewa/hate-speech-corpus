# Corpus of Hate Speech from Ten Datasets — Dataset Card (audit draft)

**Curator:** Monika Wiczewa. **Research:** *Subjectivity Spaces in Natural Language Processing*, University of Sheffield, MSc dissertation, 8 September 2025.

## Purpose
A derived collection of ten pre-existing datasets for experiments in modelling overlapping subjective characteristics in offensive and hate-related language. This is **not** a newly independently annotated dataset; the contribution is integration, transformation and experimental preparation.

## Reported composition
Chapter 4 (p. 20) reports **2,187,310 sentences before preprocessing** and **12 subjective categories**. Chapter 4 discusses merging semantically similar categories (e.g. hate/hateful/hate speech) and balancing. Do not confuse the raw total with the post-cleaning size or approximately 7,000-example neural experiment subset.

## Source provenance
See [SOURCES.md](SOURCES.md) for ten dataset entries and discrepancies requiring resolution.

## Data processing
Dissertation §4.3 describes category harmonisation, lowercasing, removal of URLs, HTML tags, digits, hashtags, mentions, punctuation and non-alphanumeric characters, English stopword removal, NLTK Snowball stemming, and train/validation/test splitting. Check notebooks for the exact implemented order and exceptions. §4.4 discusses imbalance and postponed balancing. Do not claim every discussed augmentation option was executed without notebook confirmation.

## Files
- `DataSets/`: source files
- `clean/Dataset_1.txt` … `Dataset_10.txt`, `Dataset_All.txt`: cleaned text
- `tokenize/dataset1_tokenized.txt` … `dataset10_tokenized.txt`, `Tokenize_All.txt`: tokenized variants
- `split_data/df_train.csv`, `df_val.csv`, `df_test.csv`: experimental splits
- `data_cleaning.ipynb`, `data_preprocessing.ipynb`: original notebooks

## Intended use
Research on subjectivity, abusive-language classification, dataset integration, domain differences, class overlap and robustness. No claim of representative population sampling or suitability for deployment decisions.

## Risks and limitations
Contains potentially offensive language and sensitive references. Upstream sources have heterogeneous annotations and may contain duplicates, platform-specific language, identity-term correlations and social biases. Removing stopwords can erase negation and alter semantics; stemming and stripping hashtags can change meaning. Dataset splits require leakage checks. Labels are not necessarily interchangeable across source datasets. Underlying posts may raise privacy and platform-terms concerns.

## Distribution and licensing
**Not yet verified.** Academic citation alone does not authorise redistribution. Do not apply a blanket open-data licence to upstream content. Check each source's licence, terms and original publication; consider distributing scripts/identifiers instead of text where required. Existing public hosting is not proof of permission.

## Verification status
Repository tree and notebook object hashes matched the original `egc16mw` repository at audit time. Exact row counts, per-source mapping, duplicate counts, split proportions, dependency versions and redistribution permissions remain to be checked. **This is a documentation draft, not a release-ready dataset card.**