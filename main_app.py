import tkinter as tk
from tkinter import messagebox as pu
from tkinter import ttk
from funcs import *
import re

BG        = "#0a0c12"
PANEL     = "#12151f"
CARD      = "#181b28"
BORDER    = "#22273a"
ACCENT    = "#5b5ef4"
ACCENT_H  = "#7b7ef8"
ACCENT2   = "#00c9a0"
DANGER    = "#f45b7a"
WARN      = "#f4a45b"
TEXT      = "#dde1ef"
MUTED     = "#5a6070"
ENTRY_BG  = "#1e2130"
FONT      = "Segoe UI"
FONT_MONO = "Consolas"

root = tk.Tk()
root.title("CRMLite")
root.geometry("620x680")
root.configure(bg=BG)
root.resizable(False, False)

username = ""
isadmin  = False

def clear_root():
    for w in root.winfo_children():
        w.destroy()


def styled_window(title_text, w=540, h=540):
    win = tk.Toplevel(root)
    win.title(title_text)
    win.geometry(f"{w}x{h}")
    win.configure(bg=BG)
    win.resizable(False, False)
    win.grab_set()

    hdr = tk.Frame(win, bg=PANEL, height=52)
    hdr.pack(fill="x")
    hdr.pack_propagate(False)
    tk.Label(hdr, text=title_text, font=(FONT, 13, "bold"),
             bg=PANEL, fg=TEXT).pack(side="left", padx=20)
    tk.Frame(win, bg=BORDER, height=1).pack(fill="x")

    body = tk.Frame(win, bg=BG)
    body.pack(fill="both", expand=True)
    return win, body


def grid_label(parent, text, row, col=0, span=1, color=None):
    tk.Label(parent, text=text, font=(FONT, 9),
             bg=BG, fg=color or MUTED
             ).grid(row=row, column=col, columnspan=span,
                    sticky="w", padx=24, pady=(10, 0))


def grid_entry(parent, label_text, row, show=None, width=32):
    grid_label(parent, label_text, row)
    e = tk.Entry(parent, font=(FONT, 11), bg=ENTRY_BG, fg=TEXT,
                 insertbackground=TEXT, relief="flat",
                 highlightthickness=1, highlightbackground=BORDER,
                 highlightcolor=ACCENT, show=show or "", width=width)
    e.grid(row=row, column=1, sticky="ew", padx=(6, 24), pady=(10, 0))
    return e


def styled_combo(parent, values, row):
    s = ttk.Style()
    s.theme_use("clam")
    s.configure("D.TCombobox",
                fieldbackground=ENTRY_BG, background=ENTRY_BG,
                foreground=TEXT, bordercolor=BORDER,
                arrowcolor=ACCENT, selectbackground=ACCENT,
                selectforeground=TEXT, padding=4)
    cb = ttk.Combobox(parent, values=values, state="readonly",
                      style="D.TCombobox", font=(FONT, 11))
    cb.grid(row=row, column=0, columnspan=2, sticky="ew", padx=24, pady=(6, 0))
    cb.current(0)
    return cb


def action_btn(parent, text, command, row=None, color=ACCENT, fg_col="#ffffff",
               col=0, span=2, pady=14):
    b = tk.Button(parent, text=text, command=command,
                  font=(FONT, 10, "bold"), bg=color, fg=fg_col,
                  relief="flat", cursor="hand2", pady=9, bd=0,
                  activebackground=ACCENT_H, activeforeground="#fff")
    if row is not None:
        b.grid(row=row, column=col, columnspan=span,
               sticky="ew", padx=24, pady=pady)
    else:
        b.pack(fill="x", padx=24, pady=4)
    return b


def divider(parent, row=None):
    f = tk.Frame(parent, bg=BORDER, height=1)
    if row is not None:
        f.grid(row=row, column=0, columnspan=3, sticky="ew", padx=24, pady=6)
    else:
        f.pack(fill="x", padx=24, pady=8)
    return f


