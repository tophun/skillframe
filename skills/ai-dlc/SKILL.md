---
name: ai-dlc
description: AI-Driven Development Lifecycle (AI-DLC) 방법론에 따라 소프트웨어 개발 업무를 수행한다. 사용자가 "AI-DLC", "Mob Elaboration", "Bolt", "Inception/Construction/Operations Phase", "Domain Design", "Unit 분해", "Intent 분해", "DDD 기반 개발 방법" 같은 용어를 언급하거나, "이 요구사항을 단계적으로 진행하고 싶어", "기획부터 배포까지 AI 주도 워크플로우로 진행해줘", "green-field/brown-field 개발 시작하자" 같은 요청을 하면 반드시 이 스킬을 사용한다. AWS의 AI-DLC 방법론을 충실히 따르며 Inception → Construction → Operations 흐름과 사람 oversight gate를 강제한다.
---

# AI-DLC: AI-Driven Development Lifecycle

이 스킬은 AWS Raja SP가 제안한 **AI-Driven Development Lifecycle (AI-DLC)** 방법론에 따라 소프트웨어 개발 업무를 수행하는 프로토콜이다. AI가 워크플로우를 주도(planning, decomposition, generation)하고 사람은 critical decision junction에서 oversight를 수행하는 "역방향(reverse direction)" 패러다임을 강제한다.

이 스킬은 **rigid skill**이다. 단계 순서, oversight gate, artefact 산출 위치는 임의로 건너뛰거나 압축하지 않는다. AI-DLC의 본질은 "loss function으로서의 사람 검증"을 통해 downstream 낭비를 조기에 차단하는 것이기 때문이다.

## 언제 이 스킬을 사용하는가

- 사용자가 새 시스템(green-field) 또는 기존 시스템 변경(brown-field)을 AI-DLC 흐름으로 진행하길 원할 때
- "Intent → Unit → Bolt"로 작업을 분해해야 할 때
- Mob Elaboration / Mob Construction / Mob Testing 의 ritual을 실행해야 할 때
- DDD flavor (Domain Design → Logical Design → Code → Deployment Unit)로 구현해야 할 때
- 기존 SDLC를 AI-Native 흐름으로 전환하는 가이드가 필요할 때

## 핵심 원칙 요약 (반드시 준수)

1. **Reverse Conversation Direction** — AI가 먼저 plan/breakdown/recommendation을 만들어 사람에게 제시하고, 사람은 approver 역할을 한다. 사람이 task별 instruction을 하나씩 던져주는 방식이 아니다.
2. **Plan-First Gate** — 모든 단계는 markdown plan 파일(체크박스 포함)을 먼저 작성하고 사용자 승인을 받은 뒤 실행한다. critical decision은 절대 단독으로 내리지 않는다.
3. **Loss Function Oversight** — 각 단계의 산출물은 사람의 validation/correction을 받고 다음 단계의 semantically rich context가 된다. 한 단계가 미흡하면 즉시 멈추고 보정한다.
4. **DDD Flavor 기본** — 별도 지시가 없으면 Domain-Driven Design 원칙(aggregate, value object, entity, domain event, repository, factory, bounded context)으로 모델링한다.
5. **Artefact Persistence & Traceability** — 모든 산출물은 `aidlc-docs/`(또는 사용자 지정 root) 하위 정해진 위치에 markdown으로 보관한다. backward/forward traceability(예: domain model 요소 ↔ user story)를 유지한다.
6. **Bolts, not Sprints** — 반복 단위는 시간/일 단위의 Bolt다. 4~6주 sprint 호흡으로 일정을 짜지 않는다.
7. **Build Better Systems Faster** — AI는 heavy-lifting(planning, decomposition, generation, test execution, observability triage)을 하고 사람은 oversight·strategic alignment에 집중한다.

> 전체 10대 원칙과 근거는 `references/principles.md` 참고.

## 워크스페이스 초기화 (첫 실행 시 1회)

세션 시작 시 작업 루트에 `aidlc-docs/` 트리가 없으면 다음 스크립트를 실행해 만든다. 사용자에게 "어느 폴더를 AI-DLC 작업 루트로 쓸까요?"를 먼저 묻고, 답을 받으면 그 경로에서 실행한다.

```bash
bash <skill-path>/scripts/init_aidlc_workspace.sh <project-root>
```

생성되는 표준 구조:

```
<project-root>/aidlc-docs/
├── plans/                # 각 단계 계획 md (checkbox)
├── requirements/         # 요구사항/기능 변경 문서
├── story-artifacts/      # user stories, acceptance criteria
├── design-artifacts/     # domain model, logical design, ADR
├── risks/                # NFR, risk register matching
├── tests/                # test plan, test result, validation report
├── deployment/           # IaC, deployment unit manifest
├── operations/           # observability, runbook, postmortem
└── prompts.md            # 세션에서 사용한 프롬프트 누적 기록
```

## 마스터 워크플로우

사용자가 어떤 intent로 진입하든 다음 게이트 시퀀스를 따른다. 각 게이트에서 plan md를 먼저 만들고 승인을 받는다.

