# PR Body Rules

PR body는 저장소의 PR 템플릿이 있으면 그 구조를 우선한다. 없으면 이 문서의 기본
템플릿을 사용한다.

## 템플릿 탐색 순서

1. `.github/pull_request_template.md`
2. `.github/PULL_REQUEST_TEMPLATE.md`
3. `.github/pull_request_template/*.md`
4. `.github/PULL_REQUEST_TEMPLATE/*.md`

템플릿이 있으면 섹션 구조, 체크박스, 안내 문구를 유지하고 내용을 채운다. 불필요한
섹션을 임의로 삭제하지 않는다. 해당 없음은 `N/A`로 명시한다.

## 기본 템플릿

```markdown
## 요약

-

## 변경사항

-

## 관련 이슈

-
```

## 관련 이슈 추론

브랜치명, 커밋 메시지, diff에서 다음 패턴을 찾는다.

- `#123`
- `fixes #123`
- `closes #123`
- `[A-Z][A-Z0-9]+-[0-9]+`

찾을 수 없으면 `N/A`를 사용한다.
