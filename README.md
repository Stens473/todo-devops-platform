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
├── docker-compose.yml      # PostgreSQL + FastAPI orchestration
├── init.sql               # Database initialization script
├── .dockerignore          # Docker build exclusions
├── .gitignore             # Git exclusions
├── static/
│   └── style.css          # External CSS stylesheet
└── templates/
    └── index.html         # Jinja2 HTML template
```

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

```bash
cd todo-devops-platform
docker-compose up --build
```

Access the app at: **http://localhost:8000**

To stop:
```bash
docker-compose down
```

To stop and remove all data:
```bash
docker-compose down -v
```

### Option 2: Local Development

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
