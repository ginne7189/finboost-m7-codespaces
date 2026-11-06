# FinBoost M7 — Codespaces 실습

가상 송금 API로 정상 거래, 재요청, 오류, 이벤트와 Docker 실행 환경을 확인합니다. 실제 은행이나 결제사에 연결하지 않습니다.

[Codespaces에서 새 실습 환경 열기](https://codespaces.new/ginne7189/finboost-m7-codespaces)

1. GitHub 계정으로 로그인합니다.
2. 위 링크 또는 **Code → Codespaces → Create codespace on main**을 선택합니다.
3. 환경 구성이 끝나고 터미널을 사용할 수 있으면 [CODESPACES.md](CODESPACES.md)를 따릅니다.
4. 학습자용 HTML 교안 2~5단원의 명령을 같은 순서로 실행합니다. 여기서는 app.py가 있는 저장소 루트가 실습 폴더입니다.

Python 3.14와 Docker 엔진, Compose 및 Container Tools 확장은 `.devcontainer/devcontainer.json`에서 준비합니다. 첫 구성에는 다운로드 시간이 걸립니다. 개인별 사용 가능량과 수업 종료 후 Codespace 중지는 직접 확인합니다.

코드의 설명은 [docs/](docs/)에 있습니다. GitHub에 올리지 않는 것은 `.env`, 실습 DB, 개인별 실행 결과입니다.
