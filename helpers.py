from datetime import date, datetime
import random
from app_data import MEETING_STATUSES_FLOW
from PIL import Image
import base64
import os

def convert_png_to_jpg(data, meeting_id):
    temporary_filename = f'TEMPORARY_BOARDS/board{meeting_id}.jpg'
    im = Image.open(data)
    im.save(temporary_filename, 'JPEG')
    image_file = open(temporary_filename, "rb").read()
    # jpg_base64 = base64.b64encode(image_file.read())
    os.remove(os.path.join(temporary_filename))
    return image_file

def get_invitation_title():
    return f'Zaproszenie na korepetycje {get_current_date()}'

def get_current_date():
    return date.today().strftime("%d/%m/%Y")

def get_meeting_id():
    return f'{datetime.now().strftime("%Y%m%d%H%M%S")}{random.randint(1000, 9999)}'

def get_invitation_text(meeting_id, destination):
    return f'Oto twój link do spotkania z korepetytorem: {destination}/client_meeting.html?{meeting_id}'

def get_content_of_mail_after_meeting():
    return '''
    Witaj,
    W załączniku przesyłamy tablicę z dzisiejszego spotkania. Miłego dnia!

    Pozdrawiamy
    team MathMasters
    '''

def status_is_present(current_status, new_status):
    current_status_index = MEETING_STATUSES_FLOW.index(current_status)
    new_status_index = MEETING_STATUSES_FLOW.index(new_status)
    return new_status_index > current_status_index
