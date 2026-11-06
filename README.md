# FinBoost 가상 송금 실습 v17

이 폴더와 HTML 교안을 함께 사용합니다. Python3.14로 로컬 실습하고 Docker 이미지는3.12를 사용합니다.
기본 API는 추가 패키지가 없습니다. JupyterLab을 사용할 때만 requirements-workspace.txt를 설치합니다.

## 먼저 읽기
1. docs/01_scope.md: 만들 기능과 성공 조건
2. docs/02_openapi.json: 실제 API 계약
3. docs/03_data_model.md: 세 테이블과 트랜잭션 경계
4. docs/04_test_matrix.md: 요구사항별 검사
5. docs/05_deployment.md: 실행/CI/운영의 차이

## 실행
같은 폴더의 터미널 A: python3.14 app.py
터미널 B: python3.14 client.py health
Windows는 python3.14 대신 py -3.14를 사용합니다.
DB는 data/lab.db, --save 결과는 evidence/파일명.json에 생성됩니다.
검사: python3.14 -m unittest -v

## 소스 안내
app.py는 HTTP 처리와 거래 로직, client.py는 요청과 결과 저장, worker.py는 후속 처리 상태 변경입니다.
학습 규모를 위해 한 API 파일에 모았으며 별도 controller/service/repository 디렉터리는 구현하지 않았습니다.
v17에서는 Python 파일의 줄바꿈과 들여쓰기를 정리했습니다. AST가 이전과 동일한지 비교했습니다.
실제 은행/결제사, 외부 알림, 운영용 원장, 사용자별 계좌권한은 구현하지 않았습니다.
실제 비밀키와 실계좌를 사용하거나 인터넷에 공개하지 않습니다.


## 환경 설정: 환경 분리 실습
python configure_lab.py --init
docker compose up -d --build api
docker compose run --rm --interactive=false client health
docker compose run --rm --interactive=false client transfer --key compose-001
docker compose logs --tail 20 api

자료의 5단원을 따라 포트 변경과 컨테이너 교체 후 기록 보존을 확인합니다.
.env는 로컬 Python에 자동 적용되지 않습니다. 실제 클라우드 배포는 하지 않습니다.

## 환경 전환 시 주의
1~4단원은 호스트 Python의 data/lab.db를 사용합니다. 5단원은 별도 Compose 볼륨의 새 DB를 사용합니다. 같은 소스코드여도 두 DB의 잔액과 거래는 자동 복사되지 않습니다.
configure_lab.py --init 뒤 --check로 실제 적용 설정을 확인합니다. 셸 환경변수가 .env보다 우선할 수 있습니다.
client의 request_id는 서버 로그와 대응하고 transfer_id는 성공한 업무 거래를 가리킵니다. 실패 응답에는 transfer_id가 없을 수 있습니다.
