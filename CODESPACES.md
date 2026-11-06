# Codespaces 환경 준비와 확인

수업의 실행 경로는 로컬 또는 Codespaces 중 하나입니다. Codespaces를 선택하면 내 컴퓨터에 Python과 Docker를 별도로 설치하거나 실습 ZIP을 풀지 않습니다. 이 저장소의 원격 개발 환경 안에 Python 3.14, Docker와 Compose가 준비됩니다.

이 문서는 **환경 준비만** 안내합니다. 서버 실행, 송금, Docker 이미지 빌드 명령은 HTML 교안의 **2~5단원**에서 순서대로 진행합니다. 두 안내를 번갈아 실행하지 않습니다.

## 1. 환경 열기

1. [실습 Codespaces 열기](https://codespaces.new/ginne7189/finboost-m7-codespaces)를 누르고 GitHub에 로그인합니다.
2. 저장소가 `ginne7189/finboost-m7-codespaces`인지 확인하고 환경을 만듭니다.
3. 환경 구성이 끝나고 브라우저의 VS Code 편집기가 열릴 때까지 기다립니다.
4. HTML 교안의 **실습 환경 준비 → 실습 환경 → Codespaces**를 선택합니다. 이후 같은 선택을 유지합니다.

## 2. 준비 상태 확인

상단 Terminal → New Terminal을 선택하고 아래 명령을 실행합니다.

```sh
pwd
python3.14 --version
python3.14 -c "from pathlib import Path; print(Path('app.py').is_file())"
docker version
docker compose version
```

확인할 결과:

- 경로: `/workspaces/finboost-m7-codespaces`
- Python: `3.14.x`
- 파일 확인: `True`
- Docker: Client와 Server가 모두 표시됨
- Compose: 버전이 표시됨

준비 중 연결 오류가 나면 환경 구성이 끝났는지 확인한 뒤 다시 실행합니다. `app.py`가 없으면 다른 폴더나 저장소를 연 상태인지 확인합니다.

**여기서는 서버를 켜지 않습니다.** 준비 후 HTML 교안 1단원으로 이동하고, 2단원에서 터미널 A/B를 열어 서버 실행과 연결 확인을 시작합니다.

## 선택: 내 컴퓨터의 VS Code로 연결

브라우저에서 작업할 수 있으면 이 단계는 필요 없습니다.

1. 내 컴퓨터의 VS Code에서 확장 화면을 엽니다.
2. **GitHub Codespaces** 확장(게시자 **GitHub**, 식별자 `GitHub.codespaces`)을 설치합니다.
3. 왼쪽 Remote Explorer에서 GitHub Codespaces를 선택하고, 환경을 만든 것과 같은 GitHub 계정으로 로그인합니다.
4. 본인의 실습 환경에 연결합니다. 연결된 창에서 위의 준비 확인 명령을 다시 실행합니다.

창은 내 컴퓨터에 열리지만 Python, Docker와 파일은 원격 Codespaces 환경에 있습니다. 로컬 폴더의 터미널과 섞지 않습니다.

[GitHub 공식 VS Code 연결 안내](https://docs.github.com/en/codespaces/developing-in-a-codespace/using-github-codespaces-in-visual-studio-code)

## 주소, 결과 저장과 종료

터미널에서 사용하는 `127.0.0.1`은 Codespaces 환경 자신입니다. `client.py` 요청에는 교안의 주소를 그대로 사용합니다. 브라우저로 API를 열 때만 Ports 탭의 전달 주소를 사용하고 포트 공개 범위는 Private을 유지합니다.

수업이 끝나면 evidence 폴더의 필요한 JSON 파일을 우클릭 → Download로 내려받고, 6단원 결과 HTML도 저장합니다. Docker 실습을 마쳤다면 `docker compose down`을 실행합니다. 이어서 [내 Codespaces 목록](https://github.com/codespaces)에서 해당 환경을 Stop으로 중지합니다. 브라우저나 VS Code 창만 닫는 것과 다릅니다.

중지 후에도 저장공간 사용량은 남습니다. 삭제하거나 개발 컨테이너를 재구성하기 전에는 필요한 결과를 내려받습니다. Docker 볼륨 보존 실습은 Codespaces 삭제 뒤 복구를 보장하지 않습니다.

GitHub 계정, 인터넷 연결과 개인별 Codespaces 사용 가능량이 필요합니다. Codespaces는 개발 환경이며, 이 수업에서 실제 은행 송금이나 AWS 운영 배포를 하지는 않습니다.
