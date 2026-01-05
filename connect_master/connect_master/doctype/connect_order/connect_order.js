frappe.ui.form.on("Connect Order", {
	refresh(frm) {
		if (frm.doc.delivery_address) {
			frm.trigger('render_address');
		}
		if (frm.doc.contact) {
			frm.trigger('render_contact');
		}
	},
	delivery_address(frm) {
		frm.trigger('render_address');
	},
	contact(frm) {
		frm.trigger('render_contact');
	},
	render_address(frm) {
		if (frm.doc.delivery_address) {
			frappe.db.get_doc('Address', frm.doc.delivery_address).then(address => {
				let html = `
					<div class="address-display">
						<div class="text-muted small uppercase" style="margin-bottom: 5px;">Address</div>
						<h5>${address.address_title ? `${address.address_title}<br>` : ''}</h5>
                        ${address.address_line1 ? `${address.address_line1}<br>` : ''}
						${address.address_line2 ? `${address.address_line2}<br>` : ''}
						${address.city ? `${address.city}, ` : ''}
						${address.state ? `${address.state} ` : ''}
						${address.pincode ? `${address.pincode}` : ''}
						${(address.city || address.state || address.pincode) ? '<br>' : ''}
						${address.country ? `${address.country}<br>` : ''}
					</div>
				`;
				frm.fields_dict.address_html.$wrapper.html(html);
			});
		} else {
			frm.fields_dict.address_html.$wrapper.html("");
		}
	},
	render_contact(frm) {
		if (frm.doc.contact) {
			frappe.call({
				method: "frappe.contacts.doctype.contact.contact.get_contact_details",
				args: {
					contact: frm.doc.contact
				},
				callback: function(r) {
					if (r.message) {
						let data = r.message;
						let html = `
							<div class="address-display">
								<div class="text-muted small uppercase" style="margin-bottom: 5px;">Contact</div>
								${data.contact_display ? `<strong>${data.contact_display}</strong><br>` : ''}
								${data.contact_designation ? `${data.contact_designation}<br>` : ''}
								${data.contact_department ? `${data.contact_department}<br>` : ''}
								${data.contact_email ? `${data.contact_email}<br>` : ''}
								${data.contact_mobile ? `${data.contact_mobile}<br>` : ''}
								${data.contact_phone ? `${data.contact_phone}<br>` : ''}
							</div>
						`;
						frm.fields_dict.contact_html.$wrapper.html(html);
					}
				}
			});
		} else {
			frm.fields_dict.contact_html.$wrapper.html("");
		}
	}
});
