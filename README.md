# CIP_HS2026_102

**Topics, Cantons and Party Participation in Swiss Parliamentary Business**

This project analyses parliamentary business of the Swiss Parliament: which topics are covered, how these topics are distributed across the cantons and which political parties participate most often. Data is collected from the Swiss Parliament website (Curia Vista, council members) via web scraping and from the Parliament's Open Data Web Services, then cleaned, combined and analysed in Python.

## Research Questions

**Main question:** What patterns can be found in Swiss parliamentary business regarding topics, cantons and political parties?

1. Which topics occur most often in completed parliamentary business?
2. How are the topics of completed parliamentary business distributed across the cantons of the involved council members?
3. Which political parties participate most often in parliamentary business?

## Repository Structure

```
CIP_HS2026_102/
├── Collection/                  # Data acquisition (web scraping, API)
│   ├── scrape_curia_vista.py    # Selenium scraper for Curia Vista
│   └── data/                    # Raw scraped data
├── Preparation/                 # Data cleaning and transformation
│   ├── data_cleaning.ipynb      # Mandatory cleaning steps
│   └── data/                    # Cleaned data
├── Analysis/                    # Analysis and visualisations
│   └── example_analysis.ipynb   # Example analysis (test sample)
├── Project/                     # Project management
│   ├── Feasibility_Study.md
│   ├── Project_Plan.md
│   └── Status.md
├── requirements.txt
└── README.md
```

## Data Sources

- **Curia Vista** – search for parliamentary business: https://www.parlament.ch/de/ratsbetrieb/suche-curia-vista
- **Council members** – name, party, canton, council: https://www.parlament.ch/de/ratsmitglieder?k=*
- **Open Data Web Services** of the Swiss Parliament (validation / structured data): https://ws-old.parlament.ch/

Business items and council members are linked via the `CouncillorId`.

## Technologies Used

- Python 3
- Webscraping: Selenium, BeautifulSoup, requests
- Data Processing: pandas, numpy
- Visualization: matplotlib
- Statistical Analysis: tbd.
- Environment: Jupyter Notebook

## Installation

**Prerequisites:** Python 3.10 or newer, Git and Google Chrome (required by Selenium; the matching ChromeDriver is downloaded automatically by Selenium Manager).

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd CIP_HS2026_102
   ```

2. Create and activate a virtual environment:

   ```bash
   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate

   # Windows (PowerShell)
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Select the `.venv` interpreter as Jupyter kernel in VS Code, or start Jupyter with `jupyter notebook`.

## Usage

### 1. Data Collection

```bash
python Collection/scrape_curia_vista.py
```

The scraper opens the Curia Vista search, selects the filters "Anfrage" and "Erledigt", pages through the result list and visits every business detail page. The result is saved to `Collection/data/curia_vista_anfragen_erledigt.csv`.

Settings at the top of the script:
- `MAX_PAGES` – number of result pages (10 items each); `None` scrapes all pages (several hours)
- `HEADLESS` – `True` runs Chrome without a visible window

### 2. Data Processing

Open and run `Preparation/data_cleaning.ipynb`. It checks missing data, datatypes, value ranges and outliers, reshapes the topics into a long table and adds additional columns. Output files are written to `Preparation/data/`.

### 3. Analysis and Visualization

Open and run `Analysis/example_analysis.ipynb`. It reads the cleaned data from `Preparation/data/` and visualises the topics (RQ1) and the party participation (RQ3). The notebook is currently based on a test sample and will be extended once the full dataset is available.

## Individual Contributions

### Noah David Kiefer (noahdavid.kiefer@stud.hslu.ch)
- ...

### Louisa Zurlinden (louisa.zurlinden@stud.hslu.ch)
- ...

### Dara Velkov (dara.velkov@stud.hslu.ch)
- ...

## AI Disclaimer

Generative AI is used during the project to support the programming process, for example to explain error messages or help solve problems in the Python code. It also supports the work with web scraping and API requests, as well as improving the wording of the documentation. The analysis and interpretation of the results and the final conclusions are carried out by the group members.
