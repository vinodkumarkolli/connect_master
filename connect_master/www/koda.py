import frappe

def get_context(context):
    # 1. Prevent Frappe from wrapping your SPA in the standard website navbar/footer
    context.full_page = True
    context.no_cache = 1
    
    # 2. Add 'boot' data so the SPA knows the user status immediately without an extra API call
    # This is helpful for the SPA to decide between a "Login" view and "Home" view
    context.boot = get_boot_data()
    
    return context

def get_boot_data():
    """Returns essential session data for the frontend"""
    user = frappe.session.user
    return {
        "is_logged_in": user != "Guest",
        "user": user,
        "full_name": frappe.utils.get_fullname(user) if user != "Guest" else "Guest",
        "csrf_token": frappe.sessions.get_csrf_token()
    }