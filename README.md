# 5점/10점 짜리 프로젝트

# 구현 목표
###  본 프로젝트는 닌텐도에서 처음 나온 "수박 게임(suica game)"이 목적이며, 과일을 떨어뜨려서 같은 과일이 합쳐지는 것을 이용해서 더 큰 과일을 만드는 것이 게임의 목표입니다. 게임 종료 조건은 '수박 과일'이 만들어 진 경우 승리하며, 일정 높이 이상 과일이 넘어가게 되면 패배합니다.

# 구현 기능

* pygame, box2d 기반 게임 board(환경) 구현
* 키보드 입력으로 과일 조준 기능
* 동일 과일이 충돌 시 합쳐지는 기능

# Reference
[1] https://github.com/pybox2d/pybox2d "pybox2d" 

[2] https://github.com/pygame/pygame "pygame"

# 지원 Operating Systems 및 실행 방법

## 지원 Operating Systems
|OS| 지원 여부 |
|-----|--------|
|windows | :o:  |
| Linux  | :x: |
|MacOS  | :x:  |

## 실행 방법
### Windows

1. python3.12를 설치한다
2. swiging을 설치한다
```
1. https://sourceforge.net/projects/swig/files/swigwin/swigwin-3.0.2/swigwin-3.0.2.zip/download 에서 파일 다운로드

2. C:\ 경로에 압축해제

3. 시작 > 시스템 환경변수 > 환경 변수... > 시스템 변수, Path, 편집 > 새로만들기, 편집 C:\swigwin-3.0.2 추가 
```
3. Microsoft Visual c++ Build Tools 설치
```
1. https://visualstudio.microsoft.com/ko/visual-cpp-build-tools/ 에서   Build Tools 다운로드 후 실행

2. Visual Studio Installer가 실행 된 경우 해당 버전의 "수정(Modify)" 클릭

3. Desktop & Mobile 에서 c++ build Tools 체크 표시 이후 설치

4. 시스템 재부팅
```
4. powershell 창에서 아래 pip3 library를 설치

```
pip3 install pygame
pip3 install box2d box2d-kengz
```

5. 재부팅 이후 python3 main.py를 실행하면 게임 창이 뜨면서 실행됨.

### Linux

1. Docker를 설치한다.
2. Dockerfile을 build한다
   ```
   docker build -t watermelon:0.1 .
   ```
3. docker container를 실행한다
   ```
   docker run -it watermelon:0.1 /bin/bash
   ```
4. workspace 폴더 내에서 게임을 실행한다. (검증x)
   ```
   cd workspace
   python3 main.py
   ```


### MacOS

# 실행 예시
<span style="color:red">동영상 업로드 시 gif로 변환 후 링크를 삽입</span>
<span style="color:red">아래 홈페이지 참고 : https://onlydev.tistory.com/15 </span>

![example](https://github.com/RmKuma/oss_personal_project_phase1/assets/20412048/98ecfe0c-34c5-4592-86e9-defded705a36)

# 코드 설명
## main.py
### class WatermelonGame
- Description : watermelon 게임을 수행하는 메인 클래스
  1. Def __init__ : 최초 게임을 초기화하는 단계, screen, world, contact_listener, watermelons(과일 body를 저장) 등을 초기화함.
  2. Def create_ground : 아래, 좌, 우의 벽(바운더리)를 생성하여 과일이 화면밖으로 나가는 것을 방지

### class ContactListener
- Description : 과일 간의 충돌을 탐지하는 ContactListener
  1. Def BeginContact() : 충돌 시 자동으로 실행되는 box2d 함수, 충돌 된 두 과일의 body를 to_destroy 어레이에 저장한다.
 

# TODO List
* 점수 계산하기
* 게임 끝나는 조건 추가하기
* 좌우 키를 누르고 있으면 빠르게 이동하기
* start, end, restart, menu 버튼 추가하기