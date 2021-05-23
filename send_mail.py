import smtplib
import getpass
from email.message import EmailMessage
import os
import mimetypes


def _get_domain(address):
    """
    Finds the service domain from sender's email address
    :param address: sender's email address
    :return: domain
    """
    if address.endswith("@gmail.com") and len(address) > 10:
        return "smtp.gmail.com"
    elif address.endswith("@yahoo.com") and len(address) > 10:
        return "smtp.mail.yahoo.com"
    elif (address.endswith("@outlook.com") or address.endswith("@hotmail.com")) and len(address) > 12:
        return "smtp-mail.outlook.com"
    else:
        '''
        If unknown email address is provided then the function recalls itself until a valid email is provided.
        '''
        address = input("Please Enter a valid email address: ").strip()
        return _get_domain(address)


def get_pass():
    """
    Take user's email address and password.
    :return: Sender's Email address and password
    """
    address = input("Your Email: ").strip()
    if '@' in address and ".com" in address:
        domain = _get_domain(address)
        password = getpass.getpass("Enter your password: ")
        return domain, address, password
    else:
        print("Email address not in proper format.\n< name@service.com >")
        return get_pass()


def send_this_mail(email_obj, recipient):
    """
    Send the email object to all the recipient.
    :param email_obj: EmailMessage object
    :param recipient: list of recipient/s email address
    :return: None
    """
    domain, address, password = get_pass()
    email_obj["From"] = address
    email_obj['To'] = ", ".join(recipient)
    with smtplib.SMTP_SSL(domain, 465) as smtp:
        try:
            smtp.login(address, password)
        except:
            print("Login Error - Please check your login credential.")
        try:
            print(smtp.send_message(email_obj))
        except Exception as e:
            print(e)
    return None


def _get_attachments():
    """
    :return: a list of file/attachment path
    """
    choice = input("Any attachments ?(y/n): ").strip()
    attachments_path = []
    while choice == "y" or choice == "Y":
        path = input("Enter attachment path: ")
        if os.path.exists(path):
            attachments_path.append(path)
        else:
            print("Invalid path")
        choice = input("More attachment ? (y/n): ").strip()
    return attachments_path


def email_object(attachments=None):
    """
    :param attachments: list of attachment/s file path
    :return: Email object
    """
    message = EmailMessage()
    message["Subject"] = input("Subject: ").strip()
    message.set_content(input("Body: "))
    if attachments is not None:
        for attachment in attachments:
            attachment_n = os.path.basename(attachment)
            mime_type, _ = mimetypes.guess_type(attachment)
            mime_type, mime_subtype = mime_type.split('/', 1)
            with open(attachment, 'rb') as ap:
                message.add_attachment(ap.read(), maintype=mime_type, subtype=mime_subtype, filename=attachment_n)
    return message


def _get_recipients():
    """
    :return: a list of recipient's email address
    """
    recipient = [input("Enter recipient's email address: ")]
    choice = input("Add more recipient ? (y/n) : ")
    while choice == "y" or choice == "Y":
        recipient.append("Enter recipient's email address: ")
        choice = input("Add more recipient ? (y/n) : ")
    return recipient


reci = _get_recipients()
attach_file = _get_attachments()
msg = email_object(attach_file)
send_this_mail(msg, recipient=reci)
