# Copyright (c) 2026, Vinod Kumar K and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ConnectAnnouncement(Document):
	pass

@frappe.whitelist(allow_guest=True)
def get_active_announcements(location):
	announces = frappe.get_list("Connect Announcement",
		filters={"active": 1, "display_location": location},
		fields=["name", "announcement_type", "display_html"],
		order_by="creation desc"
	)
	return announces
