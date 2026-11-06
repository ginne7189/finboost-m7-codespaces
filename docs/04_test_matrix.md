# 요구사항과 검사 기준

| 시나리오 | 기대 결과 | 자동 검사 |
|---|---|---|
| 정상 10000원 송금 | 201, 잔액90000/30000 | test_success |
| 같은 요청 재시도 | 200, 동일 거래ID, 잔액 유지 | test_replay |
| 같은 키와 다른 금액 | 409 | test_conflict |
| 잔액 초과 | 422, 초기 잔액 유지 | test_insufficient |
| 잘못된 금액 자료형/범위 | 400 | test_invalid_amounts |
| 없는 계좌 | 404 | test_missing_account |
| 키 없음 | 400 | test_missing_key |
| DB 재초기화 후 기존 요청 | 200 | test_restart_persistence |
| 동일 키 동시4요청 | 201 한 번, 200 세 번, 잔액 보존 | test_concurrent_replay |
| worker 재실행 | 처리1건 뒤0건 | test_worker_replay |
| HTTP 기본 경로 | health200, 무인증401, 잘못된JSON400 | test_http_auth_json_paths |

python -m unittest -v 로 실행합니다. 실제 OS 프로세스 재시작, 컨테이너 볼륨,
은행/API 연계, 네트워크 응답 유실은 위 자동 검사의 검증 범위를 넘어섭니다.
재시작 DB 검사는 init_db를 다시 호출하는 검사입니다. 컨테이너 재시작은 교안의 별도 실습입니다.
ResourceWarning 등이 있으면 테스트 성공 여부와 별도로 원인을 확인합니다.