def info_badge(parent, text, color=ACCENT2):
    lbl = tk.Label(parent, text=text, font=(FONT, 9, "bold"),
                   bg=color, fg="#0a0c12", padx=8, pady=3)
    return lbl


def order_success_dialog(parent_win, msg, order_id):
    dialog = tk.Toplevel(root)
    dialog.title("Order Submitted")
    dialog.geometry("380x210")
    dialog.configure(bg=BG)
    dialog.resizable(False, False)
    dialog.grab_set()

    tk.Frame(dialog, bg=ACCENT2, height=4).pack(fill="x")

    tk.Label(dialog, text="✔  Order submitted",
             font=(FONT, 14, "bold"), bg=BG, fg=ACCENT2
             ).pack(pady=(20, 4))
    tk.Label(dialog, text=msg, font=(FONT_MONO, 10),
             bg=BG, fg=MUTED).pack()

    btn_frame = tk.Frame(dialog, bg=BG)
    btn_frame.pack(fill="x", padx=24, pady=20)
    btn_frame.columnconfigure(0, weight=1)
    btn_frame.columnconfigure(1, weight=1)

    def do_pdf():
        if order_id:
            ok, path = export_order_pdf(order_id)
            if ok:
                pu.showinfo("CRMLite", f"PDF saved!\n{path}")
            else:
                pu.showerror("CRMLite", str(path))
        dialog.destroy()
        parent_win.destroy()

    def do_skip():
        dialog.destroy()
        parent_win.destroy()

    tk.Button(btn_frame, text="📄  Export PDF", command=do_pdf,
              font=(FONT, 10, "bold"), bg=ACCENT, fg="#fff",
              relief="flat", cursor="hand2", pady=8, bd=0
              ).grid(row=0, column=0, sticky="ew", padx=(0, 5))

    tk.Button(btn_frame, text="Skip", command=do_skip,
              font=(FONT, 10), bg=CARD, fg=MUTED,
              relief="flat", cursor="hand2", pady=8, bd=0
              ).grid(row=0, column=1, sticky="ew", padx=(5, 0))


def log_in():
    global username, isadmin
    username = ""
    isadmin  = False
    clear_root()

    tk.Frame(root, bg=BG).place(relx=0, rely=0, relwidth=1, relheight=1)

    card = tk.Frame(root, bg=PANEL, bd=0, relief="flat")
    card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=400)

    tk.Frame(card, bg=ACCENT, height=4).pack(fill="x")

    tk.Label(card, text="CRMLite", font=(FONT, 26, "bold"),
             bg=PANEL, fg=TEXT).pack(pady=(28, 2))
    tk.Label(card, text="Sign in to continue", font=(FONT, 10),
             bg=PANEL, fg=MUTED).pack(pady=(0, 18))

    def field(label, show=None):
        tk.Label(card, text=label, font=(FONT, 9),
                 bg=PANEL, fg=MUTED).pack(anchor="w", padx=32)
        e = tk.Entry(card, font=(FONT, 11), bg=ENTRY_BG, fg=TEXT,
                     insertbackground=TEXT, relief="flat",
                     highlightthickness=1, highlightbackground=BORDER,
                     highlightcolor=ACCENT, show=show or "", width=28)
        e.pack(padx=32, pady=(3, 10), fill="x")
        return e

    user_e  = field("Username")
    passw_e = field("Password", show="•")

    err_lbl = tk.Label(card, text="", font=(FONT, 9),
                       bg=PANEL, fg=DANGER)
    err_lbl.pack()

    def auth(event=None):
        global username, isadmin
        username = user_e.get().strip()
        success, isadmin = check_user_pass(username, passw_e.get())
        if success:
            home()
        else:
            err_lbl.config(text="Incorrect username or password.")
            passw_e.delete(0, tk.END)

    passw_e.bind("<Return>", auth)

    tk.Button(card, text="Sign In", command=auth,
              font=(FONT, 11, "bold"), bg=ACCENT, fg="#fff",
              relief="flat", cursor="hand2", pady=9, bd=0,
              activebackground=ACCENT_H
              ).pack(fill="x", padx=32, pady=(8, 0))


