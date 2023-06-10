import psycopg2
from app_data import DATABASE_URLS
from datetime import date

connection = psycopg2.connect(DATABASE_URLS['development'])
cursor = connection.cursor()

def create_new_meeting(receiver, meeting_id):
    sql_query = f"INSERT INTO meetings (client_email, meeting_id, date) VALUES ('{receiver}', {meeting_id}, '{date.today()}');"
    cursor.execute(sql_query)
    connection.commit()
    if (cursor.closed == False):
        cursor.close()
    if (connection.closed == False):
        connection.close()

def start_meeting_by_id(meeting_id):
    sql_query = f"UPDATE meetings SET status = 'STARTED' WHERE meeting_id = {meeting_id}"
    cursor.execute(sql_query)
    connection.commit()
    if (cursor.closed == False):
        cursor.close()
    if (connection.closed == False):
        connection.close()