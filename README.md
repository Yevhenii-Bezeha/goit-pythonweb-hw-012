# FastAPI Contacts Management API

## 🚀 Overview
This project is a **FastAPI-based REST API** that allows users to manage their contacts. It includes authentication, email verification, JWT authorization, rate limiting, and avatar uploading via Cloudinary.

## 📌 Features
- **User Authentication & Authorization** (JWT-based)
- **User Registration with Email Verification**
- **CRUD Operations for Contacts**
- **User Rate Limiting** (SlowAPI)
- **CORS Support**
- **Cloudinary Integration for Avatar Uploads**
- **Docker & PostgreSQL Support**
- **Redis Caching**
- **Password Reset Functionality**
- **User Roles (Admin/User)**
- **Sphinx Documentation**

## 🛠 Tech Stack
- **Python 3.11**
- **FastAPI**
- **SQLAlchemy** (PostgreSQL)
- **JWT (PyJWT & OAuth2)**
- **Passlib (Password Hashing)**
- **Cloudinary (Image Uploads)**
- **Docker & Docker Compose**
- **SlowAPI (Rate Limiting)**
- **Redis (Caching)**
- **Sphinx (Documentation)**

## 🔧 Installation & Setup

### 1️⃣ **Clone the Repository**
```bash
git https://github.com/AnastasiaRiabova/goit-pythonweb-hw-12.git
cd goit-pythonweb-hw-12
```

### 2️⃣ **Create a Virtual Environment & Install Dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3️⃣ **Set Up Environment Variables**
Create a `.env` file and add:
```env
SECRET_KEY=
ACCESS_TOKEN_EXPIRE_MINUTES=
DATABASE_URL=
SMTP_SERVER=
SMTP_PORT=
SMTP_EMAIL=
SMTP_PASSWORD=
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
REDIS_HOST=
REDIS_PORT=
```

### 4️⃣ **Run with Docker Compose**
```bash
docker-compose up --build
```

### 5️⃣ **Run PostgreSQL & Redis Locally (without Docker Compose)**
If using Docker manually, run:
```bash
# PostgreSQL
docker run --name fastapi_db -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres

# Redis
docker run --name fastapi_redis -p 6379:6379 -d redis
```
Or start existing containers:
```bash
docker start fastapi_db fastapi_redis
```

### 6️⃣ **Run FastAPI Server**
```bash
uvicorn main:app --reload
```
The API will be available at: `http://127.0.0.1:8000`

## 📜 API Documentation

### Interactive Documentation
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

### Generated Documentation
To generate and view the Sphinx documentation:
```bash
cd docs
make html
```
The documentation will be available in `docs/_build/html/index.html`

## 🧪 Testing

### Running Tests
To run the tests with coverage reporting:
```bash
PYTHONPATH=$PYTHONPATH:. pytest tests/ -v --cov=. --cov-report=term-missing
```

### Test Coverage
Current test coverage:
- Overall: 84%
- `database.py`: 92%
- `main.py`: 69%
- `models.py`: 100%
- `tests/conftest.py`: 100%
- `tests/test_auth.py`: 100%
- `tests/test_contacts.py`: 100%

### Test Categories

#### Authentication Tests (`tests/test_auth.py`)
- Token creation
- Password verification
- User registration
- Duplicate user check
- Login functionality
- Invalid credentials handling
- Current user information
- Invalid token handling
- Password reset functionality
- User role verification

#### Contacts Tests (`tests/test_contacts.py`)
- Contact creation
- Contact list retrieval
- Single contact retrieval
- Contact update
- Contact deletion
- Unauthorized access handling
- Non-existent contact handling

## 🔐 Authentication & Authorization

### User Roles
- **User**: Standard user with basic access
- **Admin**: Administrator with additional privileges
  - Can change their avatar
  - Has full access to all features

### Password Reset
1. Request password reset:
   ```bash
   POST /forgot-password/
   ```
2. Check email for reset link
3. Reset password using the token:
   ```bash
   POST /reset-password/{token}
   ```

### Redis Caching
- User data is cached in Redis for 30 minutes
- Cache is automatically updated when user data changes
- Improves performance by reducing database queries

## 🛠 Development

### Code Style
The project follows PEP 8 guidelines. To check code style:
```bash
flake8 .
```

### Documentation
All functions and classes have docstrings following Google style. To generate documentation:
```bash
cd docs
make html
```

### Testing
To run specific test files:
```bash
PYTHONPATH=$PYTHONPATH:. pytest tests/test_auth.py -v
```

To run a specific test:
```bash
PYTHONPATH=$PYTHONPATH:. pytest tests/test_auth.py::test_login_success -v
```

## 📦 Dependencies
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- JWT
- Passlib
- Cloudinary
- Sphinx
- pytest
- pytest-cov
- flake8

## 🔒 Security
- JWT-based authentication
- Password hashing with bcrypt
- Rate limiting
- CORS protection
- Email verification
- Role-based access control

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact Management
- **Create Contact:** `