import tkinter as tk
from tkinter import messagebox as pu
from tkinter import ttk
from funcs import *

BG        = "#0f1117"
PANEL     = "#1a1d27"
BORDER    = "#2a2d3e"
ACCENT    = "#6c63ff"
ACCENT2   = "#00d4aa"
DANGER    = "#ff5370"
TEXT      = "#e8eaf0"
MUTED     = "#6b7280"
ENTRY_BG  = "#252836"
FONT      = "Segoe UI"

root = tk.Tk()
root.title("CRMLite")
root.geometry("560x600")
root.configure(bg=BG)
root.resizable(False, False)


def styled_window(title_text, w=520, h=520):
    win = tk.Toplevel(root)
    win.title(title_text)
    win.geometry(f"{w}x{h}")
    win.configure(bg=BG)
    win.resizable(False, False)
    header = tk.Frame(win, bg=BG)
    header.pack(fill="x")
    tk.Label(header, text=title_text, font=(FONT, 14, "bold"), bg=BG, fg=TEXT
             ).pack(anchor="w", padx=24, pady=(20, 4))
    tk.Frame(header, bg=BORDER, height=1).pack(fill="x", padx=24, pady=(0, 12))
    body = tk.Frame(win, bg=BG)
    body.pack(fill="both", expand=True)
    return win, body


def grid_entry(parent, label_text, row, show=None):
    tk.Label(parent, text=label_text, font=(FONT, 10), bg=BG, fg=MUTED
             ).grid(row=row, column=0, sticky="w", padx=24, pady=(8, 0))
    e = tk.Entry(parent, font=(FONT, 11), bg=ENTRY_BG, fg=TEXT,
                 insertbackground=TEXT, relief="flat",
                 highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor=ACCENT, show=show or "", width=30)
    e.grid(row=row, column=1, sticky="ew", padx=(4, 24), pady=(8, 0))
    return e


def styled_combo(parent, values, row):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("D.TCombobox",
                    fieldbackground=ENTRY_BG, background=ENTRY_BG,
                    foreground=TEXT, bordercolor=BORDER,
                    arrowcolor=ACCENT, selectbackground=ACCENT,
                    selectforeground=TEXT)
    cb = ttk.Combobox(parent, values=values, state="readonly",
                      style="D.TCombobox", font=(FONT, 11))
    cb.grid(row=row, column=0, columnspan=2, sticky="ew", padx=24, pady=(4, 0))
    cb.current(0)
    return cb


def action_btn(parent, text, command, row=None, color=ACCENT, fg_col="#ffffff"):
    b = tk.Button(parent, text=text, command=command,
                  font=(FONT, 11, "bold"), bg=color, fg=fg_col,
                  relief="flat", cursor="hand2", pady=8, bd=0)
    if row is not None:
        b.grid(row=row, column=0, columnspan=2, sticky="ew", padx=24, pady=14)
    else:
        b.pack(fill="x", padx=24, pady=4)
    return b


username = ""
isadmin  = False


def clear_root():
    for w in root.winfo_children():
        w.destroy()


