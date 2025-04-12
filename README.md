# 🚀 Kareer API Server

한국에서 직업을 얻고 싶은 외국인들을 도와주는 프로젝트 Kareer의 API 및 웹소켓 서버입니다. 개발 진행중이며, 2025년 4월 중에 어플 출시를 목표로 하고 있습니다.

## 📋 목차

- [소개](#소개)
- [기술 스택](#기술-스택)
- [시작하기](#시작하기)
- [프로젝트 구조](#프로젝트-구조)
- [API 문서](#api-문서)
- [개발 가이드](#개발-가이드)
- [배포](#배포)
- [기여하기](#기여하기)
- [만드는 이](#만드는-이)
- [라이센스](#라이센스)

## 🎯 소개

Kareer는 한국에서 취업을 희망하는 외국인들을 위한 종합 취업 플랫폼입니다. 이 저장소는 Kareer의 백엔드 API 서버를 포함하고 있습니다.

### 주요 기능

- 사용자 인증 및 권한 관리
- 이력서 관리
- 채용 정보 검색 및 필터링
- 실시간 채용 알림
- 기업-구직자 매칭 시스템

## 🛠️ 기술 스택

### Backend

- **Framework:** Django 5.1.7, Django Rest Framework 3.15.2
- **Database:** MySQL (AWS RDS)
- **Authentication:** JWT (SimpleJWT 5.5.0)
- **API Documentation:** Swagger/ReDoc (Coming Soon)

### DevOps

- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Cloud:** AWS (RDS, EC2, S3)

### 개발 도구

- **Code Formatting:** Black, isort
- **Testing:** Django Test Framework
- **Version Control:** Git
- **Environment Management:** python-dotenv

## 🚀 시작하기

### 필수 요구사항

- Python 3.10+
- Docker & Docker Compose
- MySQL 8.0+

### 로컬 개발 환경 설정

1. 저장소 클론

```bash
git clone https://github.com/yourusername/kareer-server.git
cd kareer-server
```

2. 가상환경 생성 및 활성화

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

3. 의존성 설치

```bash
pip install -r requirements.txt
```

4. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일을 적절히 수정하세요
```

5. 데이터베이스 마이그레이션

```bash
python manage.py migrate
```

6. 개발 서버 실행

```bash
python manage.py runserver
```

### Docker를 이용한 실행

```bash
docker-compose up --build
```

## 📁 프로젝트 구조

```
.
├── authentication          # 인증 관련 기능
│   ├── admin.py
│   ├── models.py
│   ├── interfaces.py      # 인터페이스 정의
│   ├── strategies.py      # 인증 전략 패턴
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── common                 # 공통 유틸리티
│   ├── models.py
│   ├── utils.py
│   └── errors.py
├── users                 # 사용자 관리
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── services
│   │   └── user_whole_career_services.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── jobs                  # 채용 정보 관리
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── services
│   │   └── job_search_services.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
└── config               # 프로젝트 설정
    ├── asgi.py
    ├── wsgi.py
    ├── settings.py
    └── urls.py
```

## 📚 API 문서

API 문서는 Swagger/ReDoc을 통해 제공될 예정입니다. (개발 중)

- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

## 💻 개발 가이드

### 코드 스타일

- Black을 사용한 코드 포맷팅
- isort를 사용한 import 정렬
- Type hints 사용 권장

### 테스트

```bash
# 전체 테스트 실행
python manage.py test

# 특정 앱의 테스트 실행
python manage.py test users
```

### 브랜치 전략

- main: 프로덕션 환경
- develop: 개발 환경
- feature/\*: 새로운 기능 개발
- bugfix/\*: 버그 수정

## 🚀 배포

### Docker를 이용한 배포

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 환경 변수 설정

프로덕션 환경에서는 다음 환경 변수들이 필요합니다:

- `DJANGO_SETTINGS_MODULE`
- `SECRET_KEY`
- `DATABASE_URL`
- `ALLOWED_HOSTS`
- `DEBUG`

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👩‍💻 만드는 이

윤유상 - Backend Developer

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 📄 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
