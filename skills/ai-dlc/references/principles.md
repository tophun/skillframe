# AI-DLC 핵심 원칙 (10가지)

이 원칙들은 AI-DLC의 phase, role, artefact, ritual을 정의하는 토대다. 메서드를 변형/적용할 때 반드시 이 원칙에 비추어 검토한다.

## 1. Reimagine rather than Retrofit
기존 SDLC/Agile에 AI를 끼워 맞추지 않는다. 전통적 방법론은 월/주 단위 iteration을 전제로 daily standup, retrospective, story point 같은 ritual을 만들었다. AI 주도 개발은 시간/일 단위 cycle이라 real-time validation이 필요하고, velocity 같은 지표는 business value로 대체되는 게 적절하다.

**적용**: 새 워크플로우를 설계할 때 "기존에 그랬으니까"를 근거로 단계를 남기지 않는다. AI 속도/유연성/agentic capability에 맞춰 재구성한다.

## 2. Reverse the Conversation Direction
AI가 먼저 conversation을 시작하고 사람이 approver가 된다. 사람이 task별로 instruction을 던지는 게 아니다. AI가 high-level intent를 받아 actionable task로 쪼개고 trade-off를 제안하면, 사람은 critical junction에서 confirm/select/override한다.

**유비**: Google Maps. 사람은 목적지(intent)만 정하고 시스템이 turn-by-turn direction을 제공, 사람은 oversight 유지.

## 3. Integration of Design Techniques into the Core
Scrum/Kanban이 design technique을 out-of-scope로 둔 것이 품질 문제(2022년 미국에서만 $2.41 trillion 손실)를 키웠다. AI-DLC는 DDD/BDD/TDD 같은 design technique을 메서드의 core에 둔다. 본 스킬은 **DDD flavor**를 기본으로 사용한다.

## 4. Align with AI Capability
현재 AI는 high-level intent를 자율적으로 코드로 옮길 만큼 신뢰할 수 없다. AI-DLC는 AI-Driven paradigm을 채택하되, validation/decision-making/oversight의 ultimate responsibility는 developer에게 둔다.

## 5. Cater to Building Complex Systems
AI-DLC는 functional adaptability, architectural complexity, trade-off, scalability, integration, customization을 동시에 요구하는 시스템을 위한 것이다. 단순 시스템(low-code/no-code 가능)은 적용 범위 밖이다.

## 6. Retain What Enhances Human Symbiosis
기존 메서드의 산출물 중 사람-AI 정렬에 도움 되는 것은 그대로 가져온다. 예: **user story**(사람과 AI가 만들 대상에 합의하는 잘 정의된 contract), **risk register**(조직의 위험 프레임워크 준수). 단, 실시간 사용에 맞게 최적화한다.

## 7. Facilitate Transition through Familiarity
하루 만에 익히고 시작할 수 있어야 한다. 익숙한 용어 관계를 보존하되 modernized terminology를 도입한다. 예: Sprint(4~6주 호흡)를 그대로 쓰지 않고 **Bolt**(시간/일 단위 intense cycle)로 rebrand.

## 8. Streamline Responsibilities for Efficiency
AI가 task decomposition과 decision-making을 담당하므로 developer는 infrastructure / front-end / back-end / DevOps / security 같은 specialization silo를 가로지른다. **Product Owner와 Developer**는 그대로 유지된다(business 정합성, design quality, risk framework 준수). 추가 role은 critically necessary할 때만 도입한다.

## 9. Minimise Stages, Maximise Flow
handoff와 transition을 최소화하고 continuous iterative flow를 추구. 단, AI 산출물이 'quick-cement'(굳어서 변경 어려운 상태)가 되지 않도록 critical decision junction마다 사람 validation을 둔다. 이 validation은 **loss function** 역할로, downstream 낭비를 사전에 잘라낸다.

## 10. No Hard-Wired, Opinionated SDLC Workflows
green-field, brown-field, refactor, defect-fix, microservice scaling 등 pathway별로 정해진 워크플로우를 강요하지 않는다. AI가 pathway에 맞는 Level 1 Plan을 제안하면 사람이 interactive dialogue로 보정하고, Level 2(subtask)로 내려간다. 실행은 AI가, 결과의 verification/validation은 사람이.

---

## 원칙 위반을 발견했을 때

세션 중 다음을 발견하면 즉시 멈추고 보정:
- AI가 plan 없이 코드 생성 시작 → 원칙 9 위반 (loss function 누락)
- 사용자에게 task별 instruction을 받아 따라가는 모드로 빠짐 → 원칙 2 위반
- design technique을 외부 자료로 미루고 코드부터 짜는 흐름 → 원칙 3 위반
- 4주 sprint 단위 일정 산출 → 원칙 7 위반 (Bolt로 변환)
- artefact가 휘발 (chat 안에만 존재) → 원칙 6 위반 (traceability 깨짐)
