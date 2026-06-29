import sqlite3
import bcrypt
import streamlit as st
from pathlib import Path

_DB_PATH = str(Path(__file__).parent.parent.parent / "data.db")


@st.cache_resource
def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = _get_connection()

    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id),
                exercise_name TEXT NOT NULL,
                reps INTEGER NOT NULL DEFAULT 0,
                sets INTEGER NOT NULL DEFAULT 0,
                time INTEGER NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)


# ==========================
# USER AUTHENTICATION
# ==========================

def get_user(username: str):
    conn = _get_connection()

    return conn.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
    ).fetchone()


def register_user(username: str, password: str):
    conn = _get_connection()

    existing = get_user(username)

    if existing:
        return None

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    with conn:
        conn.execute(
            """
            INSERT INTO users(username,password)
            VALUES(?,?)
            """,
            (username, hashed_password)
        )

    return get_user(username)


def login_user(username: str, password: str):
    user = get_user(username)

    if user is None:
        return None

    if bcrypt.checkpw(
        password.encode(),
        user["password"].encode()
    ):
        return user

    return None


# ==========================
# EXERCISE HISTORY
# ==========================

def add_exercise(user_id, exercise_name, reps, sets, time):
    conn = _get_connection()

    with conn:
        existing = conn.execute("""
            SELECT *
            FROM exercises
            WHERE user_id=?
            AND exercise_name=?
            AND DATE(created_at)=DATE('now')
        """, (user_id, exercise_name)).fetchone()

        if existing:

            conn.execute("""
                UPDATE exercises
                SET reps=reps+?,
                    sets=sets+?,
                    time=time+?
                WHERE id=?
            """, (
                reps,
                sets,
                time,
                existing["id"]
            ))

        else:

            conn.execute("""
                INSERT INTO exercises
                (
                    user_id,
                    exercise_name,
                    reps,
                    sets,
                    time
                )
                VALUES(?,?,?,?,?)
            """, (
                user_id,
                exercise_name,
                reps,
                sets,
                time
            ))


def get_users_exercises(user_id):
    conn = _get_connection()

    return conn.execute("""
        SELECT *
        FROM exercises
        WHERE user_id=?
        ORDER BY created_at DESC
    """, (user_id,)).fetchall()
