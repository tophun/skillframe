---
name: skillframe-pr
description: GitHub Pull Request 생성, 기존 PR 업데이트, PR 본문 작성, PR 리뷰 코멘트 작성을 수행하는 skillframe 개인용 한국어 PR 워크플로우. 사용자가 "PR 만들어줘", "pull request 만들어줘", "PR 올려줘", "PR 업데이트해줘", "기존 PR 정리해줘", "PR 리뷰 남겨줘", "/pr", "skillframe:pr", "/skillframe:pr"처럼 GitHub PR 생성/수정/리뷰를 요청하면 사용한다. gh CLI와 git 상태를 점검하고, .github PR 템플릿이 있으면 그 구조를 따르며, 없으면 스킬 기본 템플릿으로 한국어 PR을 작성한다. 실제 gh pr create 실행 전에는 반드시 사용자 승인을 받으며, GitHub 리뷰 제출은 항상 pending review로 작성한 뒤 사용자에게 제출 여부를 물어본다.
---

# Skillframe PR

GitHub PR을 리뷰어가 이해하기 쉬운 형태로 생성하거나 업데이트한다. PR title과 body는
기본적으로 한국어로 작성하고, 저장소의 PR 템플릿이 있으면 그 구조를 우선한다.

이 스킬은 사용자가 PR 생성, 기존 PR 업데이트, PR 리뷰 코멘트 작성을 요청했을 때
자동으로 사용한다.

## 절대 규칙

- 실제 `gh pr create` 실행 직전에는 반드시 사용자에게 title, base/head, body, draft 여부를 보여주고 승인받는다.
- GitHub PR 리뷰는 inline comment를 pending review로 누적하고, summary comment도 같은 pending review에 추가한다.
- 사용자가 명시적으로 요청하기 전까지 pending review를 submit하지 않는다.
- `gh` 미설치, GitHub 미로그인, branch 미push 같은 문제는 즉시 중단 보고로 끝내지 말고 성공 가능한 다음 명령을 안내한다.
- 히스토리 재작성(`rebase`, `commit --amend`, squash, `push --force-with-lease`)은 명시 승인 없이 실행하지 않는다.
- 관련 없는 사용자 변경사항은 stage, commit, stash, discard, revert하지 않는다.
- PR이 이미 있으면 새 PR을 만들지 말고 기존 PR 업데이트 흐름으로 전환한다.

## 기본 점검

1. 저장소와 도구 상태를 확인한다.

```bash
git rev-parse --show-toplevel
git status --short
git branch --show-current
gh --version
gh auth status
```

2. `gh`가 없으면 설치를 안내한다.

```bash
brew install gh
```

macOS가 아니면 `https://cli.github.com/` 설치 안내를 제공한다.

3. 로그인되어 있지 않으면 다음을 안내한다.

```bash
gh auth login
```

4. 현재 브랜치가 `main` 또는 `master`이면 기능 브랜치를 만들거나 전환하도록 안내한다.
사용자가 원하면 `codex/` prefix를 기본으로 브랜치를 만든다.

## 컨텍스트 수집

1. base branch를 찾는다.

```bash
git remote show origin
git symbolic-ref refs/remotes/origin/HEAD --short
```

원격 HEAD를 찾지 못하면 `main`, `master`, `develop` 순서로 존재 여부를 확인한다.

2. 원격 상태를 갱신한다.

```bash
git fetch origin
```

3. 기존 PR을 확인한다.

```bash
gh pr view --json number,url,title,body,baseRefName,headRefName,state,isDraft
```

기존 PR이 있으면 생성하지 않고 업데이트 계획을 세운다.

4. 변경 범위와 의도를 분석한다.

```bash
git log origin/<base>..HEAD --oneline --no-decorate
git diff origin/<base>..HEAD --stat
git diff origin/<base>..HEAD
```

작업 트리에 커밋되지 않은 변경이 있으면 diff를 읽고 PR에 포함할지 판단한다. 포함해야
하면 리뷰어 친화적인 커밋 단위로 stage/commit한다. 커밋 단위가 애매하거나 unrelated
변경이 섞여 있으면 사용자에게 묻는다.

## 커밋과 푸시

- PR에 필요한 변경이 아직 커밋되지 않았으면 이 스킬 안에서 커밋할 수 있다.
- 커밋 메시지는 가능하면 Conventional Commit을 사용하고 한국어 요약을 쓴다.
- 더 정교한 커밋 분리가 필요하면 `skillframe-commit` 흐름을 따른다.
- branch가 원격에 없으면 PR 생성 전에 push한다.

```bash
git push -u origin HEAD
```

- rebase 또는 squash가 필요해 보이면 이유와 위험을 설명하고 사용자 승인을 받은 뒤 실행한다.
- rebase 이후 push가 필요하면 `--force-with-lease`만 사용한다.

