# PR Title Rules

PR title은 커밋 메시지와 비슷한 Conventional Commit 형태를 사용한다.

## 형식

JIRA 티켓이 있는 경우:

```text
<type>(<scope>): <TICKET>, <한국어 요약>
```

JIRA 티켓이 없는 경우:

```text
<type>(<scope>): <한국어 요약>
```

scope는 선택 사항이다. 변경 범위가 하나의 도메인, 화면, 기능, 패키지, 스킬로
분명할 때만 사용한다. 유용한 scope가 없으면 생략한다.

## Type 선택

type은 PR 전체 diff의 주된 성격을 기준으로 정한다. 여러 커밋이 섞여 있으면
리뷰어가 이 PR을 어떤 변경으로 봐야 하는지를 우선한다.

허용되는 type:

- `feat`: 새 기능, 새 사용자 흐름, 새 스킬/도구 동작
- `fix`: 버그 수정, 잘못된 동작 보정
- `refactor`: 의도한 동작 변화 없는 구조 개선
- `docs`: 문서만 변경
- `test`: 테스트만 변경
- `chore`: 제품 동작과 무관한 유지보수
- `build`: 빌드, 패키지, 의존성 변경
- `ci`: CI, 배포 자동화 변경
- `style`: 포맷팅만 변경
- `revert`: 이전 변경 되돌림

## 요약

요약은 한국어로 작성하고, 제목만 보고 diff 방향을 예측할 수 있게 쓴다.
`작업`, `수정`, `정리`, `기능 개선`처럼 범위가 흐린 단어만으로 끝내지 않는다.

좋은 예시:

```text
feat(visit-log): PE-107, 상담록 도메인 분류와 방문예정 UI 정비
feat: PE-108, 방문 로그 템플릿 관리 기능 추가
fix(contact): 중복 연락처 생성 방지
docs(skillframe): commit/pull-request 스킬 호출명 문서화
```
