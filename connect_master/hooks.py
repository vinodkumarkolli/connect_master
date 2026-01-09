app_name = "connect_master"
app_title = "Connect Master"
app_publisher = "Vinod Kumar K"
app_description = "This is the new Sravi Enterprises attempt to design and develop an application to connect the orders placed by the customers to the channel partners"
app_email = "sravienterprises1@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
    {
		"name": "connect_master",
		"logo": "/assets/connect_master/images/radar-logo.png",
		"title": "Connect Master",
		"route": "/koda",
		#"has_permission": "connect_master.api.permission.has_app_permission"
	}
]
	

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/connect_master/css/connect_master.css"
# app_include_js = "/assets/connect_master/js/connect_master.js"

# include js, css files in header of web template
# web_include_css = "/assets/connect_master/css/connect_master.css"
# web_include_js = "/assets/connect_master/js/connect_master.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "connect_master/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "connect_master/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "koda"

# website user home page (by Role)
role_home_page = {
	"Customer": "koda",
    "Partner Admin":"koda/dash",
    "Territory Admin":"koda/dash",
    "System Manager":"desk"
}

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "connect_master.utils.jinja_methods",
# 	"filters": "connect_master.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "connect_master.install.before_install"
after_install = "connect_master.utils.after_install"

# Uninstallation
# ------------

# before_uninstall = "connect_master.uninstall.before_uninstall"
after_uninstall = "connect_master.utils.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "connect_master.utils.before_app_install"
# after_app_install = "connect_master.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "connect_master.utils.before_app_uninstall"
# after_app_uninstall = "connect_master.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "connect_master.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"hourly": [
		"connect_master.connect_master.doctype.connect_order.connect_order.check_unresolved_orders"
	],
}

# Testing
# -------

# before_tests = "connect_master.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "connect_master.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "connect_master.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "connect_master.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["connect_master.utils.before_request"]
# after_request = ["connect_master.utils.after_request"]

# Job Events
# ----------
# before_job = ["connect_master.utils.before_job"]
# after_job = ["connect_master.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"connect_master.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []
fixtures = [
    # Export all Custom Fields
    {"dt": "Custom Field","filters": [["module", "in", ["Connect Master"]]]},
    {"dt": "Custom DocPerm"},
    # Export all Property Setters
    {"dt": "Service Territory"},
    # Export specific Clients Scripts
    {"dt": "Service Channel"},
    # Export specific DocType records
    {"dt": "Connect Item"},
    {"dt":"Email Template"},
    {"dt":"Connect Email Settings"},
    {"dt":"User","filters": [["email", "=", "customer@example.com"]]}
    # {"dt":"Connect Channel Partner"}
]

website_route_rules = [{'from_route': '/koda/<path:app_path>', 'to_route': 'koda'}]