🤖 AI Email Response Agent

This project is an AI-powered agent that automatically reads emails and their attachments, understands their context, and generates accurate, polite, and grounded replies using OpenAI’s GPT models (GPT-3.5 / GPT-4).

📌 Features

✅ Automatically processes emails from .eml, .msg formats
✅ Extracts and reads email body + all attachment content (PDF, DOCX, TXT, etc.)
✅ Uses a structured, hallucination-resistant prompt strategy
✅ Responds using OpenAI GPT-3.5 or GPT-4
✅ Saves parsed email, attachment data, and AI-generated response as .json

🏗 How It Works

Scans the emails/ folder for supported email files

For each email:

Extracts the email body

Reads and merges all attachment content

Generates a clean prompt with all extracted content

Sends it to OpenAI ChatGPT via API

Saves:

📧 *_email_details.json (email body + metadata)

📎 *_attachment_details.json (attachment contents)

🤖 *_response_mail.json (AI-generated reply)
