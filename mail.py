import os
import smtplib
import requests
import validators

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


URL = 'https://script.googleusercontent.com/macros/echo?user_content_key=65eirCRhjvHx6XnaJb6yicdJqCw3ITTsPBnTBWHX9AqzG'\
    'oA7xOhOr_IyGzwIKDF1FhEYQN4Mk-Ws5wBYwGS7oAkJwq9q1GEHm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnEVvqx-k'\
    'uTyynDs87B0KIRw4WGwaIu2iLivPlsyF7KQlBh9kMh9BLwwA9c3NkOuRrYa6Ar8Jygf33jRX1nkQX4XDg6I4JxZ6WNz9Jw9Md8uu&lib=MnTjVF'\
    '8bTE4ny8Yhas7KUsdqK-6lY-9os'


def get_email(decor):
    def valid():
        # заполнем mass_email всеми получеными email
        mass_email = []
        for i in decor()['data']:
            mass_email.append(i['e_mail'])

        # проверяем email на валидность и добавляем в valid_email
        valid_email = []
        for i in mass_email:
            if validators.email(i) == True:
                valid_email.append(i)

        # избавляемся от дублированых email
        valid_email = list(set(valid_email))
        
        return valid_email
    return valid


@get_email
def get_json():
    # # получаем данные с json
    data = requests.get(URL)
    data = data.json()
    return data
get_json()


SMTP_SERVER = 'smtp.ukr.net'
PASSWORD_API = 'hjBFw3jq77TFp5Li'
USER_ = 'vladsadullaiev04@ukr.net'
password_for_email = '76mi9pKApvVpZwU'


valid_e_mail = get_json()


def mail_sender(recipient: list):
    """
    sending e-mail with a receipt
    """
    server = SMTP_SERVER
    PASSWORD = PASSWORD_API
    USER = USER_


    recipient = valid_e_mail


    recipient = [*recipient]
    sender = USER
    subject = 'Тема сообщения'
    text = 'Test'

    # for sending a file-----------------
    filepath = "D:\A_Main\Python\Hillel\Hw_6\mail.py"

    from os.path import exists
    file_exists = exists(filepath)
    if not file_exists:
        print('file unavailable')
        return False
    basename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    # ------------------------------------

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'Python script <' + sender + '>'
    msg['To'] = ', '.join(recipient)
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'decorator'

    part_text = MIMEText(text, 'plain')

    # for sending a file----------------------------------------------------------------------
    part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(basename))
    part_file.set_payload(open(filepath, "rb").read())
    part_file.add_header('Content-Description', basename)
    part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename, filesize))
    encoders.encode_base64(part_file)
    msg.attach(part_file)
    # ----------------------------------------------------------------------------------------

    msg.attach(part_text)

    mail = smtplib.SMTP_SSL(server)
    mail.login(USER, PASSWORD)
    mail.sendmail(sender, recipient, msg.as_string())
    mail.quit()
    return True

mail_sender((valid_e_mail, 'Test'))
