import os, sys
import sqlite3
import hashlib
import subprocess

API_KEY = "sk-test-1234567890abcdef"


def get_user(db_path, username):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # SQL injection: user input is formatted straight into the query
    cur.execute("SELECT * FROM users WHERE name = '%s'" % username)
    return cur.fetchone()


def hash_password(password):
    # weak hash
    return hashlib.md5(password.encode()).hexdigest()


def run_command(cmd):
    # shell injection risk
    return subprocess.call(cmd, shell=True)


def calculate(expr):
    try:
        return eval(expr)
    except:
        return None


def total(items):
    result = 0
    for i in items:
        result += i.price
    return reslt
