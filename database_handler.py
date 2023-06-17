import psycopg2
from app_data import DATABASE_URLS
from datetime import date
from psycopg2.extras import RealDictCursor

url_type = 'development'
# url_type = 'production'

def create_new_meeting(receiver, meeting_id):
    cursor, connection = open_connection()
    sql_query = f"INSERT INTO meetings (client_email, meeting_id, date) VALUES ('{receiver}', {meeting_id}, '{date.today()}');"
    cursor.execute(sql_query)
    connection.commit()
    close_connection(cursor, connection)

def change_status_of_meeting(meeting_id, new_status):
    cursor, connection = open_connection()
    sql_query = f"UPDATE meetings SET status = '{new_status}' WHERE meeting_id = {meeting_id}"
    cursor.execute(sql_query)
    connection.commit()
    close_connection(cursor, connection)

def get_status_of_meeting(meeting_id):
    cursor, connection = open_connection()
    sql_query = f"SELECT status FROM meetings WHERE meeting_id = {meeting_id}"
    cursor.execute(sql_query)
    status = cursor.fetchone()['status']
    close_connection(cursor, connection)
    return status
    

def get_number_of_waiting_clients():
    cursor, connection = open_connection()
    sql_query = f"SELECT meeting_id FROM meetings WHERE status = 'STARTED' AND date='{date.today()}' ORDER BY meeting_id"
    cursor.execute(sql_query)
    number_of_clients = cursor.rowcount
    longest_waiting_meeting = cursor.fetchone() if number_of_clients > 0 else 0
    close_connection(cursor, connection)
    return number_of_clients, longest_waiting_meeting

def get_meeting_by_id(meeting_id):
    cursor, connection = open_connection()
    sql_query = f"SELECT * FROM meetings WHERE meeting_id = {meeting_id}"
    cursor.execute(sql_query)
    meeting = cursor.fetchone()
    close_connection(cursor, connection)
    return meeting

def open_connection():
    connection = psycopg2.connect(DATABASE_URLS[url_type])
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    return cursor, connection

def close_connection(cursor, connection):
    if (cursor.closed == False):
        cursor.close()
    if (connection.closed == False):
        connection.close()