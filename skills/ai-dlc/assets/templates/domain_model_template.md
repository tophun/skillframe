---
artefact_type: domain_model
unit: <unit_name>
bounded_context: <name>
status: draft
linked_user_stories: []
---

# Domain Model: <Unit / Bounded Context>

> infrastructure-independent. AWS service 이름이나 DB 이름이 등장하면 logical design으로 옮긴다.

## Ubiquitous Language
| Term | 정의 |
|---|---|
| <도메인 용어1> | <뜻> |
| <도메인 용어2> | <뜻> |

## Aggregates

### Aggregate: <AggregateRoot>
- 책임:
- invariants (불변조건):
- 포함 entities / value objects:
- 외부에 노출하는 method:
- 발행하는 domain event:

## Entities

### Entity: <Name>
- 식별자: <id>
- 속성:
- 행위:
- 라이프사이클:

## Value Objects

### Value Object: <Name>
- 속성 (immutable):
- 동등성 규칙:

## Domain Events

### Event: <EventName>
- 발생 조건:
- payload:
- consumer 후보:

## Repositories
- `<AggregateRoot>Repository`
  - 메서드: `findById`, `save`, ...

## Factories
- `<AggregateRoot>Factory` — 복잡한 생성 로직이 있는 경우만

## 상호작용 (가장 중요한 use case)

### Use case: <이름>
1. 외부 trigger (user action / scheduled / event)
2. Aggregate에 들어와 어떤 method를 호출
3. 어떤 invariant 검증
4. 어떤 domain event 발행
5. 결과 응답

(시퀀스 다이어그램이 필요하면 mermaid 코드 블록으로 첨부)

## Open Questions for Validation
- <비즈니스 룰의 빈 곳>
- <엣지 케이스 — 예: "신규 고객의 purchase history가 없을 때">
