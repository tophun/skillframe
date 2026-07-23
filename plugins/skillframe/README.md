# skillframe (plugin)

개인용 Git 커밋/PR 흐름 + 코드리뷰 컨텍스트 분석 + 한국어 윤문 Claude Code 플러그인.

## 스킬

| 노출 이름 | 하는 일 |
| --- | --- |
| `skillframe:create-pull-request` | GitHub PR 생성과 기존 PR 본문/draft 보정을 처리. repository template과 말투 규칙을 읽고, `gh pr create/edit/ready` 실행 전 승인 게이트를 연다. |
| `skillframe:code-review` | GitHub PR을 다단계 에이전트로 리뷰하고, 검증된 이슈만 해당 코드 라인에 **인라인 코멘트 + 코드 제안(suggestion)** 으로 게시. 게시 전 승인, 신뢰도 80점 필터. |
| `skillframe:code-review-context` | diff를 기준으로 리뷰 범위를 정하고, 필요할 때 codegraph로 변경 영향의 caller/callee와 관련 테스트를 추적. |
| `skillframe:humanize-korean` | AI가 쓴 한글 텍스트의 AI 티를 탐지·분류해 내용은 그대로 두고 문체만 자연스럽게 윤문. fast/strict 모드. |

## 명령

| 명령 | 하는 일 |
| --- | --- |
| `/commit` | 작업 내용을 공통 작업단위별로 묶어 여러 Git 커밋으로 생성. |
| `/commit-push-pr` | 브랜치 생성(필요한 경우), 커밋, push, Draft PR 생성. 기존 PR 승인 게이트 준수. |
| `/clean_gone` | remote에서 삭제된 `[gone]` 브랜치와 연결된 worktree를 확인하고 안전하게 정리. |

`create-pull-request`와 `code-review`는 코멘트/PR 문장 윤문에 같은 플러그인의
`humanize-korean`을 사용할 수 있고, `code-review`는 리뷰 범위 분석에
`code-review-context`를 사용한다 — 별도 설치 불필요.

## CI

`.github/workflows/validate.yml`은 PR과 `main` push에서 다음을 검증합니다.

- plugin manifest, frontmatter, 상대 링크, fast 경로 구조
- TruffleHog 기반 credential scan (`verified`, `unknown` 결과 발견 시 실패)

## 에이전트

`ai-tell-detector` · `korean-style-rewriter` · `content-fidelity-auditor` · `naturalness-reviewer`(strict) · `korean-ai-tell-taxonomist`(분류 체계 유지보수).

기본 fast 경로는 `humanize-korean` 스킬이 에이전트 없이 직접 처리합니다. 기존 `humanize-monolith`는 호환용으로만 보존되어 새 실행 경로에서는 사용하지 않습니다.

## 설치

```text
/plugin marketplace add tophun/skillframe
/plugin install skillframe@skillframe
```

Codex에서 같은 명령을 슬래시 명령으로 사용하려면 레포 루트의
`prompts/*.md`를 `~/.codex/prompts/`에 복사합니다. 자세한 설치 방법은
루트 `README.md`의 `Codex custom commands`를 참고하세요.

## 사용

- PR 생성/보정: "PR 만들어줘", "PR 올려줘", "PR 본문 고쳐줘", `/pr`
- 코드리뷰: PR 링크와 함께 "코드리뷰", "리뷰해줘", `/code-review`
- 윤문 fast(기본): "AI 티 없애줘", "사람이 쓴 것처럼 윤문"
- 윤문 strict(선택): `--strict` 또는 "정밀 모드"
