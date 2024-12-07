from flask import Flask, send_from_directory, request, jsonify
from threading import Thread, Lock

backend = Flask(__name__, static_folder='frontend')
WEB_ADDR = "http://127.0.0.1:5000"
LOCK = Lock()
tasks = []

@backend.route('/')
def home():
    return send_from_directory('frontend', 'index.html')

@backend.route('/frontend.js')
def serve_js():
    return send_from_directory('frontend', 'frontend.js')

@backend.route('/style.css')
def serve_css():
    return send_from_directory('frontend', 'style.css')

@backend.route('/tasks', methods=['GET'])
def routeTasks():
    return jsonify(tasks)

@backend.route('/update-task', methods=['POST'])
def update_task():
    """Endpoint to handle checkbox updates."""
    data = request.json
    task_id = data.get('id')
    completed = data.get('completed')

    # Update the corresponding task
    for task in tasks:
        if task['id'] == task_id:
            with LOCK:
                task['completed'] = completed
            print(f"Task {task_id} updated to {'completed' if completed else 'not completed'}")
            break

    return jsonify({"status": "success"}), 200

def launchWebApp(input_tasks):
    """Launches the web app with dynamic tasks."""
    global tasks
    tasks = [{"id": idx + 1, "description": task, "completed": False} for idx, task in enumerate(input_tasks)]

    # # Run Flask in a separate thread
    thread = Thread(target=backend.run, kwargs={'debug': True, 'use_reloader': False})
    thread.daemon = True  # Ensures the thread will close when the main program exits
    thread.start()
    #backend.run(debug=True)

    return WEB_ADDR

def getTasksFromWebApp():
    return tasks


# Run the application
if __name__ == '__main__':
    launchWebApp(['Example'])
