#!/usr/bin/env bash
# init_aidlc_workspace.sh — AI-DLC 표준 작업 폴더 트리를 생성한다.
#
# 사용법:
#   bash init_aidlc_workspace.sh <project-root>
# 예:
#   bash init_aidlc_workspace.sh ./my-app
#
# 멱등성을 가진다 — 이미 존재하는 폴더/파일은 보존한다.

set -euo pipefail

ROOT="${1:-.}"

if [[ ! -d "$ROOT" ]]; then
  echo "[AI-DLC] project root '$ROOT'가 존재하지 않습니다. 먼저 디렉토리를 만들어 주세요." >&2
  exit 1
fi

BASE="$ROOT/aidlc-docs"

DIRS=(
  "$BASE/plans"
  "$BASE/plans/bolts"
  "$BASE/requirements"
  "$BASE/story-artifacts"
  "$BASE/units"
  "$BASE/design-artifacts/domain"
  "$BASE/design-artifacts/logical"
  "$BASE/design-artifacts/adr"
  "$BASE/design-artifacts/reverse"
  "$BASE/risks"
  "$BASE/tests"
  "$BASE/deployment"
  "$BASE/operations/runbook"
  "$BASE/operations/incidents"
  "$BASE/operations/postmortem"
  "$BASE/operations/anomaly_log"
)

for d in "${DIRS[@]}"; do
  mkdir -p "$d"
done

# 빈 anchor 파일 — git이 빈 디렉토리를 보존하도록
for d in "${DIRS[@]}"; do
  if [[ -z "$(ls -A "$d" 2>/dev/null || true)" ]]; then
    : > "$d/.gitkeep"
  fi
done

# prompts.md 누적 로그 (없을 때만 생성)
if [[ ! -f "$BASE/prompts.md" ]]; then
  cat > "$BASE/prompts.md" <<'EOF'
# AI-DLC Prompts Log

이 파일은 본 프로젝트 세션에서 사용된 모든 표준 프롬프트를 시간 순으로 누적한다.
각 entry는 `## YYYY-MM-DD HH:mm — <phase> — <task>` 형태의 헤더로 구분한다.

EOF
fi

# README — 워크스페이스 안내
if [[ ! -f "$BASE/README.md" ]]; then
  cat > "$BASE/README.md" <<'EOF'
# aidlc-docs

이 폴더는 AI-Driven Development Lifecycle (AI-DLC) 산출물의 root다.

| 폴더 | 용도 |
|---|---|
| `plans/` | 단계별 plan md (checkbox 기반) |
| `plans/bolts/` | Bolt 단위 계획 |
| `requirements/` | intent, PRFAQ, measurement criteria |
| `story-artifacts/<unit>/` | user story와 acceptance criteria |
| `units/` | Unit 정의 |
| `design-artifacts/domain/` | Domain Model (DDD) |
| `design-artifacts/logical/` | Logical Design |
| `design-artifacts/adr/` | Architecture Decision Records |
| `design-artifacts/reverse/` | (brown-field) 역공학 산출물 |
| `risks/` | NFR, risk register matching |
| `tests/` | test plan, test result, validation report |
| `deployment/` | IaC, deployment unit manifest |
| `operations/runbook/` | 운영 시나리오별 절차 |
| `operations/incidents/` | incident 기록 |
| `operations/postmortem/` | 사후 분석 |
| `operations/anomaly_log/` | 이상 감지 로그 |
| `prompts.md` | 세션에서 사용된 표준 프롬프트 누적 |

본 구조는 `skills/ai-dlc/scripts/init_aidlc_workspace.sh`로 생성된다.
EOF
fi

echo "[AI-DLC] workspace ready at: $BASE"
ls -1 "$BASE"
