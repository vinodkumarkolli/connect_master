frappe.ui.form.on("Service Territory", {
	refresh(frm) {
		frappe.call({
			method: "connect_master.api.get_users_by_role",
			args: {
				doctype: "User",
				txt: "",
				searchfield: "name",
				start: 0,
				page_len: 1000,
				filters: {
					role: "Territory Admin",
				},
			},
			callback: function (r) {
				if (r.message) {
					let users = r.message.map((u) => u[0]);
					frm.set_query("territory_admins", function () {
						return {
							filters: {
								name: ["in", users],
							},
						};
					});
				}
			}
		});
	},
});