def home():
    clear_root()

    topbar = tk.Frame(root, bg=PANEL, height=52)
    topbar.pack(fill="x")
    topbar.pack_propagate(False)

    tk.Label(topbar, text="CRMLite", font=(FONT, 14, "bold"),
             bg=PANEL, fg=ACCENT).pack(side="left", padx=20)
    tk.Label(topbar, text=f"@{username}", font=(FONT, 10),
             bg=PANEL, fg=MUTED).pack(side="left", padx=2)

    tk.Button(topbar, text="Logout", command=log_in,
              font=(FONT, 9), bg=BORDER, fg=MUTED,
              relief="flat", cursor="hand2", padx=10, pady=3, bd=0
              ).pack(side="right", padx=16, pady=14)

    tk.Frame(root, bg=BORDER, height=1).pack(fill="x")

    if isadmin:
        banner = tk.Frame(root, bg=ACCENT, height=32)
        banner.pack(fill="x")
        banner.pack_propagate(False)
        tk.Label(banner,
                 text=f"Administrator  ·  Customers: {total_cust()}  ·  Revenue: €{total_net()}",
                 font=(FONT, 9, "bold"), bg=ACCENT, fg="#fff"
                 ).pack(side="left", padx=16)
    else:
        banner = tk.Frame(root, bg="#1e1015", height=32)
        banner.pack(fill="x")
        banner.pack_propagate(False)
        tk.Label(banner, text="Regular user  ·  Limited functionality",
                 font=(FONT, 9), bg="#1e1015", fg=DANGER
                 ).pack(side="left", padx=16)

    tk.Label(root, text=f"Session started: {now()}",
             font=(FONT_MONO, 8), bg=BG, fg=MUTED
             ).pack(anchor="w", padx=20, pady=(10, 6))
    tk.Frame(root, bg=BORDER, height=1).pack(fill="x", padx=20)

    actions = [
        ("🛒", "New Order",           create_order,          ACCENT2, "#0a0c12"),
        ("👤", "Register Customer",   create_customer,       ACCENT,  "#ffffff"),
        ("📦", "Register Product",    create_product,        ACCENT,  "#ffffff"),
        ("🔄", "Change Order Status", change_order_status,   ACCENT,  "#ffffff"),
        ("📄", "Export Order PDF",    export_order_pdf_ui,   ACCENT,  "#ffffff"),
        ("➕", "Add App User",        create_user,           ACCENT,  "#ffffff"),
        ("⚙️", "Change User Type",    change_user_type,      ACCENT,  "#ffffff"),
        ("✏️", "Edit Customer",       modify_cust_info,      ACCENT,  "#ffffff"),
        ("🗑️", "Delete Customer",     delete_cust,           DANGER,  "#ffffff"),
    ]

    grid = tk.Frame(root, bg=BG)
    grid.pack(fill="both", expand=True, padx=20, pady=14)
    grid.columnconfigure(0, weight=1)
    grid.columnconfigure(1, weight=1)
    grid.columnconfigure(2, weight=1)

    for i, (icon, label, cmd, color, fg) in enumerate(actions):
        r, c = divmod(i, 3)
        cell = tk.Frame(grid, bg=CARD, cursor="hand2")
        cell.grid(row=r, column=c, sticky="nsew", padx=5, pady=5)
        cell.bind("<Button-1>", lambda e, f=cmd: f())

        tk.Label(cell, text=icon, font=(FONT, 20),
                 bg=CARD, fg=color
                 ).pack(pady=(16, 4))
        tk.Label(cell, text=label, font=(FONT, 9, "bold"),
                 bg=CARD, fg=TEXT, wraplength=120, justify="center"
                 ).pack(pady=(0, 16))

        def on_enter(e, f=cell, col=color):
            f.configure(bg=col)
            for ch in f.winfo_children():
                ch.configure(bg=col)

        def on_leave(e, f=cell):
            f.configure(bg=CARD)
            for ch in f.winfo_children():
                ch.configure(bg=CARD)

        cell.bind("<Enter>", on_enter)
        cell.bind("<Leave>", on_leave)
        for child in cell.winfo_children():
            child.bind("<Button-1>", lambda e, f=cmd: f())
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)

    for r in range(3):
        grid.rowconfigure(r, weight=1)


