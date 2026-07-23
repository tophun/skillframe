---
name: skillframe-code-review-context
description: PR 또는 커밋 리뷰에서 diff를 출발점으로 변경 영향 범위와 관련 테스트를 좁혀 파악한다. 공유 API, 모듈 경계, 보안·데이터·동시성 경로를 건드린 변경에 사용하며 codegraph가 없으면 수동 탐색으로 계속한다.
---

# Skillframe Codex: Code Review Context

코드리뷰에 필요한 맥락만 단계적으로 수집한다. 저장소 전체를 읽는 것이 목적이
아니라, 변경된 코드의 동작과 영향 범위를 판단할 수 있는 최소한의 근거를 만드는
것이 목적이다.

## 기본 원칙

1. 항상 diff부터 읽는다.
2. 변경이 모듈 경계를 넘거나 공유 계약을 바꿀 때만 탐색 범위를 넓힌다.
3. codegraph는 영향 범위를 찾는 보조 수단이지 런타임 동작의 증명이 아니다.
4. 그래프가 없거나 부정확하면 repository search, 언어 도구, 빌드 설정, 테스트를
   이용한 수동 탐색으로 계속한다.

## 절차

### 1. 리뷰 대상 확정

- 저장소 루트, base 커밋, head 커밋, 리뷰 대상(PR 또는 커밋)을 확인한다.
- `AGENTS.md`, `CONTRIBUTING.md`, PR 템플릿, 리뷰 규칙을 먼저 찾는다.
- diff를 읽고 변경 파일, 심볼, public interface, 설정·마이그레이션, 테스트를
  목록화한다.

PR이라면 다음 정보를 우선 수집한다.

```bash
gh pr view <pr> --repo <owner/repo> --json number,url,state,isDraft,mergedAt,headRefOid,baseRefName,headRefName
gh pr diff <pr> --repo <owner/repo>
```

### 2. 필요한 깊이 선택

- **로컬 변경:** 변경 파일, 인접 helper, 직접 호출자, 직접 테스트
- **모듈 변경:** 모듈 경계, public contract, 호출자·구현체·오류 경로·관련 테스트
- **고위험 또는 cross-cutting 변경:** 데이터 흐름, 권한·검증 경계, persistence/API/event,
  외부 side effect, 실패 복구, 관련 소비자와 테스트

변경과 관계없는 전체 그래프나 파일을 읽지 않는다.

### 3. codegraph 조건부 사용

codegraph를 사용하기 전 저장소 문서와 CLI 도움말로 실제 명령을 확인한다. 문서와
도구가 없다면 아래 수동 탐색으로 대체한다.

- 초기화되지 않았거나 그래프 메타데이터가 없을 때만 `init`한다.
- checkout·merge 이후 현재 커밋에 맞는 index가 없을 때만 `index`한다.
- 변경된 심볼의 caller, callee, 구현체, import 소비자, 관련 테스트만 조회한다.
- 보통 깊이 2~3에서 멈추고, 경계가 드러날 때만 확장한다.
- generated, vendored, 무관한 third-party 코드는 제외한다.

codegraph 상태를 `reused`, `initialized`, `indexed`, `unavailable`, `stale`,
`incomplete` 중 하나로 기록한다.

### 4. 맥락 검증

각 변경 동작에 대해 다음을 확인한다.

- 호출자는 변경된 코드에 어떤 전제를 두는가?
- 구현체·adapter·serializer가 계약과 호환되는가?
- validation, authorization, error handling, retry, transaction, cache, concurrency,
  side effect가 바뀌었는가?
- 성공·실패·경계·회귀 테스트가 있는가?
- dynamic dispatch, reflection, dependency injection, code generation, runtime config가
  정적 탐색에 빠졌을 가능성이 있는가?

### 5. 리뷰어에게 넘길 요약

최종 리뷰에는 필요한 만큼만 다음을 기록한다.

1. 확인한 범위와 그 범위가 충분하다고 판단한 이유
2. codegraph 상태와 제한 사항
3. 중요한 비정적 경로
4. 실행한 테스트와 실행하지 못한 테스트

발견 사항마다 정확한 파일·라인, 관찰 가능한 영향, 근거, 가장 작은 수정 방향을
붙인다.