### Step 0. Intent 등록 & Pathway 식별
- 사용자의 한 줄 intent를 `aidlc-docs/requirements/intent.md`에 기록.
- pathway 식별: green-field / brown-field / refactor / defect-fix / NFR 개선 중 무엇인가?
- pathway별 분기는 `references/inception.md` 참조.

### Step 1. Level 1 Plan 생성 (AI 주도)
- AI가 intent와 pathway에 기반해 phase 단위 high-level plan을 `aidlc-docs/plans/level1_plan.md`로 작성한다.
- 사람은 단계 추가/삭제/수정으로 oversight를 가한다.
- 승인 후에만 다음 단계로 진행.

### Step 2. Inception Phase — Mob Elaboration
- 산출물: `requirements/`, `story-artifacts/`, `risks/`, `aidlc-docs/units/<unit>.md`
- 자세한 절차·prompt는 `references/inception.md` 참조.

### Step 3. Construction Phase — Mob Programming / Mob Testing / Mob Construction
- Domain Design → Logical Design (with ADR) → Code & Unit Test → Deployment Unit
- brown-field일 경우 reverse-engineering(static + dynamic model 추출) 단계가 추가된다.
- 자세한 절차·prompt는 `references/construction.md` 참조.

### Step 4. Operations Phase
- Deploy → Observability → Incident triage with runbooks
- 자세한 절차는 `references/operations.md` 참조.

### Step 5. Iteration (Bolt closeout)
- 한 Bolt가 끝나면 traceability 갱신, prompts.md 누적, 다음 Bolt 후보를 제안한다.

## 모든 단계에서 강제되는 행동 규약

이 규약은 Appendix A의 표준 프롬프트 패턴에서 추출한 것이다. 모든 task 시작 시 다음을 따른다.

1. **역할 선언**: "Your Role:" 형태로 본인의 역할(예: software architect, product manager, cloud architect)을 명시.
2. **plan 먼저**: 작업 내용을 `aidlc-docs/plans/<task>_plan.md` 또는 해당 단계의 plan 위치에 체크박스 리스트로 작성.
3. **clarification 표시**: plan 항목 중 사용자 확인이 필요한 부분은 step 안에 그대로 남겨두고 질문한다. 단독 결정 금지.
4. **승인 요청**: plan을 사용자에게 보여주고 review/approval을 명시적으로 요청.
5. **승인 후 step-by-step 실행**: plan을 그대로 따라 한 step씩 실행, 각 step 완료마다 plan의 체크박스를 `[x]`로 갱신.
6. **artefact 저장 위치 준수**: 위 폴더 트리를 어기지 않는다.
7. **prompts.md 갱신**: 본 세션에서 사용한 표준 프롬프트는 `aidlc-docs/prompts.md`에 누적한다.

## 표준 프롬프트 라이브러리

Setup / User Stories / Units / Domain Model / Code Generation / Architecture / IaC 표준 프롬프트는 `references/prompts-library.md`에 있다. AI-DLC ritual을 실행할 때는 이 프롬프트들을 그대로 또는 약간 변형해서 사용한다.

## 템플릿

산출물 작성 시 `assets/templates/` 의 템플릿을 베이스로 사용한다.

| 산출물 | 템플릿 |
|---|---|
| 단계별 plan (checkbox) | `assets/templates/plan_template.md` |
| User Story | `assets/templates/user_story_template.md` |
| Unit 정의 | `assets/templates/unit_template.md` |
| PRFAQ | `assets/templates/prfaq_template.md` |
| NFR 정의 | `assets/templates/nfr_template.md` |
| ADR | `assets/templates/adr_template.md` |
| Domain Model | `assets/templates/domain_model_template.md` |
| Logical Design | `assets/templates/logical_design_template.md` |

## 자주 어기는 함정 (피하기)

- ❌ Plan 없이 바로 코드 생성 → AI-DLC 위반. 반드시 plan-first gate.
- ❌ 한 번에 phase를 건너뛰고 코드만 짜기 → loss function 작동 안 함, 품질 붕괴.
- ❌ 4주짜리 일정으로 나눠서 schedule하기 → Bolt(시간/일)로 잘게 쪼갠다.
- ❌ artefact를 chat에만 남기고 파일로 안 떨어뜨리기 → traceability와 context memory가 깨진다.
- ❌ 사용자 확인 없이 critical decision(아키텍처 패턴 선택, NFR trade-off, 도메인 경계 등) 단독 결정.

## 빠른 참조 흐름도

```
Intent
  └→ Level 1 Plan (사람 승인)
       └→ [Inception]
             ├ AI가 user stories/NFR/risks 생성
             ├ AI가 cohesive Unit으로 묶음
             ├ Product Owner validation
             └ PRFAQ / Bolt 후보 제안
       └→ [Construction] per Unit
             ├ Domain Model (DDD) → 사람 review
             ├ Logical Design + ADR → 사람 approve
             ├ Code + Unit Test 생성 → 사람 review
             └ Deployment Unit 패키징
       └→ [Operations]
             ├ Deploy 승인
             ├ Observability + anomaly detection
             └ Runbook 기반 mitigation 승인
  └→ Bolt closeout & 다음 Bolt 제안
```

언제든지 사용자가 phase를 명시적으로 건너뛰겠다고 하면 plan에 그 결정 사유를 기록하고 진행한다 — 사람의 oversight가 우선이다.
