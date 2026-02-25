import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")

DB_PATH = os.path.join(STORAGE_DIR, "honeypot_logs.db")