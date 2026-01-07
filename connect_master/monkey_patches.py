import email.utils
import frappe
from frappe.email.doctype.email_account.email_account import EmailAccount
from frappe.core.doctype.user.user import User

def patch_email_account():
    # Patch default_sender property to handle None email_id
    def default_sender(self):
        return email.utils.formataddr((self.name, self.get("email_id") or "notifications@example.com"))
    
    EmailAccount.default_sender = property(default_sender)

    # Patch create_dummy classmethod to use email_id instead of sender
    @classmethod
    def create_dummy(cls):
        return cls.from_record({
            "email_id": "notifications@example.com",
            "email_account_name": "Notifications",
            "enable_outgoing": 1,
            "default_outgoing": 1,
            "no_smtp_authentication": 1
        })
    
    EmailAccount.create_dummy = create_dummy

def patch_user():
    # Patch User to skip welcome email during migration
    original_send_welcome_mail_to_user = User.send_welcome_mail_to_user
    
    def send_welcome_mail_to_user(self):
        # Check flags that indicate migration or install
        if frappe.flags.in_migrate or frappe.flags.in_install or frappe.flags.in_setup_wizard:
            return
        return original_send_welcome_mail_to_user(self)
    
    User.send_welcome_mail_to_user = send_welcome_mail_to_user