def log_in():
    clear_root()
    card = tk.Frame(root, bg=PANEL)
    card.place(relx=0.5, rely=0.5, anchor="center", width=340, height=340)

    tk.Label(card, text="CRMLite", font=(FONT, 22, "bold"), bg=PANEL, fg=ACCENT
             ).pack(pady=(28, 2))
    tk.Label(card, text="Sign in to continue", font=(FONT, 10), bg=PANEL, fg=MUTED
             ).pack(pady=(0, 16))

    def field(label, show=None):
        tk.Label(card, text=label, font=(FONT, 10), bg=PANEL, fg=MUTED
                 ).pack(anchor="w", padx=28)
        e = tk.Entry(card, font=(FONT, 11), bg=ENTRY_BG, fg=TEXT,
                     insertbackground=TEXT, relief="flat",
                     highlightthickness=1, highlightbackground=BORDER,
                     highlightcolor=ACCENT, show=show or "", width=26)
        e.pack(padx=28, pady=(2, 10), fill="x")
        return e

    user_e  = field("Username")
    passw_e = field("Password", show="•")

    msg_lbl = tk.Label(card, text="", font=(FONT, 9), bg=PANEL, fg=DANGER)
    msg_lbl.pack()

    def auth():
        global username, isadmin
        username = user_e.get()
        success, isadmin = check_user_pass(username, passw_e.get())
        if success:
            home()
        else:
            msg_lbl.config(text="Incorrect username or password.")
            passw_e.delete(0, tk.END)

    tk.Button(card, text="Sign In", command=auth,
              font=(FONT, 11, "bold"), bg=ACCENT, fg="#fff",
              relief="flat", cursor="hand2", pady=7, bd=0
              ).pack(fill="x", padx=28, pady=(6, 0))


def home():
    clear_root()

    topbar = tk.Frame(root, bg=PANEL, height=54)
    topbar.pack(fill="x")
    topbar.pack_propagate(False)
    tk.Label(topbar, text="CRMLite", font=(FONT, 14, "bold"), bg=PANEL, fg=ACCENT
             ).pack(side="left", padx=20)
    tk.Label(topbar, text=f"@{username}", font=(FONT, 10), bg=PANEL, fg=MUTED
             ).pack(side="left", padx=4)
    tk.Button(topbar, text="Logout", command=log_in,
              font=(FONT, 9), bg=BORDER, fg=MUTED,
              relief="flat", cursor="hand2", padx=8, pady=2, bd=0
              ).pack(side="right", padx=16, pady=14)

    if isadmin:
        badge = tk.Frame(root, bg=ACCENT, height=28)
        badge.pack(fill="x")
        badge.pack_propagate(False)
        tk.Label(badge,
                 text=f"Administrator  ·  Customers: {total_cust()}  ·  Revenue: {total_net()}",
                 font=(FONT, 9, "bold"), bg=ACCENT, fg="#fff"
                 ).pack(side="left", padx=16)
    else:
        badge = tk.Frame(root, bg="#2a1f1f", height=28)
        badge.pack(fill="x")
        badge.pack_propagate(False)
        tk.Label(badge, text="Regular user  ·  Limited functionality",
                 font=(FONT, 9), bg="#2a1f1f", fg=DANGER
                 ).pack(side="left", padx=16)

    tk.Label(root, text=f"Last updated: {now()}", font=(FONT, 9), bg=BG, fg=MUTED
             ).pack(anchor="w", padx=20, pady=(10, 4))
    tk.Frame(root, bg=BORDER, height=1).pack(fill="x", padx=20)

    actions = [
        ("🛒  New Order",           create_order),
        ("👤  Register Customer",   create_customer),
        ("📦  Register Product",    create_product),
        ("🔄  Change Order Status", change_order_status),
        ("➕  Add App User",        create_user),
        ("⚙️  Change User Type",    change_user_type),
        ("✏️  Edit Customer",       modify_cust_info),
        ("🗑️  Delete Customer",     delete_cust),
    ]

    grid = tk.Frame(root, bg=BG)
    grid.pack(fill="both", expand=True, padx=20, pady=12)
    grid.columnconfigure(0, weight=1)
    grid.columnconfigure(1, weight=1)

    for i, (label, cmd) in enumerate(actions):
        r, c = divmod(i, 2)
        tk.Button(grid, text=label, command=cmd,
                  font=(FONT, 10, "bold"), bg=PANEL, fg=TEXT,
                  activebackground=ACCENT, activeforeground="#fff",
                  relief="flat", cursor="hand2",
                  anchor="w", padx=14, pady=12, bd=0
                  ).grid(row=r, column=c, sticky="ew", padx=5, pady=4)


