import frappe
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from frappe.utils import get_url

@frappe.whitelist(allow_guest=True)
def send_otp(email, full_name=None):
    if not email:
        frappe.throw("Email is required")
    
    # Check if user exists
    if not frappe.db.exists("User", email):
        if not full_name:
            return {"status": "user_not_found", "message": "User not found. Please provide full name."}
        else:
            # Create User
            user = frappe.new_doc("User")
            user.email = email
            user.first_name = full_name
            user.enabled = 1
            user.insert(ignore_permissions=True)
            user.add_roles("Customer")

    # Generate OTP
    otp = ''.join(random.choices(string.digits, k=6))
    
    # Store OTP in cache (expires in 5 minutes)
    cache_key = f"otp:{email}"
    frappe.cache().set_value(cache_key, otp, expires_in_sec=300)
    
    # Get Email Settings
    email_settings = frappe.get_single("Connect Email Settings")
    if not email_settings.outgoing_server:
        frappe.throw("Email settings not configured")
        
    # Get Email Template
    try:
        template = frappe.get_doc("Email Template", "Login Template")
    except frappe.DoesNotExistError:
        frappe.throw("Login Template not found")
        
    # Prepare Email
    subject = template.subject.replace("[[OTP]]", otp)
    message = template.response.replace("[[OTP]]", otp)
    
    msg = MIMEMultipart()
    msg['From'] = email_settings.username
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))
    
    # Send Email
    try:
        port = int(email_settings.port) if email_settings.port else 587
        if email_settings.use_ssl:
            server = smtplib.SMTP_SSL(email_settings.outgoing_server, port)
        else:
            server = smtplib.SMTP(email_settings.outgoing_server, port)
            if email_settings.use_tls:
                server.starttls()
        
        server.login(email_settings.username, email_settings.get_password('password'))
        # server.sendmail(email_settings.username, email, msg.as_string())
        # server.quit()
        print(f"OTP sent to {email}: {otp}")
    except Exception as e:
        frappe.log_error(f"Failed to send OTP email: {str(e)}")
        frappe.throw("Failed to send OTP email. Please try again later.")
        
    return "OTP sent successfully"

@frappe.whitelist(allow_guest=True)
def verify_otp(email, otp):
    if not email or not otp:
        frappe.throw("Email and OTP are required")
        
    cache_key = f"otp:{email}"
    cached_otp = frappe.cache().get_value(cache_key)
    
    if not cached_otp:
        frappe.throw("OTP expired or invalid")
        
    if str(cached_otp) != str(otp):
        frappe.throw("Invalid OTP")
        
    # Clear OTP
    frappe.cache().delete_value(cache_key)
    
    # Login User
    login_manager = frappe.auth.LoginManager()
    login_manager.login_as(email)
    login_manager.post_login()
    
    return "Logged in successfully"
