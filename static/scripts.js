document.addEventListener("DOMContentLoaded", () => {
    const taskForm = document.getElementById("task-form");
    const taskNameInput = document.getElementById("task-name");
    const taskDescInput = document.getElementById("task-desc");
    const tasksList = document.getElementById("tasks");

    taskForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const task = taskNameInput.value;
        const description = taskDescInput.value;

        await fetch("/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({
                task: task,
                description: description
            })
        });

        taskNameInput.value = "";
        taskDescInput.value = "";
        fetchTasks();
    });

    tasksList.addEventListener("click", async (event) => {
        if (event.target.classList.contains("delete")) {
            const taskId = event.target.dataset.id;
            await fetch(`/delete/${taskId}`, { method: "POST" });
            fetchTasks();
        } else if (event.target.type === "checkbox") {
            const taskId = event.target.dataset.id;
            const status = event.target.checked;
            await fetch(`/update/${taskId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ status: status })
            });
            fetchTasks();
        }
    });

    async function fetchTasks() {
        const response = await fetch("/tasks");
        const tasks = await response.json();

        tasksList.innerHTML = "";
        tasks.forEach(task => {
            const taskItem = document.createElement("li");
            taskItem.className = task[3] ? "done" : "";
            taskItem.innerHTML = `
                <div class="task-item">
                    <input type="checkbox" data-id="${task[0]}" ${task[3] ? "checked" : ""}>
                    <span>${task[1]} - ${task[2]}</span>
                </div>
                <a href="#" class="delete" data-id="${task[0]}">Delete</a>
            `;
            tasksList.appendChild(taskItem);
        });
    }

    fetchTasks();
    setInterval(fetchTasks, 5000);  // Refresh tasks every 5 seconds
});
