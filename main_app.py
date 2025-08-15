import read_attachment_files
import read_mails
import os
import json
from open_ai_call import ChatGPTWrapper

def save_all_into_file(data, output_path):
    try:
       with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    except Exception as e:
        print(f"An Error Occuring while saving data: {e}")


if __name__ == "__main__":

    # read_attachment_files.clear_all_files_folder("attachments")
    # file_path = "emails/Project Alpha – Weekly Update and Action Items.msg"
    # email_data=read_mails.read_any_email(file_path)
    # attachment_data=read_attachment_files.extract_all_files_from_folder("attachments")
    # print(type(email_data), type(attachment_data))
    # save_all_into_file(email_data, "Email Data.json")
    # save_all_into_file(attachment_data, "Attachment Data.json")
    wrapper = ChatGPTWrapper(model="gpt-3.5-turbo")
    response = wrapper.get_chat_response(
        prompt="Tell me a joke",
        system_prompt="You are a friendly and witty coder."
    )
    print(response)