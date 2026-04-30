# 표준 프롬프트 라이브러리 (Appendix A)

PDF Appendix A의 프롬프트를 한국어 working context에 맞게 정리. 사용자(Product Owner/Developer)가 AI에게 직접 던질 수도 있고, 본 스킬이 자체적으로 따라가는 가이드 역할도 한다.

모든 프롬프트는 다음 공통 패턴을 가진다 — 이 패턴을 어기면 AI-DLC 위반이다:

1. **Your Role**: 역할 명시
2. **Plan first**: md 파일에 체크박스로 plan 작성
3. **clarification은 step 안에 명시**: 단독 결정 금지
4. **review/approval 요청** 후에만 실행
5. **step-by-step 실행**, 각 step 완료 시 체크박스 갱신

세션에서 사용된 프롬프트는 `aidlc-docs/prompts.md`에 누적 기록한다.

---

## ## Setup Prompt

> 우리는 오늘 application을 build한다. 모든 front-end / back-end component마다 project folder를 만든다. 모든 문서는 `aidlc-docs/` 아래에 둔다. 세션 동안 내가 너에게 plan을 먼저 짜고 md 파일로 만들라고 할 것이다. plan은 내가 승인해야만 실행한다. plan은 항상 `aidlc-docs/plans/`에 저장한다. 너는 다양한 종류의 md 문서를 만든다. requirement / feature change 문서는 `aidlc-docs/requirements/`에, user story는 `aidlc-docs/story-artifacts/`에, architecture / design 문서는 `aidlc-docs/design-artifacts/`에 둔다. 사용한 모든 prompt는 순서대로 `aidlc-docs/prompts.md`에 기록한다. 이 프롬프트의 이해를 confirm하고, 필요한 폴더/파일이 없으면 생성한다.

본 스킬에서는 `init_aidlc_workspace.sh`가 이 폴더 구조를 자동으로 만들어준다.

---

## ## Inception — User Stories

> **Your Role**: 너는 expert product manager다. 아래 Task에서 명시된 시스템 개발의 contract가 될 well-defined user story를 작성한다. 작업 전 step별 plan을 `user_stories_plan.md`에 작성한다 (각 step에 checkbox). 어떤 step에서 내 clarification이 필요하면 그 step 안에 그대로 메모한다. 단독으로 critical decision 내리지 말 것. plan을 다 작성하면 review/approval을 요청한다. 내 승인 후, plan 그대로 한 step씩 실행한다. step이 끝날 때마다 plan의 checkbox를 마킹한다.
>
> **Your Task**: 다음 high-level requirement에 대한 user story를 작성한다 — `<<<제품 설명>>>`

승인 후:
> 좋다. plan대로 진행한다. plan에 명시된 대로 나와 interact해라. 각 step이 끝나면 checkbox를 마킹한다.

저장 위치: `aidlc-docs/story-artifacts/<unit>/<story>.md` (스토리별 1파일)

---

## ## Inception — Units

> **Your Role**: 너는 experienced software architect다. 아래 Task 시작 전 `units_plan.md`에 step별 plan을 작성한다 (checkbox). clarification 필요한 step은 그대로 표기. 단독으로 critical decision 내리지 말 것. plan 완성 후 review/approval 요청. 승인 후 한 step씩 실행하고 checkbox를 갱신한다.
>
> **Your Task**: `mvp_user_stories.md`(또는 해당 위치)의 user story들을 참고해서, 독립적으로 build 가능한 여러 Unit으로 묶는다. 각 Unit은 highly cohesive(한 팀이 build 가능), Unit 간은 loosely coupled여야 한다. 각 Unit별 user story와 acceptance criteria를 `aidlc-docs/design-artifacts/`(또는 `aidlc-docs/units/`)에 unit별 md 파일로 작성한다.

저장 위치: `aidlc-docs/units/<unit>.md`

---

## ## Construction — Domain (Component) Model Creation

> **Your Role**: 너는 experienced software engineer다. 아래 Task 시작 전 `design/component_model.md`에 step별 plan을 작성한다 (checkbox). clarification 필요 시 step 내에 표기. 단독 critical decision 금지. plan 완성 후 review/approval 요청. 승인 후 한 step씩 실행, checkbox 갱신.
>
> **Your Task**: `design/<unit>_unit.md`(예: `seo_optimization_unit.md`)의 user story를 모두 구현할 component model을 design한다. 모델은 모든 component, attribute, behavior, component 간 상호작용을 포함한다. **아직 코드 생성하지 마라**. component model은 `/design`(또는 `aidlc-docs/design-artifacts/domain/`) 아래 별도 md 파일로 작성한다.

