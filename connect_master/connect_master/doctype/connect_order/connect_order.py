# Copyright (c) 2025, Vinod Kumar K and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now


class ConnectOrder(Document):
	def before_submit(self):
		pass

@frappe.whitelist()
def add_timeline_event(order_name, event_type, payload):
	import json
	if isinstance(payload, str):
		payload = json.loads(payload)

	user = frappe.session.user
	if user == "Guest":
		frappe.throw("Please login")

	doc = frappe.get_doc("Connect Order", order_name)
	
	if doc.user != user and user != "Administrator":
		frappe.throw("Not authorized")

	event = {
		"event_type": event_type,
		"recorded_time": now(),
		"is_internal": 0,
		"created_by": user
	}

	if event_type == "Comment":
		if isinstance(payload, dict):
			event["event_detail"] = payload.get("comment") or payload.get("event_detail")
		else:
			event["event_detail"] = str(payload)
	else:
		if isinstance(payload, dict):
			event.update(payload)

	doc.append("timeline", event)
	doc.save(ignore_permissions=True)

@frappe.whitelist()
def get_channel_partners(territory, channel):
	if not territory or not channel:
		return []

	# Get lft, rgt of the territory
	territory_details = frappe.db.get_value("Service Territory", territory, ["lft", "rgt", "name"], as_dict=True)
	if not territory_details:
		return []

	lft, rgt = territory_details.lft, territory_details.rgt

	ancestors = []
	if lft and rgt:
		# Find ancestors (including self)
		ancestors = frappe.get_all("Service Territory",
			filters={"lft": ["<=", lft], "rgt": [">=", rgt]},
			pluck="name"
		)
	
	# Ensure self is in ancestors (fallback if NSM is not set up or broken)
	if territory not in ancestors:
		ancestors.append(territory)

	# Resolve channel ID if name was passed
	channel_id = channel
	if not frappe.db.exists("Service Channel", channel):
		# Try finding by channel_name
		c_name = frappe.db.get_value("Service Channel", {"channel_name": channel}, "name")
		if c_name:
			channel_id = c_name

	partners = frappe.db.sql("""
		SELECT
			cp.name, cp.partner_name, cp.description
		FROM
			`tabConnect Channel Partner` cp
		JOIN
			`tabConnect Map Service Channel` cmsc ON cmsc.parent = cp.name
		JOIN
			`tabConnect Map Service Territory` cmst ON cmst.parent = cp.name
		JOIN
			`tabService Territory` st ON st.name = cmst.service_territory
		WHERE
			cp.disabled = 0
			AND cmsc.service_channel = %(channel)s
			AND cmst.service_territory IN %(territories)s
			AND cmst.parentfield = 'service_territories'
			AND NOT EXISTS (
				SELECT 1
				FROM `tabConnect Map Service Territory` excluded
				WHERE excluded.parent = cp.name
				AND excluded.parentfield = 'excluded_service_territories'
				AND excluded.service_territory IN %(territories)s
			)
		GROUP BY
			cp.name, cp.partner_name, cp.description
		ORDER BY
			MAX(st.lft) DESC
	""", {
		"channel": channel_id,
		"territories": tuple(ancestors)
	}, as_dict=True)

	for p in partners:
		# Address
		addr = frappe.db.sql("""
			SELECT a.address_line1, a.city, a.pincode
			FROM `tabAddress` a
			JOIN `tabDynamic Link` dl ON dl.parent = a.name
			WHERE dl.link_doctype = 'Connect Channel Partner' AND dl.link_name = %s AND a.disabled = 0
			ORDER BY a.is_primary_address DESC LIMIT 1
		""", (p.name,), as_dict=True)
		
		if addr:
			a = addr[0]
			parts = [a.address_line1, a.city, a.pincode]
			p.address_html = ", ".join([str(x) for x in parts if x])
		else:
			p.address_html = ""

		# Contact
		cont = frappe.db.sql("""
			SELECT c.first_name, c.last_name, c.mobile_no, c.email_id
			FROM `tabContact` c
			JOIN `tabDynamic Link` dl ON dl.parent = c.name
			WHERE dl.link_doctype = 'Connect Channel Partner' AND dl.link_name = %s
			ORDER BY c.is_primary_contact DESC LIMIT 1
		""", (p.name,), as_dict=True)

		if cont:
			c = cont[0]
			name = f"{c.first_name or ''} {c.last_name or ''}".strip()
			details = []
			if c.mobile_no: details.append(c.mobile_no)
			if c.email_id: details.append(c.email_id)
			p.contact_html = f"<div>{name}</div><div class='text-gray-500'>{', '.join(details)}</div>"
		else:
			p.contact_html = ""

	return partners
