import read_attachment_files as read_att
import read_mails
import os
import json
from open_ai_call import ChatGPTWrapper
from utils import generate_prompt, save_as_json

# AI Agent to respond to mails
def respond_mails_AI_agent(mail_folder_path="emails"):

    # Iterate for all mails in folder to read, mails and attachments 
    for filename in os.listdir(mail_folder_path):
        email_extensions = ('.eml', '.msg', '.mbox')
        if filename.endswith(email_extensions):
            file_path = os.path.join(mail_folder_path, filename)
            print(f"For the mail : {filename}\n")
            read_att.clean_folder("attachments")

            # read email body
            email_data=read_mails.read_any_email(file_path)
            email_body=email_data.get('body')
            mail_header_name=os.path.splitext(filename)[0]

            # read attachments
            attachment_data=read_att.extract_all_files_from_folder("attachments")
            attachment_merged=""
            for attachment in attachment_data:
                text_content = attachment.get('text')
                attachment_merged+=str(text_content)
                attachment_merged+=" - "

            engineered_prompt=generate_prompt(email_body, attachment_merged)
            print(f"Input Prompt: {engineered_prompt}\n")
            save_as_json(email_data, f"{mail_header_name}_email_details.json")
            save_as_json(attachment_data, f"{mail_header_name}_attachment_details.json")

            wrapper = ChatGPTWrapper(model="gpt-3.5-turbo")
            response = wrapper.get_chat_response(
                prompt=engineered_prompt,
                system_prompt="You are a professional AI assistant for email replies. Use only the provided email and attachments to generate accurate, clear, and polite responses. Do not assume or hallucinate information. If data is missing, say so clearly."
            )
            print(response)
            response_json = json.dumps({"email_response": response}, ensure_ascii=False, indent=2)
            save_as_json(response_json, f"{mail_header_name}_response_mail.json")
            print(f"AI Agent responded successfully for the mail {mail_header_name}")

if __name__ == "__main__":
    # call ai agent
    respond_mails_AI_agent(mail_folder_path="emails")