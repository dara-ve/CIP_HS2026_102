# Project Status

_Last updated: 2026-09-25_

## Where to continue (short overview)

- **Pipeline works end-to-end on a test sample of 20 completed Anfragen:** scraping → cleaning → example analysis → API validation.
- **Most important next step:** scrape more business items (and decide which business types, see below), then re-run the notebooks.
- **Still missing for the research questions:** canton (council members data, needed for RQ2) and BFS party strength (RQ3).
- **Order to run:** `01_Collection/scrape_curia_vista.py` → `02_Preparation/data_cleaning.ipynb` → `03_Analysis/example_analysis.ipynb`; `04_Validation/api_validation.ipynb` works on the raw data.
- **Open decisions for the group:** business types and time period, election year / party mapping for BFS data.

## Done

**Project setup**
- [x] Project structure set up (`00_Project/`, `01_Collection/`, `02_Preparation/`, `03_Analysis/`)
- [x] `.gitignore`, virtual environment (`.venv`) and `requirements.txt` (selenium, beautifulsoup4, requests, pandas, numpy, matplotlib, jupyter)
- [x] Feasibility study (`00_Project/Feasibility_Study.md`) integrated into project plan and README
- [x] Project plan incl. course requirements check (`00_Project/Project_Plan.md`, section 10)
- [x] README filled in (description, research questions, structure, data sources, installation, usage, AI disclaimer)
- [x] Current state committed and pushed to GitHub
- [x] Folders renamed with numbering (`00_Project`, `01_Collection`, `02_Preparation`, `03_Analysis`, `04_Validation`), paths in code and documentation adjusted

**Data acquisition** – `01_Collection/scrape_curia_vista.py`
- [x] Selenium scraper for Curia Vista: selects the filters "Anfrage" + "Erledigt" (~4,065 results) and pages through the result list
- [x] Visits each business detail page and extracts submitter, CouncillorId, parliamentary group, party, submission date, council, state, responsible authority, cosigners and topics
- [x] `robots.txt` checked: the scraped pages are allowed
- [x] First API check (ws-old.parlament.ch) with one business item: most fields identical to the website; topics only as codes; party and canton via the councillor endpoint (details: `Project_Plan.md`, section 3.1)
- [x] Tested with 2 pages (20 business items), all fields filled → `01_Collection/data/curia_vista_anfragen_erledigt.csv`

**Data preparation** – `02_Preparation/data_cleaning.ipynb`
- [x] All mandatory cleaning steps of the course: missing data, datatypes, expected ranges, outliers (flagged in `is_outlier`), long table per topic, enrichment (`submission_year`, `party_short`, `topic_count`)
- [x] Output: `02_Preparation/data/anfragen_clean.csv`, `02_Preparation/data/anfragen_topics_long.csv`

**Analysis** – `03_Analysis/example_analysis.ipynb`
- [x] Example analysis on the test sample (not representative)
- [x] RQ1: bar chart of topics; RQ3: bar chart of parties; heatmap topic × party
- [x] RQ2 placeholder: table topic × council (canton still missing)

**Validation** – `04_Validation/api_validation.ipynb`
- [x] All 20 scraped business items retrieved from the API (ws-old.parlament.ch) with `requests` and compared field by field
- [x] 100 % match: business number, type, submitter, CouncillorId, party (via councillor endpoint), submission date, council, state, responsible authority, cosigners
- [x] Parliamentary group: 16 of 20 match; for 4 items (26.1031, 26.1030, 26.1028, 26.1020) the API returns no faction in `author` (website value available)
- [x] Topics: API only returns codes (`additionalIndexing`); number of codes = number of scraped topics for 20 of 20 (mapping code → name not verified)

## In Progress

- (nothing in progress – add your name when you start a task)

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
- [ ] **API validation on the larger dataset**: re-run `04_Validation/api_validation.ipynb` once more business items are scraped; write the summary in the notebook
  - [ ] Find a mapping from topic codes (`additionalIndexing`) to topic names
  - [ ] Check whether the councillor endpoint returns the party at submission time or only the current party
- [ ] **BFS election results** (PX-Web px-x-1702020000_104): download party strength ("Parteistärke in %", "Fiktive Wählende") per party and election year

**3. Data preparation**
- [ ] Merge business items with council members via `CouncillorId` (fulfils "combine / merge")
- [ ] Handle business items without a council member (committees, cantons) → separate category + limitation
- [ ] Merge BFS party strength with the business items via the party (mapping table for different abbreviations, e.g. "Grüne"/"GRÜNE", "MCR"/"MCG"; define which election year applies)

**4. Analysis & visualisation**
- [ ] Answer RQ1–RQ3 on the full dataset in `03_Analysis/`
- [ ] RQ2: replace the council placeholder with cantons (e.g. heatmap topic × canton)
- [ ] Check figures: axis labels, legends, captions, readability
- [ ] RQ3: compare the number of business items per party with the party strength (BFS)

**5. Documentation & submission**
- [ ] Check feasibility study length (max. 2 pages), submit on ILIAS with group number in the file name
- [ ] Final documentation (max. 6 pages): introduction, methods, discussion, conclusion; mention the `robots.txt` check
- [ ] Fill in individual code contributions in the README
- [ ] Complete the project plan (work packages, responsibilities, timeline)

## Blockers / Open Issues

- Detail pages are rendered by Angular and load slowly; the scraper waits explicitly for the fields to appear.
- Scraping all business items takes several hours (one detail page per business item).
