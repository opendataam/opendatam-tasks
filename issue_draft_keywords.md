## Goal
Add Armenian language support (`hy`) to the `armenian-keywords` repository to enable filtering of Armenian text content.

## Tasks
- [ ] Create a new directory `data/hy` in the [armenian-keywords](https://github.com/opendataam/armenian-keywords) repository.
- [ ] Translate or adapt `keywords.csv` from `data/en` or `data/ru` into Armenian.
- [ ] Translate or adapt `geonames.csv` (names of cities, regions, monasteries) into Armenian.
- [ ] Add `names.csv` with common Armenian first names in Armenian script.
- [ ] Submit a Pull Request to the `armenian-keywords` repository.

## Context
The [armenian-keywords](https://github.com/opendataam/armenian-keywords) repository is used to filter cultural data from international sources. Currently, it supports English (`en`) and Russian (`ru`), but lacks native Armenian (`hy`) support. Adding this is crucial for finding content in the Armenian language.

## Requirements
- Create a public fork of the repository.
- Maintain the existing CSV structure: `value` (the keyword) and `category` (e.g., `geo`, `person`, `culture`).
- Ensure the character encoding is UTF-8.

## Resources
- [armenian-keywords Repository](https://github.com/opendataam/armenian-keywords)
- [Example English Data](https://github.com/opendataam/armenian-keywords/tree/main/data/en)
