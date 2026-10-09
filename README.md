# UAT Validation Agent — Black Bulls

PS04 synthetic cloud demonstration. This package is a deployment companion to the full local application, not a replacement for it.

## Run

Use Python 3.12. Install `pip install -r requirements.txt`, then run `python -m streamlit run app.py`.

## Deploy to Streamlit Community Cloud

1. Create a GitHub repository named `uat-validation-demo`.
2. Upload the CONTENTS of this folder to the repository root, including the Excel and JSON files. Commit the files. Do not upload the ZIP itself.
3. Sign in at https://share.streamlit.io/ with GitHub.
4. Create an app from this repository, select branch `main`, and entrypoint `app.py`.
5. Choose Python 3.12 in advanced settings if available, then deploy.
6. Check all four tabs, download the Excel report, and test the timing boundary at 2.0 seconds.

The package requires no API keys, FastAPI service or Ollama server. All included cases are synthetic. The exported report includes reviewer Pavan's recorded decisions. Customer documents, subscriber identifiers and packet captures are not included.

## What runs live

Streamlit renders the report and audit trail and computes a hypothetical event/timing result when inputs change. The AI outputs are saved historical results, clearly labelled. New model inference and persistent approvals are available in the full local application only. A hosted model/backend and persistent access-controlled storage would be needed for a full online workflow.

## Verified baseline

Four requirements; three tests; three recorded approved links. Linked coverage 75%; event/timing criteria completeness 25%. T01 FAIL (3.4 > 2 seconds); T02 PASS (1.2 <= 5 seconds); T03 INCONCLUSIVE (timestamp missing). R02 has no approved link. These are baseline demonstration outcomes, not accuracy estimates or customer UAT certification.

## Local architecture

Document extraction retains source locations. TF-IDF retrieval produces candidate requirements. Qwen3:8b runs a generator call and a critic call through local Ollama. Python checks exact quotations and structured event/timing fields. SQLite stores reviewer decisions tied to source snapshots. The validation engine checks evidence against approved requirements and exports an Excel audit trail. The UI is Streamlit; the local service is FastAPI.

The critic produced false findings in the supplied runs. The report demonstrates explicit disagreements and human corrections, not infallible AI. Link approval does not approve execution verdicts. Customer-data extraction and selected packet consistency checks exist in the separate local project. A comprehensive requirements parser, broader retrieval corpus and larger independent evaluation remain further work.

## Repository contents

`app.py`, `requirements.txt`, `saved_ai_runs.json`, `Approved_UAT_Report.xlsx`, `README.md`, `DEMO_SCRIPT.md`.
