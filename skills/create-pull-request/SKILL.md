---
name: skillframe:create-pull-request
description: skillframe 저장소의 `skills/create-pull-request` 경로에 있는 개인용 한국어 GitHub PR 생성 워크플로우. 사용자가 "$skillframe:create-pull-request", "PR 만들어줘", "pull request 만들어줘", "PR 올려줘", "/pr", "/create-pull-request", "$create-pull-request", 또는 "skillframe:create-pull-request"처럼 새 GitHub PR 생성을 요청하면 사용한다. 기존 PR 변경과 리뷰 작업은 이 스킬의 범위가 아니다. gh CLI와 git 상태를 점검하고, references의 title/body 규칙에 따라 한국어 PR을 작성한다. 실제 gh pr create 실행 전에는 반드시 사용자 승인을 받는다.
---

# Skillframe: Create Pull Request

새 GitHub PR을 리뷰어가 이해하기 쉬운 형태로 만든다. PR title과 body는 기본적으로
한국어로 작성하고, 세부 작성 규칙은 `references/`를 따른다.

이 스킬은 새 PR 생성에만 사용한다. 기존 PR 변경과 리뷰 작업은 다루지 않는다.

## 스킬 식별

- 설치 경로: `skills/create-pull-request/`
- 스킬 이름: `skillframe:create-pull-request`
- 컨텍스트: `skillframe`
- 호출 해석: `$skillframe:create-pull-request`를 기본 호출명으로 사용한다. `/pr`,
  `/create-pull-request`, `$create-pull-request`, `skillframe:create-pull-request`로
  호출된 경우에도 이 스킬을 "skillframe create-pull-request"로 식별한다.

## 절대 규칙

- 실제 `gh pr create` 실행 직전에는 반드시 사용자에게 title, base/head, body, draft 여부를 보여주고 승인받는다.
- 기존 PR이 있으면 업데이트하지 말고 기존 PR URL을 보고한 뒤 중단한다.
- `gh` 미설치, GitHub 미로그인, branch 미push 같은 문제는 즉시 중단 보고로 끝내지 말고 성공 가능한 다음 명령을 안내한다.
- 히스토리 재작성(`rebase`, `commit --amend`, squash, `push --force-with-lease`)은 명시 승인 없이 실행하지 않는다.
- 관련 없는 사용자 변경사항은 stage, commit, stash, discard, revert하지 않는다.
- 기본 생성 형태는 draft PR이다. 사용자가 ready PR을 명시하면 draft를 끈다.

## 기본 점검

- 저장소와 도구 상태를 `git rev-parse --show-toplevel`, `git status --short`,
  `git branch --show-current`, `gh --version`, `gh auth status`로 확인한다.
- `gh`가 없으면 macOS는 `brew install gh`, 그 외 환경은 `https://cli.github.com/`
  설치 안내를 제공한다.
- 로그인되어 있지 않으면 `gh auth login`을 안내한다.
- 현재 브랜치가 `main` 또는 `master`이면 기능 브랜치를 만들거나 전환하도록 안내한다.
  사용자가 원하면 `codex/` prefix를 기본으로 브랜치를 만든다.

## 컨텍스트 수집

- base branch를 `git remote show origin` 또는
  `git symbolic-ref refs/remotes/origin/HEAD --short`로 찾는다. 실패하면
  `main`, `master`, `develop` 순서로 확인한다.
- `git fetch origin`으로 원격 상태를 갱신한다.
- `gh pr view --json number,url,title,baseRefName,headRefName,state,isDraft`로
  현재 branch의 기존 PR을 확인한다. 있으면 새 PR을 만들지 않는다.
- `git log origin/<base>..HEAD --oneline --no-decorate`,
  `git diff origin/<base>..HEAD --stat`, `git diff origin/<base>..HEAD`로
  변경 범위와 의도를 분석한다.

작업 트리에 커밋되지 않은 변경이 있으면 PR에 포함할지 판단한다. 포함해야 하면
리뷰어 친화적인 커밋 단위로 stage/commit한다. 커밋 단위가 애매하거나 unrelated
변경이 섞여 있으면 사용자에게 묻는다.

## 커밋과 푸시

- PR에 필요한 변경이 아직 커밋되지 않았으면 이 스킬 안에서 커밋할 수 있다.
- 커밋 메시지는 가능하면 Conventional Commit을 사용하고 한국어 요약을 쓴다.
- 더 정교한 커밋 분리가 필요하면 skillframe의 `commit` 흐름을 따른다.
- branch가 원격에 없으면 PR 생성 전에 `git push -u origin HEAD`로 push한다.
- rebase 또는 squash가 필요해 보이면 이유와 위험을 설명하고 사용자 승인을 받은 뒤 실행한다.
- rebase 이후 push가 필요하면 `--force-with-lease`만 사용한다.

## PR 생성 흐름

1. title 후보를 만든다.
   - `references/pr-title.md`의 규칙을 따른다.
   - 리뷰어가 diff 방향을 예측할 수 있게 구체적으로 쓴다.

2. body를 만든다.
   - `references/pr-body.md`의 템플릿 탐색과 작성 규칙을 따른다.
   - 검증 섹션에는 실제 실행한 명령과 결과를 쓴다.
   - 검증하지 못한 항목은 "미실행"으로 명시하고 이유를 적는다.

3. 생성 전 승인 게이트를 연다.
   - PR title
   - base branch와 head branch
   - draft 여부
   - PR body 전체
   - push 여부와 현재 원격 branch 상태

4. 사용자가 승인한 뒤 임시 파일로 body를 저장하고 `gh pr create --title "<title>" --body-file /tmp/skillframe-create-pull-request-body.md --base <base>`로 생성한다. draft PR이면 `--draft`를 추가한다.

5. 생성 후 PR number 또는 URL만 핵심 결과로 보고한다. 필요한 경우 실행한 검증 명령을
짧게 덧붙인다.

## 오류 대응

- 커밋이 base보다 앞서 있지 않으면 다른 branch에서 작업했는지 확인한다.
- branch가 push되지 않았으면 `git push -u origin HEAD`를 실행하거나 안내한다.
- 기존 PR이 있으면 기존 PR URL을 보여주고 새 PR 생성을 중단한다.
- merge conflict가 있으면 충돌 파일을 보여주고 rebase 또는 merge 전략을 제안한다.
- PR body 템플릿을 찾지 못해도 중단하지 않고 `references/pr-body.md`를 따른다.

## 최종 보고

완료 보고는 간결하게 한다.

- 새 PR number/URL
- base/head와 draft 여부
- 실행한 핵심 검증 명령이 있으면 한 줄
