# Construction Phase — Mob Programming / Mob Testing / Mob Construction

Construction Phase는 Inception에서 정의된 Unit을 **tested, operations-ready Deployment Unit**으로 변환한다. 흐름:

```
Domain Design → Logical Design (+ ADR) → Code & Unit Test → Test Execution → Deployment Unit
```

ritual은 mob을 한 방에 모으고(본 세션 컨텍스트에서는 conversation 자체) AI가 task를 추천하고 option을 제시하는 형태로 흐른다 — design pattern, UX, test 등.

---

## 0. 진입 조건

- 해당 Unit의 Inception artefact (user story, NFR, risk, measurement) 존재
- Level 1 Plan이 승인됨
- Bolt 단위로 어디까지 build할지 합의됨

## 1. (Brown-Field 한정) Reverse Engineering

기존 시스템에 변경을 가하는 경우 먼저 코드를 **semantically rich modelling representation**으로 끌어올린다. AI가 두 모델을 추출:
- **Static Model** — 컴포넌트, description, responsibility, 관계
- **Dynamic Model** — 가장 중요한 use case들에서 컴포넌트가 어떻게 상호작용하는지 (sequence, message flow)

Developer + Product Manager가 함께 review/validate/correct. 이 단계가 끝나야 green-field 흐름과 동일하게 진행 가능.

저장 위치: `aidlc-docs/design-artifacts/reverse/<area>_static.md`, `..._dynamic.md`

## 2. Domain Design (Mob Programming)

**목적**: Unit의 core business logic을 인프라 독립적으로 모델링.

**기법**: DDD tactical/strategic modelling.

**산출 요소**:
- Aggregate (예: `Order` aggregate root with `OrderLine` entities)
- Value Object (예: `Money`, `Address`)
- Entity (예: `Customer`, `Product`)
- Domain Event (예: `OrderPlaced`, `PaymentFailed`)
- Repository (aggregate별)
- Factory (복잡한 생성 로직)

**예 (Recommendation Algorithm Unit)**:
- Entity: `Product`, `Customer`, `PurchaseHistory`
- Aggregate: `RecommendationContext` aggregating purchase history + inventory window
- Domain Event: `RecommendationGenerated`

**Developer review**: 비즈니스 룰의 누락/오해석을 잡아낸다. 예: "신규 고객은 purchase history가 없는데 어떻게 다룰지" 같은 missing case.

**저장 위치**: `aidlc-docs/design-artifacts/domain/<unit>_domain.md` (`assets/templates/domain_model_template.md` 사용)

**표준 프롬프트**: `prompts-library.md`의 `## Domain (component) model creation` 섹션.

## 3. Logical Design (+ ADR)

**목적**: Domain Design에 NFR과 architectural pattern을 입혀 구현 가능한 청사진 생성.

**고려할 패턴 예시**:
- 데이터 분리: CQRS, Event Sourcing
- 신뢰성: Circuit Breaker, Bulkhead, Retry with backoff
- 통신: Event-Driven (EventBridge/SNS/SQS), Saga, Outbox
- 일관성: Strong vs Eventual, Idempotency Key
- 캐싱: Read-through, Write-through, Cache-aside

**AWS service 선택 기준**: well-architected principle (operational excellence, security, reliability, performance, cost, sustainability) 기준으로 매핑. 예시:
- 서버리스 컴퓨팅 → AWS Lambda / Step Functions
- 이벤트 라우팅 → Amazon EventBridge / SNS / SQS
- KV 저장 → Amazon DynamoDB
- 검색 → Amazon OpenSearch
- 추론 → Amazon Bedrock

**ADR 작성**: 모든 major decision에는 1개 ADR. 형식은 `assets/templates/adr_template.md`. Developer가 review하고 trade-off 명시. 예: "Lambda 채택 — scalability 우선. Storage는 query latency 위해 RDS가 아닌 DynamoDB로 override."

**저장 위치**:
- Logical Design: `aidlc-docs/design-artifacts/logical/<unit>_logical.md`
- ADR: `aidlc-docs/design-artifacts/adr/ADR-NNNN-<slug>.md`

## 4. Code & Unit Test 생성

