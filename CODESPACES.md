# Codespaces에서 시작하기

GitHub 로그인 → 이 저장소의 Code → Codespaces → Create codespace on main을 선택합니다.
설정과 확장 설치가 끝나고 터미널을 사용할 수 있을 때 시작합니다.

## 1. 같은 폴더에서 터미널 두 개 사용

터미널 A:
```sh
python3.14 --version
python3.14 app.py
```
서버를 켜 둡니다. 터미널 패널의 +로 B를 엽니다.

터미널 B:
```sh
python3.14 client.py health --save 01-health.json
python3.14 client.py accounts --save 02-before.json
```
이후 교안 2~4단원의 명령을 같은 순서로 실행합니다. 10000원 송금, 재요청, 오류와 worker 처리 기준은 같습니다.

## 2. Docker 실습
```sh
docker version
docker compose version
python3.14 configure_lab.py --check
docker compose up -d --build api
docker compose run --rm --interactive=false client health
```
이후 교안 5단원대로 진행합니다. Codespaces 안에서 띄운 Docker 컨테이너와 로컬 PC의 Docker는 별개입니다.
터미널의 localhost는 Codespaces 환경 자신입니다. 브라우저로 API를 보려면 Ports 탭의 해당 포트 주소를 엽니다. 포트 공개 범위는 Private을 유지합니다.

## 3. 결과 보관과 종료

evidence 폴더의 필요한 JSON 파일을 우클릭해 Download로 내려받습니다. 제출 문서는 별도로 저장합니다.
`docker compose down`은 실습 컨테이너를 종료하는 명령입니다. 그 뒤 GitHub의 Codespaces 목록에서도 해당 Codespace의 Stop을 선택해야 개발 환경 실행이 멈춥니다.
Codespace를 삭제하거나 개발 컨테이너를 재구성하기 전에는 결과를 내려받습니다. Docker 내부 볼륨 보존을 Codespaces 삭제 뒤 복구까지 보장하는 것으로 해석하지 않습니다.

## 이용 조건

GitHub 계정, 인터넷 연결, Codespaces 사용 가능량이 필요합니다. 개인별 무료 사용량과 조직 정책을 사전에 확인합니다. 이 환경은 개발 실습용이며 실제 은행 송금과 운영 클라우드 배포는 하지 않습니다.
