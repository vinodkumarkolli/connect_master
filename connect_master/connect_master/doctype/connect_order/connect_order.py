# Copyright (c) 2025, Vinod Kumar K and contributors
# For license information, please see license.txt

import frappe
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from frappe.model.document import Document
from frappe.utils import now


class ConnectOrder(Document):
	def before_submit(self):
		pass

	def on_submit(self):
		self.send_order_notifications()

	def send_order_notifications(self):
		# 1. Territory Admin Notification
		self.notify_territory_admins()
		
		# 2. Channel Partner Notification
		self.notify_channel_partners()

	def notify_territory_admins(self):
		if not self.delivery_address:
			return

		# Get resolved territory from Address
		resolved_territory = frappe.db.get_value("Address", self.delivery_address, "custom_resolved_territory")
		if not resolved_territory:
			return

		admins = []
		current_territory = resolved_territory
		
		# Traverse up until admins are found
		while current_territory:
			territory_doc = frappe.get_doc("Service Territory", current_territory)
			
			# Check for admins in current territory
			if territory_doc.territory_admins:
				for admin in territory_doc.territory_admins:
					if admin.user:
						admins.append(admin.user)
			
			if admins:
				break
			
			# Move to parent
			current_territory = territory_doc.parent_service_territory
		
		if admins:
			self.send_email(admins)
		else:
			# Raven alert placeholder (pass for now)
			pass

	def notify_channel_partners(self):
		if not self.channel_partner:
			return

		partner_doc = frappe.get_doc("Connect Channel Partner", self.channel_partner)
		
		if partner_doc.notification_type == "Transactional":
			recipients = []
			if partner_doc.users:
				for user_row in partner_doc.users:
					if user_row.user:
						recipients.append(user_row.user)
			
			if recipients:
				self.send_email(recipients)

	def send_email(self, recipients):
		# Remove duplicates
		recipients = list(set(recipients))
		final_recipients = []
		for user in recipients:
			email = frappe.db.get_value("User", user, "email") or user
			final_recipients.append(email)
		
		if not final_recipients:
			return

		# Get Email Settings
		email_settings = frappe.get_single("Connect Email Settings")
		
		# Get Email Template
		template_name = "Order Notification for internal users"
		try:
			template = frappe.get_doc("Email Template", template_name)
		except frappe.DoesNotExistError:
			frappe.log_error(f"Email Template {template_name} not found")
			return

		# Render Template
		context = {"doc": self}
		subject = frappe.render_template(template.subject, context)
		message = frappe.render_template(template.response_html or template.response, context)

		if email_settings.settings_type == "Frappe Inbuilt":
			sender = None
			if email_settings.email_account:
				sender = frappe.db.get_value("Email Account", email_settings.email_account, "email_id")

			frappe.sendmail(
				recipients=final_recipients,
				subject=subject,
				message=message,
				sender=sender,
				now=True
			)
		else:
			if not email_settings.outgoing_server:
				frappe.log_error("Email settings not configured for Connect Order notification")
				return
			
			try:
				port = int(email_settings.port) if email_settings.port else 587
				
				# Connect to server
				if email_settings.use_ssl:
					server = smtplib.SMTP_SSL(email_settings.outgoing_server, port)
				else:
					server = smtplib.SMTP(email_settings.outgoing_server, port)
					if email_settings.use_tls:
						server.starttls()
				
				# Login
				server.login(email_settings.username, email_settings.get_password('password'))
				
				for recipient in final_recipients:
					msg = MIMEMultipart()
					msg['From'] = email_settings.sender_email
					msg['To'] = recipient
					msg['Subject'] = subject
					msg.attach(MIMEText(message, 'html'))
					
					server.sendmail(email_settings.sender_email, recipient, msg.as_string())
				
				server.quit()
				
			except Exception as e:
				frappe.log_error(f"Failed to send Connect Order notification: {str(e)}")

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
		# Check if user is linked to the delivery address
		is_linked = False
		if doc.delivery_address:
			is_linked = frappe.db.exists("Dynamic Link", {
				"parent": doc.delivery_address,
				"parenttype": "Address",
				"link_doctype": "User",
				"link_name": user
			})
		
		if not is_linked:
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

def check_unresolved_orders():
	from frappe.utils import add_days, now_datetime
	
	# 2 days ago
	threshold_date = add_days(now_datetime(), -7)
	
	orders = frappe.get_all("Connect Order", filters={
		"order_status": ["not in", ["Cancelled", "Fulfilled"]],
		"unresolved_push": 0,
		"order_date": ["<", threshold_date]
	}, pluck="name")
	
	if orders:
		frappe.db.set_value("Connect Order", orders, "unresolved_push", 1)
