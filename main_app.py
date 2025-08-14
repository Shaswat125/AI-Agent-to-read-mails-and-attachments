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
    print("Subject:", email_data['subject'])
    print("From:", email_data['from'])
    print("To:", email_data['to'])
    print("Date:", email_data['date'])
    print("Body:\n", email_data['body'])
    print("Attachment report:\n", email_data['attachment'])

    attachment_data=read_attachment_files.extract_all_files_from_folder("attachments")
    for file_data in attachment_data:
        filename = file_data.get('filename')
        text_content = file_data.get('text')
        
        print(f"\n--- Text extracted from {filename} ---\n")
        print(text_content)  # or print(text_content[:1000]) to limit
        print("\n" + "="*40 + "\n")