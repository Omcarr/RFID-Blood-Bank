import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_notification(recipient_email, subject, message_body):
    sender_email = "youremail@example.com"
    password = "yourpassword"

    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the message body
    msg.attach(MIMEText(message_body, 'plain'))

    # SMTP server setup and sending email
    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)
    print(f"QR code saved as {filename}.")



def generate_donor_certificate(donor_name, date):
    filename = f"{donor_name}_certificate.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 20)
    c.drawString(100, 750, "Blood Donation Certificate")
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"This is to certify that {donor_name}")
    c.drawString(100, 680, f"has donated blood on {date}.")
    c.drawString(100, 660, "We appreciate their contribution to saving lives.")
    c.save()
    print(f"Certificate generated for {donor_name}!")

# Example usage
generate_donor_certificate("John Doe", "10/29/2024")
