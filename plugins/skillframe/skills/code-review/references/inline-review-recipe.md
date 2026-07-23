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
  "body": "### Code review\n\n인라인으로 N건 남겼습니다.\n\n🤖 Generated with [Claude Code](https://claude.ai/code)",
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

- 본문 `body`에 `### Code review`를 포함해야 적격성 재확인(중복 리뷰 방지)이 동작한다.
- `event: "COMMENT"` — 승인/변경요청 없이 코멘트만. (approve/request-changes 아님)

## 3. suggestion 블록 규칙

| 목적 | suggestion 내용 |
| --- | --- |
| 라인 **삭제** | ` ```suggestion ` 와 ` ``` ` 사이를 **비움** (앵커한 라인 전체 삭제) |
| 라인 **유지+일부만 삭제** | 남길 코드를 그대로 넣음 (예: 가드는 두고 `console.log`만 제거하려면 앵커 63-64, suggestion에 `if (!result.stored) return;` 만) |
| 라인 **교체** | 새 코드를 넣음 |

- **들여쓰기는 원본과 100% 일치**해야 `Commit suggestion`이 깨끗하게 적용된다.
- 삭제 제안 시 앞뒤 빈 줄이 겹치지 않도록, 필요하면 인접 빈 줄까지 앵커 범위에 포함한다.
- suggestion으로 표현하기 어려운 구조적 변경(예: 동기 호출 재설계)은 suggestion 없이 설명 코멘트로만 남긴다.

## 4. 게시 및 검증

```bash
gh api -X POST repos/{owner/repo}/pulls/{n}/reviews --input payload.json \
  --jq '{id, state, html_url}'

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