def create_order():
    win, body = styled_window("New Order", h=600)

    ph_lbl = tk.Label(body, text="Customer phone number",
                      font=(FONT, 9), bg=BG, fg=MUTED)
    ph_lbl.pack(anchor="w", padx=24, pady=(14, 0))

    ph_row = tk.Frame(body, bg=BG)
    ph_row.pack(fill="x", padx=24, pady=(3, 0))

    phone_e = tk.Entry(ph_row, font=(FONT, 11), bg=ENTRY_BG, fg=TEXT,
                       insertbackground=TEXT, relief="flat",
                       highlightthickness=1, highlightbackground=BORDER,
                       highlightcolor=ACCENT, width=24)
    phone_e.pack(side="left")

    tk.Button(ph_row, text="Search", command=lambda: sbt_find_cust(),
              font=(FONT, 10, "bold"), bg=ACCENT, fg="#fff",
              relief="flat", cursor="hand2", padx=12, pady=4, bd=0
              ).pack(side="left", padx=(8, 0))

    info_lbl = tk.Label(body, text="", font=(FONT, 10),
                        bg=BG, fg=ACCENT2, justify="left")
    info_lbl.pack(anchor="w", padx=24, pady=(6, 0))

    tk.Frame(body, bg=BORDER, height=1).pack(fill="x", padx=24, pady=10)

    sku_row = tk.Frame(body, bg=BG)
    tk.Label(sku_row, text="Product SKU", font=(FONT, 9),
             bg=BG, fg=MUTED).pack(side="left")
    sku_e = tk.Entry(sku_row, font=(FONT, 11), bg=ENTRY_BG, fg=TEXT,
                     insertbackground=TEXT, relief="flat",
                     highlightthickness=1, highlightbackground=BORDER,
                     highlightcolor=ACCENT, width=16)
    sku_e.pack(side="left", padx=(8, 6))

    product_frame = tk.Frame(body, bg=BG)
    total_var     = tk.DoubleVar(value=0.0)
    total_lbl     = tk.Label(body, text="Total: €0.00",
                              font=(FONT, 13, "bold"), bg=BG, fg=ACCENT)
    submit_holder = tk.Frame(body, bg=BG)

    row_counter      = [0]
    phone_int_holder = [None]

    def add_product():
        sku = sku_e.get().strip()
        if not sku:
            pu.showerror("CRMLite", "Please enter a SKU."); return
        try:
            sku_int = int(sku)
        except ValueError:
            pu.showerror("CRMLite", "SKU must be a number."); return
        if check_product(sku_int):
            title, price = fetch_product_info(sku_int)
            tk.Label(product_frame,
                     text=f"  • {title}  —  €{float(price):.2f}",
                     font=(FONT, 10), bg=BG, fg=TEXT
                     ).grid(row=row_counter[0], column=0, sticky="w", pady=1)
            total_var.set(total_var.get() + float(price))
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
        if phone_int_holder[0] is None:
            pu.showerror("CRMLite", "Search for a customer first."); return
        if total_var.get() == 0:
            pu.showerror("CRMLite", "Add at least one product."); return
        result, msg = new_order(phone_int_holder[0], total_var.get(), username)
        if result:
            match    = re.search(r'\d+', msg)
            order_id = int(match.group()) if match else None
            order_success_dialog(win, msg, order_id)
        else:
            pu.showerror("CRMLite", msg)

    tk.Button(submit_holder, text="✔  Submit Order", command=submit_order,
              font=(FONT, 11, "bold"), bg=ACCENT2, fg="#0a0c12",
              relief="flat", cursor="hand2", pady=9, bd=0
              ).pack(fill="x")

    def sbt_find_cust():
        ph = phone_e.get().strip()
        if not ph:
            pu.showerror("CRMLite", "Please enter a phone number."); return
        try:
            pi = int(ph)
        except ValueError:
            pu.showerror("CRMLite", "Invalid phone number."); return
        if check_phone(pi):
            phone_int_holder[0] = pi
            name, phone, email, notes = fetch_customer_info(pi)
            info_lbl.config(text=f"✔  {name}  ·  {phone}  ·  {email}")
            sku_row.pack(fill="x", padx=24, pady=(0, 4))
            product_frame.pack(fill="x", padx=24)
            total_lbl.pack(anchor="w", padx=24, pady=(6, 0))
            submit_holder.pack(fill="x", padx=24, pady=10)
        else:
            pu.showerror("CRMLite", f"No customer with number {ph}.\nAdd them first.")


