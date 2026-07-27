# 인라인 리뷰 + 코드 제안 게시 recipe

GitHub PR에 인라인 코멘트와 `suggestion`을 한 번의 리뷰로 게시하는 방법.

## 1. PR head SHA와 라인 번호 확보

```bash
# head 커밋 SHA (리뷰 commit_id + 본문 permalink용)
gh pr view {n} --repo {owner/repo} --json headRefOid,headRefName

# 게시할 파일의 정확한 라인/들여쓰기 (head 기준)
git fetch origin {branch} -q
git show origin/{branch}:{path} | sed -n '{start},{end}p'
```

- 인라인 코멘트는 **PR head 파일 기준 라인 번호**로 앵커한다.
- 추가·변경된 라인은 `side: "RIGHT"`. 여러 줄이면 `start_line`(+`start_side`)와 `line`(+`side`)로 범위 지정.

## 2. 리뷰 페이로드 (payload.json)

```json
{
  "commit_id": "<PR head 40자리 SHA>",
  "event": "COMMENT",
  "comments": [
    {
      "path": "apps/.../page.tsx",
      "start_line": 39,
      "start_side": "RIGHT",
      "line": 42,
      "side": "RIGHT",
      "body": "설명 문장(①무엇→②왜).\n\n아래 suggestion으로 지울 수 있습니다.\n\n```suggestion\n```"
    },
    {
      "path": "apps/.../useNiceNameCheck.ts",
      "start_line": 63,
      "start_side": "RIGHT",
      "line": 64,
      "side": "RIGHT",
      "body": "설명 문장.\n\n```suggestion\n          if (!result.stored) return;\n```"
    }
  ]
}
```

- 최상위 review-level `body`는 의도적으로 생략한다. `### Code review`, 리뷰 요약, `Generated with Claude Code` 문구를 추가하지 않는다.
- 인라인 코멘트의 각 `comments[].body`에만 문제 설명과 필요한 `suggestion`을 작성한다.
- `event: "COMMENT"` — 승인/변경요청 없이 코멘트만. (approve/request-changes 아님)

## 3. suggestion 블록 규칙

| 목적 | suggestion 내용 |
| --- | --- |
| 라인 **삭제** | ` ```suggestion ` 와 ` ``` ` 사이를 **비움** (앵커한 라인 전체 삭제) |
| 라인 **유지+일부만 삭제** | 남길 코드를 그대로 넣음 (예: 가드는 두고 `console.log`만 제거하려면 앵커 63-64, suggestion에 `if (!result.stored) return;` 만) |
| 라인 **교체** | 새 코드를 넣음 |
| **여러 줄** 교체 | 앵커를 `start_line`~`line`으로 잡고 그 범위를 대체할 코드 전체를 넣음 |

- **들여쓰기는 원본과 100% 일치**해야 `Commit suggestion`이 깨끗하게 적용된다.
- 삭제 제안 시 앞뒤 빈 줄이 겹치지 않도록, 필요하면 인접 빈 줄까지 앵커 범위에 포함한다.
- **여러 줄이라는 이유로 suggestion을 포기하지 않는다.** 연속된 라인 범위는 `start_line`~`line` 앵커로 통째로 제안할 수 있다. 앵커 범위는 diff hunk 안에 있어야 하므로, 고칠 코드가 hunk 밖이면 그 라인이 포함된 hunk를 기준으로 다시 앵커한다.
- 정말 suggestion으로 표현할 수 없을 때만(떨어진 여러 위치를 동시에 고쳐야 하거나, 동기 호출 재설계 같은 구조 변경) 일반 코드블록으로 예시를 붙인다.

### suggestion을 못 붙일 때 쓰지 않는 문장

왜 suggestion이 아닌지 설명하지 않는다. "수정 범위가 350-359행까지 걸쳐 있어 suggestion 대신 예시로 적어둡니다", "판단이 필요해 suggestion에는 넣지 않았습니다" 같은 문장은 리뷰 받는 사람에게 정보를 주지 않는다. 코드블록만 붙이고 사족 없이 끝낸다.

## 4. 게시 및 검증

```bash
gh api -X POST repos/{owner/repo}/pulls/{n}/reviews --input payload.json \
  --jq '{id, state, html_url}'

# review-level body가 비어 있는지 확인
gh api repos/{owner/repo}/pulls/{n}/reviews/{reviewId} \
  --jq '{body, state, comments: .comments}'

# 라인·suggestion 부착 확인
gh api repos/{owner/repo}/pulls/{n}/comments \
  --jq '.[] | select(.pull_request_review_id=={reviewId}) | {path, line, start_line, has_suggestion: (.body|contains("```suggestion"))}'
```

## 5. 재게시 시 기존 코멘트 정리

잘못 남긴 최상단 일반 코멘트가 있으면 삭제 후 인라인으로 다시 남긴다.

```bash
gh api repos/{owner/repo}/issues/{n}/comments --jq '.[] | {id, user: .user.login, head: (.body[0:30])}'
gh api -X DELETE repos/{owner/repo}/issues/comments/{commentId}
```

## 본문 permalink는 full SHA로

코멘트 본문에 코드 링크를 넣을 땐 마크다운 렌더링을 위해 **full 40자리 SHA**를 쓴다.
형식: `https://github.com/{owner}/{repo}/blob/{full_sha}/{path}#L{start}-L{end}` (앞뒤 1줄 이상 문맥 포함).
