from flask import request
from app_config import app
from email_handler import *
from database_handler import *
from helpers import *
from flask import jsonify

@app.post("/meeting/request")
def request_meeting():
    try:
        request_data = request.get_json()
        receiver = request_data['email']
        target_domain = request_data['domain']
        mail_subject = get_invitation_title()
        meeting_id = get_meeting_id()
        mail_text = get_invitation_text(meeting_id, target_domain)
        message = create_message(receiver, mail_subject, mail_text)
        send_message(message)
        create_new_meeting(receiver, meeting_id)
        return jsonify({'message': 'success'}), 200
    except Exception as error:
        return jsonify({'message': 'error'}), 404

@app.put('/meeting/start/<meeting_id>')
def start_meeting(meeting_id):
    try:
        start_meeting_by_id(meeting_id)
        return jsonify({'message': 'updated'}), 200
    except Exception:
        return jsonify({'message': 'error'}), 404

@app.get('/waiting_clients')
def get_waiting_clients():
    sql_query = "SELECT * FROM meetings WHERE status = 'STARTED'"