def create_customer():
    win, body = styled_window("Register Customer", h=400)
    body.columnconfigure(1, weight=1)

    phone_e = grid_entry(body, "Phone",  0)
    name_e  = grid_entry(body, "Name",   1)
    email_e = grid_entry(body, "Email",  2)
    notes_e = grid_entry(body, "Notes",  3)
    if not isadmin:
        notes_e.config(state="disabled")

    def sbt():
        phone = phone_e.get().strip()
        name  = name_e.get().strip()
        email = email_e.get().strip()
        notes = notes_e.get().strip()
        if not (phone and name and email):
            pu.showerror("CRMLite", "Please fill in name, email and phone."); return
        try:
            phone = int(phone)
        except ValueError:
            pu.showerror("CRMLite", "Phone must be a number."); return
        if check_phone(phone):
            pu.showerror("CRMLite", "A customer with this number already exists.")
        else:
            pu.showinfo("CRMLite", new_customer(name, phone, email, notes or "None", username))
            win.destroy()

    action_btn(body, "Register Customer", sbt, row=4, color=ACCENT2, fg_col="#0a0c12")


def create_product():
    if not isadmin:
        pu.showerror("CRMLite", "Administrator privileges required."); return

    win, body = styled_window("New Product", h=320)
    body.columnconfigure(1, weight=1)

    grid_label(body, "Admin Function", 0, color=DANGER)
    title_e = grid_entry(body, "Product name", 1)
    price_e = grid_entry(body, "Price (€)",    2)

    def sbt():
        title = title_e.get().strip()
        price = price_e.get().strip()
        try:
            price = float(price)
            if price < 0 or not title:
                raise ValueError
            pu.showinfo("CRMLite", new_product(title, price, username))
            win.destroy()
        except ValueError:
            pu.showerror("CRMLite", "Enter a valid title and price.")
            price_e.delete(0, tk.END)

    action_btn(body, "Register Product", sbt, row=3, color=ACCENT2, fg_col="#0a0c12")


def change_order_status():
    win, body = styled_window("Change Order Status", h=400)
    body.columnconfigure(1, weight=1)

    ord_e = grid_entry(body, "Order ID", 0)

    result_lbl = tk.Label(body, text="", font=(FONT_MONO, 9),
                          bg=BG, fg=ACCENT2, justify="left", wraplength=460)
    result_lbl.grid(row=1, column=0, columnspan=2, sticky="w", padx=24, pady=6)

    status_cb  = styled_combo(body, ['Fulfilled', 'Refunded', 'Pending', 'Unknown'], row=2)
    status_cb.grid_remove()

    confirm_btn = action_btn(body, "Update Status", lambda: None, row=3)
    confirm_btn.grid_remove()

    ord_id_found = [None]

    def do_search():
        try:
            oid = int(ord_e.get())
        except ValueError:
            pu.showerror("CRMLite", "Order ID must be a number."); return
        res, msg = check_orders(oid)
        if res:
            ord_id_found[0] = oid
            result_lbl.config(text=msg)
            status_cb.grid()
            confirm_btn.grid()
        else:
            pu.showerror("CRMLite", "No order found with that ID.")

    def do_update():
        msg = modify_status(ord_id_found[0], status_cb.get(), username)
        pu.showinfo("CRMLite", msg); win.destroy()

    confirm_btn.config(command=do_update)

    tk.Button(body, text="Search", command=do_search,
              font=(FONT, 10, "bold"), bg=ACCENT, fg="#fff",
              relief="flat", cursor="hand2", padx=12, pady=4, bd=0
              ).grid(row=0, column=2, padx=(4, 24), pady=(10, 0))


