# GitHub 대기 중인 인라인 리뷰 작성

리뷰 코멘트는 로컬 초안으로 모두 모은 뒤, 하나의 `PENDING` 리뷰에 인라인 코멘트만
담아 작성한다. 리뷰를 자동 제출하지 않는다.

## 페이로드

```json
{
  "commit_id": "<PR head의 전체 SHA>",
  "event": "PENDING",
  "comments": [
    {
      "path": "src/example.ts",
      "line": 42,
      "side": "RIGHT",
      "body": "문제가 발생하는 조건과 사용자 영향을 짧게 설명합니다.\n\n```suggestion\nconst replacement = value;\n```"
    }
  ]
}
```

- 최상위 `body`는 넣지 않는다.
- `comments` 외에 리뷰 요약, `### Code review`, 생성 도구 문구를 넣지 않는다.
- 추가·변경된 라인은 `side: "RIGHT"`를 사용한다.
- 여러 줄 코멘트는 `start_line`과 `start_side`를 함께 지정한다.
- suggestion의 들여쓰기와 코드는 PR head의 실제 내용과 정확히 일치해야 한다.
- suggestion으로 안전하게 표현할 수 없는 구조 변경은 설명만 남긴다.

## 작성

```bash
gh api -X POST repos/<owner>/<repo>/pulls/<number>/reviews \
  --input payload.json
```

응답의 `state`가 `PENDING`인지 확인한다. `APPROVE`, `REQUEST_CHANGES`, `COMMENT`로
제출하지 않는다.

사용자가 명시적으로 제출을 요청한 경우에만 대기 중인 리뷰를 제출한다. 그 전까지는
리뷰어가 GitHub UI에서 직접 검토·제출할 수 있는 초안으로 남긴다.
