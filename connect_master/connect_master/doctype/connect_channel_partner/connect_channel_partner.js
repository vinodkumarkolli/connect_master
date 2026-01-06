// Copyright (c) 2026, Vinod Kumar K and contributors
// For license information, please see license.txt

frappe.ui.form.on("Connect Channel Partner", {
	refresh(frm) {
		if (!frm.doc.__islocal) {
			render_address(frm);
			render_contact(frm);
		}

		frappe.call({
			method: "connect_master.api.get_users_by_role",
			args: {
				doctype: "User",
				txt: "",
				searchfield: "name",
				start: 0,
				page_len: 1000,
				filters: {
					role: "Partner Admin",
				},
			},
			callback: function (r) {
				if (r.message) {
					let users = r.message.map((u) => u[0]);
					frm.set_query("users", function () {
						return {
							filters: {
								name: ["in", users],
							},
						};
					});
				}
			},
		});

		frm.set_query("service_territories", function () {
			return {
				filters: {
					allow_in_search: 1,
					disabled:0
				},
			};
		});
	},
});

function render_address(frm) {
	frappe.call({
		method: 'frappe.client.get_list',
		args: {
			doctype: 'Address',
			filters: [
				['Dynamic Link', 'link_doctype', '=', frm.doctype],
				['Dynamic Link', 'link_name', '=', frm.doc.name]
			],
			fields: ['name', 'address_type', 'address_line1', 'address_line2', 'city', 'state', 'pincode', 'country', 'email_id', 'phone', 'is_primary_address']
		},
		callback: function(r) {
			if (r.message && r.message.length > 0) {
				let html = r.message.map(addr => `
					<div class="address-display" style="margin-bottom: 15px;">
						<div class="text-muted small uppercase" style="margin-bottom: 5px;">${addr.address_type || 'Address'} ${addr.is_primary_address ? '(Primary)' : ''}</div>
						${addr.address_line1 ? `${addr.address_line1}<br>` : ''}
						${addr.address_line2 ? `${addr.address_line2}<br>` : ''}
						${addr.city ? `${addr.city}, ` : ''}
						${addr.state ? `${addr.state} ` : ''}
						${addr.pincode ? `${addr.pincode}` : ''}
						${(addr.city || addr.state || addr.pincode) ? '<br>' : ''}
						${addr.country ? `${addr.country}<br>` : ''}
						${addr.email_id ? `Email: ${addr.email_id}<br>` : ''}
						${addr.phone ? `Phone: ${addr.phone}<br>` : ''}
					</div>
				`).join('<hr>');
				
				if(frm.fields_dict.address_html) {
					frm.fields_dict.address_html.$wrapper.html(html);
				}
			} else {
				if(frm.fields_dict.address_html) {
					frm.fields_dict.address_html.$wrapper.html('<div class="text-muted">No address found</div>');
				}
			}
		}
	});
}

function render_contact(frm) {
	frappe.call({
		method: 'frappe.client.get_list',
		args: {
			doctype: 'Contact',
			filters: [
				['Dynamic Link', 'link_doctype', '=', frm.doctype],
				['Dynamic Link', 'link_name', '=', frm.doc.name]
			],
			fields: ['name', 'first_name', 'last_name', 'email_id', 'mobile_no', 'phone', 'designation', 'is_primary_contact']
		},
		callback: function(r) {
			if (r.message && r.message.length > 0) {
				let html = r.message.map(contact => `
					<div class="contact-display" style="margin-bottom: 15px;">
						<div class="text-muted small uppercase" style="margin-bottom: 5px;">${contact.is_primary_contact ? 'Primary Contact' : 'Contact'}</div>
						<strong>${contact.first_name} ${contact.last_name || ''}</strong><br>
						${contact.designation ? `${contact.designation}<br>` : ''}
						${contact.email_id ? `${contact.email_id}<br>` : ''}
						${contact.mobile_no ? `${contact.mobile_no}<br>` : ''}
						${contact.phone ? `${contact.phone}<br>` : ''}
					</div>
				`).join('<hr>');
				
				if(frm.fields_dict.contact_html) {
					frm.fields_dict.contact_html.$wrapper.html(html);
				}
			} else {
				if(frm.fields_dict.contact_html) {
					frm.fields_dict.contact_html.$wrapper.html('<div class="text-muted">No contact found</div>');
				}
			}
		}
	});
}
