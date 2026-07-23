---
name: skillframe-code-review
description: GitHub PR 링크나 번호와 함께 코드리뷰, PR 리뷰, 리뷰해줘, review this PR를 요청할 때 사용한다. diff를 먼저 분석하고 검증된 이슈만 대기 중인 GitHub 인라인 리뷰 초안으로 작성하며 자동 제출하지 않는다. PR 생성·본문 수정·merge·label·reviewer 변경에는 사용하지 않는다.
---

# Skillframe Codex: Code Review

GitHub PR을 변경 라인 중심으로 검토하고, 재현 가능하거나 근거가 충분한 문제만
대기 중인 인라인 리뷰 초안으로 남긴다. 사람을 평가하지 않고 구현의 정확성, 보안,
데이터 손실, 사용자 영향, 유지보수성, 테스트 위험을 우선한다.

## 범위

사용한다:

- PR 링크 또는 번호와 함께 `코드리뷰`, `리뷰해줘`, `PR 리뷰`, `review this PR`
- `$skillframe-code-review`

사용하지 않는다:

- PR 생성·본문 수정 → `skillframe-create-pull-request`
- 커밋·push·merge
- label, reviewer, milestone, project 변경

## 반드시 지키는 규칙

1. 리뷰를 시작할 때 `skillframe-code-review-context`의 절차를 적용한다.
2. 항상 diff를 먼저 보고, 리뷰하지 않은 코드의 문제를 PR 이슈로 올리지 않는다.
3. 실제 문제로 확인된 `MUST`·`SHOULD` 수준만 남긴다. 스타일 취향은 제외한다.
4. 코멘트는 짧고 직접적으로 쓴다. 무엇이 문제인지, 왜 문제가 되는지, 가장 작은
   수정 방향을 함께 적는다.
5. 수정할 수 있고 안전한 경우에만 `suggestion` 블록을 붙인다.
6. 한국어 코멘트는 게시 전에 사용 가능한 `$humanize-korean` 스킬로 윤문한다. 해당
   스킬이 없으면 식별자·숫자·경로·인용·코드 블록은 보존한 채 직접 간결하게 다듬는다.
7. 모든 코멘트를 로컬에서 먼저 모은다. 게시할 때는 하나의 `PENDING` 리뷰에 인라인
   코멘트만 넣는다.
8. 리뷰를 자동 제출하지 않는다. 사용자가 명시적으로 요청한 경우에만 제출한다.
9. 최상위 리뷰 요약, 일반 PR 코멘트, 별도 상단 코멘트를 남기지 않는다.

## 워크플로우

### 1. 적격성 확인

```bash
gh --version
gh auth status
gh pr view <pr> --repo <owner/repo> \
  --json number,url,state,isDraft,mergedAt,closed,headRefOid,baseRefName,headRefName
gh api repos/<owner>/<repo>/pulls/<number>/comments --paginate
```

다음이면 새 리뷰를 만들지 않고 중단한다.

- PR이 closed 또는 merged 상태
- draft PR인 경우, 사용자가 draft 리뷰를 명시적으로 요청하지 않음
- 같은 head 커밋에 이미 동일 리뷰어의 중복 코멘트가 있음
- PR 대상과 저장소를 확인할 수 없음

### 2. 컨텍스트 수집

`skillframe-code-review-context`를 사용해 다음을 확인한다.

```bash
gh pr diff <pr> --repo <owner/repo>
gh pr view <pr> --repo <owner/repo> --json files,commits
```

저장소의 `AGENTS.md`, `CONTRIBUTING.md`, PR 템플릿과 관련 테스트를 읽는다. 변경이
공유 계약·모듈 경계·보안·데이터·동시성 경로를 건드릴 때만 caller, callee, 구현체,
소비자, 관련 테스트까지 확장한다. codegraph가 없거나 stale하면 수동 탐색으로
계속하고 제한 사항을 기록한다.

### 3. 리뷰 패스

변경된 라인을 기준으로 다음 관점에서 독립적으로 확인한다.

- 입력 검증, 권한 확인, 민감 데이터 노출
- null·빈 값·경계값·오류 경로와 예외 처리
- 상태 전이, 중복 실행, retry·transaction·concurrency
- API·이벤트·serializer·migration·설정 계약의 호환성
- 변경된 동작의 직접 호출자와 관련 회귀 테스트
- 저장소 지침과 기존 구현의 불변식

각 후보에 대해 `references/scoring-rubric.md`로 신뢰도를 판단한다. 80점 미만,
기존 문제, 추측성 문제, 변경되지 않은 라인의 문제는 제외한다.

### 4. 코멘트 작성

각 코멘트는 다음 순서를 따른다.

1. 무엇이 문제인가
2. 어떤 입력·실행 경로에서 문제가 발생하는가
3. 사용자 영향은 무엇인가
4. 가장 작은 수정 방향은 무엇인가

예:

```text
이 분기에서는 `items`가 빈 배열일 때도 첫 항목에 접근합니다. 검색 결과가 없으면
런타임 오류가 발생해 요청 전체가 실패할 수 있으니, 접근 전에 빈 결과를 처리하면
좋겠습니다.
```

suggestion을 만들 때는 PR head의 정확한 코드와 들여쓰기를 확인한다.

```bash
git show <head-sha>:<path> | sed -n '<start>,<end>p'
```

### 5. 대기 중인 리뷰 초안 작성

후보를 모두 검토하고 코멘트 문장을 윤문한 뒤 `references/pending-review-recipe.md`에
따라 `payload.json`을 만든다. 최상위 `body` 없이 인라인 `comments`만 포함한다.

```bash
gh api -X POST repos/<owner>/<repo>/pulls/<number>/reviews \
  --input payload.json
```

생성 결과가 `PENDING`인지 확인한다. 자동으로 `COMMENT`, `APPROVE`,
`REQUEST_CHANGES` 상태로 제출하지 않는다.

### 6. 결과 보고

사용자에게는 다음만 간결하게 보고한다.

- 대기 중인 리뷰 초안이 작성되었는지
- 코멘트 수와 각 코멘트의 파일·라인
- 실행한 테스트와 실행하지 못한 테스트
- codegraph 상태와 중요한 제한 사항

리뷰 요약을 GitHub PR에 남기지는 않지만, 대화에서 사용자가 확인할 수 있도록 필요한
범위의 결과를 보고할 수 있다.
