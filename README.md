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
### MacOS

# 실행 예시


# 코드 설명

