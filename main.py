from fastapi import FastAPI, HTTPException

app = FastAPI()

# "מסד נתונים" בזיכרון
tasks = []
counter = 1

@app.get("/tasks")
def get_tasks(priority: int | None = None):
    if priority is None:
        return tasks
#
    if not 1 <= priority <= 3:
        raise HTTPException(
            status_code=400,
            detail="Priority must be from 1 to 3"
        )

    return [
        task
        for task in tasks
        if task.get("priority", 2) == priority
    ]

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks")
def add_task(task: dict):
    global counter

    priority = task.get("priority", 2)

    if type(priority) is not int or not 1 <= priority <= 3:
        raise HTTPException(status_code=400, detail="Priority must be an integer from 1 to 3")
    
    new_task = {
        "id": counter,
        "title": task.get("title"),
        "owner": task.get("owner"),
        "priority": priority
    }
    tasks.append(new_task)
    counter += 1
    return new_task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")
