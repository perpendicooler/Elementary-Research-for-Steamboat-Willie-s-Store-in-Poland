# Data

`poland_towns_from_dataset.csv` is the Poland-only populated-place extract used by the repository.

It was generated from the supplied `dataset.json` by filtering:

- `country_code == "PL"`
- populated-place feature class (`feature_class == "P"`)
- records with valid latitude and longitude

The repository intentionally uses the compact Poland-only CSV instead of committing the much larger raw global JSON file.

If the original raw dataset must be preserved, keep it outside the normal Git history or use Git LFS after confirming its redistribution terms.
