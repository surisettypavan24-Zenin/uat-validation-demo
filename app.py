import json
from pathlib import Path
from io import BytesIO
import streamlit as st
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='UAT Validation | Black Bulls', page_icon='🔎', layout='wide')
st.title('UAT Validation Agent')
st.caption('Black Bulls · PS04 · Synthetic demonstration')
st.info('Cloud edition: saved local-Qwen reviews and verified report, plus live timing calculations. No live LLM runs or new approval decisions are made here. The full local app supports those workflows.')
runs = json.loads((ROOT/'saved_ai_runs.json').read_text(encoding='utf-8'))
report_bytes = (ROOT/'Approved_UAT_Report.xlsx').read_bytes()
wb = load_workbook(BytesIO(report_bytes), read_only=True, data_only=True)
def records(sheet):
    rows = list(wb[sheet].values)
    return [dict(zip(rows[0], row)) for row in rows[1:]]
summary = {r['Item']:r['Value'] for r in records('Summary')}
cols = st.columns(3)
cols[0].metric('Linked coverage', f"{summary['Linked coverage percent']}%")
cols[1].metric('Event/timing criteria coverage', f"{summary['Event/timing criteria coverage percent']}%")
cols[2].metric('Recorded approved links', len(records('Link Approvals')))
tabs = st.tabs(['Verified results','AI review trail','Try timing checks','Architecture'])
with tabs[0]:
    st.subheader('Evidence outcomes')
    st.dataframe(records('Evidence Outcomes'), hide_index=True, use_container_width=True)
    st.subheader('Open findings')
    st.dataframe(records('Findings'), hide_index=True, use_container_width=True)
    with st.expander('Traceability and recorded approvals'):
        st.dataframe(records('Traceability'), hide_index=True)
        st.dataframe(records('Link Approvals'), hide_index=True)
    st.download_button('Download verified Excel report', report_bytes, 'Approved_UAT_Report.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    st.caption('This is the original exported synthetic report. Link approval and execution review are separate; execution findings remain pending human review.')
with tabs[1]:
    selected=st.selectbox('Saved AI review',range(len(runs)),format_func=lambda i:runs[i]['test_id'])
    run=runs[selected]
    st.write('Model:',run['model'],' · Recorded run:',run['run_id'])
    st.caption('Recorded outputs from local Ollama. Source quotations passing validation do not establish semantic correctness.')
    st.json(run['test_snapshot'])
    left,right=st.columns(2)
    with left:
        st.subheader('Generator'); st.json(run['generator'])
    with right:
        st.subheader('Critic'); st.json(run['critic']['critic'])
    st.subheader('Independent timing check'); st.json(run['timing_check'])
    st.subheader('AI quality flags'); st.json(run['quality_flags'])
    decisions=[r for r in records('Link Approvals') if r['AI Run']==run['run_id']]
    st.subheader('Subsequent recorded human decision'); st.dataframe(decisions, hide_index=True)
    st.caption('The original AI snapshot remains pending; the separate approval record above records the later decision.')
    st.download_button('Download original AI snapshot',json.dumps(run,indent=2),run['run_id']+'.json',mime='application/json')
with tabs[2]:
    from decimal import Decimal
    st.subheader('Interactive timing experiment')
    st.caption('Separate hypothetical calculation; changing these values does not modify the saved report or approval records.')
    required=st.number_input('Required maximum seconds',min_value=0.0,value=2.0,step=0.1)
    elapsed=st.number_input('Observed elapsed seconds',min_value=0.0,value=3.4,step=0.1)
    missing=st.checkbox('A request or response timestamp is missing')
    event=st.checkbox('Required event matches the observed event',value=True)
    if missing:
        st.warning('INCONCLUSIVE — a timestamp is missing.')
    elif not event:
        st.error('FAIL — observed event differs from the required event.')
    elif Decimal(str(elapsed))>Decimal(str(required)):
        st.error(f'FAIL — {elapsed:g} seconds exceeds {required:g} seconds.')
    else:
        st.success(f'PASS — {elapsed:g} seconds is within {required:g} seconds.')
    st.caption('This experiment assumes the evidence belongs to the correct transaction. Equality with the maximum passes.')
with tabs[3]:
    st.subheader('Full local workflow')
    st.markdown('1. Extract documents with source locations.\n2. Retrieve requirement candidates using TF-IDF cosine similarity.\n3. Qwen3 proposes a link; a separate call critiques it.\n4. Python verifies quotations and compares structured timing criteria.\n5. A human records a source-bound link decision.\n6. Deterministic evidence checks and Excel export use approved links.')
    st.subheader('Scope and limits')
    st.write('This cloud package demonstrates four synthetic requirements and three tests. It is not a broad accuracy benchmark. Same-model generator and critic share failure modes. Raw-log transaction association and structured timing fields are supplied. Customer packet checks and document findings remain in the local project.')
    st.write('Local stack: Streamlit, FastAPI, SQLite, Ollama/Qwen3:8b, TShark, Python. Cloud stack: Streamlit with saved synthetic artifacts. No laptop localhost endpoints are called from the cloud.')
wb.close()
