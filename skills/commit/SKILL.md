---
name: skillframe:commit
description: skillframe 저장소의 `skills/commit` 경로에 있는 개인용 한국어 커밋 워크플로우. 사용자가 명시적으로 "$skillframe:commit", "/commit", "$commit", "skillframe:commit", 또는 "/skillframe:commit"이라고 요청했을 때 이 스킬을 skillframe의 commit 스킬로 인지하고 사용한다. 현재 git 변경사항을 리뷰어가 이해하기 쉬운 커밋 단위로 나누고, 브랜치에서 JIRA 티켓을 추론해 한국어 Conventional Commit 메시지로 실제 커밋한다. 일반적인 "커밋해줘", "커밋 메시지 작성해줘" 요청에는 다른 커밋 스킬과 충돌하지 않도록 이 스킬을 자동 사용하지 않는다.
---

# Skillframe: Commit

리뷰어가 쉽게 이해할 수 있도록 변경사항을 원자적인 커밋 단위로 나누고,
간결한 한국어 Conventional Commit 메시지로 커밋한다.

이 스킬은 사용자가 `$skillframe:commit`, `/commit`, `skillframe:commit`,
`/skillframe:commit`, 또는 `$commit`을 명시했을 때 사용한다. `/commit`과
`$commit`은
"skillframe의 commit 스킬"을 뜻하는 개인 호출 문구로 해석한다.
일반적인 자연어 커밋 요청에는 자동으로 끼어들지 않는다.

사용자가 커밋을 요청한 경우 이 스킬은 변경사항을 stage하고 `git commit`을
실행할 수 있다. 단, 사용자가 명시적으로 요청하지 않는 한 히스토리를
재작성하지 않고, 관련 없는 사용자 변경사항은 보존한다.

## 스킬 식별

- 설치 경로: `skills/commit/`
- 스킬 이름: `skillframe:commit`
- 컨텍스트: `skillframe`
- 호출 해석: `$skillframe:commit`을 기본 호출명으로 사용한다. `/commit` 또는
  `$commit`으로 호출된 경우에도 이 스킬을 "skillframe commit"으로 식별한다.

## 기본 동작

- 커밋 메시지는 기본적으로 한국어로 작성한다.
- Conventional Commit의 type과 선택적 scope를 사용한다.
- 현재 브랜치에서 JIRA 티켓을 추론할 수 있으면 메시지에 포함한다.
- 리뷰어가 독립적으로 이해할 수 있는 단위로 커밋을 나눈다.
- body는 범위, 위험, 마이그레이션, 트레이드오프 설명이 필요할 때만 추가한다.

## 작업 흐름

1. 저장소 상태를 확인한다.
   - `git status --short`를 실행한다.
   - `git branch --show-current`를 실행한다.
   - `git diff --cached`와 `git diff`를 분리해서 읽는다.
   - staged 변경과 unstaged 변경은 같은 의도라고 확신하기 전까지 분리해서
     판단한다.

2. 브랜치 메타데이터를 추론한다.
   - 브랜치의 첫 경로 조각이 허용된 type이면 커밋 type 후보로 사용한다.
   - 브랜치에서 `[A-Z][A-Z0-9]+-[0-9]+` 형태의 JIRA 티켓을 추출한다.
   - 예시:
     - `feat/PE-77-visit-log-form` -> type `feat`, ticket `PE-77`
     - `fix/PROJ-123-login-session` -> type `fix`, ticket `PROJ-123`
     - `feature/login-session` -> ticket 없음, diff 기준으로 type 추론
   - JIRA 티켓이 없어도 멈추지 않는다. 메시지에서 ticket만 생략한다.

3. 리뷰어 친화적인 커밋 단위로 나눈다.
   - 하나의 커밋에는 하나의 기능, 버그 수정, 리팩터링, 테스트, 문서, 유지보수
     변경만 담는 것을 선호한다.
   - 모델이나 entity 변경은 컴파일에 필요한 직접 호출부와 함께 묶는다.
   - 테스트는 검증하는 동작과 함께 묶되, 광범위한 테스트 정리만 따로 분리한다.
   - frontend/backend, 동작 변경/리팩터링, 생성 파일/수동 파일, 정리/기능 변경은
     서로 관련이 약하면 분리한다.
   - 한 파일 안에 무관한 hunk가 섞여 있으면 hunk 단위로 stage한다.
   - hunk 분리가 위험하거나 의도가 애매하면 커밋하기 전에 사용자에게 묻는다.

