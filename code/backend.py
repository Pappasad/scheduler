from flask import Flask, send_from_directory, request, jsonify

backend = Flask(__name__, static_folder='frontend')

@backend.route('/')
def home():
    return send_from_directory('frontend', 'index.html')

@backend.route('/frontend.js')
def serve_js():
    return send_from_directory('frontend', 'frontend.js')

@backend.route('/style.css')
def serve_css():
    return send_from_directory('frontend', 'style.css')

tasks = []

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
            task['completed'] = completed
            print(f"Task {task_id} updated to {'completed' if completed else 'not completed'}")
            break

    return jsonify({"status": "success"}), 200

def launchWebApp(input_tasks):
    """Launches the web app with dynamic tasks."""
    global tasks
    tasks = [{"id": idx + 1, "description": task, "completed": False} for idx, task in enumerate(input_tasks)]
    backend.run(debug=True)


# Run the application
if __name__ == '__main__':
    launchWebApp(['1', '2', 'N'])
