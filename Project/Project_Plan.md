# Project Plan

> Working document – to be refined by the team. Based on the [Feasibility Study](Feasibility_Study.md).

**Project Title:** Topics, Cantons and Party Participation in Swiss Parliamentary Business
**Group:** 102

## 1. Context

This project analyses parliamentary business in Switzerland: which topics are covered, how these topics are distributed across the cantons and which political parties participate most often.

We scrape the **Curia Vista** database of the Swiss Parliament (parlament.ch) with Selenium and BeautifulSoup. Curia Vista contains all parliamentary business items (motions, postulates, interpellations, questions, …) of the National Council and the Council of States, including submitter, parliamentary group, date, status and subject area.

As a supplement, we scrape the **council members page** (canton, party, council, term of office). Both datasets are linked via the **CouncillorId**. The **Open Data Web Services** of the Parliament are used to retrieve structured data and to validate the scraped data.

## 2. Research Questions

**Main question:** What patterns can be found in Swiss parliamentary business regarding topics, cantons and political parties?

1. Which topics occur most often in completed parliamentary business?
2. How are the topics of completed parliamentary business distributed across the cantons of the involved council members?
3. Which political parties participate most often in parliamentary business?

## 3. Data Sources

| Role | Source | Method | Notes |
|---|---|---|---|
| Main source | Curia Vista (https://www.parlament.ch/de/ratsbetrieb/suche-curia-vista) | Selenium + BeautifulSoup | Dynamic filters (business type, state) and paging |
| Additional source | Council members (https://www.parlament.ch/de/ratsmitglieder?k=*) | Selenium + BeautifulSoup | Name, party, canton, council |
| API / validation | Open Data Web Services (https://ws-old.parlament.ch/) | `requests` | Structured data, cross-check if scraped data is incomplete |
| Optional | Election results – BFS PX-Web (px-x-1702020000_104) | Download (Excel/CSV) | Possible link to past election results |

- BFS election results: https://www.pxweb.bfs.admin.ch/pxweb/de/px-x-1702020000_104/px-x-1702020000_104/px-x-1702020000_104.px
- Join key between business items and council members: `CouncillorId`

## 4. Methodological Approach

1. **Data collection:** Selenium interacts with the dynamic elements (filters, search, paging); BeautifulSoup parses the rendered HTML. `requests` retrieves structured data from the API.
2. **Data preparation:** pandas checks missing values, datatypes, value ranges, outliers and inconsistent formats; scraped and API data are combined via IDs.
3. **Analysis & visualisation:** answer the three research questions with at least two different types of visualisations.

## 5. Work Packages

### 5.1 Data Collection (`Collection/`)

- [ ] ...

### 5.2 Data Preparation (`Preparation/`)

- [ ] ...

### 5.3 Analysis & Visualisation (`Analysis/`)

- [ ] ...

### 5.4 Documentation & Submission

- [ ] ...

## 6. Risks and Mitigation

| Risk | Mitigation |
|---|---|
| Website structure changes / dynamically loaded content breaks the scraper | Test with a small number of business items first; adjust Selenium/BeautifulSoup code |
| Website and API use different structures and variable names | Compare both sources first; connect via IDs; rename/format columns with pandas |
| Business submitted by a committee or canton instead of a council member | Check actor type during preparation; use only cases with a clear party/canton link; treat others separately and mention as limitation |
| Missing or incomplete data (especially older business items); parties/topics change over time | Check completeness per time period; select a suitable analysis period (focus on recent years if needed); cross-check website and API |

## 7. Responsibilities

| Task | Responsible |
|---|---|
| ... | ... |

## 8. Timeline / Milestones

| Milestone | Deadline | Status |
|---|---|---|
| Feasibility study | ... | Done |
| ... | ... | ... |

## 9. Open Questions

- Which time period will be analysed (depends on data completeness)?
- Which business types are included (only "Anfragen" or also motions, postulates, interpellations)?
- Include BFS election results?

## 10. Course Requirements Check

Comparison with the course requirements (`CIP_Project_Description.pdf`). Status as of 2026-09-24.

✅ = done · 🟡 = partially done · ❌ = open

### Feasibility Study (ILIAS)

| Requirement | Status | Notes |
|---|---|---|
| Introduction: scope and purpose | ✅ | Chapter 1 |
| At least three research questions | ✅ | Main question + 3 sub-questions |
| Key data sources described | ✅ | Chapter 3 |
| Risks regarding data collection/quality + mitigation | ✅ | Chapter 5 |
| Max. 2 pages | 🟡 | Check page count in the final Word/PDF layout |
| Group number in file name, submitted once | ❌ | e.g. `CIP_HS2026_102_Feasibility_Study.pdf` |

### Data Acquisition

| Requirement | Status | Notes |
|---|---|---|
| Collect the data yourself (scraping / API / simulation) | 🟡 | Curia Vista scraper done (tested with 20 items) |
| Consult `robots.txt` | ✅ | parlament.ch only disallows `/_layouts/`, `/_vti_bin/`, `/_catalogs/`, `/publish/`; the scraped pages are allowed. Mention this in the documentation |
| Interact with at least one dynamic element | ✅ | Filter checkboxes (business type, state) and paging |
| Use Selenium **and BeautifulSoup** | 🟡 | Selenium ✅, BeautifulSoup ❌ → parse detail pages with BeautifulSoup |
| Complementary sources, combined for new insights | ❌ | Council members (canton!) and API still open |
| APIs: consult documentation, try different requests | ❌ | ws-old.parlament.ch |

### Data Transformation / Cleansing

| Requirement | Status | Notes |
|---|---|---|
| Check for gaps / missing data | ✅ | `data_cleaning.ipynb` |
| Check datatypes, change if needed | ✅ | |
| Check expected value ranges | ✅ | |
| Identify outliers, treat them reasonably | ✅ | Flagged in `is_outlier` |
| Format dataset for the task (combine, merge, resample, …) | 🟡 | Topics as long table ✅; **merge** with council members / API data still open |
| Enrich with at least one additional column | ✅ | `submission_year`, `party_short`, `topic_count` |
| Run on the full dataset | ❌ | So far only 20 test rows → run with more business items |

### Analysis and Visualization

| Requirement | Status | Notes |
|---|---|---|
| Answer the research questions with Python | 🟡 | Example analysis on test sample (`Analysis/example_analysis.ipynb`); RQ2 open |
| Visualise results with tables/figures | 🟡 | matplotlib: bar charts + heatmap |
| Axis labels (units), readability, captions, legends | 🟡 | Titles, axis labels, source/n; review for final figures |

### Final Documentation (ILIAS, max. 6 pages)

| Requirement | Status | Notes |
|---|---|---|
| Introduction: overview + motivation | ❌ | Can build on the feasibility study |
| Methods: data sources, cleaning steps, analysis methods | ❌ | |
| Discussion of results (main focus) | ❌ | |
| At least two different types of visualisations | ❌ | e.g. bar chart + heatmap |
| Conclusion: learnings, limitations, outlook | ❌ | Limitations: committees/cantons as submitters, time period |
| Max. 6 pages, group number in file name | ❌ | |

### GitHub Repository

| Requirement | Status | Notes |
|---|---|---|
| Naming `CIP_[HS/FS][YEAR]_groupnumber` | ✅ | `CIP_HS2026_102` |
| Code in the repository | ✅ | Committed and pushed |
| Short README where each student refers to their code contribution | 🟡 | README done, contributions still open |
| Code structure, readability, repository organisation | 🟡 | Folder structure in place; keep it consistent |

### Consistency Check: Research Questions vs. Data

| Research question | Data needed | Current state |
|---|---|---|
| RQ1: Topics in **completed** business | Topics of all completed business items | Scraper only collects business type "Anfrage" → extend to all types (filter "Erledigt" only) or narrow the question |
| RQ2: Topics per **canton** | Canton of the submitter | Canton not in Curia Vista data → scrape council members and merge via `CouncillorId` |
| RQ3: Party participation in **all** business | Party for all business items (not only completed) | Currently only completed "Anfragen" → scrape without state filter |
