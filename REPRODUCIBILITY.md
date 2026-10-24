# Reproducibility and audit protocol

## Current notebooks
`data_cleaning.ipynb` and `data_preprocessing.ipynb` are preserved in the repository. No verified environment lockfile or clean end-to-end reproduction has been established yet.

## Required checks before claiming reproducibility
1. Inventory raw files and determine schema, provenance, source URL, publication and redistribution rights for each.
2. Extract notebook imports, NLTK downloads, working-directory assumptions and random seeds; pin dependency versions.
3. Run each notebook in a clean environment with outputs saved separately; never overwrite original data.
4. Count records and labels at raw, cleaned, tokenized and split stages; record dropped/null/duplicate rows and category merges.
5. Verify whether cleaning removes negation and whether stemming applies per token or to joined strings.
6. Check exact and normalized duplicate overlap between train, validation and test, and overlaps across upstream sources.
7. Compare outputs against dissertation Chapter 4 and Appendices A and D; document discrepancies without silently changing historical figures.
8. Check upstream licensing and platform redistribution rules before publicly releasing reconstructed data.

## Original dissertation claim
**2,187,310 raw sentences across 12 subjective categories before preprocessing** (Chapter 4, p. 20). This is not a verified present-day repository row count.

## Status
This is an audit checklist, not a claim that the notebooks have been rerun successfully.