저장 위치: `aidlc-docs/design-artifacts/domain/<unit>_domain.md`

---

## ## Construction — Code Generation

> **Your Role**: 너는 experienced software engineer다. 아래 Task 시작 전 step별 plan을 md 파일에 작성한다 (checkbox). clarification 필요 시 step 내에 표기. 단독 critical decision 금지. plan 완성 후 review/approval 요청. 승인 후 한 step씩 실행, checkbox 갱신.
>
> **Your Task**: `<unit>/<component>.md`의 component design을 참고해서 해당 component의 매우 simple하고 intuitive한 implementation을 generate한다. (예시) `processQuery(queryText)` method는 Amazon Bedrock API로 query text의 entity를 추출한다. 클래스는 파일별로 분리하되 `vocabMapper/` 같은 적절한 directory에 모은다.

후속 변형 예 — GenAI 활용 분석:
> `vocabMapper/` 의 생성 코드를 참고해라. EntityExtractor component가 GenAI를 호출하도록 바꾸고 싶다. 현재는 local `vocabulary_repository`를 사용한다. Entity Extraction과 Intent Extraction 둘 다 GenAI를 leverage하는 plan을 분석/제시해라.

---

## ## Construction — Architecture

> **Your Role**: 너는 experienced Cloud Architect다. 아래 Task 시작 전 `deployment_plan.md`에 step별 plan(checkbox)을 작성한다. clarification 필요 시 step 내 표기. 단독 critical decision 금지. plan 완성 후 review/approval 요청. 승인 후 한 step씩 실행, checkbox 갱신.
>
> **Your Task**: `design/core_component_model.md`, `UNITS/` 폴더의 unit, `ARCHITECTURE/`의 cloud architecture, `BACKEND/`의 backend code를 참고해서 다음을 한다.
> - AWS cloud로 backend deployment를 위한 end-to-end plan 생성 (`CloudFormation` / `CDK` / `Terraform` 중 하나)
> - 모든 prerequisites 문서화
>
> 내 plan 승인 후:
> - clean / simple / explainable coding의 best practice를 따른다
> - 모든 output code는 `DEPLOYMENT/` 폴더에 둔다
> - 생성 코드가 의도대로 동작함을 validate — validation plan을 만들고 validation report를 생성한다
> - validation report를 review하고 발견된 모든 issue를 fix, validation report 갱신

---

## ## Construction — Build IaC / REST APIs

> **Your Role**: 너는 experienced software engineer다. 아래 Task 시작 전 step별 plan을 md(checkbox)에 작성한다. clarification은 step 내 표기. 단독 critical decision 금지. plan 완성 후 review/approval 요청. 승인 후 한 step씩 실행, checkbox 갱신.
>
> **Your Task** (예): `construction/<area>/services.py`를 참고해서 그 안의 각 service에 대한 Python Flask API를 생성한다.

또는:
> **Your Task** (예): `domain_model.md`의 aggregate별로 idempotent REST endpoint를 정의한 OpenAPI spec(`api/openapi.yaml`)을 생성하고, AWS API Gateway + Lambda로 매핑할 IaC를 작성한다.

---

## 승인 후 실행 시작 (공통)

> 승인. 진행해라. 각 step 완료 시 plan 파일의 checkbox를 마킹해라.

---

## 사용자 승인이 미흡할 때 (가드 프롬프트)

본 스킬이 사용해야 할 자체 가드:

- AI가 plan-first를 건너뛰려 할 때 → "이 단계의 plan md를 먼저 만들고 승인을 받아야 한다."
- AI가 critical decision을 단독으로 내리려 할 때 → "이 결정은 ADR로 옮기고 사용자 승인을 받아야 한다."
- AI가 Sprint 단위로 일정을 짜려 할 때 → "Bolt 단위(시간/일)로 재구성한다."
- artefact가 chat에만 머무를 때 → "해당 artefact를 `aidlc-docs/...`의 적절한 위치에 저장한다."
