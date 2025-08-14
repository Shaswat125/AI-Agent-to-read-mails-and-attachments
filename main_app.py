import read_attachment_files
import read_mails
import os, pandas

def clear_attachment_folder(folder_path="attachments"):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted: {filename}")
            except Exception as e:
                print(f"Failed to delete {filename}: {e}")
    print(f"All files cleared from '{folder_path}'")

if __name__ == "__main__":

    
    clear_attachment_folder("attachments")
    file_path = "Project Alpha – Weekly Update and Action Items.msg"
    email_data=read_mails.read_any_email(file_path)

    print("Recovered Mail is:")
    print("Body:\n", email_data.get('body'))
    print("Attachment report:\n", email_data.get('attachment'))

    attachment_data=read_attachment_files.extract_all_files_from_folder("attachments")
    for file_data in attachment_data:
        text_content = file_data.get('text')
        print(text_content)
        print("\n" + "="*40 + "\n")