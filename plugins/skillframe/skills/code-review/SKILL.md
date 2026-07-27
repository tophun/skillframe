---
name: code-review
description: 사용자가 GitHub PR(링크·번호)에 대해 "코드리뷰", "리뷰해줘", "PR 리뷰", "review this PR", "$code-review", "/code-review"를 요청할 때 사용한다. 코드 변경을 검토해 GitHub에 리뷰를 남기려는 상황. 커밋 작성·PR 생성·머지·라벨/리뷰어 변경에는 사용하지 않는다(PR 생성/본문 수정은 create-pull-request 담당).
---

# Skillframe: Code Review

GitHub PR을 **탐색·추론·평가·작성 서브에이전트**로 나눠 분석하고, 검증된 이슈만 **해당 코드 라인에 인라인 코멘트 + 코드 제안(suggestion)** 으로 남긴다.

## 핵심 원칙

1. **인라인으로만 남긴다.** 최상단 일반 코멘트나 리뷰 요약(`gh pr comment`, review-level `body`)은 남기지 않는다. 문제가 있는 정확한 코드 라인에만 붙인다.
2. **코드 제안을 붙인다.** 고칠 수 있는 이슈에는 ` ```suggestion ` 블록을 붙여 GitHub UI에서 `Commit suggestion` 한 번으로 반영하게 한다.
3. **게시 전 승인받는다.** GitHub에 남는 작업이므로 살아남은 이슈와 게시 범위를 먼저 확인받는다. 승인된 집합이 이후 단계의 유일한 범위다.
4. **역할별로 위임한다.** 오케스트레이터는 diff를 통독하지 않는다. 서브에이전트에 맡기고 구조화된 결과만 받아 조립한다.
5. **N회 도는 단계에서 아끼고, 1회짜리 게이트에서는 정확도를 산다.**

## 언제 쓰나 / 안 쓰나

- **쓴다:** PR 링크/번호 + "코드리뷰/리뷰해줘/review this PR", `/code-review`, `$code-review`
- **안 쓴다:** 커밋 작성, PR 생성/본문 수정(→ `create-pull-request`), 머지·라벨·리뷰어 변경

## 서브에이전트

| 단계 | 에이전트 | 모델 (기본 → 승급) |
| --- | --- | --- |
| 탐색 | `skillframe:code-review-explorer` | Haiku |
| 추론 (레인당 1개, 병렬) | `skillframe:code-review-analyst` | Sonnet → Opus |
| 평가 | `skillframe:code-review-judge` | Sonnet → Opus |
| 코멘트 작성 | `skillframe:code-review-writer` | Haiku → Sonnet |

승급은 별도 정의 없이 같은 에이전트를 `model` 오버라이드로 부른다. **승급 조건과 각 에이전트의 작업 규칙은 에이전트 정의(`plugins/skillframe/agents/`)에 있다. 여기서 반복하지 않는다** — 한쪽만 고쳐지면 갈라진다.

오케스트레이터가 지킬 것은 이 넷뿐이다.

- **에이전트에 `name`을 붙이지 않는다.** 이름을 붙이면 addressable 백그라운드 에이전트가 되어 결과 JSON을 반환하지 않고 idle 알림만 반복한다. 이름 없이 호출해야 반환값을 받는다. 병렬은 한 메시지에 여러 호출을 넣어서 얻는다.
- 각 레인에는 담당 파일의 hunk만 넘긴다. 전체 diff나 파일 전문을 통째로 넘기지 않는다.
- analyst 레인은 한 메시지에서 동시에 띄운다.
- 서브에이전트에 GitHub 쓰기를 맡기지 않는다.

## 워크플로우

1. **적격성 확인** — `gh` 직접 호출. PR이 (a) closed/merged, (b) draft, (c) 자동·사소, (d) 동일 head 커밋에 이미 해당 리뷰어의 인라인 코멘트가 존재 중 하나면 중단.
   `gh pr view {n} --repo {owner/repo} --json state,isDraft,mergedAt,closed,headRefOid`, `gh api repos/{owner/repo}/pulls/{n}/comments --paginate`
2. **탐색** — `code-review-explorer` 1개. PR 번호와 저장소를 넘기면 diff·hunk·CLAUDE.md 경로·관련 테스트·레인 배분안·`deep_lane_files`를 JSON으로 돌려준다. 리뷰 범위 판단은 `$code-review-context`를 따른다. codegraph는 그 스킬의 조건을 만족할 때만 explorer에 지시한다.
3. **추론** — `code-review-analyst`를 explorer가 제안한 레인 수만큼 **동시에** 띄운다. `deep_lane_files`가 승급 조건에 걸리면 `model: opus`, `lane: deep`으로 1개 추가한다.
4. **평가** — `code-review-judge` 1개에 **모든 레인의 이슈를 한 번에** 넘긴다. 3단계에서 Opus 레인이 돌았으면 judge도 Opus로 올린다. 80점 미만 제외, 남는 게 없으면 중단. `needs_deep_review`가 나오면 그 이슈만 3단계 Opus 레인으로 한 번 되돌린다.
5. **적격성 재확인** — 게시 직전 1단계 조건을 다시 확인.
6. **사용자 승인** — 살아남은 이슈와 `near_miss`를 함께 보여주고 게시 범위를 확인받는다.
7. **코멘트 작성** — `code-review-writer` 1개에 승인된 이슈와 `references/comment-style.md`의 **절대 경로**를 넘긴다. 별도 윤문 패스를 돌리지 않는다.
8. **게시** — writer가 돌려준 `comments`를 `gh api .../pulls/{n}/reviews` 페이로드에 담는다. 최상위 `body`는 비운다. 상세는 `references/inline-review-recipe.md`.

### 오케스트레이터가 직접 하는 일

탐색·추론·평가·작성은 전부 위임한다. 남는 건 넷뿐이다 — `gh` 적격성 확인(1·5), 서브에이전트 배분과 결과 조립, 사용자 승인(6), 게시와 게시 후 검증(8).

## 게시 후 검증 (필수)

```bash
gh api repos/{owner}/{repo}/pulls/{n}/comments \
  --jq '.[] | select(.pull_request_review_id=={reviewId}) | {path, line, start_line, has_suggestion: (.body|contains("```suggestion"))}'
