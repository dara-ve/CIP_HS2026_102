# Project Status

_Last updated: 2026-09-24_

## Done

**Project setup**
- [x] Project structure set up (`Collection/`, `Preparation/`, `Analysis/`, `Project/`)
- [x] `.gitignore`, virtual environment (`.venv`) and `requirements.txt` (selenium, beautifulsoup4, requests, pandas, numpy, matplotlib, jupyter)
- [x] Feasibility study (`Project/Feasibility_Study.md`) integrated into project plan and README
- [x] Project plan incl. course requirements check (`Project/Project_Plan.md`, section 10)
- [x] README filled in (description, research questions, structure, data sources, installation, usage, AI disclaimer)
- [x] Current state committed and pushed to GitHub

**Data acquisition** – `Collection/scrape_curia_vista.py`
- [x] Selenium scraper for Curia Vista: selects the filters "Anfrage" + "Erledigt" (~4,065 results) and pages through the result list
- [x] Visits each business detail page and extracts submitter, CouncillorId, parliamentary group, party, submission date, council, state, responsible authority, cosigners and topics
- [x] `robots.txt` checked: the scraped pages are allowed
- [x] Tested with 2 pages (20 business items), all fields filled → `Collection/data/curia_vista_anfragen_erledigt.csv`

**Data preparation** – `Preparation/data_cleaning.ipynb`
- [x] All mandatory cleaning steps of the course: missing data, datatypes, expected ranges, outliers (flagged in `is_outlier`), long table per topic, enrichment (`submission_year`, `party_short`, `topic_count`)
- [x] Output: `Preparation/data/anfragen_clean.csv`, `Preparation/data/anfragen_topics_long.csv`

**Analysis** – `Analysis/example_analysis.ipynb`
- [x] Example analysis on the test sample (not representative)
- [x] RQ1: bar chart of topics; RQ3: bar chart of parties; heatmap topic × party
- [x] RQ2 placeholder: table topic × council (canton still missing)

## In Progress

- ...

## Next Steps

Prioritised according to the course requirements (see `Project_Plan.md`, section 10).

**1. More data (more business items)**
- [ ] Run the scraper with more business items than the 20 test items (`MAX_PAGES` larger or `None` for all ~4,065 completed Anfragen; all pages take several hours)
- [ ] Align the scraper with the research questions: RQ1/RQ2 need *all* completed business types, RQ3 needs *all* business items (not only "Anfrage" + "Erledigt")
- [ ] Select the analysis time period based on data completeness
- [ ] Re-run the cleaning and analysis notebooks on the larger dataset and review the checks

**2. Data acquisition**
- [ ] Use BeautifulSoup for parsing the detail pages (course requirement: "Use Selenium and BeautifulSoup")
- [ ] Scrape the council members page (canton, party, council) → required for RQ2
- [ ] Retrieve data from the Open Data Web Services (ws-old.parlament.ch) with `requests`, try different requests, compare with scraped data

**3. Data preparation**
- [ ] Merge business items with council members via `CouncillorId` (fulfils "combine / merge")
- [ ] Handle business items without a council member (committees, cantons) → separate category + limitation

**4. Analysis & visualisation**
- [ ] Answer RQ1–RQ3 on the full dataset in `Analysis/`
- [ ] RQ2: replace the council placeholder with cantons (e.g. heatmap topic × canton)
- [ ] Check figures: axis labels, legends, captions, readability

**5. Documentation & submission**
- [ ] Check feasibility study length (max. 2 pages), submit on ILIAS with group number in the file name
- [ ] Final documentation (max. 6 pages): introduction, methods, discussion, conclusion; mention the `robots.txt` check
- [ ] Fill in individual code contributions in the README
- [ ] Complete the project plan (work packages, responsibilities, timeline)
- [ ] Decide whether to include BFS election results (optional)

## Blockers / Open Issues

- Detail pages are rendered by Angular and load slowly; the scraper waits explicitly for the fields to appear.
- Scraping all business items takes several hours (one detail page per business item).
