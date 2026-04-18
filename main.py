import os
import uuid
import time
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# ============================================================================
# Configuration
# ============================================================================

PORT = int(os.getenv("PORT", 8000))
HOST = "0.0.0.0"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://todo_user:todo_password@localhost:5432/todo_db")

# ============================================================================
# Database Setup - Base & Models FIRST
# ============================================================================

Base = declarative_base()

# ============================================================================
# Database Models
# ============================================================================

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    done = Column(Boolean, default=False)
    due_date = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

# ============================================================================
# Initialize Database with Retry Logic
# ============================================================================

def init_db():
    """Initialize database with retry logic."""
    max_retries = 10
    retry_count = 0

    while retry_count < max_retries:
        try:
            engine = create_engine(DATABASE_URL, echo=False)
            # Test connection
            with engine.connect() as conn:
                print("✅ Connected to PostgreSQL!")
                Base.metadata.create_all(bind=engine)
                print("✅ Tables created successfully!")
                return engine
        except Exception as e:
            retry_count += 1
            print(f"⏳ Waiting for PostgreSQL... (attempt {retry_count}/{max_retries})")
            if retry_count < max_retries:
                time.sleep(2)
            else:
                print(f"❌ Failed to connect to PostgreSQL after {max_retries} attempts")
                raise

engine = init_db()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ============================================================================
# Pydantic Models
# ============================================================================

class Task(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    done: bool = False
    due_date: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# ============================================================================
# Dependency
# ============================================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# Initialize FastAPI app
# ============================================================================

app = FastAPI(title="TODO Application")

# Setup static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# ============================================================================
# Helper Functions
# ============================================================================

def create_task(db: Session, title: str, description: Optional[str] = None, due_date: Optional[str] = None) -> Task:
    """Create a new task with a unique ID."""
    task_id = str(uuid.uuid4())
    task = TaskDB(
        id=task_id,
        title=title,
        description=description,
        done=False,
        due_date=due_date,
        created_at=datetime.now()
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return Task.from_orm(task)


def get_all_tasks(db: Session) -> list[Task]:
    """Get all tasks sorted by creation date (newest first)."""
    tasks = db.query(TaskDB).order_by(TaskDB.created_at.desc()).all()
    return [Task.from_orm(task) for task in tasks]


def toggle_task(db: Session, task_id: str) -> Optional[Task]:
    """Toggle the done status of a task."""
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if task:
        task.done = not task.done
        db.commit()
        db.refresh(task)
        return Task.from_orm(task)
    return None


def delete_task(db: Session, task_id: str) -> bool:
    """Delete a task by ID."""
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False


# ============================================================================
# Routes
# ============================================================================

@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    """Display all tasks."""
    tasks = get_all_tasks(db)
    today = datetime.now().date().isoformat()
    coming_soon = (datetime.now().date() + timedelta(days=3)).isoformat()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "tasks": tasks,
            "completed_count": sum(1 for t in tasks if t.done),
            "total_count": len(tasks),
            "today": today,
            "coming_soon": coming_soon
        }
    )


@app.post("/tasks")
async def create_new_task(
    request: Request,
    title: str = Form(...),
    description: str = Form(default=""),
    due_date: str = Form(default=""),
    db: Session = Depends(get_db)
):
    """Create a new task and redirect to home."""
    if title.strip():
        create_task(
            db=db,
            title=title.strip(),
            description=description.strip() if description else None,
            due_date=due_date if due_date else None
        )
    return RedirectResponse(url="/", status_code=303)


@app.post("/tasks/{task_id}/toggle")
async def toggle_task_endpoint(task_id: str, db: Session = Depends(get_db)):
    """Toggle the done status of a task."""
    toggle_task(db, task_id)
    return RedirectResponse(url="/", status_code=303)


@app.post("/tasks/{task_id}/delete")
async def delete_task_endpoint(task_id: str, db: Session = Depends(get_db)):
    """Delete a task."""
    delete_task(db, task_id)
    return RedirectResponse(url="/", status_code=303)


# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=HOST,
        port=PORT
    )
