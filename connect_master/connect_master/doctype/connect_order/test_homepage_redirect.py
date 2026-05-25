# Copyright (c) 2026, Vinod Kumar K and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from connect_master.utils import ensure_homepage_default

class TestHomepageRedirect(IntegrationTestCase):
	def test_ensure_homepage_default(self):
		# Save original setup_complete and homepage defaults
		original_setup_complete = frappe.db.get_single_value("System Settings", "setup_complete")
		original_homepage = frappe.db.get_value("DefaultValue", {"defkey": "desktop:home_page", "parent": "__default"}, "defvalue")

		try:
			# Mock system settings to setup_complete = 1
			frappe.db.set_single_value("System Settings", "setup_complete", 1)

			# Forcefully set default to "setup-wizard" to replicate the redirection loop issue
			frappe.db.set_default("desktop:home_page", "setup-wizard")

			# Run the correction logic
			ensure_homepage_default()

			# Assert that the logic corrected the default to "workspace"
			corrected_homepage = frappe.db.get_value("DefaultValue", {"defkey": "desktop:home_page", "parent": "__default"}, "defvalue")
			self.assertEqual(corrected_homepage, "workspace")

		finally:
			# Restore original system settings and homepage defaults
			frappe.db.set_single_value("System Settings", "setup_complete", original_setup_complete)
			if original_homepage:
				frappe.db.set_default("desktop:home_page", original_homepage)
			else:
				frappe.db.delete("DefaultValue", {"defkey": "desktop:home_page", "parent": "__default"})
			frappe.db.commit()
