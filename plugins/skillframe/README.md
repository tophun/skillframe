# skillframe (plugin)

개인용 PR 생성 + 코드리뷰 + 한국어 윤문 Claude Code 플러그인.

## 스킬

| 노출 이름 | 하는 일 |
| --- | --- |
| `skillframe:create-pull-request` | GitHub PR 생성과 기존 PR 본문/draft 보정을 처리. repository template과 말투 규칙을 읽고, `gh pr create/edit/ready` 실행 전 승인 게이트를 연다. |
| `skillframe:code-review` | GitHub PR을 다단계 에이전트로 리뷰하고, 검증된 이슈만 해당 코드 라인에 **인라인 코멘트 + 코드 제안(suggestion)** 으로 게시. 게시 전 승인, 신뢰도 80점 필터. |
| `skillframe:humanize-korean` | AI가 쓴 한글 텍스트의 AI 티를 탐지·분류해 내용은 그대로 두고 문체만 자연스럽게 윤문. fast/strict 모드. |

`create-pull-request`와 `code-review`는 코멘트/PR 문장 윤문에 같은 플러그인의
`humanize-korean`을 사용할 수 있다 — 별도 설치 불필요.

## 에이전트

`humanize-monolith`(fast) · `ai-tell-detector` · `korean-style-rewriter` · `content-fidelity-auditor` · `naturalness-reviewer` · `korean-ai-tell-taxonomist`(strict 파이프라인).

## 설치

```text
/plugin marketplace add tophun/skillframe
/plugin install skillframe@skillframe
```

## 사용

- PR 생성/보정: "PR 만들어줘", "PR 올려줘", "PR 본문 고쳐줘", `/pr`
- 코드리뷰: PR 링크와 함께 "코드리뷰", "리뷰해줘", `/code-review`
- 윤문: "AI 티 없애줘", "사람이 쓴 것처럼 윤문"
