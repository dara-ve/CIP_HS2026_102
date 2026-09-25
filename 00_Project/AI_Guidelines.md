# AI Guidelines

Rules for any AI assistant working on this project (code, data, documentation).

## 1. Never invent anything

- Do not make up data, numbers, results, sources, URLs, quotes, dates, names or facts.
- Every statement about the data must be backed by the project data or by code output that has actually been run.
- Never fill gaps with plausible-looking values (e.g. missing parties, cantons, topics). Missing stays missing and is handled in the cleaning step.
- If something could not be verified (e.g. a website or API was not reachable), say so explicitly instead of guessing.

## 2. Only use project data and given context – otherwise ask

Allowed sources:
- Files in this repository (code, data, `00_Project/` documents)
- The course requirements: `00_Project/CIP_Project_Description.pdf`
- The data sources defined in the [Project Plan](Project_Plan.md) and the [Feasibility Study](Feasibility_Study.md)
- Information the group members provide directly

If information is missing, unclear or contradictory: **ask before continuing**. This includes:
- Changing research questions, scope, time period or business types
- Adding new data sources
- Decisions about how to treat data (e.g. removing rows, excluding groups)

## 3. No AI mentions in project outputs

- Do not mention in code, comments, notebooks, documentation, commit messages or pull requests that content was created with AI.
- No AI signatures, no "Co-Authored-By" lines for AI, no "generated with …" notes, no phrases like "As an AI …".
- Exception: the **AI Disclaimer** section in the README and in the final documentation is written by the group and must not be removed or changed by the AI.

## 4. Follow the course requirements

- Check every step against `00_Project/CIP_Project_Description.pdf` (see [Project Plan](Project_Plan.md), section 10).
- Focus on Python: data acquisition (Selenium, BeautifulSoup, requests), cleaning (pandas, numpy), visualisation (matplotlib / seaborn / plotly).
- Figures need axis labels (with units), legends, captions and good readability.
- Page limits: feasibility study max. 2 pages, final documentation max. 6 pages.

## 5. Results and interpretation

- Report results exactly as the code outputs them; do not round or embellish without saying so.
- Clearly separate **facts** (what the data shows) from **interpretation**. Interpretations and conclusions are made by the group; the AI may only suggest them, marked as suggestions.
- Mention limitations (e.g. business items submitted by committees or cantons, incomplete older data).

## 6. Code and data

- Language of all project files (code, comments, documentation): **English**.
- Write simple, readable code that matches the existing style; add short comments where the logic is not obvious.
- Scripts and notebooks must be reproducible: results come from code in the repository, not from manual edits of data files.
- Never modify raw data in `01_Collection/data/` by hand; cleaning happens in `02_Preparation/`.
- Test scrapers with a small sample first before running them on the full dataset.
- Scraping: respect `robots.txt`, keep delays between requests, do not overload the server.
- No passwords, tokens or personal credentials in the repository.

## 7. Collaboration

- Do not commit, push or delete files without explicit approval.
- Do not fill in the individual contributions of group members in the README – each member writes their own.
- After each completed step, update [Status.md](Status.md) (done / next steps).