def create_order():
    win, body = styled_window("New Order", h=560)

    tk.Label(body, text="Customer phone number", font=(FONT, 10), bg=BG, fg=MUTED
             ).pack(anchor="w", padx=24)

    ph_row = tk.Frame(body, bg=BG)
    ph_row.pack(fill="x", padx=24, pady=(2, 0))
    phone_e = tk.Entry(ph_row, font=(FONT, 11), bg=ENTRY_BG, fg=TEXT,
                       insertbackground=TEXT, relief="flat",
                       highlightthickness=1, highlightbackground=BORDER,
                       highlightcolor=ACCENT, width=24)
    phone_e.pack(side="left")
    tk.Button(ph_row, text="Search", command=lambda: sbt_find_cust(),
              font=(FONT, 10, "bold"), bg=ACCENT, fg="#fff",
              relief="flat", cursor="hand2", padx=10, pady=4, bd=0
              ).pack(side="left", padx=(8, 0))

    info_lbl = tk.Label(body, text="", font=(FONT, 10), bg=BG, fg=ACCENT2, justify="left")
    info_lbl.pack(anchor="w", padx=24, pady=(6, 0))

    tk.Frame(body, bg=BORDER, height=1).pack(fill="x", padx=24, pady=8)

    sku_row = tk.Frame(body, bg=BG)
    tk.Label(sku_row, text="Product SKU", font=(FONT, 10), bg=BG, fg=MUTED
             ).pack(side="left")
    sku_e = tk.Entry(sku_row, font=(FONT, 11), bg=ENTRY_BG, fg=TEXT,
                     insertbackground=TEXT, relief="flat",
                     highlightthickness=1, highlightbackground=BORDER,
                     highlightcolor=ACCENT, width=18)
    sku_e.pack(side="left", padx=(8, 6))

    product_frame = tk.Frame(body, bg=BG)
    total_var = tk.DoubleVar(value=0.0)
    total_lbl = tk.Label(body, text="Total: €0.00", font=(FONT, 13, "bold"), bg=BG, fg=ACCENT)
    submit_btn_holder = tk.Frame(body, bg=BG)
    row_counter = [0]
    phone_int_holder = [None]

    def add_product():
        sku = sku_e.get()
        if not sku:
            pu.showerror("CRMLite", "Please enter a SKU!"); return
        try:
            sku_int = int(sku)
        except ValueError:
            pu.showerror("CRMLite", "SKU must be a number!"); return
        if check_product(sku_int):
            title, price = fetch_product_info(sku_int)
            tk.Label(product_frame,
                     text=f"  • {title}  —  €{price:.2f}",
                     font=(FONT, 10), bg=BG, fg=TEXT
                     ).grid(row=row_counter[0], column=0, sticky="w", pady=1)
            total_var.set(total_var.get() + price)
            total_lbl.config(text=f"Total: €{total_var.get():.2f}")
            row_counter[0] += 1
            sku_e.delete(0, "end")
        else:
            pu.showerror("CRMLite", f"No product with SKU {sku_int}.")

    tk.Button(sku_row, text="Add", command=add_product,
              font=(FONT, 10, "bold"), bg=ACCENT, fg="#fff",
              relief="flat", cursor="hand2", padx=8, pady=4, bd=0
              ).pack(side="left")

    def submit_order():
        result, msg = new_order(phone_int_holder[0], total_var.get(), username)
        if result:
            pu.showinfo("CRMLite", msg); win.destroy()
        else:
            pu.showerror("CRMLite", msg)

    tk.Button(submit_btn_holder, text="✔  Submit Order", command=submit_order,
              font=(FONT, 11, "bold"), bg=ACCENT2, fg="#0f1117",
              relief="flat", cursor="hand2", pady=8, bd=0
              ).pack(fill="x")

    def sbt_find_cust():
        ph = phone_e.get()
        if not ph:
            pu.showerror("CRMLite", "Please enter a phone number!"); return
        try:
            pi = int(ph)
        except ValueError:
            pu.showerror("CRMLite", "Invalid phone number!"); return
        if check_phone(pi):
            phone_int_holder[0] = pi
            name, phone, email, notes = fetch_customer_info(pi)
            info_lbl.config(text=f"✔  {name}  ·  {phone}  ·  {email}")
            sku_row.pack(fill="x", padx=24, pady=(0, 4))
            product_frame.pack(fill="x", padx=24)
            total_lbl.pack(anchor="w", padx=24, pady=(4, 0))
            submit_btn_holder.pack(fill="x", padx=24, pady=8)
        else:
            pu.showerror("CRMLite", f"No customer with number {ph}.\nAdd them first.")


