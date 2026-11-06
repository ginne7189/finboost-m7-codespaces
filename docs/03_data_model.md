# 데이터 모델과 저장 경계

실제 스키마는 app.py의 init_db에서 생성합니다.

| 테이블 | 컬럼 | 역할과 실제 제약 |
|---|---|---|
| accounts | id TEXT PRIMARY KEY | 가상 계좌 식별자 |
| accounts | balance INTEGER NOT NULL CHECK(balance>=0) | 원화 잔액 |
| transfers | key TEXT PRIMARY KEY | 멱등 요청 키 |
| transfers | payload TEXT NOT NULL | 정규화한 JSON 요청 문자열 |
| transfers | result TEXT NOT NULL | 거래번호, 금액 등을 담은 JSON 응답 문자열 |
| events | id TEXT PRIMARY KEY | 거래 생성 시 transfer_id와 같은 값 사용 |
| events | kind TEXT NOT NULL | transfer.accepted |
| events | processed INTEGER NOT NULL DEFAULT 0 | 0은 미처리, worker가 1로 변경 |

## 관계의 한계
foreign key는 선언되어 있지 않습니다. events.id와 응답의 transfer_id는 코드에서 같은 값을 넣는 논리적 관계입니다.
transfers에는 별도의 from_account/to_account 컬럼이 없으며 payload에 보관합니다.
이 구조는 복식부기 원장, 취소/환불 원장, 금융기관 정산 데이터를 구현한 것이 아닙니다.

## 한 번에 저장하는 작업
transfer에서 BEGIN IMMEDIATE 뒤 기존 키와 잔액을 확인합니다.
두 잔액 변경, transfers 결과, events 생성을 같은 트랜잭션에 묶습니다.
커밋이 끝난 뒤 HTTP 응답을 보냅니다. 한 DB 안의 경계이며 외부 금융기관까지 묶지는 않습니다.
