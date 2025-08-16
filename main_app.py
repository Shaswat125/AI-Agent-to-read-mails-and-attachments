import read_attachment_files as read_att
import read_mails
import os
import json
from open_ai_call import ChatGPTWrapper
from utils import generate_prompt, save_as_json

if __name__ == "__main__":
    # Iterate for all mails in folder 
    for filename in os.listdir("emails"):
        email_extensions = ('.eml', '.msg', '.mbox')
        if filename.endswith(email_extensions):
            file_path = os.path.join("emails", filename)
            print(f"{filename}\n")
            read_att.clean_folder("attachments")

            email_data=read_mails.read_any_email(file_path)
            # get email body
            email_body=email_data.get('body')

            attachment_data=read_att.extract_all_files_from_folder("attachments")
            # merge attachments
            attachment_merged=""
            for attachment in attachment_data:
                text_content = attachment.get('text')
                attachment_merged+=str(text_content)
                attachment_merged+=" - "

            engineered_prompt=generate_prompt(email_body, attachment_merged)
            print(engineered_prompt)
            save_as_json(email_data, "Email Data.json")
            save_as_json(attachment_data, "Attachment Data.json")

            # wrapper = ChatGPTWrapper(model="gpt-3.5-turbo")
            # response = wrapper.get_chat_response(
            #     prompt=engineered_prompt,
            #     system_prompt="You are a professional AI assistant for email replies. Use only the provided email and attachments to generate accurate, clear, and polite responses. Do not assume or hallucinate information. If data is missing, say so clearly."
            # )
            # print(response)
            # response_json = json.dumps({
            #     "email_response": response
            # }, ensure_ascii=False, indent=2)
            # save_as_json(response_json, "open ai response json Data.json")