def export_order_pdf_ui():
    win, body = styled_window("Export Order PDF", h=280)
    body.columnconfigure(1, weight=1)

    ord_e = grid_entry(body, "Order ID", 0)

    result_lbl = tk.Label(body, text="", font=(FONT, 9),
                          bg=BG, fg=ACCENT2, wraplength=460)
    result_lbl.grid(row=2, column=0, columnspan=2, sticky="w", padx=24, pady=4)

    def sbt():
        try:
            oid = int(ord_e.get())
        except ValueError:
            pu.showerror("CRMLite", "Order ID must be a number."); return
        ok, path = export_order_pdf(oid)
        if ok:
            result_lbl.config(text=f"✔  Saved to: {path}")
            pu.showinfo("CRMLite", f"PDF saved!\n{path}")
            win.destroy()
        else:
            pu.showerror("CRMLite", str(path))

    action_btn(body, "📄  Export PDF", sbt, row=1, color=ACCENT2, fg_col="#0a0c12")


def create_user():
    if not isadmin:
        pu.showerror("CRMLite", "You don't have permission for this action."); return

    win, body = styled_window("Add User", h=440)
    body.columnconfigure(1, weight=1)

    user_e   = grid_entry(body, "Username",        0)
    passw1_e = grid_entry(body, "Password",        1, show="•")
    passw2_e = grid_entry(body, "Repeat password", 2, show="•")
    type_cb  = styled_combo(body, ["Regular User", "Administrator"], row=3)

    def sbt():
        p1, p2 = passw1_e.get(), passw2_e.get()
        if not user_e.get().strip():
            pu.showerror("CRMLite", "Username cannot be empty."); return
        if p1 != p2:
            pu.showerror("CRMLite", "Passwords don't match.")
            passw1_e.delete(0, tk.END); passw2_e.delete(0, tk.END); return
        if len(p1) < 4:
            pu.showerror("CRMLite", "Password must be at least 4 characters."); return
        utype = "admin" if type_cb.get() == "Administrator" else "user"
        ok, msg = new_user(username, user_e.get().strip(), p1, utype)
        if ok:
            pu.showinfo("CRMLite", msg); win.destroy()
        else:
            pu.showerror("CRMLite", msg)
            user_e.delete(0, tk.END); passw1_e.delete(0, tk.END); passw2_e.delete(0, tk.END)

    action_btn(body, "Add User", sbt, row=4, color=ACCENT2, fg_col="#0a0c12")


def change_user_type():
    if not isadmin:
        pu.showerror("CRMLite", "You don't have access rights."); return

    win, body = styled_window("Change User Type", h=360)
    body.columnconfigure(1, weight=1)

    uname_e = grid_entry(body, "Username", 0)

    found_lbl = tk.Label(body, text="", font=(FONT, 10),
                         bg=BG, fg=ACCENT2)
    found_lbl.grid(row=1, column=0, columnspan=2, sticky="w", padx=24, pady=4)

    type_cb = styled_combo(body, ["Regular User", "Administrator"], row=2)
    type_cb.grid_remove()

    upd_btn = action_btn(body, "Update", lambda: None, row=3)
    upd_btn.grid_remove()

    user_found = [None]

    def do_search():
        um = uname_e.get().strip()
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
              font=(FONT, 10, "bold"), bg=ACCENT, fg="#fff",
              relief="flat", cursor="hand2", padx=12, pady=4, bd=0
              ).grid(row=0, column=2, padx=(4, 24), pady=(10, 0))


