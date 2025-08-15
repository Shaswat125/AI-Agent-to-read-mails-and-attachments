import read_attachment_files
import read_mails
import os
import json
from open_ai_call import ChatGPTWrapper
from jinja2 import Environment, FileSystemLoader

def save_all_into_file(data, output_path):
    try:
       with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    except Exception as e:
        print(f"An Error Occuring while saving data: {e}")

def generate_prompt(email_body, attachments):
    env = Environment(loader=FileSystemLoader("prompts"))
    template = env.get_template("email_prompt.j2")
    return template.render(email_body=email_body, attachments=attachments)

if __name__ == "__main__":

    read_attachment_files.clear_all_files_folder("attachments")
    file_path = "emails/Project Alpha – Weekly Update and Action Items.msg"
    email_data=read_mails.read_any_email(file_path)
    # get email body
    email_body=email_data.get('body')

    attachment_data=read_attachment_files.extract_all_files_from_folder("attachments")
    # merge attachments
    attachment_merged=""
    for attachment in attachment_data:
        text_content = attachment.get('text')
        attachment_merged+=str(text_content)
        attachment_merged+=" - "

    engineered_prompt=generate_prompt(email_body, attachment_merged)
    print(engineered_prompt)
    save_all_into_file(email_data, "Email Data.json")
    save_all_into_file(attachment_data, "Attachment Data.json")

    wrapper = ChatGPTWrapper(model="gpt-3.5-turbo")
    response = wrapper.get_chat_response(
        prompt=engineered_prompt,
        system_prompt="AI Assistant"
    )
    print(response)
