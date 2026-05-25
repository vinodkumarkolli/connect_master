# Copyright (c) 2025, Vinod Kumar K and Contributors
# See license.txt

# import frappe
from frappe.tests import IntegrationTestCase


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]



class IntegrationTestServiceTerritory(IntegrationTestCase):
	"""
	Integration tests for ServiceTerritory.
	Use this class for testing interactions between multiple components.
	"""

	def setUp(self):
		super().setUp()
		import frappe
		# Ensure "Test Country" is present as the root
		if not frappe.db.exists("Service Territory", "Test Country"):
			root = frappe.new_doc("Service Territory")
			root.name = "Test Country"
			root.territory_name = "Test Country"
			root.insert()

		if not frappe.db.exists("Service Territory", "600048"):
			t1 = frappe.new_doc("Service Territory")
			t1.name = "600048"
			t1.territory_name = "600048"
			t1.parent_service_territory = "Test Country"
			t1.insert()
			
		if not frappe.db.exists("Service Territory", "Coimbatore"):
			t2 = frappe.new_doc("Service Territory")
			t2.name = "Coimbatore"
			t2.territory_name = "Coimbatore"
			t2.allow_in_search = 1
			t2.parent_service_territory = "Test Country"
			t2.insert()

	def test_resolve_territory_pincode(self):
		from connect_master.api import resolve_territory
		# Exact pincode match
		res = resolve_territory(pincode="600048")
		self.assertEqual(res, "600048")

	def test_resolve_territory_city(self):
		from connect_master.api import resolve_territory
		# City match (with allow_in_search=1)
		res = resolve_territory(city="Coimbatore")
		self.assertEqual(res, "Coimbatore")

	def test_resolve_territory_fallback(self):
		from connect_master.api import resolve_territory
		# Fallback to root
		res = resolve_territory()
		self.assertEqual(res, "Test Country")



