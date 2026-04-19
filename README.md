# TODO Application

A modern TODO web application built with **FastAPI**, **PostgreSQL**, and **Docker**. Features a responsive 2-column layout with a form on the left and a scrollable task list on the right.

## Features

- ✅ Create tasks with optional descriptions and due dates
- ✅ Mark tasks as done/undone with visual feedback
- ✅ Delete tasks with confirmation
- ✅ Track completion progress (X/Y tasks completed)
- ✅ Persistent data storage with PostgreSQL
- ✅ Responsive 2-column UI (form left, list right)
- ✅ Task due date tracking with overdue indicators
- ✅ Clean, modern design with smooth interactions
- ✅ Fully containerized with Docker Compose
- ✅ Easy deployment ready

## Project Structure

```
todo-devops-platform/
├── main.py                  # FastAPI application with SQLAlchemy ORM
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker container configuration
├── docker-compose.yml      # PostgreSQL + FastAPI orchestration (uses .env)
├── init.sql               # Database initialization script
├── .env                   # Environment variables (DO NOT COMMIT)
├── .env.example          # Example environment template (for documentation)
├── .gitlab-ci.yml        # GitLab CI/CD pipeline configuration
├── .dockerignore         # Docker build exclusions
├── .gitignore            # Git exclusions
├── static/
│   └── style.css         # External CSS stylesheet
└── templates/
    └── index.html        # Jinja2 HTML template
```

## Environment Configuration

### Setup

1. **Copy the example environment file:**

```bash
cp .env.example .env
```

2. **Edit `.env` with your settings:**

```bash
# Application
PORT=8000
HOST=0.0.0.0

# PostgreSQL
POSTGRES_USER=todo_user
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=todo_db
DATABASE_URL=postgresql://todo_user:your_secure_password_here@postgres:5432/todo_db
```

⚠️ **IMPORTANT**: Never commit the `.env` file! It's included in `.gitignore` to protect sensitive data.

### Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Application server port | 8000 |
| `HOST` | Server host binding | 0.0.0.0 |
| `POSTGRES_USER` | Database username | todo_user |
| `POSTGRES_PASSWORD` | Database password | *(required)* |
| `POSTGRES_DB` | Database name | todo_db |
| `DATABASE_URL` | Full PostgreSQL connection string | *(auto-generated)* |

---

## Technology Stack

- **Backend**: FastAPI + Uvicorn
- **Database**: PostgreSQL 15 + SQLAlchemy ORM
- **Frontend**: HTML + CSS (no frameworks)
- **Containerization**: Docker + Docker Compose
- **Template Engine**: Jinja2

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Or: Python 3.11+ & PostgreSQL 15+

### Option 1: Docker Compose (Recommended) 🐳

**Development:**
```bash
cd todo-devops-platform
docker-compose up --build
```

**Production:**
```bash
cd todo-devops-platform
docker-compose -f docker-compose.prod.yml up -d
```

Access the app at: **http://localhost:8000**

To stop:
```bash
# Development
docker-compose down

# Production
docker-compose -f docker-compose.prod.yml down
```

To stop and remove all data:
```bash
# Development
docker-compose down -v

# Production
docker-compose -f docker-compose.prod.yml down -v
```

### Development vs Production

**Development** (`docker-compose.yml`):
- Builds image locally
- Mounts code as volume (live reload)
- Uses default PostgreSQL settings
- Good for local development

**Production** (`docker-compose.prod.yml`):
- Uses pre-built image from GitLab Registry
- No volume mounts (immutable container)
- Optimized PostgreSQL settings (256MB shared buffers)
- Health checks enabled
- Auto-restart on failure
- Proper networking with bridge network
- Security options enabled
- Better resource management

---

## Option 2: Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Setup PostgreSQL:**
```bash
# Create database and user
createdb -U postgres todo_db
createuser todo_user
```

3. **Run the app:**
```bash
export DATABASE_URL="postgresql://todo_user:todo_password@localhost:5432/todo_db"
python main.py
```

The app will start on `http://localhost:8000`

## Environment Variables

- `PORT` - Server port (default: 8000)
- `DATABASE_URL` - PostgreSQL connection string (default: `postgresql://todo_user:todo_password@localhost:5432/todo_db`)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Display all tasks |
| POST | `/tasks` | Create a new task |
| POST | `/tasks/{task_id}/toggle` | Toggle task completion |
| POST | `/tasks/{task_id}/delete` | Delete a task |

