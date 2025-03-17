# 🚀 Kareer API Server

한국에서 직업을 얻고 싶은 외국인들을 도와주는 프로젝트 Kareer의 API 및 웹소켓 서버입니다. 개발 진행중이며, 2025년 4월 중에 어플 출시를 목표로 하고 있습니다.

---

## 🛠️ 기술 스택

- **Backend:** Django, Django Rest Framework (DRF)
- **Database:** MySQL (AWS RDS)
- **Authentication:** JWT (SimpleJWT)

## 📁 프로젝트 구조
```
.
├── authentication
│   ├── admin.py
│   ├── models.py
│   ├── interfaces.py
│   ├── strategies.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── common
│   ├── models.py
│   ├── utils.py
│   └── errors.py
├── users
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── services
│   │   └── user_whole_career_services.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── jobs
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── services
│   │   └── job_search_services.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
└── config
    ├── asgi.py
    ├── wsgi.py
    ├── settings.py
    └── urls.py
```

## 👩‍💻 만드는 이
윤유상 - Backend Developer

## 📄 라이센스
- MIT License
