# fastapi-user-calculations

FastAPI-based calculator service with **user registration/login** and full **BREAD** (Browse, Read, Edit, Add, Delete) operations for calculations.

- **GitHub repository:**  
  https://github.com/pavankumarNagaraju/fastapi-user-calculations  

- **GitHub Actions (CI):**  
  https://github.com/pavankumarNagaraju/fastapi-user-calculations/actions  

- **Docker Hub repository:**  
  https://hub.docker.com/repository/docker/pavankumarnagarju/fastapi-user-calculations/general  

---

## Features

### User Routes

- `POST /users/register`  
  Register a new user with:
  - `email`
  - `full_name`
  - `password` (hashed before storing)

- `POST /users/login`  
  Validate credentials and return a success message + user ID if valid.

Password hashing uses **Passlib** with `pbkdf2_sha256` for secure storage.

### Calculation Routes (BREAD)

`/calculations` supports full CRUD:

- **Browse**: `GET /calculations/` – list all calculations  
- **Read**: `GET /calculations/{calc_id}` – get a single calculation  
- **Add**: `POST /calculations/` – create a calculation and compute result  
- **Edit**: `PUT /calculations/{calc_id}` – update operands/operation and recompute  
- **Delete**: `DELETE /calculations/{calc_id}` – remove a calculation

Supported operations (case-insensitive):

- `add`
- `subtract`
- `multiply`
- `divide` (returns 400 on division by zero)

---

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy ORM
- SQLite for local development/testing
- PostgreSQL in GitHub Actions CI
- Passlib (`pbkdf2_sha256`) for password hashing
- Pytest for integration tests
- Docker & Docker Compose
- GitHub Actions for CI/CD (tests + Docker Hub push)

---

## Project Structure (simplified)

```text
app/
  ├─ main.py               # FastAPI app & router registration
  ├─ database.py           # SessionLocal, Base, engine
  ├─ models.py             # SQLAlchemy models (User, Calculation)
  ├─ schemas.py            # Pydantic schemas for requests/responses
  ├─ security.py           # Password hashing & verification
  └─ routers/
       ├─ users.py         # /users/register and /users/login
       └─ calculations.py  # /calculations BREAD endpoints

tests/
  ├─ test_users_integration.py
  └─ test_calculations_integration.py

Dockerfile
docker-compose.yml
requirements.txt
pytest.ini
.github/workflows/python-app.yml
```

---

## Running Locally (Without Docker)

### 1. Clone the repo

```bash
git clone https://github.com/pavankumarNagaraju/fastapi-user-calculations.git
cd fastapi-user-calculations
```

### 2. Create and activate a virtual environment (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Ensure the app uses SQLite

By default, `app/database.py` uses:

```python
DATABASE_URL = "sqlite:///./test.db"
```

If you previously set `DATABASE_URL` in your environment (for Postgres), clear or override it in PowerShell:

```powershell
Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
# or explicitly:
$env:DATABASE_URL = "sqlite:///./test.db"
```

### 5. Run the application

```powershell
uvicorn app.main:app --reload
```

Then open:

- Swagger UI: http://localhost:8000/docs  
- ReDoc: http://localhost:8000/redoc  

From here you can manually test user registration/login and calculation endpoints.

---

## Running Tests Locally

By default, tests are executed against a local SQLite database (`test.db`).

If you have `DATABASE_URL` set, override it in your PowerShell session:

```powershell
$env:DATABASE_URL = "sqlite:///./test.db"
```

Then run:

```powershell
python -m pytest
```

The integration tests will:

- Register a new user and log in.
- Create, list, fetch, update, and delete a calculation via the API.

---

## Running with Docker Compose

The project includes a `docker-compose.yml` file that can run the FastAPI app and a Postgres service.

1. Make sure Docker Desktop is running.

2. From the project root, run:

```powershell
docker-compose up --build
```

3. Once the containers are up, open:

```text
http://localhost:8001/docs
```

You can test all endpoints directly from the Swagger UI inside the container.

---

## Using the Published Docker Image (from Docker Hub)

You can also run the image that is built and published by the GitHub Actions workflow:

1. Pull the image:

```bash
docker pull pavankumarnagarju/fastapi-user-calculations:latest
```

2. Run the container:

```bash
docker run -p 8000:8000 pavankumarnagarju/fastapi-user-calculations:latest
```

3. Open the API docs:

```text
http://localhost:8000/docs
```

---

## CI/CD with GitHub Actions

The CI workflow is defined in `.github/workflows/python-app.yml`.

For each push to the `main` branch, it:

- Checks out the repository.
- Sets up Python and installs dependencies.
- Starts a Postgres service and configures `DATABASE_URL`.
- Runs pytest.
- On success, logs in to Docker Hub using `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets.
- Builds and pushes the image tagged as:

```text
pavankumarnagarju/fastapi-user-calculations:latest
```

You can view all workflow runs at:

```text
https://github.com/pavankumarNagaraju/fastapi-user-calculations/actions
```

---

## Links

- GitHub repository:  
  https://github.com/pavankumarNagaraju/fastapi-user-calculations

- GitHub Actions runs:  
  https://github.com/pavankumarNagaraju/fastapi-user-calculations/actions

- Docker Hub repository:  
  https://hub.docker.com/repository/docker/pavankumarnagarju/fastapi-user-calculations/general
