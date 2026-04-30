---
artefact_type: unit
id: UNIT-<NAME>
intent: <intent_id>
status: draft
bolts: []
---

# Unit: <Unit Name>

## Mission
<이 Unit이 전달하는 measurable value 한 단락>

## DDD 위치
- subdomain: <core | supporting | generic>
- bounded context: <name>

## 포함 User Story
- US-<UNIT>-001 — <한 줄 요약>
- US-<UNIT>-002 — ...

## Loose Coupling 검증
- 다른 Unit과의 contact point: <event/API/data>
- 동기/비동기: <synchronous | asynchronous via event>
- 데이터 소유권: <명확히 어느 Unit이 source of truth인가>

## Suggested Bolts
- BOLT-001: <시간/일 단위로 끝낼 수 있는 작은 단위>
- BOLT-002: ...

## NFR
- <스토리에서 합의된 NFR 묶음>

## Risk
- <조직 risk register와 매칭되는 항목>

## Measurement Criteria
- business metric: <예: cross-sell conversion rate>
- technical metric: <예: API p95 latency>
