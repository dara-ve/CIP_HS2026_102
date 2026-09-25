# Project Plan

> Working document – to be refined by the team. Based on the [Feasibility Study](Feasibility_Study.md).

**Project Title:** Topics, Cantons and Party Participation in Swiss Parliamentary Business
**Group:** 102

## 1. Context

This project analyses parliamentary business in Switzerland: which topics are covered, how these topics are distributed across the cantons and which political parties participate most often.

We scrape the **Curia Vista** database of the Swiss Parliament (parlament.ch) with Selenium and BeautifulSoup. Curia Vista contains all parliamentary business items (motions, postulates, interpellations, questions, …) of the National Council and the Council of States, including submitter, parliamentary group, date, status and subject area.

As a supplement, we scrape the **council members page** (canton, party, council, term of office). Both datasets are linked via the **CouncillorId**. The **Open Data Web Services** of the Parliament (http://ws-old.parlament.ch) are used to validate the web scraping. **Election results** of the Federal Statistical Office (BFS) are merged via the party.

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
| Validation | Open Data Web Services (http://ws-old.parlament.ch) | `requests` | Validation of the web scraping (see 3.1) |
| Enrichment | Election results – BFS PX-Web (px-x-1702020000_104) | Download | Party strength per party and election year → merge with parties (see 3.2) |

- Join key between business items and council members: `CouncillorId`

### 3.1 API as Validation of the Web Scraping

The API http://ws-old.parlament.ch will be used to **validate the web scraping**, as it is expected to deliver the same data as the website.

**Field overview** based on one business item of the test sample (26.1034, `/affairs/20261034`) and its submitter (`/councillors/4223`):

| Field | Website (scraped) | API | Same? |
|---|---|---|---|
| Business number, type | 26.1034, Anfrage | `shortId` 26.1034, `affairType` Anfrage | ✅ |
| Submitter + CouncillorId | Molina Fabian, 4223 | `author.councillor` Molina Fabian, id 4223 | ✅ |
| Parliamentary group | Sozialdemokratische Fraktion | `author.faction` Sozialdemokratische Fraktion | ✅ |
| Submission date, council | 19.06.2026, Nationalrat | `deposit` 2026-06-19, Nationalrat | ✅ |
| State | Erledigt | `state` Erledigt | ✅ |
| Responsible authority | Departement des Innern (EDI) | `relatedDepartments` EDI | ✅ |
| Cosigners | Berli Rudi | `roles` type cosign: Berli Rudi | ✅ |
| Topics | Internationale Politik; Sozialer Schutz; Staatspolitik | Only codes in `additionalIndexing` ("04;08;2836"), no names; `descriptors` empty | ❌ not directly |
| Party | Sozialdemokratische Partei der Schweiz | Not in the business item; only via `/councillors/{id}` (`party` SP) | 🟡 via councillor |
| Canton | – (not on the business page) | `/councillors/{id}`: `canton` "Zürich", `cantonName` "ZH" | ➕ additional |

**Systematic comparison** of all 20 test items in `04_Validation/api_validation.ipynb` (2026-09-25):
- 100 % match: business number, type, submitter, CouncillorId, party (via councillor endpoint), submission date, council, state, responsible authority, cosigners
- Parliamentary group: 16 of 20; for 4 items the API returns no faction (website value available)
- Topics: only codes in the API; number of codes = number of scraped topics for 20 of 20

**Conclusion so far:** the API delivers most of the same fields and is suitable for validation. Open points:
- Topics are only available as codes → a mapping from code to topic name is needed (not verified yet).
- The councillor endpoint returns the **current** party, not necessarily the party at the time of submission.
- Repeat the comparison with the larger dataset.
- The councillor endpoint also provides the canton, which is needed for RQ2.

### 3.2 BFS Election Results (Party Strength)

Source: https://www.pxweb.bfs.admin.ch/pxweb/de/px-x-1702020000_104/px-x-1702020000_104/px-x-1702020000_104.px

Available values per party and election year (National Council elections), e.g. "Parteistimmen", "Fiktive Wählende" and "Parteistärke in %". Example: Switzerland 2023

| Party | Fictitious voters | Party strength in % |
|---|---|---|
| SVP | 713,471 | 27.93 |
| SP | 466,714 | 18.27 |
| FDP | 364,053 | 14.25 |
| Mitte | 359,075 | 14.06 |
| Grüne | 249,892 | 9.78 |
| GLP | 192,944 | 7.55 |
| EVP | 49,828 | 1.95 |
| EDU | 31,513 | 1.23 |

Further parties in the table: LPS, CSP, PdA, Sol., FGA, SD, Lega, MCR, CVP, BDP, LdU, POCH, Rep., PSA, FPS, Sep., Übrige ("..." = no value).

**Idea:** merge the party strength with the scraped business items via the party (`party_short`). This allows comparing the number of business items per party with its electoral strength (RQ3).

To be clarified:
- Party abbreviations differ (e.g. BFS "Grüne" vs. `party_short` "GRÜNE", BFS "MCR" vs. "MCG") → mapping table needed.
- Which election year applies to which business item (e.g. 2023 election for the legislative period 2023–2027)?
- Download format (CSV/Excel) and which dimensions (years, cantons) are needed.

## 4. Methodological Approach

1. **Data collection:** Selenium interacts with the dynamic elements (filters, search, paging); BeautifulSoup parses the rendered HTML. `requests` retrieves structured data from the API.
2. **Data preparation:** pandas checks missing values, datatypes, value ranges, outliers and inconsistent formats; scraped and API data are combined via IDs.
3. **Analysis & visualisation:** answer the three research questions with at least two different types of visualisations.

## 5. Work Packages

Detailed tasks and progress are tracked in [Status.md](Status.md).

### 5.1 Data Collection (`01_Collection/`)

- [x] Curia Vista scraper (Selenium) – tested with 20 completed Anfragen
- [ ] Scrape more business items / all relevant business types
- [ ] Add BeautifulSoup for parsing
- [ ] Council members scraper (canton, party)
- [ ] Download BFS election results

### 5.2 Data Preparation (`02_Preparation/`)

- [x] Cleaning notebook with all mandatory cleaning steps (test sample)
- [ ] Merge business items with council members (`CouncillorId`) and BFS party strength (party)
- [ ] Re-run on the larger dataset

### 5.3 Analysis & Visualisation (`03_Analysis/`)

- [x] Example analysis on the test sample (RQ1, RQ3, heatmap)
- [ ] Answer RQ1–RQ3 on the full dataset (RQ2 with cantons)

### 5.4 Validation (`04_Validation/`)

- [x] API validation of the 20 test items
- [ ] Re-run on the larger dataset, mapping of topic codes

### 5.5 Documentation & Submission

- [x] Feasibility study
- [ ] Final documentation (max. 6 pages)
- [ ] README: individual contributions

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
- Which election year / party mapping for the BFS election results?

## 10. Course Requirements Check

Comparison with the course requirements (`CIP_Project_Description.pdf`). Status as of 2026-09-25.

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
| Complementary sources, combined for new insights | 🟡 | API used for validation (`04_Validation/`); council members (canton!) and BFS election results still open |
| APIs: consult documentation, try different requests | 🟡 | ws-old.parlament.ch: `/affairs/{id}` and `/councillors/{id}` used in `04_Validation/api_validation.ipynb` (section 3.1) |

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
| Answer the research questions with Python | 🟡 | Example analysis on test sample (`03_Analysis/example_analysis.ipynb`); RQ2 open |
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
