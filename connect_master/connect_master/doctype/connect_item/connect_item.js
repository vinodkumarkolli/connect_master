// Copyright (c) 2025, Vinod Kumar K and contributors
// For license information, please see license.txt

frappe.ui.form.on("Connect Item", {
	refresh(frm) {
		// Display image in image_html field when item_image is uploaded
		if (frm.doc.item_image) {
			frm.set_df_property('image_html', 'options', `<img src="${frm.doc.item_image}" style="max-width: 100%; max-height: 300px;">`);
		} else {
			frm.set_df_property('image_html', 'options', '');
		}
	},
	
	item_image(frm) {
		// Update image_html when item_image changes
		if (frm.doc.item_image) {
			frm.set_df_property('image_html', 'options', `<img src="${frm.doc.item_image}" style="max-width: 100%; max-height: 300px;">`);
		} else {
			frm.set_df_property('image_html', 'options', 'No image uploaded');
		}
	}
});
