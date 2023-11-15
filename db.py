import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os
from scanner import full_scan
from datetime import datetime
from log import log_event
import json
load_dotenv()  # load environment variables from .env file

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def execute_query(query, args=None):
    try:
        with psycopg2.connect(
                    database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    host=DB_HOST,
                    port=DB_PORT
                ) as conn:
            with conn.cursor() as cur:
                cur.execute(query, args)
                rows = cur.fetchall() if cur.description else None
                conn.commit()
        log_event("info", f"Executed query: {query}")
        return rows
    except OperationalError as e:
        log_event("error", f"Error executing query: {query}. Error message: {e}")
        return []

def get_profiles():
    query = "SELECT * FROM profiles"
    log_event("info", "Getting profiles")
    return execute_query(query)

def add_profile(profile):
    query = "INSERT INTO profiles (login, password, host, port) VALUES (%s, %s, %s, %s) RETURNING id"
    args = tuple(profile)
    profile_id = execute_query(query, args)[0][0]
    log_event("info",  f"Added profile with id: {profile_id}")
    return profile_id

def get_profile(profile_id):
    query = "SELECT login, password, host, port FROM profiles WHERE id=%s"
    args = (profile_id,)
    log_event("info",  f"Getting profile with id: {profile_id}")
    return execute_query(query, args)

def delete_profile(profile_id):
    query = "DELETE FROM profiles WHERE id=%s"
    args = (profile_id,)
    execute_query(query, args)
    log_event("info",  f"Deleted profile with id: {profile_id}")

def add_scan_result(profile_id, report_info):
    query = """
        INSERT INTO scan_results (
            profile_id,
            os_name,
            os_version,
            os_architecture,
            full_report,
            timestamp
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """
    os_info, full_report = report_info
    args = (profile_id, *os_info, json.dumps(full_report), datetime.now())
    execute_query(query, args)
    log_event("info", f"Added scan result for profile with id: {profile_id}")

def get_scan_results():
    query = "SELECT id, profile_id, os_name, os_version, os_architecture, timestamp FROM scan_results"
    log_event("info", "Getting scan results")
    return execute_query(query)

def get_scan_report(scan_id):
    query = "SELECT full_report FROM scan_results WHERE id=%s"
    args = (scan_id,)
    return result[0][0] if (result := execute_query(query, args)) else None

def scan_profile(profile, profile_id=None):
    scan_data = full_scan(profile)
    os_info = scan_data.get("PRETTY_NAME", "unknown"), scan_data.get("VERSION", "unknown"), scan_data.get("machine", "unknown")
    profile_id = add_profile(profile) if profile_id is None else profile_id
    report_info = os_info, scan_data
    add_scan_result(profile_id, report_info)
    query = "SELECT id FROM scan_results ORDER BY id DESC LIMIT 1"
    scan_id = execute_query(query)[0][0]
    log_event("info",  f"Get New Scan with id: {scan_id}")
    return scan_id

def create_tables():
    profiles_query = """
        CREATE TABLE IF NOT EXISTS profiles (
            id SERIAL PRIMARY KEY,
            login TEXT,
            password TEXT,
            host TEXT,
            port INTEGER
        )
    """
    scan_results_query = """
        CREATE TABLE IF NOT EXISTS scan_results (
            id SERIAL PRIMARY KEY,
            profile_id INTEGER REFERENCES profiles(id) ON DELETE CASCADE,
            os_name TEXT,
            os_version TEXT,
            os_architecture TEXT,
            full_report JSONB,
            timestamp TIMESTAMP
        )
    """
    execute_query(profiles_query)
    execute_query(scan_results_query)
    log_event("info", "Created tables and checked if exists")
