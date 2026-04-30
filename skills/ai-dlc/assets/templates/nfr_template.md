---
artefact_type: nfr
unit: <unit_name or "global">
status: draft
---

# Non-Functional Requirements

> 정량 가능한 기준만 둔다. 모호한 형용사("빠른") 금지.

## Performance
- latency p50 / p95 / p99: <ms>
- throughput: <req/s>
- cold start tolerance: <ms or n/a>

## Scalability
- concurrent users: <수치>
- 데이터 volume 성장률: <GB/month>
- horizontal vs vertical 전략: <명시>

## Availability
- SLA: <99.9% 등>
- RPO / RTO: <시간>

## Reliability
- 실패 시 graceful degradation 정책: <캐시 사용 / 빈 응답 / fallback>
- retry policy / backoff: <명시>

## Security
- authn / authz: <메커니즘>
- encryption at rest: <KMS key 정책>
- encryption in transit: <TLS 버전>
- secret 관리: <Secrets Manager / Parameter Store>
- 데이터 분류 및 PII 처리: <명시>

## Privacy / Compliance
- GDPR / CCPA / 국내 PIPA 등 적용 범위
- 데이터 보존/삭제 정책

## Observability
- 필수 metric: <목록>
- 필수 log structure: <필드>
- 필수 trace span: <목록>

## Cost
- monthly budget ceiling: <$>
- cost-per-request 목표: <$>

## Operability
- 배포 빈도 목표: <per day>
- rollback 시간 목표: <분 이내>
