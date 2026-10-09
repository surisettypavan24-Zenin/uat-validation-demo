# Three-minute demonstration

## 0:00 — Problem

UAT reviewers need to connect requirements to tests, identify missing acceptance criteria and verify evidence. A recorded status such as Done does not itself prove that a requirement passed.

## 0:25 — Results

Open Verified results. Explain that this is a synthetic baseline: four requirements, three tests and three approved links. Coverage is 75%, but only 25% has complete event/timing criteria. T01 is late, T02 is within the limit and T03 lacks a timestamp.

## 1:00 — AI and checks

Open AI review trail. Select T02. The critic says timing is missing while quoting within 5 seconds. The deterministic check identifies the contradiction, and the human decision explains the correction. Select T03: the critic and Python both identify the four-versus-two-second mismatch.

## 1:50 — Interactive boundary

Open Try timing checks. Set required maximum to 2 and observed duration to 3.4: FAIL. Change observed duration to 2: PASS at the boundary. Check missing timestamp: INCONCLUSIVE. These hypothetical changes do not overwrite the saved report.

## 2:20 — Audit and export

Return to Verified results, expand recorded approvals and download Excel. Explain that original AI outputs and later human decisions are separate records. Link approval does not turn execution failure into a pass.

## 2:45 — Scope

The public cloud edition replays saved AI reviews and performs live timing experiments. Live Qwen3 inference and approval persistence run in our local application. Our next evaluation expands scenarios and measures false findings on independently labelled cases. We do not claim production readiness or universal accuracy.