**기준**:
- Logical Design을 입력으로 AI가 코드 + unit test 생성
- well-architected principle 준수
- domain layer는 인프라 의존 없이 작성 (hexagonal/ports-and-adapters)
- 클래스/모듈은 cohesive하게 분리, 한 파일 한 책임

**프로세스**:
1. AI가 generation plan을 `aidlc-docs/plans/<unit>_codegen_plan.md`로 작성
2. 사용자 승인
3. step-by-step 생성, step마다 plan 체크박스 갱신
4. AI가 unit test 실행
5. 결과 분석 및 fix recommendation 제시
6. Developer review → fix 승인 → 재실행

**예** (Recommendation Algorithm Unit):
- `recommendation/` 모듈에 collaborative filtering 구현
- DynamoDB data source 연결
- functional test, security test, performance test 자동 생성

**표준 프롬프트**: `prompts-library.md`의 `## Code Generation` 섹션.

## 5. Mob Testing — Testing & Validation

**활동**:
- AI가 **functional / security / performance** test를 모두 실행
- 결과 분석, issue highlight
- 실패 케이스에 대한 fix 제안 (예: query plan 최적화, retry 추가)
- Developer가 finding/fix를 validate, approve, rerun

**저장**:
- 테스트 plan: `aidlc-docs/tests/<unit>_test_plan.md`
- 결과: `aidlc-docs/tests/<unit>_result_<timestamp>.md`
- validation report: `aidlc-docs/tests/validation_report.md`

## 6. Mob Construction (Cross-Unit Integration)

여러 Unit이 동시에 build될 때 한 방에 모여 진행하는 ritual. 핵심 활동:
- Domain Model 단계에서 도출된 **integration specification** 교환
- inter-Unit 결정 (event schema 합의, API contract, idempotency 정책)
- 각 Unit이 자기 Bolt를 deliver

본 세션 컨텍스트에서는 사용자가 여러 Unit을 동시에 진행 중일 때 AI가 자발적으로 cross-Unit consistency를 점검해야 한다 (예: 같은 Domain Event 이름이 두 Unit에서 다르게 정의됐는지).

## 7. Deployment Unit 패키징

**구성**:
- 실행 가능한 코드 (container image, Lambda artefact)
- configuration (Helm chart, parameter store)
- IaC (Terraform / CDK / CloudFormation)
- 동반 테스트: functional, static & dynamic security, load test

**검증**:
- AI가 test suite 실행
- failure point ↔ code change/configuration/dependency 상관 분석
- functional acceptance, security compliance, NFR adherence, operational risk 모두 통과해야 다음 phase로

**저장 위치**: `aidlc-docs/deployment/<unit>/manifest.md` + IaC 파일

**표준 프롬프트**: `prompts-library.md`의 `## Architecture`, `## Build IaC/Rest APIs` 섹션.

---

## 완료 조건 (Definition of Done for Construction)

- [ ] (brown-field) static + dynamic model이 추출/검증됨
- [ ] Domain Model이 작성, developer 검증됨
- [ ] Logical Design 작성, ADR 모두 review/approve됨
- [ ] Code 생성, unit test 작성, 실행 통과
- [ ] functional / security / performance 테스트 결과가 기록됨
- [ ] Deployment Unit 패키징 완료, IaC 검증됨
- [ ] 모든 산출물의 traceability(domain element ↔ user story ↔ ADR) 갱신됨
- [ ] 사용자 명시적 승인이 plan에 기록됨

---

## 함정 회피

- ❌ Domain Model을 건너뛰고 Logical Design부터 시작 → 비즈니스 룰이 인프라에 종속되어 변경 비용 폭증
- ❌ ADR을 사후작성 (코드 작성 후 정당화) → 결정 과정의 trade-off가 보존되지 않는다
- ❌ unit test를 AI 생성물에 대해서만 작성, integration 시나리오 누락 → Mob Testing 단계의 functional test로 보완
- ❌ AWS service 선택을 hand-waving (왜 Lambda인지 모호함) → ADR로 강제 명문화
- ❌ brown-field에서 reverse engineering 생략 → AI가 잘못된 mental model로 변경을 가하게 됨
