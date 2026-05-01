import requests

API_URL = "http://127.0.0.1:8000/tasks"

def get_tasks():
    try:
        res=requests.get(API_URL)
        res.raise_for_status() 
        return res.json()
    except Exception as e:
        return[]

def add_task(title,description,priority,due_date):
    try:
        data={
            "title":title,
            "description":description,
            "priority":priority,
            "due_date":due_date,
            "completed":False
        }
        requests.post(API_URL,json=data)
        return True
    except:
        return False
    
def delete_task(task_id):
    try:
        requests.delete(f"{API_URL}/{task_id}")
        return True
    except:
        return False

def update_task(task_id, title,description,priority,due_date,completed):
    try:
        data={
            "title":title,
            "description":description,
            "priority":priority,
            "due_date":due_date,
            "completed":completed
        }
        requests.put(f"{API_URL}/{task_id}",json=data)
        return True
    except:
        return False

def search_tasks(keyword):
    try:
        res=requests.get(f"{API_URL}/search?keyword={keyword}",timeout=5)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        return []

    
