---
name: create-pull-request
description: 사용자가 새 GitHub PR, pull request, 풀리퀘 생성을 요청하거나 기존 PR의 설명/draft 상태 보정을 요청할 때 사용한다. "/pr", "PR 만들어줘", "PR 올려줘", "PR 본문 고쳐줘", "커밋하고 PR"을 포함하며 PR 코드리뷰/댓글/merge/label/reviewer 변경에는 사용하지 않는다
---

# Skillframe: Create Pull Request

GitHub PR을 생성하거나, 이미 만들어진 PR의 설명과 상태를 리뷰어가 이해하기 쉬운
형태로 보정한다.

본문은 무엇을 왜 바꿨는지 먼저 밝히고, 핵심 구현 방식과 적용 범위를 설명한다.
커밋이나 조사 이력을 나열하지 않는다. `references/pr-body.md`의 작성 후 점검으로
불필요한 세부 사항을 덜어내고, 리뷰에 필요한 제약과 검증 한계는 남긴다.

**핵심 원칙:** `gh pr create`, `gh pr edit`, `gh pr ready`는 template/reference,
diff, 기존 PR 상태를 확인하고 사용자 승인을 받은 뒤에만 실행한다.

## 적용 범위

이 스킬은 두 가지 작업만 처리한다.

1. 새 PR 생성
   - local branch의 diff를 읽어 PR 제목과 본문을 작성한다.
   - 필요하면 branch를 push한다.
   - 생성 전 사용자 승인을 받는다.

2. 기존 PR 설명 보정
   - 기존 PR의 설명과 draft 상태만 보정한다.
   - 수정 전 사용자 승인을 받는다.

다음 작업은 이 스킬 범위가 아니다.

- PR 코드리뷰, inline comment, pending review
- reviewer, label, milestone, project 변경
- merge, close, reopen

범위 밖 작업이 함께 요청되면 이 스킬에서는 PR 설명/draft 보정만 처리하고, 나머지는
수행하지 않는다고 분리 안내한다.

## 필수 점검

이 스킬은 GitHub CLI `gh`가 필요하다. `gh`가 없으면 PR 생성/수정을 진행하지 않고
설치 방법을 안내한다.

먼저 상태를 확인한다.

```bash
gh --version
git status --short
git branch --show-current
gh auth status
git fetch origin
```

`gh --version`이 실패하면 macOS에서는 `brew install gh`를 안내하고, 그 외 환경에서는
GitHub CLI 설치 문서 `https://cli.github.com/`를 안내한다. `gh auth status`가 실패하면
`gh auth login` 실행을 요청한다.

항상 읽는다:

- `references/pr-title.md`
- `references/pr-body.md`
- `references/pr-tone.md`
- repository PR template, 있으면 사용

기존 PR을 확인한다. 생성 요청 중 기존 PR이 있으면 중복 PR 생성을 막기 위해 새 PR을
만들지 않고, 기존 PR 링크와 만들지 않는 이유를 사용자에게 제공한다.

```bash
gh pr view --json number,url,title,baseRefName,headRefName,state,isDraft
gh pr list --head "$(git branch --show-current)" --state open --json number,url,title,baseRefName,headRefName,state,isDraft
```

## 사용자 확인

사용자의 입력 또는 선택이 필요하면 일반 메시지로 추측하지 않는다. 사용 가능한 환경에 맞춰
Claude에서는 `AskUserQuestion`, Codex에서는 `user-input prompt`를 사용한다.

반드시 확인한다:

- 관련 여부가 애매한 변경을 stage/commit/push할지
- branch 생성, rebase, amend, squash, force-push 여부
- PR 내용과 draft 상태 승인
- 기존 PR을 보정할지 새 요청을 중단할지

## 생성 흐름

1. base branch를 `origin/HEAD`, `main`, `master`, `develop` 순서로 찾고
   `origin/<base>..HEAD` 범위를 분석한다.

   ```bash
   git log origin/<base>..HEAD --oneline --no-decorate
   git diff origin/<base>..HEAD --stat
   git diff origin/<base>..HEAD
   ```

2. 작업 트리에 커밋되지 않은 변경이 있으면 PR에 포함할지 판단한다. 관련 없는 변경은
   stage, commit, push, stash, discard, revert하지 않는다.

3. 커밋 요청이 포함된 경우 관련 변경만 선별 stage하고, 포함 파일과 commit message를
   승인받은 뒤 commit한다. 복잡한 커밋 분리는 별도 commit workflow를 사용한다.

4. upstream이 없으면 branch가 맞는지 확인한 뒤 `git push -u origin HEAD`를 실행한다.
   rebase, amend, squash, force-push는 명시 승인 없이 하지 않는다.

5. `references/`와 repository template에 맞춰 한국어 PR 내용을 작성한다. 말투는
   `references/pr-tone.md`를 따른다. 검증 섹션에는
   실제 실행한 명령만 적고, 미실행 항목은 `미실행`과 이유를 적는다.

6. 실행 전 사용자에게 PR 제목, base/head, draft 여부, 본문 전체, push 상태를 보여주고
   승인받는다. 사용자가 ready를 명시하지 않으면 draft가 기본값이다.

7. 승인받은 PR 본문을 임시 파일에 저장한 뒤, 승인 후에만 생성한다.

   ```bash
   gh pr create --title "<title>" --body-file <approved-body-file> --base <base> --draft
   ```

## 기존 PR 보정 흐름

사용자가 기존 PR의 설명이나 draft 상태 보정을 명시한 경우에만 사용한다.

1. 현재 branch PR 또는 사용자가 준 PR URL/번호를 읽는다.

   ```bash
   gh pr view <pr> --json number,url,title,body,baseRefName,headRefName,state,isDraft
   ```

2. `references/`, `references/pr-tone.md`, repository template에 맞춰 보정안을 만든다.
   template 섹션과 체크박스는 보존한다. ready 전환은 사용자가 명시한 경우에만 제안한다.

3. 실행 전 PR URL, 변경 전/후 제목, 변경 전/후 draft 상태, 교체할 본문 전체를 보여주고
   승인받는다.

4. 승인받은 PR 본문을 임시 파일에 저장한 뒤, 승인 후에만 수정한다.

   ```bash
   gh pr edit <pr> --title "<title>" --body-file <approved-body-file>
   gh pr ready <pr>
   ```

   `gh pr ready`는 ready 전환이 승인된 경우에만 실행한다.

## 위험 신호

절대 하지 않는다:

- `gh` 미설치 또는 미인증 상태에서 PR 생성/수정 진행
- template/reference를 읽기 전 `gh pr create`, `gh pr edit`, `gh pr ready` 실행
- open PR이 있는 branch에서 새 PR 생성
- 승인 게이트 생략
- `gh pr create --fill`로 PR 제목/본문 작성 대체
- 실행하지 않은 테스트를 통과한 것처럼 기재
- PR 코드리뷰, 댓글, merge 요청을 이 스킬로 처리

## 최종 보고

짧게 보고한다:

- PR URL
- base/head와 draft 상태
- 생성인지 보정인지
- 핵심 검증 결과, 있으면 포함
