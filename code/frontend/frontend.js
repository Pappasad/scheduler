// SchedulerApp.js
class SchedulerApp {
    constructor() {
        this.tasks = [];
        this.header_text = 'Scheduler';
    }

    async fetchTasks() {
        try {
            const response = await fetch('/tasks');
            this.tasks = await response.json();
        } catch (error) {
            console.error('Error fetching tasks:', error);
        }
    }

    createHeader() {
        const header = document.createElement('header');
        header.style.width = '100%';
        header.style.textAlign = 'center';
        header.style.padding = '20px 0';

        const titleElement = document.createElement('h1');
        titleElement.textContent = this.header_text;
        titleElement.style.fontSize = '3rem';
        titleElement.style.color = 'black';
        titleElement.style.margin = '0';

        header.appendChild(titleElement);
        document.body.insertBefore(header, document.body.firstChild);
    }

    createTaskList() {
        let taskListContainer = document.getElementById('task-list-container');
    
        // Create the container if it doesn't exist
        if (!taskListContainer) {
            taskListContainer = document.createElement('div');
            taskListContainer.id = 'task-list-container';
            taskListContainer.style.margin = '40px auto'; // Space below the header
            taskListContainer.style.maxWidth = '600px';
            taskListContainer.style.padding = '20px';
            taskListContainer.style.backgroundColor = '#f9f9f9';
            taskListContainer.style.borderRadius = '8px';
            taskListContainer.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
            document.body.appendChild(taskListContainer);
        }

        taskListContainer.innerHTML = '';
    
        this.tasks.forEach((task) => {
            const taskLabel = document.createElement('div');
            taskLabel.className = 'task-label';
            taskLabel.style.display = 'flex';
            taskLabel.style.alignItems = 'center';
            taskLabel.style.padding = '10px';
            taskLabel.style.borderBottom = '1px solid #ddd';
    
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.style.marginRight = '15px';
    
            const taskDesc = document.createElement('div');
            taskDesc.className = 'task-description';
            taskDesc.textContent = task.description;
            taskDesc.style.flexGrow = '1';

            // Add event listener for the checkbox
            checkbox.addEventListener('change', () => {
                if (checkbox.checked) {
                    taskDesc.style.textDecoration = 'line-through'; // Strike-through
                    taskDesc.style.color = 'black'; // Ensure text is visible
                    taskLabel.style.backgroundColor = 'lightgreen'; // Highlight the task
                    taskLabel.classList.add('task-completed');
                } else {
                    taskDesc.style.textDecoration = 'none'; // Remove strike-through
                    taskDesc.style.color = ''; // Reset to default
                    taskLabel.style.backgroundColor = ''; // Reset background
                    taskLabel.classList.remove('task-completed');
                }
            });

            // Add event listener to notify backend on checkbox change
            checkbox.addEventListener('change', async () => {
                await this.notifyBackend(task.id, checkbox.checked);
            });

            // Add event listener to update the message when a checkbox is clicked
            checkbox.addEventListener('change', () => this.updateMessage());
    
            taskLabel.appendChild(checkbox);
            taskLabel.appendChild(taskDesc);
            taskListContainer.appendChild(taskLabel);
        });
    }

    updateMessage() {
        const checkboxes = document.querySelectorAll('#task-list-container input[type="checkbox"]');
        const allChecked = Array.from(checkboxes).every((checkbox) => checkbox.checked);

        const messageElement = document.getElementById('all-checked-message');
        if (allChecked) {
            messageElement.textContent = 'DONE for the Day! :)';
            messageElement.style.display = 'block'; // Show the message
        } else {
            messageElement.textContent = '';
            messageElement.style.display = 'none'; // Hide the message
        }
    }

    createMessageElement() {
        const messageElement = document.createElement('div');
        messageElement.id = 'all-checked-message';
        messageElement.style.position = 'fixed';
        messageElement.style.bottom = '100px';
        messageElement.style.width = '100%';
        messageElement.style.textAlign = 'center';
        messageElement.style.color = 'green';
        messageElement.style.fontSize = '1.5rem';
        messageElement.style.display = 'none'; // Hidden initially
        document.body.appendChild(messageElement);
    }

    async notifyBackend(taskId, completed) {
        try {
            const response = await fetch('/update-task', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: taskId, completed }),
            });
            const result = await response.json();
            console.log(result);
        } catch (error) {
            console.error('Error notifying backend:', error);
        }
    }

    async populate() {
        await this.fetchTasks();
        this.createHeader();
        this.createTaskList();
        this.createMessageElement();
    }
}

const tasks = ["1", "Breakfast", "3"];
const frontend = new SchedulerApp(tasks);
frontend.populate()