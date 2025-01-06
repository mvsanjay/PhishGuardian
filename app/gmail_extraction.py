import imaplib
import email
from email.header import decode_header
import re

def clean_email_body(text):
    # Replace \r\n with a space
    text = text.replace("\r\n", " ").replace("\n", " ")

    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)

    # Extract URLs (optional: you can keep them or remove them based on your needs)
    urls = re.findall(r'(https?://\S+)', text)

    # Remove unwanted phrases like copyright or disclaimers
    unwanted_phrases = [
        "You received this email", 
        "Google LLC", 
        "Mountain View", 
        "App password created", 
        "Check activity",
        "If you didn't generate",
        "Check and secure your account now."
    ]
    for phrase in unwanted_phrases:
        text = text.replace(phrase, "")

    # Optionally remove everything after a certain marker, e.g., signature markers
    text = re.split(r'(You received this email|©)', text)[0]

    # Add extracted URLs back to the cleaned text (if needed)
    if urls:
        text += " ".join(urls)

    return text.strip()

def fetch_latest_email(username, password):
    # Connect to Gmail's IMAP server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")

    try:
        # Login with your Gmail username and App Password
        mail.login(username, password)

        # Select the inbox folder
        mail.select("inbox")

        # Search for all emails in the inbox
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            return None, "Unable to fetch emails."

        # Get list of email IDs (the most recent one is at the end of the list)
        email_ids = messages[0].split()

        # Fetch the most recent email (the last one in the list)
        latest_email_id = email_ids[-1]
        status, msg_data = mail.fetch(latest_email_id, "(RFC822)")

        if status != "OK":
            return None, "Failed to fetch the latest email."

        # Initialize the dictionary
        email_dict = {"subject": "", "text": ""}

        # Parse the email content
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                # Parse the email content
                msg = email.message_from_bytes(response_part[1])

                # Decode the subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # If subject is encoded, decode it
                    subject = subject.decode(encoding if encoding else 'utf-8')
                email_dict["subject"] = subject

                # Get the email body (handling multipart emails)
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # Decode and store the text part of the email
                            body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            email_dict["text"] = body
                            break  # Only take the plain text part
                else:
                    # For non-multipart emails (plain text emails)
                    body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                    email_dict["text"] = body

        return email_dict, None  # Return the email data and no error message
    except Exception as e:
        return None, str(e)
    finally:
        # Logout from the mail server
        mail.logout()