def create_customer():
    win, body = styled_window("Register Customer")
    body.columnconfigure(1, weight=1)

    phone_e = grid_entry(body, "Phone",  0)
    name_e  = grid_entry(body, "Name",   1)
    email_e = grid_entry(body, "Email",  2)
    notes_e = grid_entry(body, "Notes",  3)
    if not isadmin:
        notes_e.config(state="disabled")

    def sbt():
        phone, name, email, notes = phone_e.get(), name_e.get(), email_e.get(), notes_e.get()
        if not (phone and name and email):
            pu.showerror("CRMLite", "Please fill in name, email and phone!"); return
        try:
            phone = int(phone)
        except ValueError:
            pu.showerror("CRMLite", "Phone must be a number!"); return
        if check_phone(phone):
            pu.showerror("CRMLite", "A customer with this number already exists!")
        else:
            pu.showinfo("CRMLite", new_customer(name, phone, email, notes or "None", username))
            win.destroy()

    action_btn(body, "Register", sbt, row=4, color=ACCENT2, fg_col="#0f1117")


def create_product():
    if not isadmin:
        pu.showerror("CRMLite", "Administrator privileges required."); return

    win, body = styled_window("New Product", h=360)
    body.columnconfigure(1, weight=1)
    tk.Label(body, text="Admin Function", font=(FONT, 9, "bold"), bg=BG, fg=DANGER
             ).grid(row=0, column=0, columnspan=2, sticky="w", padx=24, pady=(0, 8))

    title_e = grid_entry(body, "Product name", 1)
    price_e = grid_entry(body, "Price (€)",    2)

    def sbt():
        title, price = title_e.get(), price_e.get()
        try:
            price = float(price)
            if price < 0 or not title:
                raise ValueError
            pu.showinfo("CRMLite", new_product(title, price, username))
            win.destroy()
        except ValueError:
            pu.showerror("CRMLite", "Enter a valid title and price.")
            price_e.delete(0, tk.END); title_e.delete(0, tk.END)

    action_btn(body, "Register Product", sbt, row=3, color=ACCENT2, fg_col="#0f1117")


def change_order_status():
    win, body = styled_window("Change Order Status", h=380)
    body.columnconfigure(1, weight=1)

    ord_e = grid_entry(body, "Order ID", 2)

    result_lbl = tk.Label(body, text="", font=(FONT, 10), bg=BG, fg=ACCENT2, justify="left")
    result_lbl.grid(row=3, column=0, columnspan=2, sticky="w", padx=24, pady=4)

    status_cb = styled_combo(body, ['Fulfilled', 'Refunded', 'Pending', 'Unknown'], row=4)
    status_cb.grid_remove()

    confirm_btn = tk.Button(body, text="Update Status",
                            font=(FONT, 11, "bold"), bg=ACCENT, fg="#fff",
                            relief="flat", cursor="hand2", pady=8, bd=0)
    confirm_btn.grid(row=5, column=0, columnspan=2, sticky="ew", padx=24, pady=8)
    confirm_btn.grid_remove()

    ord_id_found = [None]

    def do_search():
        try:
            oid = int(ord_e.get())
        except ValueError:
            pu.showerror("CRMLite", "Order ID must be a number.")
            ord_e.delete(0, tk.END); return
        res, msg = check_orders(oid)
        if res:
            ord_id_found[0] = oid
            result_lbl.config(text=msg)
            status_cb.grid(); confirm_btn.grid()
        else:
            pu.showerror("CRMLite", "No order found with that ID.")

    def do_update():
        msg = modify_status(ord_id_found[0], status_cb.get(), username)
        pu.showinfo("CRMLite", msg); win.destroy()

    confirm_btn.config(command=do_update)

    tk.Button(body, text="Search", command=do_search,
              font=(FONT, 11, "bold"), bg=ACCENT, fg="#fff",
              relief="flat", cursor="hand2", pady=8, bd=0
              ).grid(row=2, column=2, padx=(4, 24), pady=(8, 0))


