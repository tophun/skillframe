# Inception Phase — Mob Elaboration

Inception Phase는 **intent를 capture해서 Unit으로 번역**하는 단계다. 핵심 ritual은 **Mob Elaboration**: 한 방에서 shared screen으로 facilitator가 진행하며 AI가 중심 역할을 한다. 본 세션 컨텍스트에서는 "한 방"이 곧 현재 conversation이며, AI가 facilitator 역할을 겸한다.

이 phase는 weeks/months 분량의 sequential work를 몇 시간으로 압축하면서, mob 내부와 mob-AI 간 deep alignment를 달성하는 것이 목적이다.

---

## 입력
- Step 0에서 등록된 `aidlc-docs/requirements/intent.md`
- Pathway 식별 결과 (green-field / brown-field / refactor / defect-fix / NFR 개선)

## 출력 (Unit별로 채워진다)
- (a) **PRFAQ** — `aidlc-docs/requirements/<unit>_prfaq.md` (선택)
- (b) **User Stories + Acceptance Criteria** — `aidlc-docs/story-artifacts/<unit>/`
- (c) **NFR 정의** — `aidlc-docs/risks/nfr.md`
- (d) **Risk Description** (조직의 risk register와 매칭) — `aidlc-docs/risks/risk_register.md`
- (e) **Measurement Criteria** (business intent로 traceable) — `aidlc-docs/requirements/measurement.md`
- (f) **Suggested Bolts** (Unit을 어떻게 build할지) — `aidlc-docs/plans/bolts/`

---

## Mob Elaboration 절차

각 단계는 **plan-first**다. plan을 먼저 만들고 사용자 승인 후 실행한다.

### a. Clarifying Questions
AI가 intent의 ambiguity를 줄이기 위한 질문을 던진다. 예:
- "Who are the primary users?"
- "What key business outcomes should this achieve?"
- "성공 지표는 무엇인가요? (예: conversion lift %, latency p95)"
- "주요 trade-off가 예상되는 영역은? (cost vs performance, build vs buy)"

질문은 **한 번에 묶어서** 던지고, 답을 받기 전엔 elaboration을 진행하지 않는다.

### b. User Story / NFR / Risk Elaboration
clarified intent로부터 AI가 다음을 생성한다:
- **User Stories** (As a..., I want..., so that... + Acceptance Criteria)
- **NFR 정의** (scalability, availability, latency, security, observability 등)
- **Risk Description** (compliance, data residency, third-party dependency 등)

team(mob)이 산출물을 validate하고 oversight + correction을 가한다.

### c. Cohesive Story → Unit 묶음
AI가 highly cohesive한 user story들을 **Unit**으로 묶는다. Unit은 loosely coupled, independent build/deploy 가능해야 한다.

예: recommendation engine intent → Units = [`User Data Collection`, `Recommendation Algorithm Selection`, `API Integration`]

### d. Product Owner Validation
Product Owner(없으면 사용자가 그 역할)가 Unit을 검토하고 빠진 관점을 보강한다. 예: "User Data Collection" Unit에 GDPR/PIPA 관련 privacy compliance 요구사항이 빠졌다면 즉시 추가.

### e. PRFAQ 생성 (선택)
각 Unit 또는 전체 module에 대해 PRFAQ를 작성한다 — business intent, 기능, 기대 benefit을 한 페이지로.

### f. PRFAQ + Risk Validation
Developer + Product Owner가 PRFAQ와 연관 risk를 검증한다. overall objective와의 정렬 확인.

---

## 표준 프롬프트

`references/prompts-library.md`의 다음 섹션을 사용:
- `## User stories` 프롬프트
- `## Units` 프롬프트

---

## brown-field에서의 차이
brown-field는 inception 활동 자체는 green-field와 동일하다. 차이는 construction phase에서 reverse engineering 단계가 추가되는 것이다 (`references/construction.md` 참조).

---

## 완료 조건 (Definition of Done for Inception)

다음 체크리스트를 만족할 때만 Construction Phase로 넘어간다.

- [ ] intent가 `requirements/intent.md`에 단일한 문장으로 기록됨
- [ ] pathway가 식별됨 (green-field / brown-field / refactor / defect-fix / NFR 개선)
- [ ] Level 1 Plan이 사용자 승인됨
- [ ] 모든 user story에 acceptance criteria가 있음
- [ ] NFR이 정의됨 (또는 "해당 없음" 명시)
- [ ] Risk가 식별되어 risk register에 정렬됨
- [ ] Measurement criteria가 business intent로 traceable함
- [ ] Unit이 1개 이상 정의되고 loose coupling이 검증됨
- [ ] 각 Unit에 대한 Bolt 제안이 있음
- [ ] Product Owner(또는 사용자)의 명시적 approval 기록이 plan에 남아 있음

---

## 함정 회피

- 질문을 한 번에 던지지 않고 한 답 받고 또 묻고 하면 사용자 피로도 폭증 — **batched clarifying questions**.
- AI가 user story를 너무 잘게 쪼개려는 경향 → INVEST 원칙(특히 Valuable, Estimable, Small) 점검.
- NFR을 잊고 구현하면 Logical Design 단계에서 architecture 재설계 비용 발생 → Inception에서 반드시 명시.
- Unit 간 coupling이 발견되면 그 자리에서 boundary 재조정. 다음 phase로 미루지 않는다.