4. 사용자가 커밋을 요청했으면 실행한다.
   - 현재 커밋 단위에 속한 파일이나 hunk만 stage한다.
   - 관련 없는 staged 변경사항은 건드리지 않는다.
   - 커밋 단위마다 `git commit`을 한 번씩 실행한다.
   - 각 커밋 후 `git status --short`로 남은 변경사항을 확인한다.
   - 최종 보고에는 커밋 해시와 남은 staged, unstaged 변경사항을 포함한다.

5. 사용자가 메시지나 커밋 단위 제안만 요청했으면 커밋하지 않는다.
   - 제안 커밋 단위와 정확한 메시지를 제공한다.
   - 애매한 부분은 짧게 짚는다.

## 메시지 형식

JIRA 티켓이 있는 경우:

```text
<type>(<scope>): <TICKET>, <한국어 요약>
```

JIRA 티켓이 없는 경우:

```text
<type>(<scope>): <한국어 요약>
```

scope는 선택 사항이다. 리뷰어가 변경 범위를 예측하는 데 도움이 될 때만 사용한다.
유용한 scope가 없으면 생략한다.

```text
feat: PE-77, 방문록 등록 흐름 추가
fix: 로그인 세션 유지
```

## Type 규칙

허용되는 type:

- `feat`: 새 기능, 새 화면, 새 API, 새 사용자 흐름
- `fix`: 버그 수정, 잘못된 동작 보정
- `refactor`: 의도한 동작 변화 없는 구조 개선
- `perf`: 성능 개선
- `docs`: 문서만 변경
- `test`: 테스트만 변경
- `chore`: 제품 동작과 무관한 유지보수
- `build`: 빌드, 패키지, 의존성 변경
- `ci`: CI, 배포 자동화 변경
- `style`: 포맷팅만 변경
- `revert`: 이전 변경 되돌림

브랜치 type과 diff의 실제 성격이 다르면 diff를 우선한다. 이 경우 최종 보고에서
브랜치와 커밋 type이 달랐다는 점을 짧게 언급한다.

## 한국어 요약 규칙

- 요약은 직접적이고 리뷰어가 바로 이해할 수 있게 쓴다.
- 완전한 문장보다 명사형과 간결한 동작 표현을 선호한다.
- `tRPC hooks`, `entity`, `schema`, `resolver`, `middleware`처럼 영어가 더 명확한
  기술 용어는 영어로 유지한다.
- `작업`, `수정`, `변경사항 정리`, `기능 개선`처럼 모호한 표현은 피한다.
- 리뷰어가 메시지만 보고 diff의 방향을 예측할 수 있을 만큼 구체적으로 쓴다.
- 마침표를 붙이지 않는다.

좋은 예시:

```text
feat(visit-log-template): tRPC hooks entity 추가
feat(frontend): PE-77, 방문록 화면과 등록 폼 기반 편집 흐름 구현
fix(auth): PROJ-123, 로그인 세션 유지
refactor(api): 방문록 템플릿 resolver 분리
test(visit-log): 방문록 등록 실패 케이스 보강
```

약한 예시:

```text
feat(frontend): PE-77, 화면 작업
fix(auth): 버그 수정
chore: 변경사항 정리
```

## Body 규칙

기본적으로 body는 생략한다.

다음처럼 리뷰에 실질적으로 도움이 될 때만 body를 추가한다.

- 의도가 diff만으로 분명하지 않은 이유나 트레이드오프
- 마이그레이션 또는 배포 주의사항
- breaking change
- 보안상 민감한 동작
- revert 맥락
- 더 이상 쪼개기 어려운 큰 커밋의 범위 설명

body는 한국어로 작성한다. 한 줄은 대략 72자 안팎으로 유지한다. bullet은 스캔이
쉬워질 때만 사용한다.

breaking change가 있으면 다음 형식을 사용한다.

```text
BREAKING CHANGE: <한국어 설명>
```

## 커밋 후 최종 보고

커밋을 생성한 뒤에는 다음을 간결하게 보고한다.

- 각 커밋의 해시와 subject
- 브랜치 type과 실제 diff type이 달랐던 경우
- 남은 staged 또는 unstaged 변경사항
- 실행한 테스트나 검증 명령
