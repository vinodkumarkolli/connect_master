import frappe

def after_install():
    """Create roles and set permissions after app installation."""
    create_commerce_domain()
    create_roles()
    set_role_permissions()
    create_global_sales_user()

def create_global_sales_user():
    """Create a Global Sales User if it doesn't exist."""
    email = "globalsales@example.com"
    if not frappe.db.exists("User", email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": "Global Sales",
            "send_welcome_email": 0,
            "user_type": "System User"
        })
        user.insert(ignore_permissions=True)
    
    # Ensure the user has the "Sales User" role
    if "Sales User" not in frappe.get_roles(email):
        user = frappe.get_doc("User", email)
        user.add_roles("Sales User")

def after_uninstall():
    """Remove roles and permissions when app is uninstalled."""
    # remove_role_permissions()
    disable_roles()

def create_roles():
    """Create required roles for the application."""
    # Create Customer role (no desk access)
    if not frappe.db.exists("Role", "Customer"):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": "Customer",
            "desk_access": 0
        }).insert()
    
    # Create Territory Admin role (desk access, limited to Radar app)
    if not frappe.db.exists("Role", "Territory Admin"):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": "Territory Admin",
            "desk_access": 0,
            "home_page": "/koda/dash"
        }).insert()
    
    # Create Partner Admin role (desk access, limited to Radar app)
    if not frappe.db.exists("Role", "Partner Admin"):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": "Partner Admin",
            "desk_access": 0,
            "home_page": "/koda/dash"
        }).insert()

    # Create System Manager role if it doesn't exist (usually it does)
    if not frappe.db.exists("Role", "System Manager"):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": "System Manager",
            "desk_access": 1
        }).insert()
    else:
        # Set existing System Manager role's home_page to /desk
        system_manager_role = frappe.get_doc("Role", "System Manager")
        system_manager_role.home_page = "/desk"
        system_manager_role.save()

@frappe.whitelist()
def set_role_permissions():
    """Set permissions for the roles."""
    # For Customer role, grant access to Address and Item doctypes
    if not frappe.db.exists("Custom DocPerm", {"role": "Customer", "parent": "Address"}):
        frappe.get_doc({
            "doctype": "Custom DocPerm",
            "role": "Customer",
            "parent": "Address",
            "parenttype": "DocType",
            "permlevel": 0,
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 0,
            "submit": 0,
            "cancel": 0,
            "amend": 0
        }).insert()
    
    if not frappe.db.exists("Custom DocPerm", {"role": "Customer", "parent": "Item"}):
        frappe.get_doc({
            "doctype": "Custom DocPerm",
            "role": "Customer",
            "parent": "Item",
            "parenttype": "DocType",
            "permlevel": 0,
            "read": 1,
            "write": 0,
            "create": 0,
            "delete": 0,
            "submit": 0,
            "cancel": 0,
            "amend": 0
        }).insert()
    if not frappe.db.exists("Custom DocPerm", {"role": "Sales User", "parent": "Address"}):
        frappe.get_doc({
            "doctype": "Custom DocPerm",
            "role": "Sales User",
            "parent": "Address",
            "parenttype": "DocType",
            "permlevel": 0,
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 0,
            "submit": 0,
            "cancel": 0,
            "amend": 0
        }).insert()

def disable_roles():
    """Disable the custom roles when the app is uninstalled."""
    roles_to_disable = ["Customer", "Territory Admin", "Partner Admin"]
    
    for role_name in roles_to_disable:
        if frappe.db.exists("Role", role_name):
            role = frappe.get_doc("Role", role_name)
            role.disabled = 1
            role.save()

def remove_role_permissions():
    """Remove role permissions when the app is uninstalled."""
    roles_to_remove = ["Customer", "Territory Admin", "Partner Admin"]
    
    for role_name in roles_to_remove:
        # Remove custom docperms for this role
        custom_docperms = frappe.get_all("Custom DocPerm", filters={"role": role_name})
        for perm in custom_docperms:
            frappe.delete_doc("Custom DocPerm", perm.name)
def create_commerce_domain():
    """Create Commerce domain."""
    if not frappe.db.exists("Domain", "Commerce"):
        frappe.get_doc({
            "doctype": "Domain",
            "domain": "Commerce"
        }).insert()

def set_guest_homepage():
    """Set Guest role homepage"""
    if frappe.db.exists("Role", "Guest"):
        guest_role = frappe.get_doc("Role", "Guest")
        guest_role.save()

@frappe.whitelist()
def get_user_roles():
    roles = frappe.get_roles(frappe.session.user)
    return roles

def reset_guest_homepage():
    """Reset Guest role homepage"""
    if frappe.db.exists("Role", "Guest"):
        guest_role = frappe.get_doc("Role", "Guest")
        guest_role.save()

def get_user_home_page(user):
    """Override default homepage for System Users, but respect portal roles."""
    if not user or user == "Guest":
        return None
        
    user_roles = frappe.get_roles(user)
    
    # If the user has a specific portal role, let hooks.role_home_page handle their routing
    if any(role in user_roles for role in ["Customer", "Partner Admin", "Territory Admin"]):
        return None
        
    user_type = frappe.db.get_value("User", user, "user_type")
    if user_type == "System User":
        return "desk"
        
    return None

@frappe.whitelist()
def set_default_social_login(name):
    """
    Sets the selected Social Login Key as default and unsets others.
    """
    # Check if the document exists
    if not frappe.db.exists("Social Login Key", name):
        frappe.throw(_("Social Login Key {0} not found").format(name))

    try:
        # 1. Set 'custom_default_login' to 0 for all records
        frappe.db.sql("""
            UPDATE `tabSocial Login Key` 
            SET `custom_default_login` = 0
        """)

        # 2. Set 'custom_default_login' to 1 for the selected record
        frappe.db.set_value("Social Login Key", name, "custom_default_login", 1)
        
        # Commit changes to database
        frappe.db.commit()
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Set Default Social Login Failed"))
        frappe.throw(_("An error occurred while setting the default login key."))