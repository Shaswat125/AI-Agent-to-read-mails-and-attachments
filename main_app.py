import read_attachment_files
import read_mails
import os, pandas


if __name__ == "__main__":

    read_attachment_files.clear_all_files_folder("attachments")
    file_path = "Project Alpha – Weekly Update and Action Items.msg"
    email_data=read_mails.read_any_email(file_path)
    # print("Mail Data is:")
    # print("Body:\n", email_data.get('body'))
    # print("Attachment report:\n", email_data.get('attachment'))

    attachment_data=read_attachment_files.extract_all_files_from_folder("attachments")
    for file_data in attachment_data:
        text_content = file_data.get('text')
        print(text_content)
        print("\n" + "="*40 + "\n")