def modify_cust_info():
    win, body = styled_window("Edit Customer", h=500)
    body.columnconfigure(1, weight=1)

    phone_e = grid_entry(body, "Phone number to search", 0)

    fields_frame = tk.Frame(body, bg=BG)
    fields_frame.grid(row=2, column=0, columnspan=3, sticky="ew")
    fields_frame.columnconfigure(1, weight=1)

    old_phone_holder = [None]

    def do_search():
        ph = phone_e.get().strip()
        try:
            ph = int(ph)
        except ValueError:
            pu.showerror("CRMLite", "Please enter a valid number."); return
        if check_phone(ph):
            old_phone_holder[0] = ph
            for w in fields_frame.winfo_children():
                w.destroy()
            c_name, c_phone, c_email, c_notes = fetch_customer_info(ph)

            grid_label(fields_frame, "── Edit details ──", 0)

            entries = []
            for i, (lbl_text, val) in enumerate(
                    [("Name", c_name), ("Email", c_email),
                     ("Phone", c_phone), ("Notes", c_notes)], start=1):
                tk.Label(fields_frame, text=lbl_text, font=(FONT, 9),
                         bg=BG, fg=MUTED
                         ).grid(row=i, column=0, sticky="w", padx=24, pady=(8, 0))
                e = tk.Entry(fields_frame, font=(FONT, 11), bg=ENTRY_BG, fg=TEXT,
                             insertbackground=TEXT, relief="flat",
                             highlightthickness=1, highlightbackground=BORDER,
                             highlightcolor=ACCENT, width=28)
                e.insert(0, str(val) if val else "")
                e.grid(row=i, column=1, sticky="ew", padx=(6, 24), pady=(8, 0))
                entries.append(e)

            def do_edit():
                name_v, email_v, phone_v, notes_v = [e.get() for e in entries]
                try:
                    phone_v = int(phone_v)
                    if check_phone(phone_v) and int(phone_v) != int(old_phone_holder[0]):
                        raise ValueError
                    result, msg = edit_customer(old_phone_holder[0], name_v,
                                               phone_v, email_v, notes_v, username)
                    (pu.showinfo if result else pu.showerror)("CRMLite", msg)
                    if result:
                        win.destroy()
                except ValueError:
                    pu.showerror("CRMLite", "Invalid or already-taken phone number.")

            tk.Button(fields_frame, text="Save Changes", command=do_edit,
                      font=(FONT, 11, "bold"), bg=ACCENT2, fg="#0a0c12",
                      relief="flat", cursor="hand2", pady=8, bd=0
                      ).grid(row=5, column=0, columnspan=2,
                             sticky="ew", padx=24, pady=14)
        else:
            pu.showerror("CRMLite", "No customer found with that number.")

    tk.Button(body, text="Search", command=do_search,
              font=(FONT, 10, "bold"), bg=ACCENT, fg="#fff",
              relief="flat", cursor="hand2", padx=12, pady=4, bd=0
              ).grid(row=0, column=2, padx=(4, 24), pady=(10, 0))


def delete_cust():
    if not isadmin:
        pu.showerror("CRMLite", "Administrator privileges required."); return

    win, body = styled_window("Delete Customer", h=260)
    body.columnconfigure(1, weight=1)

    phone_e = grid_entry(body, "Phone number", 0)

    def sbt():
        try:
            ph = int(phone_e.get().strip())
        except ValueError:
            pu.showerror("CRMLite", "Please enter a valid number."); return
        if check_phone(ph):
            if pu.askyesnocancel("CRMLite", "Customer found. Permanently delete?"):
                pu.showinfo("CRMLite", del_cust(username, ph))
                win.destroy()
        else:
            pu.showerror("CRMLite", "No customer found with that number.")
            win.destroy()

    action_btn(body, "🗑️  Delete Customer", sbt, row=1, color=DANGER)


log_in()
root.mainloop()