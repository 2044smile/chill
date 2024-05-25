# chill

## Started

```cmd
# db.sqlite3 붙여넣기

docker build .
docker images
docker run -it -p 8001:8001 <IMAGE ID>

# URL 127.0.0.1:8001/swagger/

# POST /account/
{
  "user_id": "teacher4",
  "password": "teacher4",
  "status": "teacher"
}
## RESPOSNE 
{
  "id": 14,
  "user_id": "teacher4",
  "status": "teacher",
  "x_user_id": "39LI0GQcZ9"
}

# POST /hall/
{
  "teacher": 14,
  "available": 50,
  "is_closed": false
}
## RESPONSE
{
  "id": 4,
  "teacher": 14,
  "available": 50,
  "attend_code": "hV3qM",
  "x_room_id": "5EFgLid2FI",
  "is_closed": false
}
```

## Additional description

- Hall(강의장) Model 내에 정의 된 save() 메서드를 활용 했습니다. 🚀
- 회원(account) 서비스가 필요하다 판단하여 구현 했습니다. 🚀
  - 회원 정보 (status [student, teacher, admin])
  - X-USER-ID
- config/exceptions folder 예외 처리 구현 🚀

## Docker 🚀

- Docker 를 구현하여 테스트 진행 시 어느 환경에서든 손 쉽게 테스트를 진행할 수 있습니다.

```cmd
docker build .
docker images
docker run -it -p 8001:8001 <IMAGE ID>
```

## Install

```
python = "^3.10"
django = "^5.0.6"
djangorestframework = "^3.15.1"
drf-yasg = "^1.21.7" 🚀
```

### Tools

- Poetry 를 사용하여 프로젝트의 의존성을 관리 했습니다. 🚀
  - 프로젝트가 다양한 환경에서도 일관된 의존성을 유지합니다.
  - 호환 가능한 패키지 버전을 찾습니다.
- gitmoji(vscode) 커밋의 목적이나 의도를 쉽고 명확하게 알 수 있습니다. 🚀

## Model

- app
  - Hall
    - teacher(OneToOneField(User)) 
    - students(ManyToManyField(User))
      - ```limit_choices_to 를 이용하여 참조하는 모델이 하나 임에도 역할을 분담 할 수 있었다.```
    - available
      - ```최대 참석 가능 수강생을 설정```
    - attend_code
      - ```강의장 참석을 위한 코드(고유 값)```
    - is_closed
      - ```강의장 개설하면 False, 강의장 종료하면 True ```
    - x_room_id
      - ```HTTP Header```
  - BaseModel
    - created_at
    - updated_at
- account
  - User
    - user_id(unique=True)
    - password
    - statue
      - ```회원 정보(수강생, 강사, 관리자)```
    - x_user_id
      - ```HTTP Header```

### 구현 환경

- 어드민 페이지 🚀
  - ID: admin / PW: admin 
- UserViewSet 🚀
  - 유저 생성 (공통): 유저를 생성 시 status 를 추가하여 [수강생, 강사, 관리자] 를 구분 했습니다. /account
    - 유저 생성 시 x_user_id 가 발급 됩니다.
- HallViewSet
  - 강의장 개설 (강사): 강사가 새로운 강의장을 개설하는 엔드포인트입니다. POST /hall/
  - 강의장 종료 (강사): 강사가 자신의 강의장을 종료하는 엔드포인트입니다. DELETE /hall/{id}/
  - 강의장 조회 (공통): 강의장 정보를 조회하는 엔드포인트입니다. GET hall/{id}/
- StudentViewSet
  - 강의장 참석 (수강생): 수강생이 강의장에 참석하는 엔드포인트입니다. POST /student/

## exception

- 종료 된 강의장
- 수강생 인원 초과
- 본인이 작성한 강의에 등록 불가 🚀
- X-USER-ID, X-ROOM-ID 를 찾을 수 없을 때 🚀
