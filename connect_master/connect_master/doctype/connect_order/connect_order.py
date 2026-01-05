# Copyright (c) 2025, Vinod Kumar K and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now


class ConnectOrder(Document):
	def before_submit(self):
		self.append("timeline", {
			"event_type": "Status Update",
			"recorded_time": now(),
			"is_internal": 0,
			"fieldname":"order_status",
			"from_value":"Initiated",
			"to_value":self.order_status
		})
