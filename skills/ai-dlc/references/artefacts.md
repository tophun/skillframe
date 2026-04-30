# AI-DLC Artefact 정의

AI-DLC의 모든 산출물은 markdown으로 보관되어 AI의 "context memory"를 구성한다. 각 artefact는 backward/forward traceability를 가져야 한다 (예: domain model element ↔ user story ↔ unit ↔ intent).

---

## Intent
**무엇**: 달성하고자 하는 high-level statement of purpose. business goal, feature, technical outcome(예: performance scaling) 어떤 형태든 가능.

**역할**: AI 주도 decomposition의 starting point. human objective와 AI-generated plan을 정렬한다.

**저장 위치**: `aidlc-docs/requirements/intent.md`

**예**: "Develop a recommendation engine for cross-selling products."

---

## Unit
**무엇**: Intent에서 도출된 cohesive, self-contained work element. measurable value를 전달하도록 설계된다. DDD의 **Subdomain**, Scrum의 **Epic**과 유비된다.

**특성**:
- loosely coupled (다른 Unit과 독립)
- autonomous development & independent deployment 가능
- user story 모음으로 구성됨 (functional scope를 articulate)

**Decomposition 책임**: AI가 분해, developer/Product Owner가 validate/refine.

**저장 위치**: `aidlc-docs/units/<unit_name>.md` (각 Unit별 1파일)

**예**: 위 intent를 다음 Unit으로 분해 — `User Data Collection`, `Recommendation Algorithm Selection`, `API Integration`

---

## Bolt
**무엇**: AI-DLC의 가장 작은 iteration. Scrum의 Sprint와 유비되지만 **시간/일 단위**의 intense cycle.

**특성**:
- Unit 또는 Unit 내 task 묶음을 빠르게 build & validate
- 한 Unit은 1개 또는 여러 Bolt로 실행될 수 있고, 병렬/순차 모두 가능
- AI가 Bolt 계획을 제안, developer/Product Owner가 validate

**저장 위치**: `aidlc-docs/plans/bolts/<bolt_id>.md`

**왜 Sprint를 안 쓰나**: 4~6주 호흡은 AI 속도와 맞지 않다. Bolt는 "rapid, intense cycle"임을 이름으로 강조한다.

---

## Domain Design
**무엇**: Unit의 **core business logic**을 인프라 컴포넌트와 독립적으로 모델링한 것.

**구성**: AI가 DDD principle로 strategic + tactical modelling element 생성:
- Aggregate
- Value Object
- Entity
- Domain Event
- Repository
- Factory

**저장 위치**: `aidlc-docs/design-artifacts/domain/<unit>_domain.md`

**brown-field 추가**: 기존 코드가 있으면 먼저 reverse engineering으로 static model(컴포넌트·책임·관계) + dynamic model(주요 use case의 컴포넌트 상호작용) 추출 후 위로 끌어올린다.

---

## Logical Design
**무엇**: Domain Design을 NFR과 architectural design pattern으로 확장한 것.

**적용 패턴 예시**: CQRS, Circuit Breaker, Event-Driven, Saga, Outbox 등.

**산출물 동반**: 각 주요 결정에 대한 **Architecture Decision Record (ADR)**. developer가 review/approve.

**저장 위치**: `aidlc-docs/design-artifacts/logical/<unit>_logical.md`, ADR은 `aidlc-docs/design-artifacts/adr/ADR-<NNNN>-<slug>.md`

---

## Code & Unit Tests
**무엇**: Logical Design을 입력으로 AI가 생성한 실행 가능한 코드와 unit test.

**선택**: 적절한 AWS service / construct 매핑(예: DynamoDB, Lambda, EventBridge 등)을 well-architected principle 기준으로 선택.

**검증**: AI agent가 unit test를 실행, 결과 분석, fix recommendation을 developer에게 제공.

**저장 위치**: 일반 source tree (예: 프로젝트 루트의 `src/`, `tests/`). 단, 본 스킬은 폴더 구조를 강제하지 않으며 사용자가 사용하는 stack의 관습을 따른다.

---

## Deployment Unit
**무엇**: 운영 환경에서 실행 가능한 **packaged operational artefact**.

**구성 요소**:
- 패키징된 실행 코드 (예: container image, AWS Lambda zip)
- configuration (예: Helm chart, parameter store entry)
- infrastructure component (예: Terraform, CloudFormation, CDK stack)
- 동반 테스트: functional, static/dynamic security, load test scenario

**검증**: AI가 test suite 실행, 결과 분석, code change/configuration/dependency와 failure point를 correlate. 사람의 validation/test 시나리오 보정 후 진행.

**저장 위치**: `aidlc-docs/deployment/<unit>/manifest.md` + 실제 IaC 파일들

---

## 보조 Artefact

| Artefact | 위치 | 메모 |
|---|---|---|
| User Story | `aidlc-docs/story-artifacts/<unit>/<story>.md` | acceptance criteria 포함, INVEST 원칙 |
| PRFAQ | `aidlc-docs/requirements/<unit>_prfaq.md` | 선택 산출물, business intent + 기능 + 기대 benefit 요약 |
| NFR 정의 | `aidlc-docs/risks/nfr.md` | scalability, availability, performance, security, observability 등 |
| Risk Description | `aidlc-docs/risks/risk_register.md` | 조직의 risk register와 매칭 |
| Measurement Criteria | `aidlc-docs/requirements/measurement.md` | business intent로 traceable |
| ADR | `aidlc-docs/design-artifacts/adr/ADR-NNNN-*.md` | major decision 1개당 1파일 |
| Test Plan / Result | `aidlc-docs/tests/` | 시나리오, 케이스, 결과, 회귀 |
| Validation Report | `aidlc-docs/tests/validation_report.md` | 인프라 코드 검증 등 |
| Runbook | `aidlc-docs/operations/runbook/<scenario>.md` | observability + incident 대응 |
| Plan (단계별) | `aidlc-docs/plans/<task>_plan.md` | checkbox 기반, 모든 단계의 시작점 |
| Prompts log | `aidlc-docs/prompts.md` | 세션에서 사용된 표준 prompt 누적 |

---

## Traceability 규칙

각 artefact는 상위/하위 artefact와의 관계를 frontmatter나 본문 상단에 명시한다.

```markdown
---
artefact_type: user_story
id: US-CART-007
unit: shopping-cart
intent: storefront-revamp
linked_domain_elements:
  - aggregate: Cart
  - entity: CartItem
linked_adrs: [ADR-0014]
---
```

이 메타데이터로 AI가 이후 단계에서 정확한 context를 retrieve한다.
