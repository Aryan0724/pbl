import sqlite3
import json

DB_NAME = "question_papers.db"


def create_table():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
CREATE TABLE IF NOT EXISTS papers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    paper_data TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")


def save_paper(subject, topic, difficulty, paper):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute("""
INSERT INTO papers
(subject, topic, difficulty, paper_data)
VALUES (?, ?, ?, ?)
""", (subject, topic, difficulty, json.dumps(paper)))
        return cursor.lastrowid


def get_paper(paper_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        row = conn.execute(
            "SELECT * FROM papers WHERE id = ?", (paper_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def list_papers(limit=20):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        rows = conn.execute("""
SELECT id, subject, topic, difficulty, created_at
FROM papers ORDER BY id DESC LIMIT ?
""", (limit,)).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
