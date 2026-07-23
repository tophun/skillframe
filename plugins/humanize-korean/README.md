# humanize-korean

AI가 쓴 한글 텍스트를 사람이 쓴 글처럼 윤문하는 Claude Code 플러그인.

번역투·영어 인용 과다·기계적 병렬·관용구·피동 남용·접속사 남발 등 AI 티 패턴을 탐지·분류해, **내용은 한 글자도 건드리지 않고 문체·리듬·표현만** 자연스러운 한국어로 재작성한다.

## 구성

- **skill** `humanize-korean` — 오케스트레이터 (fast/strict 모드)
- **agents** — `humanize-monolith`(fast 단일 호출), `ai-tell-detector`, `korean-style-rewriter`, `content-fidelity-auditor`, `naturalness-reviewer`, `korean-ai-tell-taxonomist`(strict 파이프라인)

## 설치

```text
/plugin marketplace add tophun/skillframe
/plugin install humanize-korean@skillframe
```

## 사용

"AI 티 없애줘", "사람이 쓴 것처럼 윤문", "ChatGPT 문체 자연스럽게" 등으로 트리거. `--strict`로 5인 파이프라인 정밀 검증.

`skillframe-code-review` 플러그인이 코드리뷰 코멘트 윤문에 이 플러그인을 사용한다.
