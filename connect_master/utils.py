import frappe

def after_install():
    """Create roles and set permissions after app installation."""
    create_commerce_domain()
    create_roles()
    set_role_permissions()

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
            "desk_access": 1,
            "home_page": "/desk"
        }).insert()
    
    # Create Partner Admin role (desk access, limited to Radar app)
    if not frappe.db.exists("Role", "Partner Admin"):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": "Partner Admin",
            "desk_access": 1,
            "home_page": "/desk"
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