# Source attribution and provenance ledger

This ledger distinguishes **historical dissertation appendix attributions** from **source identity evidence**. Numbered collections are integration inputs, not necessarily ten independent original publications. Counts in the second column are historical Appendix A figures; the audited cleaned-file counts are in [AUDIT_FINDINGS.md](AUDIT_FINDINGS.md). Do not sum these as if they described the same processing stage.

| ID | Historical Appendix A count | Attribution / source evidence | Licence / reuse evidence and outstanding work |
|---|---:|---|---|
| 1 | 24,802 | Hate Speech and Offensive Language; likely Davidson et al. (2017). Similarity to Dataset 7 requires file-level mapping. | Davidson upstream repository has MIT licence; confirm coverage of third-party tweet content and exact file provenance. |
| 2 | 70,904 | Founta et al. (2018), normal/spam/hateful/abusive. | Public tweet IDs and separately controlled full-text access reported; permissions for the repository's copy have not been independently established. |
| 3 | 1,976,657 | Appendix caption says Waseem and Hovy (2016), but categories include Jigsaw toxicity material; composite mapping unresolved. | Determine precise Jigsaw edition and underlying text terms; no whole-file licence conclusion. |
| 4 | 9,055 | Composite attribution in appendix: Davidson; Fortuna and Nunes; Lima; Mathew; Zannettou. | Identify each component and applicable terms before assigning any aggregate licence. |
| 5 | 9,916 | **Confirmed from bundled README:** de Gibert, Perez, García-Pablos and Cuadros (2018), *Hate Speech Dataset from a White Supremacy Forum* (Stormfront). Appendix's Figea et al. label conflicts. | Bundled `DataSets/dataset_5/LICENSE` specifies **CC BY-SA 3.0 Spain**; follow attribution/share-alike terms and assess derived files. |
| 6 | 19,639 | Waseem and Hovy (2016), sexism/racism/neither/both. | Original tweet-ID distribution and platform terms need review for full-text republication. |
| 7 | 24,783 | Davidson et al. (2017), hate speech/offensive language. Dataset 1 overlap requires reconciliation. | Same provenance and rights questions as Dataset 1. |
| 8 | 22,142 | Jha and Mamidi (2017), benevolent/hostile/other sexism; appendix also mentions Waseem and Hovy. | Verify exact source composition and redistribution terms. |
| 9 | 16,172 | Appendix says Waseem and Hovy, while repository naming and other descriptions point to cyberbullying material; identity unresolved. | Identify precise upstream publisher, edition and terms; no blanket conclusion. |
| 10 | 13,240 | Zampieri et al. (2019), OLID/OffensEval training partition. | Official research release exists; independent unrestricted redistribution permission not established here. |

## What is and is not established
- Dataset 5 identity and bundled licence are directly supported by repository files.
- Dataset 1 and 7 may reuse overlapping Davidson material; they must not be counted as independent evidence without testing.
- The historical appendix includes inconsistent counts and captions; those are preserved as historical claims rather than silently corrected.
- Public research availability and open-source publication are acknowledged. **Unverified** means not independently confirmed in this audit, not necessarily forbidden.
- A definitive row-level provenance and rights clearance has **not** been completed for composite or transformed text.

## Reference links
- [de Gibert et al. (2018)](https://aclanthology.org/W18-5102/) and [bundled README](DataSets/dataset_5/README.md), [bundled licence](DataSets/dataset_5/LICENSE)
- [Davidson et al. (2017) upstream](https://github.com/t-davidson/hate-speech-and-offensive-language)
- [Waseem and Hovy source repository](https://github.com/zeeraktalat/hatespeech)
- [Jha and Mamidi (2017)](https://aclanthology.org/W17-2902/)
- [OLID official distribution](https://sites.google.com/site/offensevalsharedtask/olid)
- [Bibliography and citation details](BIBLIOGRAPHY.md)

## Reconciliation work still needed
Identify the exact upstream file for every `DataSets/` input, compare original hashes/schemas, separate composite dataset components, verify source-specific terms and align appendix counts with the corresponding processing stage. Do not present this ledger as final legal advice or a row-level provenance certificate.
