from jinja2 import Environment, FileSystemLoader
import os
import json

def save_as_json(data, output_path):
    try:
       with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    except Exception as e:
        print(f"An Error Occuring while saving data: {e}")

def generate_prompt(email_body, attachments):
    env = Environment(loader=FileSystemLoader("prompts"))
    template = env.get_template("email_prompt.j2")
    return template.render(email_body=email_body, attachments=attachments)

def save_as_file(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(str(data))