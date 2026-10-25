# Bible chapter reading data

A dataset and offline calculator for comparing Bible reading assignments: 1,189 chapters across the 66-book KJV and simplified CUV corpora. English words and Chinese characters are different units.

- [Read the reference](https://szj2ys.github.io/bible-chapter-reading-data/).
- All chapter counts: `docs/chapter-counts.csv`.
- The fuller [TrustBible chapter reading-time reference](https://trustbible.org/blog/how-long-to-read-each-bible-chapter/) explains the dataset and its limits. Maintained by the TrustBible team.

## Use it offline

Python 3.10 or newer; no dependencies, account or network calls.

```sh
python docs/estimate.py --book Ruth --chapter 2 --wpm 200
python docs/estimate.py --book Ruth --wpm 200
python docs/estimate.py --book John --chapter 3 --edition cuv --cpm 300
python docs/estimate.py --check
```

The first command reports 763 KJV words and 3.8 estimated minutes. Whole-book requests sum raw counts before dividing and rounding. Rates must be positive finite numbers. Invalid books and chapters produce an error.

## Data dictionary

| Column | Meaning |
| --- | --- |
| book_slug | English book identifier |
| book, book_zh | Source book names |
| chapter | One-based chapter number |
| kjv_words | Whitespace-delimited tokens of KJV verse text |
| cuv_chars | Unicode letters/numbers of CUV verse text; punctuation, spaces and symbols excluded |
| kjv_minutes_at_238wpm | Count / 238, rounded to one decimal |
| cuv_minutes_at_390cpm | Count / 390, rounded to one decimal |

## Provenance and limitations

KJV: https://github.com/aruljohn/Bible-kjv. CUV: https://github.com/seven1m/open-bibles, `chi-cuv-simp.usfx.xml`. TrustBible imported its verse corpora September 6, 2026 and checked these counts October 25, 2026. Totals: 789,634 KJV tokens and 930,059 CUV letters/numbers. We publish derived counts, not scripture text.

The 238 words/minute baseline comes from Brysbaert (2019), DOI https://doi.org/10.1016/j.jml.2019.104047, adult English non-fiction silent reading. The 390 characters/minute CUV baseline is our conversion of the paper's 260 Chinese word-units/minute using its rough 1.5 characters/word relationship; 390 is not printed in Table 5. Neither is a Bible-specific or personal measurement.

Counts depend on the edition and rules. This 66-book corpus does not represent every Christian canon. Estimates leave out discussion, reflection and breaks, and do not measure comprehension or spiritual growth. They are not validated for children or oral reading. Choose your own rate.

`--check` verifies the distributed dataset's structure, totals and estimate arithmetic; it does not independently recount upstream verse text. The full corpus recount is documented in the linked TrustBible reference.

The original calculator and documentation are MIT licensed; see LICENSE. Derived numerical facts are supplied with provenance. No source scripture text or third-party article is relicensed here.
