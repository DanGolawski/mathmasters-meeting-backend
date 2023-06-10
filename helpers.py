from datetime import date, datetime
import random
from flask import Response

def get_invitation_title():
    return f'Zaproszenie na korepetycje {get_current_date()}'

def get_current_date():
    return date.today().strftime("%d/%m/%Y")

def get_meeting_id():
    return f'{datetime.now().strftime("%Y%m%d%H%M%S")}{random.randint(1000, 9999)}'

def get_invitation_text(meeting_id, destination):
    return f'Oto twój link do spotkania z korepetytorem: {destination}/meeting.html?{meeting_id}'
