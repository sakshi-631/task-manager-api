from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = []
task_id_counter = 1

class Task(BaseModel):
    title: str
    description: str
    priority: str
    due_date: str
    completed: bool

@app.get("/")
def home():
    return {"message": "Hello FastAPI"}


@app.get("/tasks")
def get_tasks():
    return tasks


@app.post("/tasks")
def create_task(task: Task):
    global task_id_counter

    task_dict = task.dict()
    task_dict["id"] = task_id_counter

    tasks.append(task_dict)
    task_id_counter += 1

    return {"message": "Task added successfully"}


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            updated_dict = updated_task.dict()
            updated_dict["id"] = task_id

            tasks[i] = updated_dict
            return {"message": "Task updated successfully"}

    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            tasks.pop(i)
            return {"message": "Task deleted successfully"}

    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/tasks/search")
def search_tasks(keyword: str):
    result = [
        task for task in tasks
        if keyword.lower() in task["title"].lower()
    ]
    return result