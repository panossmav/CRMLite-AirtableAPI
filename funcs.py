from datetime import *
import pyairtable
import os
import dotenv
from pyairtable import Api
import hashlib
import pytz

global gr_time
gr_time = gr_time = datetime.now()



dotenv.load_dotenv()

api_key = os.getenv("airtable_api") 
base_id = os.getenv("db_id")

api=Api(api_key)
customers_table = api.table(base_id,"Customers")
products_table = api.table(base_id,"Products")
orders_table = api.table(base_id,"Orders")
users_table = api.table(base_id,"App users")
logs_table = api.table(base_id,"User Logs")
sessions_table = api.table(base_id,"Sessions")

def log_session(username):
    sessions_table.create(
        {"user":username,
        "DateTime":str(datetime.now())}
    )

def check_user_pass(u, p):
    p_e = hashlib.sha256(p.encode()).hexdigest()
    formula = f"{{Username}} = '{u}'"
    usern = users_table.all(formula=formula, fields=["Password"])
    acc_type = users_table.all(formula=formula)
    

    if usern:
        us_type = acc_type[0]["fields"].get("User Type")
        password = usern[0]["fields"].get("Password")
        if password == p_e:
            create_user_logs(u,'Logged in.')
            log_session(u)
            if us_type == 'admin':
                return True,True  # Auth success and user is an admin
            else:
                return True,False #Auth success and user is NOT an admin
        else:
            return False,False  # Wrong password
    else:
        return False,False  # No such user
    


def create_user_logs(u,act):
    logs_table.create(
        {"User":u,
        "Action":act,
        "Date / Time":now()}
        )

def now():
    return gr_time.isoformat(sep=' ', timespec='seconds')

def get_prod_price(sku):
    formula = f"{{SKU}} = {sku}"
    products=products_table.all(formula=formula)
    if products:
        price = products[0]["fields"].get("Price")
        return price
    else:
        return 0


def new_customer(n,p,e,notes,user):
    formula = f"{{Phone}} = {p}"
    check_p_ex=customers_table.all(formula=formula,fields=["Phone"])
    if check_p_ex:
        return 'Υπάρχει ήδη πελάτης με αυτό το τηλέφωνο!'
    else:
        new_cust=customers_table.create({
            "Name":n,
            "Notes":notes,
            "Phone":p,
            "Email":e
        })
        cust_id = new_cust["fields"].get("Customer ID")
        create_user_logs(user,f"Add customer {cust_id}")
        return f"Ο πελάτης {cust_id} καταχωρήθηκε!"
    
def edit_customer(o_p,n,n_p,n_e,n_n,u):
    formula = f"{{Phone}} = {o_p}"
    customer = customers_table.all(formula=formula)
    if customer:
        cust_id = customer[0]["id"]
        customers_table.update(cust_id,{
            "Name":n,
            "Phone":n_p,
            "Email":n_e,
            "Notes":n_n
        })
        create_user_logs(u,"Edit customer %d"%o_p)
        return True,'Η επεξέργασια πελάτη καταχωρήθηκε'
    else:
        return False,'Δεν υπάρχει πελάτης με αυτόν τον αριθμό. Δοκίμαστε ξάνα'


def c_check_name(p):
    formula = f"{{Phone}} = {p}"
    records = customers_table.all(formula=formula)
    if records:
        name = records[0]["fields"].get("Name")
        return name
    else:
        return 'ERROR'
    
def c_check_email(p):
    formula = f"{{Phone}} = {p}"
    records = customers_table.all(formula=formula)
    if records:
        email = records[0]["fields"].get("Email")
        return email
    else:
        return 'ERROR'
    

def c_check_notes(p):
    formula = f"{{Phone}} = {p}"
    records = customers_table.all(formula=formula)
    if records:
        notes = records[0]["fields"].get("Notes")
        return notes
    else:
        return 'ERROR'