def create_user():
    if not isadmin:
        pu.showerror("CRMLite", "You don't have permission for this action."); return

    win, body = styled_window("Add User", h=460)
    body.columnconfigure(1, weight=1)

    user_e   = grid_entry(body, "Username",        2)
    passw1_e = grid_entry(body, "Password",        3, show="•")
    passw2_e = grid_entry(body, "Repeat password", 4, show="•")
    type_cb  = styled_combo(body, ["Regular User", "Administrator"], row=5)

    def sbt():
        p1, p2 = passw1_e.get(), passw2_e.get()
        if p1 != p2:
            pu.showerror("CRMLite", "Passwords don't match!")
            passw1_e.delete(0, tk.END); passw2_e.delete(0, tk.END); return
        utype = "admin" if type_cb.get() == "Administrator" else "user"
        ok, msg = new_user(username, user_e.get(), p1, utype)
        if ok:
            pu.showinfo("CRMLite", msg); win.destroy()
        else:
            pu.showerror("CRMLite", msg)
            user_e.delete(0, tk.END); passw1_e.delete(0, tk.END); passw2_e.delete(0, tk.END)

    action_btn(body, "Add User", sbt, row=6, color=ACCENT2, fg_col="#0f1117")


def change_user_type():
    if not isadmin:
        pu.showerror("CRMLite", "You don't have access rights."); return

    win, body = styled_window("Change User Type", h=360)
    body.columnconfigure(1, weight=1)

    uname_e = grid_entry(body, "Username", 2)

    found_lbl = tk.Label(body, text="", font=(FONT, 10), bg=BG, fg=ACCENT2)
    found_lbl.grid(row=3, column=0, columnspan=2, sticky="w", padx=24, pady=4)

    type_cb = styled_combo(body, ["Regular User", "Administrator"], row=4)
    type_cb.grid_remove()

    upd_btn = tk.Button(body, text="Update",
                        font=(FONT, 11, "bold"), bg=ACCENT, fg="#fff",
                        relief="flat", cursor="hand2", pady=8, bd=0)
    upd_btn.grid(row=5, column=0, columnspan=2, sticky="ew", padx=24, pady=8)
    upd_btn.grid_remove()

    user_found = [None]

    def do_search():
        um = uname_e.get()
        ok, utype = search_user(um)
        if ok:
            user_found[0] = um
            found_lbl.config(text=f"Found: {um}  ({utype})")
            type_cb.current(1 if utype == "admin" else 0)
            type_cb.grid(); upd_btn.grid()
        else:
            pu.showerror("CRMLite", "No user found with that username.")
            uname_e.delete(0, tk.END)

    def do_update():
        ntype = "admin" if type_cb.get() == "Administrator" else "user"
        pu.showinfo("CRMLite", modfiy_user_type(username, user_found[0], ntype))
        win.destroy()

    upd_btn.config(command=do_update)

    tk.Button(body, text="Search", command=do_search,
              font=(FONT, 11, "bold"), bg=ACCENT, fg="#fff",
              relief="flat", cursor="hand2", pady=8, bd=0
              ).grid(row=2, column=2, padx=(4, 24), pady=(8, 0))


