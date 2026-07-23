# code-review

GitHub PR을 다단계 에이전트로 리뷰하고, 검증된 이슈만 **해당 코드 라인에 인라인 코멘트 + 코드 제안(suggestion)** 으로 남기는 Claude Code 플러그인.

## 특징

- 최상단 일반 코멘트가 아니라 **인라인 리뷰 코멘트**(`gh api .../pulls/{n}/reviews`)
- 고칠 수 있는 이슈엔 ` ```suggestion ` 블록을 붙여 `Commit suggestion` 한 번으로 반영
- 코멘트 문장은 `humanize-korean` 플러그인으로 윤문해 읽기 쉽게
- 게시 전 사용자 승인, 신뢰도 80점 이상만 게시

## 의존

`humanize-korean` 플러그인(같은 마켓플레이스)이 필요하다.

## 설치

```text
/plugin marketplace add tophun/skillframe
/plugin install humanize-korean@skillframe
/plugin install code-review@skillframe
```

## 사용

PR 링크와 함께 "코드리뷰", "리뷰해줘", `/code-review`, `$code-review`.