def new_product(t,p,u):
    new_p=products_table.create({
        "Title":t,
        "Price":p
        })
    create_user_logs(u,"Create product.")
    sku = new_p["fields"].get("SKU")
    return f"Το προϊόν προστέθηκε επιτυχώς! SKU: {sku}"
    
def new_order(phone,price,u):
    formula = f"{{Phone}} = {phone}"
    fetch_name=customers_table.all(formula=formula)
    if fetch_name:
        name = fetch_name[0]["id"]
        order=orders_table.create({
            "Customer":[name],
            "Status":'Fullfilled',
            "Total Price":price,
            "Customer Phone":phone,
            "Date / Time":gr_time.isoformat()
        })
        ord_id = order["fields"].get("Order ID")
        create_user_logs(u,f"Create order {ord_id}")
        return True,f"Η παραγγελία {ord_id} καταχωρήθηκε!"
    else:
        return False, 'Σφάλμα! Δοκιμάστε ξανά'



def check_orders(id):
    formula=f"{{Order ID}} = {id}"
    res = orders_table.all(formula=formula)
    if res:
        cust_db = res[0]["fields"].get("Customer")
        cust_fetch_db=customers_table.get(cust_db[0])
        cust = cust_fetch_db["fields"].get("Name")
        stat = res[0]["fields"].get("Status")
        item = res[0]["fields"].get("Total Price")
        date = res[0]["fields"].get("Date / Time")
        return True,f'Αρ. Παραγγελίας: {id} \n Όνομα: {cust} \n Κατάσταση {stat} \n Ποσό {item}€ \n Ημερομηνία: {date}'
    else:
        return False,'Δεν βρέθηκε η παραγγελία'

def modify_status(id,n,u):
    formula=f"{{Order ID}} = {id}"
    res = orders_table.all(formula=formula)
    if res:  
        r_id = res[0]["id"]
        orders_table.update(r_id,{
            "Status":n
        })
        create_user_logs(u,f"Change order {id} status to {n}")
        return f"Η κατάσταση παραγγελίας {id} άλλαξε σε {n}"
    else:
        return 'Δεν βρέθηκε η παραγγελία'

def modify_product(n_t,n_p,sku,u):
    formula = f"{{SKU}} = {sku}"
    find_prod = products_table.all(formula=formula)
    if find_prod:
        p_id = find_prod[0]["id"]
        products_table.update(p_id,{
            "Title":n_t,
            "Price":n_p
        })
        create_user_logs(u,f"Edit product {sku}")
        return f'Το προϊόν {sku} επεξεργάστηκε.'
    else:
        return f'Δεν βρέθηκε προϊόν με αυτόν τον κωδικό.'

def check_product(sku):
    formula = f"{{SKU}} = {sku}"
    res = products_table.all(formula=formula)
    if res:
        return True
    else:
        return False
    
def old_prod_title(sku):
    formula=f"{{SKU}} ={sku}"
    titles = products_table.all(formula=formula)
    title=titles[0]["fields"].get("Title")
    return title

def old_prod_price(sku):
    formula=f"{{SKU}} ={sku}"
    prices = products_table.all(formula=formula)
    price=prices[0]["fields"].get("Price")
    return price


def new_user(o_u,n_u,pwd,u_t):
    formula = f"{{Username}} = '{n_u}'"
    us_check = users_table.all(formula=formula)
    if us_check:
        return False,'Υπάρχει ήδη χρήστης με αυτό το όνομα'
    else:
        users_table.create({
            "Username":n_u,
            "Password":hashlib.sha256(pwd.encode()).hexdigest(),
            "User Type":u_t
        })
        create_user_logs(o_u,f"Create {n_u} as {u_t}")
        return True,'Ο χρήσητης αποθηκεύτηκε και μπορεί να συνδεθεί'
    
