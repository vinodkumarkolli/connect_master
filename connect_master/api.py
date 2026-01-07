import frappe
import json
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

    # Get Email Template
    try:
        template = frappe.get_doc("Email Template", "Login Template")
    except frappe.DoesNotExistError:
        frappe.throw("Login Template not found")
        
    # Prepare Email
    subject = template.subject.replace("[[otp]]", otp)
    message = template.response.replace("[[otp]]", otp)

    if email_settings.settings_type == "Frappe Inbuilt":
        sender = None
        if email_settings.email_account:
            sender = frappe.db.get_value("Email Account", email_settings.email_account, "email_id")

        frappe.sendmail(
            recipients=[email],
            subject=subject,
            message=message,
            sender=sender,
            now=True
        )
        print(f"OTP sent to {email}: {otp}")
    else:
        if not email_settings.outgoing_server:
            frappe.throw("Email settings not configured")
        
        msg = MIMEMultipart()
        msg['From'] = email_settings.sender_email
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
            server.sendmail(email_settings.sender_email, email, msg.as_string())
            server.quit()
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

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_users_by_role(doctype, txt, searchfield, start, page_len, filters):
    if isinstance(filters, str):
        filters = json.loads(filters)

    role = filters.get("role")
    if not role:
        return []

    return frappe.db.sql("""
        SELECT DISTINCT
            u.name, u.full_name
        FROM
            `tabUser` u
        INNER JOIN
            `tabHas Role` hr ON hr.parent = u.name
        WHERE
            hr.role = %(role)s
            AND u.enabled = 1
            AND (u.name LIKE %(txt)s OR u.full_name LIKE %(txt)s)
        ORDER BY
            case when u.name like %(txt)s then 0 else 1 end,
            u.name ASC
        LIMIT
            %(start)s, %(page_len)s
    """, {
        'role': role,
        'txt': "%%%s%%" % txt,
        'start': start,
        'page_len': page_len
    })

@frappe.whitelist()
def get_linked_addresses(contact_names):
    if isinstance(contact_names, str):
        contact_names = json.loads(contact_names)
    
    if not contact_names:
        return []

    # Get addresses linked via Dynamic Link
    # Using frappe.db.sql to bypass permission checks on Dynamic Link which is a system table
    dynamic_linked_addresses = frappe.db.sql("""
        SELECT parent
        FROM `tabDynamic Link`
        WHERE link_doctype = 'Contact'
        AND link_name IN %(contact_names)s
        AND parenttype = 'Address'
    """, {'contact_names': tuple(contact_names)}, as_dict=True)
    
    return [d.parent for d in dynamic_linked_addresses]

@frappe.whitelist()
def get_document_user(doctype, name):
    return frappe.db.get_value('Dynamic Link', {
        'parent': name,
        'parenttype': doctype,
        'link_doctype': 'User'
    }, 'link_name')