## PR 템플릿

다음 순서로 템플릿을 찾는다.

1. `.github/pull_request_template.md`
2. `.github/PULL_REQUEST_TEMPLATE.md`
3. `.github/pull_request_template/*.md`
4. `.github/PULL_REQUEST_TEMPLATE/*.md`

템플릿이 있으면 섹션 구조, 체크박스, 안내 문구를 유지하고 내용을 채운다. 불필요한
섹션을 임의로 삭제하지 않는다. 해당 없음은 `N/A`로 명시한다.

템플릿이 없으면 다음 기본 템플릿을 사용한다.

```markdown
## 요약

- 

## 변경사항

- 

## 관련 이슈

- 
```

관련 이슈는 브랜치명, 커밋 메시지, diff에서 `#123`, `fixes #123`, `closes #123`,
`[A-Z][A-Z0-9]+-[0-9]+` 패턴을 추론한다. 찾을 수 없으면 `N/A`를 사용한다.

## PR 생성 흐름

1. title 후보를 만든다.
   - 리뷰어가 diff 방향을 예측할 수 있게 구체적으로 쓴다.
   - 모호한 "수정", "작업", "정리"만으로 끝내지 않는다.

2. body를 만든다.
   - 저장소 템플릿 또는 기본 템플릿을 따른다.
   - 검증 섹션에는 실제 실행한 명령과 결과를 쓴다.
   - 검증하지 못한 항목은 "미실행"으로 명시하고 이유를 적는다.

3. 생성 전 승인 게이트를 연다.
   - PR title
   - base branch와 head branch
   - draft 여부
   - PR body 전체
   - push 여부와 현재 원격 branch 상태

4. 사용자가 승인한 뒤 임시 파일로 body를 저장하고 생성한다.

```bash
gh pr create --title "<title>" --body-file /tmp/skillframe-pr-body.md --base <base>
```

draft PR이면 다음을 사용한다.

```bash
gh pr create --title "<title>" --body-file /tmp/skillframe-pr-body.md --base <base> --draft
```

5. 생성 후 PR number 또는 URL만 핵심 결과로 보고한다. 필요한 경우 실행한 검증 명령을
짧게 덧붙인다.

## 기존 PR 업데이트 흐름

기존 PR이 있거나 사용자가 기존 PR 정리를 요청하면 다음을 따른다.

1. 현재 PR 정보를 확인한다.

```bash
gh pr view --json number,url,title,body,baseRefName,headRefName,state,isDraft
```

2. 새 커밋, diff, 템플릿 변경 여부를 분석한다.
3. title/body를 갱신해야 하면 변경안을 먼저 보여준다.
4. 사용자가 승인하면 `gh pr edit`으로 반영한다.

```bash
gh pr edit --title "<title>" --body-file /tmp/skillframe-pr-body.md
```

5. 완료 후 PR number 또는 URL을 보고한다.

## PR 리뷰 코멘트 흐름

사용자가 PR 리뷰, inline comment, review summary 작성을 요청하면 다음을 따른다.

1. 대상 PR을 확인한다.

```bash
gh pr view <number-or-url> --json number,url,title,files,headRefOid
gh pr diff <number-or-url>
```

2. findings는 버그, 회귀 위험, 테스트 누락, 보안/성능 위험 중심으로 작성한다.
3. inline comment는 즉시 submit하지 말고 pending review로 작성한다.
4. 모든 inline comment를 먼저 작성한 뒤 summary comment를 같은 pending review에 추가한다.
5. pending review 작성이 끝나면 사용자에게 PR number 또는 URL과 함께 "제출 대기 상태"라고 보고한다.
6. 사용자가 명시적으로 제출을 요청한 경우에만 review submit 명령을 실행한다.

리뷰 제출 전에는 반드시 다시 묻는다. "submit 해줘", "리뷰 제출해줘"처럼 명확한 요청이
있을 때만 제출한다.

## 오류 대응

- 커밋이 base보다 앞서 있지 않으면 다른 branch에서 작업했는지 확인한다.
- branch가 push되지 않았으면 `git push -u origin HEAD`를 실행하거나 안내한다.
- PR이 이미 있으면 기존 PR URL을 보여주고 업데이트 흐름으로 전환한다.
- merge conflict가 있으면 충돌 파일을 보여주고 rebase 또는 merge 전략을 제안한다.
- PR 템플릿을 찾지 못해도 중단하지 않고 기본 템플릿을 사용한다.

## 최종 보고

완료 보고는 간결하게 한다.

- 새 PR 또는 기존 PR의 number/URL
- 생성인지 업데이트인지
- 리뷰 pending 상태인지, submit 완료인지
- 실행한 핵심 검증 명령이 있으면 한 줄
