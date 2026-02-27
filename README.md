# CRMLite

A lightweight desktop CRM application built with Python and Tkinter, backed by Airtable as a database. Manage customers, products, orders, and app users from a clean dark-themed GUI.

> ⚠️ This is a WIP project. Use with caution.

---

## Requirements

- Python 3.x
- Tkinter (included in the Python standard library — no pip install needed)
- An [Airtable](https://airtable.com) account and base

Install third-party dependencies:

```bash
pip install -r requirements.txt
```

> `tkinter`, `datetime`, and `hashlib` are part of Python's standard library and do not need to be installed. Make sure your Python installation includes Tkinter (it usually does by default).

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/panossmav/Airtable-Customer-Manager.git
```

### 2. Set up your Airtable base

Create a new Airtable base with the following tables. All table and field names are **case sensitive**.

#### `Customers` *(Primary Field: Customer ID)*
| Field | Type |
|---|---|
| Name | Single line text |
| Notes | Single line text |
| Phone | Number (integer, no decimal) |
| Email | Single line text |

#### `Products` *(Primary Field: SKU)*
| Field | Type |
|---|---|
| Title | Single line text |
| Price | Number (float, 2 decimal places) |
| SKU | Autonumber |

#### `Orders` *(Primary Field: Order ID)*
| Field | Type |
|---|---|
| Customer | Link from Customers |
| Status | Single line text |
| Total Price | Number (float, 2 decimal places) |
| Customer Phone | Number (integer, no decimal) |
| Date / Time | Single line text |
| Order ID | Autonumber |
| Name | Lookup (Source: Customers → Name) |

#### `App users` *(Primary Field: User ID)*
| Field | Type |
|---|---|
| Username | Single line text |
| Password | Single line text |
| User Type | Single line text |
| User ID | Autonumber |

> **Important:** You must manually create at least one admin user directly in the `App users` table. SHA256-encrypt the password before saving it — you can use [this tool](https://emn178.github.io/online-tools/sha256.html). Set `User Type` to `admin` (lowercase, case sensitive).

#### `User Logs` *(Primary Field: Log ID)*
| Field | Type |
|---|---|
| User | Single line text |
| Action | Single line text |
| Date / Time | Single line text |
| Log ID | Autonumber |

### 3. Configure your API credentials

Create a `.env` file in the project root with your [Airtable API token](https://airtable.com/create/tokens) and base ID:

```env
airtable_api=YOUR_API_TOKEN_GOES_HERE
db_id=YOUR_BASE_ID_GOES_HERE
```

### 4. Run the app

```bash
python main.py
```

Log in with the admin credentials you created in the `App users` table.

---

## Features

All features are available from the home screen. Some are restricted to administrators only.

### 🛒 New Order
Search for a customer by phone number, then add products by SKU. Prices are summed into a running total. Submitting creates an order record in Airtable with status `Fulfilled`.

### 👤 Register Customer
Register a new customer with name, phone number, email, and notes. Phone number must be unique. The notes field is restricted to administrators.

### 📦 Register Product *(Admin only)*
Add a new product with a title and price. The SKU is auto-assigned by Airtable and shown on success.

### 🔄 Change Order Status
Look up an order by its ID and update its status to one of: Fulfilled, Refunded, Pending, or Unknown.

### ➕ Add App User *(Admin only)*
Create a new application login with a username, password, and role. Passwords are stored as SHA256 hashes.

### ⚙️ Change User Type *(Admin only)*
Search for an existing user by username and toggle their role between Regular User and Administrator.

### ✏️ Edit Customer
Search for a customer by phone number and update any of their details — name, email, phone, or notes.

### 🗑️ Delete Customer *(Admin only)*
Search for a customer by phone number and permanently delete them after confirmation.

---

## User Roles

| Feature | Regular User | Administrator |
|---|:---:|:---:|
| New Order | ✅ | ✅ |
| Register Customer | ✅ | ✅ |
| Edit Customer | ✅ | ✅ |
| Change Order Status | ✅ | ✅ |
| Customer notes field | ❌ | ✅ |
| Register Product | ❌ | ✅ |
| Add App User | ❌ | ✅ |
| Change User Type | ❌ | ✅ |
| Delete Customer | ❌ | ✅ |
| Admin stats bar | ❌ | ✅ |

---

## File Structure

```
├── main.py            # UI and application logic
├── funcs.py           # Airtable backend (data access, business logic)
├── .env               # API credentials (not committed to version control)
└── requirements.txt   # Third-party dependencies
```

---

## Notes

- The window is fixed at 560×600 and is not resizable.
- All actions are logged to the `User Logs` table in Airtable, including login, order creation, edits, and deletions.
- The timestamp shown in the app is set once at startup (`gr_time`) and does not update during a session.
- There is a known bug in `modfiy_user_type` in `funcs.py` — it mistakenly updates `customers_table` instead of `users_table`, meaning user type changes do not currently persist. This will be fixed in a future update.