@frappe.whitelist()
def search_addresses_for_punch(query):
    user = frappe.session.user
    
    # 1. Find user's assigned territories
    assigned_territories = frappe.db.sql("""
        SELECT parent FROM `tabConnect Map Users`
        WHERE parenttype = 'Service Territory' AND parentfield = 'territory_admins' AND user = %s
    """, (user,), pluck=True)
    
    allowed_territories = set(assigned_territories)
    
    # 2. Expand to child territories
    if assigned_territories:
        territory_details = frappe.db.get_all('Service Territory',
            filters={'name': ['in', assigned_territories]},
            fields=['lft', 'rgt']
        )
        
        for td in territory_details:
            descendants = frappe.db.get_all('Service Territory',
                filters={'lft': ['>=', td.lft], 'rgt': ['<=', td.rgt]},
                pluck='name'
            )
            allowed_territories.update(descendants)
            
    # 3. Search Addresses and Contacts
    # Search Addresses directly
    addresses = frappe.db.get_all('Address',
        filters=[
            ['disabled', '=', 0],
            ['address_title', 'like', f'%{query}%']
        ],
        fields=['name', 'address_title', 'address_line1', 'city', 'pincode', 'custom_address_category', 'custom_resolved_territory'],
        limit_page_length=20
    )
    
    # Search Contacts and get their addresses
    contacts = frappe.db.get_all('Contact',
        filters=[
            ['unsubscribed', '=', 0]
        ],
        or_filters=[
            ['first_name', 'like', f'%{query}%'],
            ['last_name', 'like', f'%{query}%'],
            ['mobile_no', 'like', f'%{query}%'],
            ['email_id', 'like', f'%{query}%']
        ],
        fields=['name', 'address'],
        limit_page_length=20
    )
    
    contact_addresses = [c.address for c in contacts if c.address]
    
    if contacts:
        contact_names = [c.name for c in contacts]
        dynamic_links = frappe.get_all('Dynamic Link',
            filters={
                'link_doctype': 'Contact',
                'link_name': ['in', contact_names],
                'parenttype': 'Address'
            },
            pluck='parent'
        )
        contact_addresses.extend(dynamic_links)
        
    all_address_names = set([a.name for a in addresses] + contact_addresses)
    
    if not all_address_names:
        return {'allowed': [], 'restricted': []}
        
    # Fetch details for all found addresses
    all_addresses = frappe.db.get_all('Address',
        filters={'name': ['in', list(all_address_names)], 'disabled': 0},
        fields=['name', 'address_title', 'address_line1', 'city', 'pincode', 'custom_address_category', 'custom_resolved_territory']
    )
    
    # Fetch contacts for all found addresses
    address_names = [addr.name for addr in all_addresses]
    contacts_map = {}
    if address_names:
        # Direct links
        linked_contacts = frappe.db.get_all('Contact',
            filters={'address': ['in', address_names], 'unsubscribed': 0},
            fields=['name', 'first_name', 'last_name', 'address', 'mobile_no', 'email_id']
        )
        for c in linked_contacts:
            if c.address not in contacts_map:
                contacts_map[c.address] = []
            contacts_map[c.address].append({
                'name': c.name,
                'full_name': f"{c.first_name} {c.last_name}",
                'mobile_no': c.mobile_no,
                'email_id': c.email_id
            })
            
        # Dynamic links
        dynamic_links = frappe.db.get_all('Dynamic Link',
            filters={
                'link_doctype': 'Contact',
                'parenttype': 'Address',
                'parent': ['in', address_names]
            },
            fields=['link_name', 'parent']
        )
        
        if dynamic_links:
            contact_names = [d.link_name for d in dynamic_links]
            dl_contacts = frappe.db.get_all('Contact',
                filters={'name': ['in', contact_names], 'unsubscribed': 0},
                fields=['name', 'first_name', 'last_name', 'mobile_no', 'email_id']
            )
            dl_contacts_map = {c.name: c for c in dl_contacts}
            
            for d in dynamic_links:
                c = dl_contacts_map.get(d.link_name)
                if c:
                    if d.parent not in contacts_map:
                        contacts_map[d.parent] = []
                    
                    # Avoid duplicates
                    existing_ids = [x['name'] for x in contacts_map[d.parent]]
                    if c.name not in existing_ids:
                        contacts_map[d.parent].append({
                            'name': c.name,
                            'full_name': f"{c.first_name} {c.last_name}",
                            'mobile_no': c.mobile_no,
                            'email_id': c.email_id
                        })

    allowed_list = []
    restricted_list = []
    
    for addr in all_addresses:
        # Get User linked to Address
        user_link = frappe.db.get_value('Dynamic Link', {
            'parent': addr.name,
            'parenttype': 'Address',
            'link_doctype': 'User'
        }, 'link_name')
        
        addr_obj = {
            'type': 'Address',
            'name': addr.name,
            'title': addr.address_title,
            'description': f"{addr.address_line1}, {addr.city}",
            'user': user_link,
            'contacts': contacts_map.get(addr.name, []),
            'doc': addr
        }
        
        if addr.custom_resolved_territory in allowed_territories:
            allowed_list.append(addr_obj)
        else:
            # Fetch territory admin details
            territory = addr.custom_resolved_territory
            admin_details = []
            if territory:
                admins = frappe.db.sql("""
                    SELECT user FROM `tabConnect Map Users`
                    WHERE parenttype = 'Service Territory' AND parentfield = 'territory_admins' AND parent = %s
                """, (territory,), pluck=True)
                
                for admin_user in admins:
                    u = frappe.db.get_value('User', admin_user, ['full_name', 'email', 'mobile_no'], as_dict=True)
                    if u:
                        admin_details.append(u)
            
            addr_obj['admin_details'] = admin_details
            restricted_list.append(addr_obj)
            
    return {'allowed': allowed_list, 'restricted': restricted_list}