```

## 참고 자료 (필요한 단계에서만 로드)

| 파일 | 언제 | 누가 |
| --- | --- | --- |
| [`references/comment-style.md`](references/comment-style.md) | 7단계 | writer — 코멘트 문장 루브릭 |
| [`references/scoring-rubric.md`](references/scoring-rubric.md) | 4단계 | judge — 신뢰도 채점 루브릭 |
| [`references/inline-review-recipe.md`](references/inline-review-recipe.md) | 8단계 | 오케스트레이터 — 페이로드·앵커·suggestion 문법 |

## 이 저장소 특유의 함정

일반적인 리뷰 상식은 적지 않는다. 실제로 여기서 반복해 틀린 것만 남긴다.

| 함정 | 바로잡기 |
| --- | --- |
| 여러 줄이라 suggestion을 포기 | `start_line`~`line` 범위 앵커면 여러 줄도 붙는다. 줄 수는 포기 사유가 아니다 |
| suggestion 들여쓰기 불일치 | `git show origin/{branch}:{path}`로 원본을 확인하고 100% 맞춘다 |
| 코멘트에 리뷰 도구 사정을 씀 | "suggestion 대신 예시로", "판단이 필요해 넣지 않았습니다" 전부 사족이다. 지운다 |
| "발화" 같은 어색한 한자어 | "실행된다 / 동작한다 / 트리거된다"로 쓴다 |
| Opus 심층 레인을 돌리고 judge는 Sonnet 유지 | 심판이 발견자보다 약하면 안 된다 |
| 1회짜리 게이트를 아끼려고 모델을 낮춤 | judge는 배치 1회라 절감 효과가 없다 |
| 에이전트에 `name`을 붙여 호출 | 백그라운드로 돌아 결과를 못 받는다. 이름 없이 호출한다 |
| writer 출력의 코드가 `&amp;&amp;`·`&lt;`로 나옴 | HTML 이스케이프. 게시 전 원문 문자인지 확인한다 |
