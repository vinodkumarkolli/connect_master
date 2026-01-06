# Copyright (c) 2025, Vinod Kumar K and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from connect_master.connect_master.doctype.connect_order.connect_order import get_channel_partners
from frappe.utils.nestedset import rebuild_tree

# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]

class IntegrationTestConnectOrder(IntegrationTestCase):
	"""
	Integration tests for ConnectOrder.
	Use this class for testing interactions between multiple components.
	"""
	
	def setUp(self):
		frappe.db.delete("Connect Channel Partner")
		frappe.db.delete("Service Territory")
		frappe.db.delete("Service Channel")

		# Create Channel
		self.channel = frappe.get_doc({
			"doctype": "Service Channel",
			"channel_name": "Test Channel",
			"channel_shorthand": "TC"
		}).insert()

		# Create Territories
		self.country = frappe.get_doc({
			"doctype": "Service Territory",
			"territory_name": "Test Country",
			"is_group": 1
		}).insert()

		self.state = frappe.get_doc({
			"doctype": "Service Territory",
			"territory_name": "Test State",
			"parent_service_territory": self.country.name,
			"is_group": 1
		}).insert()

		self.city = frappe.get_doc({
			"doctype": "Service Territory",
			"territory_name": "Test City",
			"parent_service_territory": self.state.name,
			"is_group": 0
		}).insert()
		
		rebuild_tree("Service Territory")

		# Create Partners
		# Partner 1: Serves Country
		self.p1 = frappe.get_doc({
			"doctype": "Connect Channel Partner",
			"partner_name": "Partner 1",
			"service_channels": [{"service_channel": self.channel.name}],
			"service_territories": [{"service_territory": self.country.name}]
		}).insert()

		# Partner 2: Serves Country, Excludes City
		self.p2 = frappe.get_doc({
			"doctype": "Connect Channel Partner",
			"partner_name": "Partner 2",
			"service_channels": [{"service_channel": self.channel.name}],
			"service_territories": [{"service_territory": self.country.name}],
			"excluded_service_territories": [{"service_territory": self.city.name}]
		}).insert()

	def test_exclusion(self):
		# Query for City
		# Ancestors of City: City, State, Country
		
		partners = get_channel_partners(self.city.name, self.channel.name)
		partner_names = [p.partner_name for p in partners]
		
		self.assertIn("Partner 1", partner_names)
		self.assertNotIn("Partner 2", partner_names)

	def test_inclusion_higher_level(self):
		# Query for State
		# Ancestors of State: State, Country
		# Partner 2 excludes City. City is NOT in ancestors of State.
		# So Partner 2 should be included.
		
		partners = get_channel_partners(self.state.name, self.channel.name)
		partner_names = [p.partner_name for p in partners]
		
		self.assertIn("Partner 1", partner_names)
		self.assertIn("Partner 2", partner_names)
