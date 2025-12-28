# Issue Template

Copy the markdown below to create a new task.

```markdown
## Goal
[One sentence summary of the objective, e.g., "Scrape metadata for all manuscripts from the Bodleian Library collection."]

## Data Source
**Name**: [Source Name]
**URL**: [Source URL]
**Type**: [Source Type, e.g., Library, Archive]

## Tasks
- [ ] **Analysis**: Analyze the detailed structure of the [target collection/website].
- [ ] **Extraction**: Develop a scraper/parser to extract the following fields (if available):
    - Title / Name
    - Date / Period
    - Author / Creator
    - Description / Abstract
    - URL to original object
    - [Add key specific fields based on source description]
- [ ] **Processing**: Clean the data and save it as a structured file (CSV, JSONL).
- [ ] **Publication**: Push the code and data to a new public GitHub repository.

## Context
[Insert detailed description of the source, its collections, and its significance here. Extracted from the data sources file.]

## Deliverables
1.  **Code**: Python script (or other language) used for extraction.
2.  **Data**: The extracted dataset in a standard format (UTF-8 encoded).
3.  **Documentation**: A simple `README.md` explaining how to use the script and describing the data columns.

## Resources
- [Link to Source]
- [Link to specific collection if applicable]
```