## Database Schema

### Tasks Table

```sql
CREATE TABLE tasks (
    id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    description VARCHAR,
    done BOOLEAN DEFAULT FALSE,
    due_date VARCHAR,
    created_at TIMESTAMP NOT NULL
);
```

## Production Deployment

### Prerequisites

- GitLab Runner configured
- Docker and Docker Compose installed
- GitLab Container Registry access

### Steps

1. **Pull latest image:**
   ```bash
   docker login registry.gitlab.com
   docker pull registry.gitlab.com/stens473-group/todo-devops-platform:latest
   ```

2. **Setup environment:**
   ```bash
   cp .env.example .env
   # Edit .env with production values
   vim .env
   ```

3. **Start services:**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Verify deployment:**
   ```bash
   docker-compose -f docker-compose.prod.yml ps
   curl http://localhost:8000
   ```

5. **View logs:**
   ```bash
   docker-compose -f docker-compose.prod.yml logs -f todo-app
   ```

### Maintenance

**Backup database:**
```bash
docker-compose -f docker-compose.prod.yml exec postgres \
  pg_dump -U todo_user todo_db > backup_$(date +%Y%m%d).sql
```

**Update to new version:**
```bash
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

---

## CI/CD Pipeline (GitLab)

The project includes an automated GitLab CI/CD pipeline (`.gitlab-ci.yml`) with the following stages:

### Build Stage
- Builds Docker image
- Pushes to GitLab Container Registry
- Triggers on: `main` branch and tags
- Tags: `$CI_COMMIT_SHORT_SHA` and `latest`

### Test Stage
- **Docker Compose Test**: Validates docker-compose setup
- **Linting**: Python code quality checks (flake8, pylint)
- Triggers on: `main` branch and merge requests

### Deploy Stage
- Manual trigger for production deployment
- Provides deployment instructions
- Triggers on: `main` branch and tags (when manually triggered)

### Setup GitLab CI/CD

1. **Ensure GitLab Runner is configured:**
   ```bash
   gitlab-runner register
   ```

2. **Configure container registry credentials** in GitLab (Settings → CI/CD → Variables)

3. **Pipeline will automatically run** on:
   - Push to `main` branch
   - Creation of tags
   - Merge requests to `main`

### View Pipeline Status

- Navigate to: **CI/CD → Pipelines** in your GitLab project
- Check logs in each job for details

---

## Database Schema

## Development

### Making Changes

- **Backend logic**: Edit `main.py`
- **Frontend UI**: Edit `templates/index.html`
- **Styling**: Edit `static/style.css`

### Hot Reload (Development)

For local development with auto-reload:

```bash
pip install uvicorn[standard]
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database Migrations

SQLAlchemy automatically creates tables on startup. For manual database access:

```bash
# Access PostgreSQL container
docker exec -it todo-postgres psql -U todo_user -d todo_db

# Query tasks
SELECT * FROM tasks;
```

## Troubleshooting

### Port already in use

Change the port in `docker-compose.yml`:
```yaml
ports:
  - "3000:8000"  # Use 3000 instead of 8000
```

### Database connection issues

Rebuild with clean state:
```bash
docker-compose down -v
docker-compose up --build
```

### Static files not loading

Ensure `static/` directory exists and contains `style.css`

## Performance Notes

- Tasks are loaded on each page refresh
- Database queries use indexing on `id` and `created_at`
- Suitable for small to medium workloads
- For high-volume usage, consider adding caching (Redis) or pagination

## Security

⚠️ **Important Security Considerations:**

1. **Never commit `.env` file** - Contains sensitive database credentials
2. **Use `.env.example`** as a template for new developers
3. **In production**:
   - Use strong, randomly generated passwords for `POSTGRES_PASSWORD`
   - Use environment secrets in GitLab CI/CD (Settings → CI/CD → Variables)
   - Never store secrets in code or container images
   - Use a secrets management solution (HashiCorp Vault, AWS Secrets Manager, etc.)
4. **Database access**:
   - Only expose database internally (not to internet)
   - Use strong network policies and firewalls
   - Consider adding SSL/TLS for database connections

---

## Future Enhancements

- User authentication & multi-user support
- Task categories/tags
- Task priority levels
- Recurring tasks
- Task notifications
- API documentation (Swagger/OpenAPI)
- Unit & integration tests
- CI/CD pipeline

## License

MIT

## Contributing

Feel free to submit issues and enhancement requests!