def modify_cust_info():
    win, body = styled_window("Edit Customer", h=480)
    body.columnconfigure(1, weight=1)

    phone_e = grid_entry(body, "Phone number to search", 2)

    fields_frame = tk.Frame(body, bg=BG)
    fields_frame.grid(row=4, column=0, columnspan=3, sticky="ew")
    fields_frame.columnconfigure(1, weight=1)

    old_phone_holder = [None]

    def do_search():
        ph = phone_e.get()
        try:
            ph = int(ph)
        except ValueError:
            pu.showerror("CRMLite", "Please enter a valid number."); return
        if check_phone(ph):
            old_phone_holder[0] = ph
            for w in fields_frame.winfo_children():
                w.destroy()
            c_name, c_phone, c_email, c_notes = fetch_customer_info(ph)

            tk.Label(fields_frame, text="── Edit details ──",
                     font=(FONT, 9), bg=BG, fg=MUTED
                     ).grid(row=0, column=0, columnspan=2, sticky="w", padx=24, pady=(8, 0))

            entries = []
            for i, (lbl_text, val) in enumerate(
                    [("Name", c_name), ("Email", c_email), ("Phone", c_phone), ("Notes", c_notes)],
                    start=1):
                tk.Label(fields_frame, text=lbl_text, font=(FONT, 10), bg=BG, fg=MUTED
                         ).grid(row=i, column=0, sticky="w", padx=24, pady=(6, 0))
                e = tk.Entry(fields_frame, font=(FONT, 11), bg=ENTRY_BG, fg=TEXT,
                             insertbackground=TEXT, relief="flat",
                             highlightthickness=1, highlightbackground=BORDER,
                             highlightcolor=ACCENT, width=28)
                e.insert(0, val)
                e.grid(row=i, column=1, sticky="ew", padx=(4, 24), pady=(6, 0))
                entries.append(e)

            def do_edit():
                name_v, email_v, phone_v, notes_v = [e.get() for e in entries]
                try:
                    phone_v = int(phone_v)
                    if check_phone(phone_v) and int(phone_v) != int(old_phone_holder[0]):
                        raise ValueError
                    result, msg = edit_customer(old_phone_holder[0], name_v, phone_v, email_v, notes_v, username)
                    (pu.showinfo if result else pu.showerror)("CRMLite", msg)
                    if result:
                        win.destroy()
                except ValueError:
                    pu.showerror("CRMLite", "Invalid or already-taken phone number.")

            tk.Button(fields_frame, text="Save Changes", command=do_edit,
                      font=(FONT, 11, "bold"), bg=ACCENT2, fg="#0f1117",
                      relief="flat", cursor="hand2", pady=8, bd=0
                      ).grid(row=5, column=0, columnspan=2, sticky="ew", padx=24, pady=14)
        else:
            pu.showerror("CRMLite", "No customer found with that number.")

    tk.Button(body, text="Search", command=do_search,
              font=(FONT, 11, "bold"), bg=ACCENT, fg="#fff",
              relief="flat", cursor="hand2", pady=8, bd=0
              ).grid(row=2, column=2, padx=(4, 24), pady=(8, 0))


def delete_cust():
    if not isadmin:
        pu.showerror("CRMLite", "Administrator privileges required!"); return

    win, body = styled_window("Delete Customer", h=280)
    body.columnconfigure(1, weight=1)

    phone_e = grid_entry(body, "Phone number", 2)

    def sbt():
        try:
            ph = int(phone_e.get())
        except ValueError:
            pu.showerror("CRMLite", "Please enter a valid number."); return
        if check_phone(ph):
            if pu.askyesnocancel("CRMLite", "Customer found. Delete them?"):
                pu.showinfo("CRMLite", del_cust(username, ph))
                win.destroy()
        else:
            pu.showerror("CRMLite", "No customer found with that number.")
            win.destroy()

    action_btn(body, "Delete", sbt, row=3, color=DANGER)


log_in()
root.mainloop()