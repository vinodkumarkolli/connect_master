# Connect Master

Connect Master is a custom Frappe application designed for **Sravi Enterprises** to streamline order taking, geocoded territory routing, and dispatching to localized independent channel partners.

---

## 1. What is Connect Master?

Connect Master facilitates a decentralized fulfillment model:
1. **Intelligent Order Taking**: Orders are placed directly via a modern Single Page Application (SPA) frontend named **Koda**.
2. **Geographic Territory Routing**: Delivery addresses are resolved to a corresponding **Service Territory** (leaf pincode or city level) by matching them against the database.
3. **Channel Partner Dispatch**: The system evaluates the territory and the business category (**Service Channel**) to present a list of eligible independent **Channel Partners**.
4. **Offline Fulfillment**: Company logistics are bypassed. Channel Partners receive notifications, accept/reject assignments, and execute delivery and payment collection offline.

---

## 2. Key Differences from Standard ERPNext Order Flow

* **No Customer DocType dependency**: Captures customer shipping details directly on the `Connect Order` using linked `Address` and `Contact` documents.
* **Geographical & Categorical Collections**: Uses nested tree geography (`Service Territory`) and business categorization (`Service Channel`) instead of customer-group divisions.
* **No Stock/Invoice Linkage**: Fulfillment is carried out offline. There is no automated generation of Sales Orders, Delivery Notes, or Sales Invoices within ERPNext.

---

## 3. Architecture & Core DocTypes

* **Connect Order (`Connect Order`)**: Main submittable document containing ordered items, address, contact, and fulfillment statuses (`Submitted`, `Assigned`, `Accepted`, `Rejected`, `Cancelled`, `Fulfilled`).
* **Service Territory (`Service Territory`)**: Tree structured geographical boundaries. Leaf nodes represent pincodes (e.g. `600048`), while parent nodes represent cities, districts, or groups.
* **Service Channel (`Service Channel`)**: Logical groupings of business categories representing credit terms and partner workflows (e.g., *Pharma*, *General Trade (GT)*, *Modern Trade (MT)*, *Direct Customer*).
* **Connect Channel Partner (`Connect Channel Partner`)**: independent partners mapped to allowed service channels and territories.
* **Connect Map Users (`Connect Map Users`)**: Links Frappe system users to specific channel partners or service territories (for admins).

---

## 4. Koda Frontend (SPA Portal)

The app ships with a built-in Single Page Application served at the `/koda` route:
* **Built with**: Vue.js, TailwindCSS, and Vite.
* **Source Directory**: located in `apps/connect_master/koda/`.
* **OTP Verification**: Authenticates users (*Customers*) via a passwordless 6-digit OTP sent to their emails.
* **Database-Driven Territory Resolution**: Automatically maps address pincodes or cities directly to the matching `Service Territory` in the backend, with a fallback to the parent-most root territory.

---

## 5. Installation & Setup

Install this app on your Frappe bench:

```bash
# Get the app from repository
bench get-app connect_master https://github.com/Sravi-Enterprises/connect-master.git --branch develop

# Install the app on your site
bench --site [your-site-name] install-app connect_master

# Run migrations to initialize roles and configurations
bench --site [your-site-name] migrate
```

---

## 6. Development & Contributing

### Directory Structure
```
connect_master/
├── connect_master/          # Python backend controllers, APIs, and fixtures
│   ├── connect_master/      # DocTypes Definitions
│   ├── fixtures/            # Core client scripts and fields exports
│   └── api.py               # Whitelisted backend APIs for Koda portal
├── koda/                    # Koda SPA Frontend Source (Vue/Vite)
└── README.md
```

### Pre-commit Configuration
Before committing any code, ensure you have `pre-commit` configured for formatting and linting:

```bash
cd apps/connect_master
pre-commit install
```

Pre-commit checks run:
* `ruff` (Python linting & formatting)
* `eslint` (JS/Vue linting)
* `prettier` (Styling & formatting)
* `pyupgrade` (Python syntax upgrade warnings)

### Building the Frontend SPA
If you make changes to the `koda/` source files, rebuild the frontend bundle:

```bash
cd apps/connect_master/koda
yarn install
yarn build
```
This compiles the SPA assets directly into `connect_master/public/frontend/` to be served by Frappe.