def del_user(c_u,d_u):
    formula = f"{{Username}} = '{d_u}'"
    res = users_table.all(formula=formula)
    if res:
        user = res[0]["id"]
        users_table.delete(user)
        create_user_logs(c_u,f"Delete user: {d_u}")
        return 'Ο χρήστης διαγράφηκε!'
    else:
        return 'Δεν βρέθηκε χρήστης με αυτό το όνομα!'

def del_cust(u,p):
    formula =f"{{Phone}} = {p}"
    res = customers_table.all(formula=formula)
    if res:
        cust_airt_id = res[0]["id"]
        customers_table.delete(cust_airt_id)
        create_user_logs(u,f"Delete customer {p}")
        return 'Ο πελάτης διαγράφηκε'
    else:
        return 'Ο πελάτης δεν βρέθηκε'
    
def update_inv(u,sku,n_inv):
    formula = f"{{SKU}} = {sku}"
    check_prod = products_table.all(formula=formula)
    if check_prod:
        curr_inv = int(check_prod[0]["fields"].get("Inventory"))
        t_inv = curr_inv + n_inv
        rec_id = check_prod[0]["id"]
        products_table.update(rec_id,{"Inventory":t_inv})
        create_user_logs(u,f"Set {sku} inventory to {t_inv}")
        return f"Νέο απόθεμα: %d"%t_inv
    else:
        return 'Δεν βρέθηκε προϊόν με αυτόν τον κωδικό'


def net_pr_cust(p,u):
    formula = f"{{Customer Phone}} = {p}"
    find_c = orders_table.all(formula=formula,fields=["Product SKU"])
    if find_c:
        t_p = 0.0
        for record in find_c:
            item = int(record["fields"].get("Product SKU"))
            formula_i = f"{{SKU}} = {item}"
            find = products_table.all(formula=formula_i,fields=["Price"])
            price = float(find[0]["fields"].get("Price"))
            price = round(price,2)
            t_p+=price
            create_user_logs(u,f"Net profit view of customer: {p}")
        return f"Τζίρος πελάτη: {t_p} €."
    else:
        return 'Δεν βρέθηκε πελάτης'

def total_cust():
    all_cust=customers_table.all()
    count = len(all_cust)
    return count

def total_net():
    all_orders = orders_table.all()
    total_net = 0.0
    for order in all_orders:
        price = order["fields"].get("Total Price")
        if price == None:
            price = 0.0
        try:
            price = float(price)
        except ValueError:
            price = 0.0
        total_net+=price
    return round(total_net,2)

def check_phone(phone):
    formula = f"{{Phone}} = {phone}"
    customer = customers_table.all(formula=formula)
    if customer:
        return True
    else:
        return False

def fetch_customer_info(phone):
    formula = f"{{Phone}} = {phone}"
    customers = customers_table.all(formula=formula)
    name = customers[0]["fields"].get("Name")
    email = customers[0]["fields"].get("Email")
    phone = phone
    notes = customers[0]["fields"].get("Notes")
    return name,phone,email,notes

def fetch_product_info(sku):
    formula = f'{{SKU}} = {sku}'
    fetch_product=products_table.all(formula=formula)
    title = fetch_product[0]["fields"].get("Title")
    price = fetch_product[0]["fields"].get("Price")
    return title,price


def search_user(u):
    formula=f"{{Username}} = '{u}'"
    fetch_users = users_table.all(formula=formula)
    if fetch_users:
        type = fetch_users[0]["fields"].get("User Type")
        return True,type
    else:
        return False,'null'

def modfiy_user_type(c_u,m_u,status):
    formula = f"{{Username}} = '{m_u}'"
    fetch_users = users_table.all(formula=formula)
    if fetch_users:
        user_id = fetch_users[0]["id"]
        customers_table.update(user_id,{
            "User Type":status
        })
        create_user_logs(c_u,f"Update {m_u} to {status}")
        return f"Ο χρήστης {m_u} 'αλλαξε σε {status}"
    else:
        return 'Error'    


