# Task Creation Guide

This guide explains how to take a data source from `armenian_data_sources.md` and turn it into a GitHub Issue for a volunteer.

## 1. Select a Data Source
Open `docs/armenian_data_sources.md` and choose a source that hasn't been processed yet.
Check past issues to ensure it hasn't been duplicated.

## 2. Analyze the Source
Visit the website and determine:
- **Type of Data**: Is it a list of books, a gallery of images, an interactive map, or a searchable database?
- **Accessibility**: Is there an API? Is it simple HTML? Do you need Selenium/Puppeteer?
- **Volume**: Are there 10 items or 100,000?

## 3. Create the Issue
Go to the [Issues](https://github.com/opendataam/opendatam-tasks/issues) tab and click "New Issue".
Use the contents of `docs/issue_template.md` as your starting point.

### Filling the Fields:

**Title**: Use a clear, action-oriented title. Prefix with `[EN]` or non-English language code if needed.
*   *Example*: `[EN] Scrape digitized manuscripts metadata from Matenadaran website`

**Goal**: One sentence summary.
*   *Example*: "Create a comprehensive dataset of all digitized manuscripts available on the Matenadaran website."

**Tasks**: Break it down.
*   Detail the steps: "Visit https://matenadaran.am", "Iterate through pages", "Extract title, date, author".
*   Specify output format: "Save as `matenadaran_manuscripts.jsonl`".

**Context**:
*   Copy relevant descriptions from `armenian_data_sources.md`.
*   Explain *why* this matters (e.g., "Preserving digital heritage").

**Requirements**:
*   Standard open-source requirements (Public repo, MIT license).
*   Add source-specific notes (e.g., "Respect `robots.txt`", "Don't overload the server").

**Resources**:
*   Link strictly to the source URL.
*   Link to any specific sub-pages or APIs found during analysis.

## 4. Labels
Apply relevant labels:
*   `extraction` for scraping.
*   `parsing` for processing downloaded files.
*   `check&load` for simple data entry.
*   `topic-culture` for cultural heritage.
