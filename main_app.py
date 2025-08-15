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

def generate_prompt(email_body, attachments):
    prompt = f"""You are a precise and cautious assistant. Your task is to generate a response to the email shown below, using only the content provided in the email body and its attachments.

        Rules:
        - Do not use any information outside of what is explicitly provided.
        - Do not make assumptions or generate content that is not grounded in the input.
        - If critical information is missing or ambiguous, respond with:  
        "The provided information is insufficient to respond accurately."
        - Quote content directly from the email or attachments where appropriate.
        - First, show your reasoning step-by-step.
        - Then write the final response to the email.

        ---

        EMAIL BODY:
        {email_body}

        ---

        ATTACHMENTS:

        {attachments}

        ...

        ---

        REASONING:
        1. Identify the main intent or request in the email.
        2. Locate supporting facts in the attachments.
        3. Ensure all facts used are quoted or referenced directly from the content.
        4. If you can answer based on available facts, continue. If not, stop and return the "insufficient info" message.

        ---

        FINAL RESPONSE:
        [Write the complete, accurate reply to the email here. If data is missing, state that clearly.]
        """
    return prompt

if __name__ == "__main__":

    read_attachment_files.clear_all_files_folder("attachments")
    file_path = "emails/Project Alpha – Weekly Update and Action Items.msg"
    email_data=read_mails.read_any_email(file_path)
    # get email body
    email_body=email_data.get('body')

    attachment_data=read_attachment_files.extract_all_files_from_folder("attachments")
    print(type(email_data), type(attachment_data))
    # merge attachments
    attachment_merged=""

    for attachment in attachment_data:
        text_content = attachment.get('text')
        attachment_merged+=str(text_content)
        attachment_merged+=" - "

    prompt=generate_prompt(email_body, attachment_merged)
    print(prompt)
    # save_all_into_file(email_data, "Email Data.json")
    # save_all_into_file(attachment_data, "Attachment Data.json")
    # wrapper = ChatGPTWrapper(model="gpt-3.5-turbo")
    # response = wrapper.get_chat_response(
    #     prompt="Tell me a joke",
    #     system_prompt="You are a friendly and witty coder."
    # )
    # print(response)