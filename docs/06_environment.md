# 같은 코드와 다른 실행 설정

## 로컬 Python
app.py는 LAB_HOST, LAB_PORT, LAB_DB_PATH, LAB_TOKEN 환경변수를 읽습니다. 명령행 --host, --port, --db가 있으면 그 값이 우선합니다. client.py는 LAB_BASE_URL과 LAB_TOKEN을 읽으며 --base가 우선합니다. 로컬 Python은 .env를 자동으로 읽지 않습니다.

## Docker Compose
configure_lab.py --init은 .env.example을 .env로 복사합니다. 기존 .env는 덮어쓰지 않습니다. Compose가 .env의 값을 compose.yaml에 치환하고 environment를 통해 컨테이너에 전달합니다. 같은 이름의 셸 환경변수가 있으면 파일보다 우선할 수 있습니다.
LAB_HOST_PORT는 내 PC의 포트입니다. API 컨테이너는 항상 8000을 사용합니다. LAB_DB_PATH는 반드시 볼륨 경로 /app/data 아래로 둡니다.

## 데이터와 비밀값
.env와 실제 DB, evidence는 Git 및 이미지에 포함하지 않습니다. .env.example에는 교육용 값만 넣습니다. 환경변수는 그 자체로 비밀 저장소가 아니며 운영에서는 접근 제어가 있는 비밀값 관리가 필요합니다.
docker compose down은 이 실습에서 컨테이너와 네트워크를 제거하며 이름 있는 볼륨은 보존합니다. down -v는 데이터를 지우므로 실습 중 사용하지 않습니다. 재시작/교체는 백업 검증이나 서버 장애 복구 검증을 대신하지 않습니다.

## 클라우드 전환 설계
SQLite 파일을 여러 서버의 각 로컬 디스크에 복사하면 거래 상태가 갈라집니다. 공통 DB를 선택하고 요청 키의 유일성, 트랜잭션 격리, 동시성, 재시도 정책을 해당 DB에서 재설계하고 검사해야 합니다. 공통 DB만 연결한다고 자동으로 정확해지지 않습니다.
현재 로그는 request_id, path, status, transfer_id, error를 출력합니다. 비밀 토큰과 요청 본문을 로그에 남기지 않습니다. 운영에서는 수집, 검색, 보존, 접근 권한을 추가로 설계합니다.
cloud-plan.mmd는 설계 초안입니다. AWS 자원을 생성하거나 배포하지 않습니다.

## 서로 다른 실습 DB
호스트 Python은 data/lab.db, Compose는 이름 있는 lab-data 볼륨을 사용합니다. 새 Compose 실습의 초기 잔액은 다시 100000/20000입니다. 기존 볼륨이면 현재 잔액을 기준으로 변화량을 비교합니다. 호스트 worker.py는 Compose 볼륨에 연결하지 않으므로 5단원의 데이터에 적용하지 않습니다.
## 설정 검사
configure_lab.py --check는 docker compose config의 실제 적용 값을 내부에서 읽고 토큰 일치, DB 경로와 로컬 바인딩을 검사합니다. 토큰은 출력하지 않습니다. 직접 config 명령의 전체 결과를 공유하지 않습니다.
