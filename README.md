# 🚀 Kareer API Server

[한국어](#korean) | [English](#english)

# Korean

한국에서 직업을 찾는 외국인들을 위한 Kareer 플랫폼의 API 및 웹소켓 서버입니다. 현재 개발 진행 중이며 2025년 6월 출시를 목표로 하고 있습니다.

## 🌟 주요 기능

- 사용자 인증 및 권한 관리
- 이력서 관리 시스템
- 채용 정보 검색 및 필터링
- 실시간 채용 알림
- 기업-구직자 매칭 시스템
- 다국어 지원 (한국어/영어)
- AI 기반 한국 생활/문화 인사이트 제공

## 🛠 기술 스택

### 백엔드

- **프레임워크:** Django 5.1.7, Django REST Framework 3.15.2
- **데이터베이스:** MySQL (AWS RDS)
- **캐시:** Redis
- **태스크 큐:** Celery
- **인증:** JWT (SimpleJWT 5.5.0)
- **API 문서:** Swagger/ReDoc

### 데브옵스 & 인프라

- **컨테이너화:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **클라우드 서비스:** AWS (EC2, RDS, S3)
- **모니터링:** Django Silk

## 📁 프로젝트 구조

```
.
├── authentication/         # 인증 관련 기능
│   ├── admin.py
│   ├── models.py
│   ├── interfaces.py      # 인터페이스 정의
│   ├── strategies.py      # 인증 전략 패턴
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── common/                # 공통 유틸리티
│   ├── models.py
│   ├── utils.py
│   └── errors.py
├── insights/             # AI 기반 인사이트 수집/제공
│   ├── models.py
│   ├── tasks.py
│   ├── tests.py
│   ├── views.py
│   ├── processors/       # GPT 기반 텍스트 처리
│   └── crawlers/         # 데이터 수집
├── users/                 # 사용자 관리
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── services/
│   │   └── user_whole_career_services.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── jobs/                  # 채용 정보 관리
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── services/
│   │   └── job_search_services.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
└── config/               # 프로젝트 설정
    ├── asgi.py
    ├── wsgi.py
    ├── settings.py
    └── urls.py
```

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

### Docker 실행

```bash
docker-compose up --build
```

## 📚 API 문서

- Swagger UI: `http://localhost:8000/swagger/`

## 🧪 테스트

```bash
# 전체 테스트 실행
python manage.py test

# 커버리지 테스트 실행
coverage run manage.py test
coverage report
```

[![Anurag's GitHub stats](https://github-readme-stats.vercel.app/api?username=anuraghazra)](https://github.com/anuraghazra/github-readme-stats)

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

---

# English

API and WebSocket server for Kareer, a platform helping foreigners find jobs in Korea. Currently under development with a target launch date of June 2025.

## 🌟 Features

- User authentication and authorization
- Resume management
- Job posting search with advanced filtering
- Real-time job notifications
- Company-candidate matching system
- Multi-language support (KR/EN)
- AI-powered Korean life/culture insights

## 🛠 Tech Stack

### Backend

- **Framework:** Django 5.1.7, Django REST Framework 3.15.2
- **Database:** MySQL (AWS RDS)
- **Cache:** Redis
- **Task Queue:** Celery
- **Authentication:** JWT (SimpleJWT 5.5.0)
- **API Documentation:** Swagger/ReDoc

### DevOps & Infrastructure

- **Containerization:** Docker, Docker Compose
- **CI/CD:** GitHub Actions
- **Cloud Services:** AWS (EC2, RDS, S3)
- **Monitoring:** Django Silk

## 📁 Project Structure

```
.
├── authentication/         # Authentication related features
│   ├── admin.py
│   ├── models.py
│   ├── interfaces.py      # Interface definitions
│   ├── strategies.py      # Authentication strategy patterns
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── common/                # Common utilities
│   ├── models.py
│   ├── utils.py
│   └── errors.py
├── insights/             # AI-powered insight collection/provision
│   ├── models.py
│   ├── tasks.py
│   ├── tests.py
│   ├── views.py
│   ├── processors/       # GPT-based text processing
│   └── crawlers/         # Data collection
├── users/                 # User management
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── services/
│   │   └── user_whole_career_services.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── jobs/                  # Job posting management
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── services/
│   │   └── job_search_services.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
└── config/               # Project configuration
    ├── asgi.py
    ├── wsgi.py
    ├── settings.py
    └── urls.py
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Docker & Docker Compose
- MySQL 8.0+

### Local Development Setup

1. Clone the repository

```bash
git clone https://github.com/yourusername/kareer-server.git
cd kareer-server
```

2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables

```bash
cp .env.example .env
# Edit .env file with your configurations
```

5. Run database migrations

```bash
python manage.py migrate
```

6. Start development server

```bash
python manage.py runserver
```

### Docker Setup

```bash
docker-compose up --build
```

## 📚 API Documentation

- Swagger UI: `http://localhost:8000/swaggers/`

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run tests with coverage
coverage run manage.py test
coverage report
```

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
