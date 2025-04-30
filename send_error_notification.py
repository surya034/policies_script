
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_error_notification(from_email, app_password, to_emails, subject, body):
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the server
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()  # Secure the connection
        server.login(from_email, app_password)  

        # Send the email
        server.sendmail(from_email, to_emails, msg.as_string())
        server.close()

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
