---
name: code-review
description: 사용자가 GitHub PR(링크·번호)에 대해 "코드리뷰", "리뷰해줘", "PR 리뷰", "review this PR", "$code-review", "/code-review"를 요청할 때 사용한다. 코드 변경을 검토해 GitHub에 리뷰를 남기려는 상황. 커밋 작성·PR 생성·머지·라벨/리뷰어 변경에는 사용하지 않는다(PR 생성/본문 수정은 create-pull-request 담당).
---

# Skillframe: Code Review

GitHub PR을 다단계 에이전트로 분석하고, 검증된 이슈만 **해당 코드 라인에 인라인 코멘트 + 코드 제안(suggestion)** 으로 남기는 개인 코드리뷰 워크플로우. 코멘트 문장은 게시 전 `humanize-korean` 스킬로 다듬어 동료가 바로 이해하게 만든다.

## 핵심 원칙 (이 4가지가 이 스킬의 존재 이유)

1. **인라인으로 남긴다.** 최상단 일반 코멘트(`gh pr comment`)가 아니라, 문제가 있는 정확한 코드 라인에 인라인 리뷰 코멘트(`gh api .../pulls/{n}/reviews`)로 남긴다.
2. **코드 제안을 붙인다.** 고칠 수 있는 이슈에는 ` ```suggestion ` 블록을 붙여 리뷰어가 GitHub UI에서 `Commit suggestion` 한 번으로 반영하게 한다.
3. **문장을 윤문한다.** 게시 전 `humanize-korean`(fast 모드)으로 코멘트 문장을 다듬는다. 백틱 안 코드 식별자는 절대 수정 금지.
4. **게시 전 승인받는다.** GitHub에 남는 작업이므로 살아남은 이슈와 게시 범위를 사용자에게 먼저 확인받는다.

## 언제 쓰나 / 안 쓰나

- **쓴다:** PR 링크/번호 + "코드리뷰/리뷰해줘/review this PR", `/code-review`, `$code-review`
- **안 쓴다:** 커밋 작성, PR 생성/본문 수정(→ `create-pull-request`), 머지·라벨·리뷰어 변경

## 워크플로우

리뷰 분석 파이프라인은 플러그인 `code-review:code-review`와 동일한 다단계 구조를 쓰되, **게시 단계를 인라인+제안+윤문으로 대체**한다.

1. **적격성 확인 (Haiku)** — PR이 (a) closed/merged, (b) draft, (c) 자동/사소, (d) 이미 "### Code review" 코멘트 존재 중 하나면 중단.
   `gh pr view {n} --repo {owner/repo} --json state,isDraft,mergedAt,closed`, `--comments`
2. **컨텍스트 수집 (병렬 Haiku)** — 관련 CLAUDE.md 경로 목록 + PR 요약(`gh pr diff {n}`).
3. **병렬 리뷰 (5개 Sonnet)** — ① CLAUDE.md 준수(없으면 생략) ② 변경 라인만 얕은 버그 스캔 ③ git blame/history 회귀 ④ 이전 PR 코멘트 재적용 ⑤ 코드 주석/불변식 위반.
4. **신뢰도 스코어링 (이슈별 Haiku)** — 각 이슈를 0-100으로 채점(루브릭·false positive 목록은 `references/scoring-rubric.md`). **80점 미만 제외.** 남는 게 없으면 중단.
5. **적격성 재확인 (Haiku)** — 게시 직전 1단계 조건을 다시 확인.
6. **사용자 승인** — 살아남은 이슈 목록을 보여주고 게시 범위를 확인받는다. 임계값(80)에 아깝게 못 미친 실질 이슈가 있으면 함께 공유해 판단을 맡긴다.
7. **코멘트 윤문** — `humanize-korean` fast 모드로 각 코멘트 문장을 다듬는다. 이 스킬(`skillframe:humanize-korean`)과 실행 에이전트는 **같은 `skillframe` 플러그인에 함께 들어 있어** 별도 설치가 필요 없다.
8. **인라인 리뷰 게시** — `gh api .../pulls/{n}/reviews`에 인라인 코멘트 + suggestion 페이로드로 게시. 상세 recipe는 `references/inline-review-recipe.md`.

## 쉽게 쓰는 코멘트 3단 구조

각 코멘트는 **① 무엇이 문제인지 → ② 왜 문제인지 → ③ 어떻게 고치는지(suggestion)** 순으로 쓴다. 전문 용어보다 동료가 바로 이해할 표현을 쓴다.

> 예) "이 `useEffect`는 `console.log`만 실행하는 디버그용 코드입니다(①). 실제 기능엔 영향이 없으니 병합 전에 지우면 좋겠습니다(②). 아래 suggestion으로 블록을 통째로 지울 수 있습니다(③)."

## 게시 후 검증 (필수)

인라인 코멘트가 의도한 라인·suggestion으로 붙었는지 확인한다.

```bash
gh api repos/{owner}/{repo}/pulls/{n}/comments \
  --jq '.[] | select(.pull_request_review_id=={reviewId}) | {path, line, start_line, has_suggestion: (.body|contains("```suggestion"))}'
```

## 흔한 실수

| 실수 | 바로잡기 |
| --- | --- |
| 최상단 일반 코멘트로 남김 | 문제 라인에 인라인으로 남긴다 (`pulls/{n}/reviews`) |
| 설명만 하고 고치는 법 없음 | 고칠 수 있으면 ` ```suggestion ` 블록을 붙인다 |
| suggestion 들여쓰기 불일치 | 원본 파일과 **정확히 같은 들여쓰기**로 작성(`git show origin/{branch}:{path}`로 확인) |
| 승인 없이 바로 게시 | 게시 전 이슈·범위를 사용자에게 확인받는다 |
| AI 티 나는 딱딱한 문장 | `humanize-korean`으로 윤문 후 게시 |
| 사용자가 수정하지 않은 라인 지적 | 변경된 라인의 이슈만 남긴다 |
