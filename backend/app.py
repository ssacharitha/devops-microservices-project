from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "tasksdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/health")
def health():
    return {"status": "ok"}, 200

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM tasks;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{"id": r[0], "title": r[1]} for r in rows])

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    title = data.get("title")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title) VALUES (%s) RETURNING id;", (title,))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return {"id": new_id, "title": title}, 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)