# Operations Phase

Operations Phase는 시스템의 **deployment, observability, maintenance**를 다룬다. AI가 telemetry(metric/log/trace)를 능동적으로 분석하고, runbook을 참조해 actionable recommendation을 제시한다. Developer는 validator로서 SLA / compliance 정렬을 보장한다.

green-field와 brown-field의 operations 활동은 동일하다.

---

## 1. Deployment

### 1.1 패키징
Construction Phase 출력물인 **Deployment Unit**(container image, Lambda artefact, Helm chart, IaC stack, 동반 테스트)을 그대로 사용한다.

### 1.2 승인 게이트
AI가 deployment configuration을 정리해 사용자에게 제시한다:
- 대상 환경: dev / staging / production
- 롤아웃 전략: blue/green, canary, rolling
- 롤백 시나리오 / abort 조건
- traffic shifting 비율

Developer가 이를 review/approve한 뒤에야 rollout 시작.

### 1.3 단계적 배포
staging → production 순서로 진행. 각 환경에서 smoke test와 NFR validation을 통과해야 다음 환경으로.

산출물: `aidlc-docs/deployment/<unit>/release-<version>.md` (배포 결과 기록)

---

## 2. Observability & Monitoring

### 2.1 활성 모니터링
AI는 다음 데이터를 능동 분석한다:
- **Metrics** — latency p50/p95/p99, error rate, throughput, saturation
- **Logs** — structured log의 anomaly detection, 빈도 변화
- **Traces** — span 분석, downstream dependency latency 분포

### 2.2 Anomaly Detection & SLA 예측
AI가 패턴을 학습/추론해 SLA violation 발생 가능성을 사전 경고. 예:
- "Peak hour 동안 recommendation API의 p95가 SLA 200ms를 초과할 것으로 예상 (현재 추세 기반). DynamoDB read capacity 1.5배 증설 권장."
- "특정 region에서 5xx error rate가 baseline 대비 4σ 상승."

### 2.3 산출물
- `aidlc-docs/operations/dashboards.md` — 어떤 metric/log/trace를 어디서 보는지
- `aidlc-docs/operations/alerts.md` — alert 정의, threshold, 라우팅
- `aidlc-docs/operations/anomaly_log/<date>.md` — 감지된 이상 기록

---

## 3. Incident Response with Runbooks

### 3.1 Runbook 통합
AI가 predefined runbook을 참조해 actionable recommendation을 만든다. 예:
- API 응답시간 저하 → "DynamoDB throughput 증설" 또는 "API Gateway traffic rebalance"
- Lambda concurrency 부족 → "reserved concurrency 상향"
- 데이터 정합성 의심 → "outbox 재처리 절차"

### 3.2 자동 실행 vs 승인 실행
- 사전 정의된 **safe action**(예: read-replica 추가)은 사용자 승인 후 AI가 실행 가능
- **destructive action**(예: rollback, data purge)은 사용자 명시적 confirmation 필수

### 3.3 산출물
- `aidlc-docs/operations/runbook/<scenario>.md` — 시나리오별 절차
- `aidlc-docs/operations/incidents/INC-NNNN.md` — incident 기록
- `aidlc-docs/operations/postmortem/PM-NNNN.md` — 사후 분석

---

## 4. Continuous Maintenance Loop

Operations는 일회성이 아니다. AI가 다음을 지속:
- dependency vulnerability scan & patch 제안
- cost anomaly 감지 (예상 대비 초과 사용)
- performance regression 추적 (배포 전후 baseline 비교)
- compliance drift 점검 (예: encryption-at-rest 누락 발생)

각 항목은 새 Unit 또는 Bolt로 backflow되어 Construction Phase로 돌아갈 수 있다.

---

## 5. Validator로서의 사람의 역할

Developer가 다음을 보장한다:
- AI의 insight/proposed action이 SLA, compliance, business priority와 정렬되는지
- runbook의 step이 destructive하지 않은지
- postmortem의 root cause 분석이 충분히 깊은지 (5 Why, fault tree)

---

## 완료 조건 (Definition of Done for Operations 셋업)

- [ ] Deployment 승인 gate가 사용자 confirmation 기록과 함께 통과됨
- [ ] dashboards/alerts 정의가 `operations/`에 저장됨
- [ ] runbook이 시나리오별로 1개 이상 작성됨
- [ ] incident 발생 시 사용할 escalation 경로가 명문화됨
- [ ] postmortem 템플릿이 준비됨
- [ ] AI가 자율 실행 가능한 action 목록과 사람 승인 필요 action 목록이 분리됨

---

## 함정 회피

- ❌ deployment 후 monitoring을 사람이 직접 짜겠다고 미루기 → AI에게 dashboard/alert 초안 작성 시키고 사람은 review
- ❌ runbook 없이 incident 대응 → AI 추천이 일관성 잃는다. runbook 작성도 새 Unit으로 처리
- ❌ AI가 destructive action을 자율 실행 → 사용자 명시 confirmation 없는 destructive는 금지
- ❌ postmortem을 chat에만 남기기 → 반드시 `operations/postmortem/`에 저장
