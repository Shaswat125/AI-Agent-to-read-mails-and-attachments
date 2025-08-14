from bs4 import BeautifulSoup
import os
from email import policy
from email.parser import BytesParser
import extract_msg, re

def read_any_email(file_path, directory_attach="attachments"):
    ext = os.path.splitext(file_path)[1].lower()

    if not os.path.exists(directory_attach):
        os.makedirs(directory_attach)

    if ext == '.eml':
        with open(file_path, 'rb') as f:
            msg = BytesParser(policy=policy.default).parse(f)

        subject = msg['subject']
        sender = msg['from']
        recipients = msg['to']
        date = msg['date']

        # Get plain text body only
        body = None
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_content()
                    break
        else:
            if msg.get_content_type() == 'text/plain':
                body = msg.get_content()

    elif ext == '.msg':
        msg_obj = extract_msg.Message(file_path)

        subject = msg_obj.subject
        sender = msg_obj.sender
        recipients = msg_obj.to
        date = msg_obj.date
         # Try plain text body first
        body = msg_obj.body

        # If empty, try HTML body and strip tags
        if not body and msg_obj.htmlBody:
            # using beautifulSoup to read body
            soup = BeautifulSoup(msg_obj.htmlBody, 'html.parser')
            body = soup.get_text()

    else:
        raise ValueError(f"Unsupported file extension: {ext}")

    return {
        'subject': subject,
        'from': sender,
        'to': recipients,
        'date': date,
        'body': body
    }

if __name__ == "__main__":
    file_path = "Project Alpha – Weekly Update and Action Items.msg"  
    # Project Alpha – Weekly Update and Action Items.eml
    email_data = read_any_email(file_path)
    print("Recovered Mail is:")
    print("Subject:", email_data['subject'])
    print("From:", email_data['from'])
    print("To:", email_data['to'])
    print("Date:", email_data['date'])
    print("Body:\n", email_data['body'])
