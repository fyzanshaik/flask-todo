import os
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, jsonify

load_dotenv()

connection_string = os.getenv('DATABASE_URL')

connection_pool = pool.SimpleConnectionPool(
    1,  
    10, 
    connection_string
)

app = Flask(__name__)

def add_task(task, description):
    conn = connection_pool.getconn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task, description) VALUES (%s, %s)", (task, description))
    conn.commit()
    cursor.close()
    connection_pool.putconn(conn)

def get_tasks():
    conn = connection_pool.getconn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, description, status FROM tasks")
    rows = cursor.fetchall()
    cursor.close()
    connection_pool.putconn(conn)
    return rows

def delete_task(task_id):
    conn = connection_pool.getconn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    connection_pool.putconn(conn)

def update_task_status(task_id, status):
    conn = connection_pool.getconn()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (status, task_id))
    conn.commit()
    cursor.close()
    connection_pool.putconn(conn)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def tasks():
    tasks = get_tasks()
    return jsonify(tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    description = request.form.get('description')
    if task:
        add_task(task, description)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    delete_task(task_id)
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['POST'])
def update(task_id):
    status = request.json.get('status')
    update_task_status(task_id, status)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
