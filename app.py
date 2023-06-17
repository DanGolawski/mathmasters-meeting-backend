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
        return jsonify({'error': error}), 400

@app.put('/meeting/status')
def start_meeting():
    try:
        request_data = request.get_json()
        current_status = get_status_of_meeting(request_data['meeting_id'])
        if (status_is_present(current_status, request_data['new_status'])):
            change_status_of_meeting(request_data['meeting_id'], request_data['new_status'])
            return jsonify({'new_status': request_data['new_status']}), 200
        else:
            return jsonify({'new_status': current_status}), 200
    except Exception as error:
        return jsonify({'error': error}), 400

@app.post('/meeting/close/<meeting_id>')
def close_meeting(meeting_id):
    try:
        meeting = get_meeting_by_id(meeting_id)
        message = create_message(meeting['client_email'], 'Tablica', get_content_of_mail_after_meeting())
        jpg_data = convert_png_to_jpg(request.files['image'].stream, meeting_id)
        message = add_attachment_to_message(message, jpg_data)
        send_message(message)
        change_status_of_meeting(meeting_id, 'FINISHED')
        return jsonify({'new_status': 'FINISHED'}), 200
    except Exception as error:
        return jsonify({'error': error}), 400

@app.put('/meeting/cancel/<meeting_id>')
def cancel_meeting(meeting_id):
    try:
        change_status_of_meeting(meeting_id, 'CANCELED')
        return jsonify({'new_status': 'CANCELED'}), 200
    except Exception as error:
        return jsonify({'error': error}), 400

@app.get('/waiting_clients')
def get_waiting_clients():
    try:
        waiting_clients, longest_waiting = get_number_of_waiting_clients()
        response = {
            'waiting_clients': waiting_clients,
            'longest_waiting_client': longest_waiting['meeting_id'] if longest_waiting != 0 else None
        }
        return jsonify(response), 200
    except Exception as error:
        return jsonify(error), 400

