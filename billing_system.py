import abc
import os.path
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class credit_card():
    # def __init__(self):
    #     self.__visa_account="none"
    #     self.__varify_code="none"
    #     self.__deposit = random.randrange(0,50000) + 200000
    def __init__(self,acc,cod,dep):
        self.__visa_account=acc
        self.__varify_code=cod
        self.__deposit=dep
    def set_account(self,acc):
        self.__visa_account=acc
    def set_code(self,code):
        self.__varify_code=code
    def set_deposit(self,money):
        self.__deposit=money
    def get_account(self):
        return self.__visa_account
    def get_deposit(self):
        return self.__deposit
    def get_code(self):
        return self.__varify_code
    
class customer():      #abstract class
    def __init__(self):
        self.__id = 0
        self.__name = "none"
        self.__password = "none"
        self.__customer_type="none"
        self.__address="none"
        self.__usage=0
        self.__history_bill=[]
        self.__fullfillment=100
        self.__budget=0
        self.__visa=credit_card("","",0)
    def set_id(self, id):
        self.__id = id
    def set_name(self, name):
        self.__name = name
    def set_password(self, pwd):
        self.__password = pwd
    def set_customer_type(self,type):
        self.__customer_type=type
    def set_visa(self,acc, cod, dep):
        self.__visa.set_account(acc)
        self.__visa.set_code(cod)
        self.__visa.set_deposit(dep)
    def set_address(self,addr):
        self.__address=addr
    def set_usage(self,use):
        self.__usage=use
    def set_history_bill(self,bill):
        self.__history_bill=bill
    def set_fullfillment(self,full):
        self.__fullfillment=full
    def set_budget(self,bud):
        self.__budget=bud

    def get_id(self):
        return self.__id
    def get_name(self):
        return self.__name
    def get_password(self):
        return self.__password
    def get_visa(self):
        return self.__visa
    def get_address(self):
        return self.__address
    def get_usage(self):
        return self.__usage
    def get_history_bill(self):
        return self.__history_bill
    def get_fullfillment(self):
        return self.__fullfillment
    def get_budget(self):
        return self.__budget
    def get_customer_type(self):
        return self.__customer_type
    

    def request_bill(self, power_inc):
        power_inc.serve(self.__id)
        return power_inc.send_bill(self.__id)
    
    def pay_bill(self, power_inc):
        power_inc.receive_bill(self.__id)
        bill = power_inc.calculate_bill(self.__id)
        self.__history_bill += [bill]
        self.__visa.set_deposit(int(self.__visa.get_deposit()) - int(bill))
        self.__usage = 0
    def complain(self, power_inc, new_ceo):
        power_inc.set_ceo(new_ceo)
        pass


class personal(customer):
    def __init__(self):
        super().__init__()
        self.set_customer_type("personal")
class industry(customer):
    def __init__(self):
        super().__init__()
        self.set_customer_type("industry")
class education(customer):    
    def __init__(self):
        super().__init__()
        self.set_customer_type("education")

class bill_format():
    def __init__(self, name, addr, use, bill, ceo):
        self.__name = name
        self.__address = addr
        self.__usage = use
        self.__bill = bill
        self.__ceo = ceo
    def print_bill(self, date):
        print("BILL:")
        print("\tname:", self.__name)
        print("\taddress:", self.__address)
        print("\tusage:", self.__usage)
        print("\tbill:", self.__bill)
        print("\tdue date:", date)
        print("\t\tSincerely, ceo:", self.__ceo)
    def get_name(self):
            return self.__name
    def get_address(self):
            return self.__address
    def get_usage(self):
            return self.__usage
    def get_bill(self):
            return self.__bill
    def get_ceo(self):
            return self.__ceo

    
class company():
    def __init__(self):
        elements=[]
        self.__ceo = "Jonas"
        self.__password = "password"
        self.__user_cnt = 0
        self.__user_lst = []
        self.__advice_lst = []
        self.__bill_rate = {"personal" : [10, 20, 30], "industry" : [5, 10, 15], "education": [2, 4, 6]}
        self.__remain_usage = 10000000
        if(os.path.isfile("user_info.txt")):
            with open("user_info.txt", "r") as f:
                elements=f.readlines()
            company_info, user_info = elements[:5], elements[5:]
            company_info = [i[:-1] for i in company_info]
            self.__ceo = company_info[0]
            self.__password = company_info[1]
            rate = [int(i) for i in company_info[2][:-1].split(' ')]
            d = {}
            d["personal"] = rate[:3]
            d["industry"] = rate[3:6]
            d["education"] = rate[6:]
            self.__bill_rate = d
            self.__remain_usage = int(company_info[3])
            string = ""
            for i in company_info[4]:
                if i != '\0': string += i
                else:
                    self.__advice_lst += [string]
                    string = ""

            info = ["name", "password", "address", "type", "account", "code", "deposit", "usage", "history", "budget"]
            info_len = len(info)
            for i in range(len(user_info)//info_len):
                indiv_info = user_info[i*info_len:(i+1)*info_len]
                indiv_info = [i[:-1] for i in indiv_info]
                #print(indiv_info)
                if indiv_info[info.index("type")] == 'personal': user = personal()
                elif indiv_info[info.index("type")] == 'industry': user = industry()
                elif indiv_info[info.index("type")] == 'education': user = education()
                user.set_name(indiv_info[info.index("name")])
                user.set_password(indiv_info[info.index("password")])
                user.set_address(indiv_info[info.index("address")])
                user.set_visa(indiv_info[info.index("account")], indiv_info[info.index("code")], int(indiv_info[info.index("deposit")]))
                user.set_usage(int(indiv_info[info.index("usage")]))
                if indiv_info[info.index("history")] != "":
                    history = [int(i) for i in indiv_info[info.index("history")][:-1].split(' ')]
                else: history = []
                user.set_history_bill(history)
                user.set_budget(int(indiv_info[info.index("budget")]))
                user.set_id(self.__user_cnt)
                self.__user_lst.append(user)
                self.__user_cnt += 1


    def set_ceo(self, new_ceo):
        self.__ceo = new_ceo
    def get_ceo(self):
        return self.__ceo
    
    def set_password(self, pwd):
        self.__password = pwd

    def get_password(self):
        return self.__password
    
    def get_user_cnt(self):
        return self.__user_cnt
    def get_users(self):
        return self.__user_lst
    
    def push_advice(self, str):
        self.__advice_lst += [str]
    def get_advice(self):
        return self.__advice_lst
    
    def set_bill_rate(self, type, idx, rate):
        if (type == 'personal' or type == 'industry' or type == 'education') and idx >= 0 and idx <= 2:
            self.__bill_rate[type][idx] = rate
    def get_bill_rate(self):
        return self.__bill_rate

    def inc_remain_usage(self, value):
        self.__remain_usage += value

    def get_remain_usage(self):
        return self.__remain_usage
    
    def add_user(self, name, pwd, addr, typ, acc, cod, dep, bud):
        if typ == 'personal': user = personal()
        elif typ == 'industry': user = industry()
        elif typ == 'education': user = education()
        else: return
        user.set_name(name)
        user.set_password(pwd)
        user.set_address(addr)
        user.set_visa(acc, cod, dep)
        user.set_budget(bud)
        user.set_id(self.__user_cnt)
        self.__user_lst.append(user)
        self.__user_cnt += 1
    def calculate_bill(self, id):
        user = self.__user_lst[id]
        type = user.get_customer_type()
        usage = user.get_usage()
        sum = 0
        if usage > 1000:
            sum += ((usage - 1000) * self.__bill_rate[type][2])
            usage = 1000
        if usage > 500:
            sum += ((usage - 500) * self.__bill_rate[type][1])
            usage = 500
        sum += usage * self.__bill_rate[type][0]
        return sum
    
    def serve(self, id):
        rand = random.randrange(0, 100) + 400
        if rand <= self.__remain_usage:
            usage = self.__user_lst[id].get_usage() + rand
        else:
            usage = self.__remain_usage
            print("capacity exhaust, serve", usage)
        self.__user_lst[id].set_usage(usage)
    def send_bill(self, id):
        user = self.__user_lst[id]
        return bill_format(user.get_name(), user.get_address(), user.get_usage(), self.calculate_bill(id), self.__ceo)
    def receive_bill(self, id):
        self.__remain_usage -= self.__user_lst[id].get_usage()
    

class simulator():
    def __init__(self):
        self.__date = str(random.randrange(1, 13)) + '/1'
        self.__inc = company()
    
    def run(self):
        while True:
            print('menu:')
            print("1. add user")
            print("2. user login")
            print("3. company monitor")
            print("4. exit")
            cmd = input("please enter command: ")
            if cmd == '1':
                self.add_user()
            elif cmd == '2':
                self.login()
            elif cmd == '3':
                self.monitor()
            elif cmd == '4':
                break
            print('\x1b[2J\x1b[H')

    def add_user(self):
        print('\x1b[2J\x1b[H')
        print('user sign up:')
        name = input("username: ")
        pwd = input("password: ")
        addr = input("address: ")
        typ = input('customer type: ')
        acc = input('account: ')
        cod = input('verification code: ')
        dep = int(input('deposit: '))
        bud = int(input('budget: '))
        self.__inc.add_user(name, pwd, addr, typ, acc, cod, dep, bud)

    def login(self):
        print('\x1b[2J\x1b[H')
        print('user login:')
        username = input('username: ')
        password = input('password: ')
        user_lst = self.__inc.get_users()
        for i in range(0, self.__inc.get_user_cnt()):
            if user_lst[i].get_name() == username and user_lst[i].get_password() == password:
                user = user_lst[i]
                print('1. check payment')
                print('2. check user info')
                print('3. update user info')
                print('4. check bill history')
                print('5. complain')
                print('6. deposit')
                print('7. back to menu')
                cmd = input('please enter command: ')
                if cmd == '7': return
                if cmd == '6':
                    val = int(input('please enter deposit sum: '))
                    user.set_visa(user.get_visa().get_account(), user.get_visa().get_code(), user.get_visa().get_deposit() + val)
                    print('deposit update successfully')
                    dummy = input('press enter to continue')
                if cmd == '5':
                    new_ceo = input('please enter new ceo: ')
                    self.__inc.set_ceo(new_ceo)
                    return
                if cmd == '4':
                    print("bill history:", user.get_history_bill())
                    dummy = input('press enter to continue')
                if cmd == '3':
                    print('\x1b[2J\x1b[H')
                    print('update user info')
                    print('1. username')
                    print('2. password')
                    print('3. address')
                    print('4. usertype')
                    print('5. visa')
                    print('0. back to menu')
                    field = input('please enter modified code: ')
                    if field == '1':
                        new_name = input('new name: ')
                        user_lst[i].set_name(new_name)
                    elif field == '2':
                        new_pwd = input('new password: ')
                        user_lst[i].set_password(new_pwd)
                    elif field == '3':
                        new_addr = input('new address: ')
                        user_lst[i].set_address(new_addr)
                    elif field == '4':
                        new_type = input('new usertype: ')
                        user_lst[i].set_customer_type(new_type)
                    elif field == '5':
                        new_acc = input('new account: ')
                        new_cod = input('new verfication code: ')
                        new_dep = int(input('new deposit: '))
                        user_lst[i].set_visa(new_acc, new_cod, new_dep)
                    else:
                        return
                if cmd == '2':
                    print('\x1b[2J\x1b[H')
                    print('check user info:')
                    print('username:', user.get_name())
                    print('password:', user.get_password())
                    print('usertype:', user.get_customer_type())
                    print('address:', user.get_address())
                    print('usage:', user.get_usage())
                    print('visa:')
                    visa = user.get_visa()
                    print('\taccount:', visa.get_account())
                    print('\tdeposit:', visa.get_deposit())
                    dummy = input('press enter to continue')
                if cmd == '1':
                    print('\x1b[2J\x1b[H')
                    print('check payment:')
                    user.request_bill(self.__inc).print_bill(self.__date)
                    print('1. pay bill')
                    print('2. back to menu')
                    com = input('please enter command:')
                    if (com == '2'):
                        return
                    elif (com == '1'):
                        user.pay_bill(self.__inc)
                        print('bill receieved!!')
                        dummy = input('press enter to continue')
                        return
    def monitor(self):
        if self.__inc.get_password() != input('password: '): return
        print('\x1b[2J\x1b[H')
        print('Welcome Monitor,', self.__inc.get_ceo(), "!")
        print('1. check user list')
        print('2. check remain power')
        print('3. check bill rate')
        print('4. change password')
        print('5. change bill rate')
        print('6. generate power')
        print('7. back to menu')
        cmd = input('please enter command: ')
        if cmd == '7': return
        elif cmd == '6':
            val = int(input('please enter demanded power: '))
            self.__inc.inc_remain_usage(val)
        elif cmd == '5':
            typ = input('type: ')
            idx = int(input('idx: '))
            val = int(input('new value: '))
            self.__inc.set_bill_rate(typ, idx, val)
        elif cmd == '4':
            new_pwd = input('new password: ')
            self.__inc.set_password(new_pwd)
        elif cmd == '3':
            print("bill rate:", self.__inc.get_bill_rate())
            dummy = input('press enter to continue')
        elif cmd == '2':
            print("power: ", self.__inc.get_remain_usage())
            dummy = input('press enter to continue')
        elif cmd == '1':
            print("id", "name", "type:", "\tusage", "address", "account", sep = '\t\t')
            user_lst = self.__inc.get_users()
            for i in range(0, self.__inc.get_user_cnt()):
                user = user_lst[i]
                print(i, user.get_name(), user.get_customer_type(), user.get_usage(), user.get_address(), user.get_visa().get_account(), sep = '\t\t')
            dummy = input('press enter to continue')

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.__inc = company()
        self.__bill = bill_format("name","addr",0,0,"name")
        self.__date = str(random.randrange(1, 13)) + '/1'
        self.title("Electricity Billing System")
        self.geometry("300x200") 
       
        self.add_user_button = tk.Button(self, text="1. Add User", command=self.add_user)
        self.add_user_button.pack(pady=10)

        self.user_login_button = tk.Button(self, text="2. User Login", command=self.user_login)
        self.user_login_button.pack(pady=10)

        self.company_monitor_button = tk.Button(self, text="3. Company Monitor", command=self.company_login)
        self.company_monitor_button.pack(pady=10)

        self.exit_button = tk.Button(self, text="4. Save & Exit", command=self.save_and_quit)
        self.exit_button.pack(pady=10)
    def add_user(self):
        self.add_user_window = tk.Toplevel(self)
        self.add_user_window.title("Add User")
        self.add_user_window.geometry("400x300")

        fields = ["Username", "Password", "Address", "Customer Type", "Account", "Verification Code", "Deposit", "Budget"]
        self.entries = {}
        for i, field in enumerate(fields):
            label = tk.Label(self.add_user_window, text=field)
            label.grid(row=i, column=0, padx=10, pady=5)
            if field != "Customer Type":
                entry = tk.Entry(self.add_user_window)
                entry.grid(row=i, column=1, columnspan=3, padx=10, pady=5)
                self.entries[field] = entry
            else:
                self.entries["Customer Type"] = "personal"
                def set_type(e): e["Customer Type"] = ["personal","industry","education"][var.get()]
                var = tk.IntVar()
                b1 = tk.Radiobutton(self.add_user_window, text="personal", variable=var, value=0, command=lambda: set_type(self.entries))
                b1.select()
                b1.grid(row=i, column=1)
                b2 = tk.Radiobutton(self.add_user_window, text="industry", variable=var, value=1, command=lambda: set_type(self.entries))
                b2.grid(row=i, column=2)
                b3 = tk.Radiobutton(self.add_user_window, text="education", variable=var, value=2, command=lambda: set_type(self.entries))
                b3.grid(row=i, column=3)

        submit_button = tk.Button(self.add_user_window, text="Submit", command=self.submit_user)
        submit_button.grid(row=len(fields), column=0, columnspan=4, pady=10)

    def submit_user(self):
        name = self.entries["Username"].get()
        pwd = self.entries["Password"].get()
        addr = self.entries["Address"].get()
        typ = self.entries["Customer Type"]
        acc = self.entries["Account"].get()
        cod = self.entries["Verification Code"].get()

        try:
            dep = int(self.entries["Deposit"].get())
            bud = int(self.entries["Budget"].get())
        except ValueError:
            messagebox.showerror("Error", "Deposit and Budget must be numbers")
            return
        self.__inc.add_user(name, pwd, addr, typ, acc, cod, dep, bud)

        self.add_user_window.destroy()

    def user_login(self):
        self.login_window = tk.Toplevel(self)
        self.login_window.title("User Login")
        self.login_window.geometry("300x200")

        self.username_label = tk.Label(self.login_window, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.login_window)
        self.username_entry.pack()

        self.password_label = tk.Label(self.login_window, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.login_window, show="*")
        self.password_entry.pack()

        self.submit_button = tk.Button(self.login_window, text="Submit", command=self.varify_login)
        self.submit_button.pack()


    def varify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_lst = self.__inc.get_users()
        user = None

        for i in range(self.__inc.get_user_cnt()):
            if user_lst[i].get_name() == username and user_lst[i].get_password() == password:
                user = user_lst[i]
                break

        if user:
            self.user_menu(user)
            self.login_window.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
        
       
    def user_menu(self, user):
        self.user_menu_window = tk.Toplevel(self)
        self.user_menu_window.title("User Menu")
        self.user_menu_window.geometry("300x380")

        check_payment_button = tk.Button(self.user_menu_window, text="1. Check Payment", command=lambda: self.check_payment(user))
        check_payment_button.pack(pady=10)

        check_user_info_button = tk.Button(self.user_menu_window, text="2. Check User Info", command=lambda: self.check_user_info(user))
        check_user_info_button.pack(pady=10)

        update_user_info_button = tk.Button(self.user_menu_window, text="3. Update User Info", command=lambda: self.update_user_info(user))
        update_user_info_button.pack(pady=10)

        check_bill_history_button = tk.Button(self.user_menu_window, text="4. Check Bill History", command=lambda: self.check_bill_history(user))
        check_bill_history_button.pack(pady=10)

        complain_button = tk.Button(self.user_menu_window, text="5. Complain", command=lambda: self.complain(user))
        complain_button.pack(pady=10)

        deposit_button = tk.Button(self.user_menu_window, text="6. Deposit", command=lambda: self.deposit(user))
        deposit_button.pack(pady=10)

        back_button = tk.Button(self.user_menu_window, text="7. Back to Menu", command=self.user_menu_window.destroy)
        back_button.pack(pady=10)

    def check_payment(self, user):
        self.check_payment_window = tk.Toplevel(self)
        self.check_payment_window.title("Check Payment")
        self.check_payment_window.geometry("400x250")

        self.__bill = user.request_bill(self.__inc)
        bill_details = f"Name: {self.__bill.get_name()}\nAddress: {self.__bill.get_address()}\nUsage: {self.__bill.get_usage()}\nBill: {self.__bill.get_bill()}\nDue date: {self.__date}\n\tSincerely, ceo:: {self.__bill.get_ceo()}"

        bill_label = tk.Label(self.check_payment_window, text=bill_details, justify=tk.LEFT)
        bill_label.pack(pady=10)

        pay_bill_button = tk.Button(self.check_payment_window, text="1. Pay Bill", command=lambda: self.pay_bill(user))
        pay_bill_button.pack(pady=10)

        back_button = tk.Button(self.check_payment_window, text="2. Back to Menu", command=self.check_payment_window.destroy)
        back_button.pack(pady=10)

    def pay_bill(self, user):
        user.pay_bill(self.__inc)
        messagebox.showinfo("Payment", "Bill paid successfully!")
        self.check_payment_window.destroy()
        


    def check_user_info(self, user):
        user_info_window = tk.Toplevel(self.user_menu_window)
        user_info_window.title("User Information")
        user_info_window.geometry("400x400")

        visa = user.get_visa()
        tk.Label(user_info_window, text="User Information", font=('Arial', 16, 'bold')).pack(pady=10)
        tk.Label(user_info_window, text=f"Name: {user.get_name()}", font=('Arial', 12)).pack(pady=5)
        tk.Label(user_info_window, text=f"Password: {str(user.get_password())}", font=('Arial', 12)).pack(pady=5)
        tk.Label(user_info_window, text=f"Address: {user.get_address()}", font=('Arial', 12)).pack(pady=5)
        tk.Label(user_info_window, text=f"Customer type: {user.get_customer_type()}", font=('Arial', 12)).pack(pady=5)
        tk.Label(user_info_window, text=f"Usage: {str(user.get_usage())}", font=('Arial', 12)).pack(pady=5)
        tk.Label(user_info_window, text=f"Account: {visa.get_account()}", font=('Arial', 12)).pack(pady=5)
        tk.Label(user_info_window, text=f"Varify code: {visa.get_code()}", font=('Arial', 12)).pack(pady=5)
        tk.Label(user_info_window, text=f"Deposit: {visa.get_deposit()}", font=('Arial', 12)).pack(pady=5)

        close_button = tk.Button(user_info_window, text="Close", command=user_info_window.destroy)
        close_button.pack(pady=20)

    def update_user_info(self, user):
        update_info_window = tk.Toplevel(self.user_menu_window)
        update_info_window.title("Update User Information")
        update_info_window.geometry("800x400")
        visa = user.get_visa()
        info_fields = ["Name", "Password", "Address", "Customer type" , "Account" , "Varify code" , "Deposit"]  # Add more fields as needed

        scrollbar = tk.Scrollbar(update_info_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(update_info_window, yscrollcommand=scrollbar.set)
        for field in info_fields:
            listbox.insert(tk.END, field)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar.config(command=listbox.yview)

        tk.Label(update_info_window, text="Enter new value\n(for customer type, you can enter 1 for personal, 2 for industry and 3 for education)", font=('Arial', 12)).pack(pady=(10, 0))
        new_value_entry = tk.Entry(update_info_window, font=('Arial', 12))
        new_value_entry.pack(pady=10)

        def submit_changes():
            selected_field = listbox.get(listbox.curselection())
            new_value = new_value_entry.get()
            
            if selected_field == "Name":
                user.set_name(new_value)
            elif selected_field == "Password":
                user.set_password(new_value)
            elif selected_field == "Address":
                user.set_address(new_value)
            elif selected_field == "Customer type":
                if new_value == "1" or new_value.lower() == "personal":
                    user.set_customer_type("personal")
                elif new_value == "2" or new_value.lower() == "industry":
                    user.set_customer_type("industry")
                elif new_value == "3" or new_value.lower() == "education":
                    user.set_customer_type("education")
            elif selected_field == "Account":
                visa.set_account(new_value)
            elif selected_field == "Varify code":
                visa.set_code(new_value)
            elif selected_field == "Deposit":
                visa.set_deposit(new_value)

            messagebox.showinfo("Info", "User information updated successfully!")
            update_info_window.destroy()
            self.user_menu_window.destroy()

        submit_button = tk.Button(update_info_window, text="Submit", command=submit_changes)
        submit_button.pack(pady=20)

    def check_bill_history(self, user):
        bill_history_window = tk.Toplevel(self.user_menu_window)
        bill_history_window.title("Bill History")
        bill_history_window.geometry("400x300")

        bill_history = user.get_history_bill()

        tk.Label(bill_history_window, text="Bill History", font=('Arial', 16, 'bold')).pack(pady=10)

        for bill in bill_history:
            tk.Label(bill_history_window, text=str(bill), font=('Arial', 12)).pack()

    def complain(self, user):
        complain_window = tk.Toplevel(self.user_menu_window)
        complain_window.title("Submit a Complaint")
        complain_window.geometry("400x300")

        tk.Label(complain_window, text="Enter your complaint", font=('Arial', 12)).pack(pady=(10, 0))

        complaint_entry = tk.Text(complain_window, height=10, width=40)
        complaint_entry.pack(pady=10)

        def submit_complaint():
            complaint_text = complaint_entry.get("1.0", "end-1c")
            self.__inc.push_advice(str(complaint_text))
            messagebox.showinfo("Info", "Complaint submitted successfully!")
            complain_window.destroy()

        submit_button = tk.Button(complain_window, text="Submit Complaint", command=submit_complaint)
        submit_button.pack(pady=20)
        

    def deposit(self, user):
        deposit_window = tk.Toplevel(self.user_menu_window)
        deposit_window.title("Make a Deposit")
        deposit_window.geometry("400x200")

        tk.Label(deposit_window, text="Enter deposit amount", font=('Arial', 12)).pack(pady=(10, 0))

        deposit_entry = tk.Entry(deposit_window, font=('Arial', 12))
        deposit_entry.pack(pady=10)
        visa = user.get_visa()
        def submit_deposit():
            deposit_amount = deposit_entry.get()
            visa.set_deposit(visa.get_deposit() + int(deposit_amount))  
            messagebox.showinfo("Info", "Deposit made successfully!")
            deposit_window.destroy()

        deposit_button = tk.Button(deposit_window, text="Submit Deposit", command=submit_deposit)
        deposit_button.pack(pady=20)

    def company_login(self):
        self.company_login_window = tk.Toplevel(self)
        self.company_login_window.title("Company Login")
        self.company_login_window.geometry("300x200")

        self.username_label = tk.Label(self.company_login_window, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.company_login_window)
        self.username_entry.pack()

        self.password_label = tk.Label(self.company_login_window, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.company_login_window, show="*")
        self.password_entry.pack()

        self.submit_button = tk.Button(self.company_login_window, text="Submit", command=self.varify_company_login)
        self.submit_button.pack()

    def varify_company_login(self):
            username = self.username_entry.get()
            password = self.password_entry.get()
            user_lst = self.__inc.get_users()
            user = None

            if password != self.__inc.get_password():
                messagebox.showerror("Login Failed", "Invalid username or password")
            else:
                self.company_menu()
                self.company_login_window.destroy()


    def company_menu(self):
        self.company_menu_window = tk.Toplevel(self)
        self.company_menu_window.title("User Menu")
        self.company_menu_window.geometry("300x380")

        Check_user_list_button = tk.Button(self.company_menu_window, text="1. Check user list", command=self.Check_user_lst)
        Check_user_list_button.pack(pady=10)

        Check_remain_power_button = tk.Button(self.company_menu_window, text="2. Check remain power", command=self.Check_remain_power)
        Check_remain_power_button.pack(pady=10)

        Check_bill_rate_button = tk.Button(self.company_menu_window, text="3. Check bill rate", command=self.Check_bill_rate)
        Check_bill_rate_button.pack(pady=10)

        Change_password_button = tk.Button(self.company_menu_window, text="4. Change password", command=self.Change_password)
        Change_password_button.pack(pady=10)

        Change_bill_rate_button = tk.Button(self.company_menu_window, text="5. Change bill rate", command=self.Change_bill_rate)
        Change_bill_rate_button.pack(pady=10)

        Generate_power_button = tk.Button(self.company_menu_window, text="6. Generate power", command=self.Generate_power)
        Generate_power_button.pack(pady=10)
        
        Check_fulfillemnt_button = tk.Button(self.company_menu_window, text="7. Check fulfillment", command=self.Check_fulfillment)
        Check_fulfillemnt_button.pack(pady=10)

        back_button = tk.Button(self.company_menu_window, text="8. Back to Menu", command=self.company_menu_window.destroy)
        back_button.pack(pady=10)

    def Check_fulfillment(self):
        self.Check_fulfillment_window = tk.Toplevel(self)
        self.Check_fulfillment_window.title("Check fulfillment")
        self.Check_fulfillment_window.geometry("300x380")
        adv = self.__inc.get_advice()
        for text in adv:
            label = tk.Label(self.Check_fulfillment_window, text=text, font=('Arial', 12))
            label.pack(pady=5)
        back_button = tk.Button(self.Check_fulfillment_window, text="Close", command=self.Check_fulfillment_window.destroy)
        back_button.pack(pady=10)


    def Check_user_lst(self):
        self.Check_user_lst_window = tk.Toplevel(self)
        self.Check_user_lst_window.title("Check User List")
        self.Check_user_lst_window.geometry("300x380")

        tk.Label(self.Check_user_lst_window, text="User List", font=('Arial', 16, 'bold')).pack(pady=10)

        user_lst = self.__inc.get_users()

        self.user_combo = ttk.Combobox(self.Check_user_lst_window, values=[user.get_name() for user in user_lst])
        self.user_combo.pack(pady=10)
        self.user_combo.bind("<<ComboboxSelected>>", self.display_user_info)
        back_button = tk.Button(self.Check_user_lst_window, text="Back to Menu", command=self.Check_user_lst_window.destroy)
        back_button.pack(pady=10)

    def display_user_info(self, event):
        selected_name = self.user_combo.get()
        for user in self.__inc.get_users():
            if user.get_name() == selected_name:
                visa = user.get_visa()
                self.user_window = tk.Toplevel(self)
                self.user_window.title("Check User List")
                self.user_window.geometry("300x380")
                info_texts = [
                    f"Name: {user.get_name()}",
                    f"Password: {user.get_password()}",
                    f"Address: {user.get_address()}",
                    f"Customer type: {user.get_customer_type()}",
                    f"Usage: {user.get_usage()}",
                    f"Account: {visa.get_account()}",
                    f"Verify code: {visa.get_code()}"
                ]
                for text in info_texts:
                    label = tk.Label(self.user_window, text=text, font=('Arial', 12))
                    label.pack(pady=5)
                back_button = tk.Button(self.user_window, text="Close", command=self.user_window.destroy)
                back_button.pack(pady=10)
                break
    
    def Check_remain_power(self):
        self.Check_remain_power_window = tk.Toplevel(self)
        self.Check_remain_power_window.title("Check remain power")
        self.Check_remain_power_window.geometry("300x140")
        tk.Label(self.Check_remain_power_window, text="Remain Power", font=('Arial', 16, 'bold')).pack(pady=10)
        tk.Label(self.Check_remain_power_window, text=str(self.__inc.get_remain_usage()), font=('Arial', 12, 'bold')).pack(pady=10)
        
    def Check_bill_rate(self):
        self.Check_bill_rate_window = tk.Toplevel(self)
        self.Check_bill_rate_window.title("Check bill rate")
        self.Check_bill_rate_window.geometry("500x140")
        tk.Label(self.Check_bill_rate_window, text="Bill Rate", font=('Arial', 16, 'bold')).pack(pady=10)
        bill_rate = self.__inc.get_bill_rate()
        tk.Label(self.Check_bill_rate_window, text=str(bill_rate), font=('Arial', 12, 'bold')).pack(pady=10)
        
    def Change_password(self):
        self.Change_password_window = tk.Toplevel(self)
        self.Change_password_window.title("Change password")
        self.Change_password_window.geometry("300x180")
        tk.Label(self.Change_password_window, text="Input new password", font=('Arial', 12, 'bold')).pack(pady=10)
        new_value_entry = tk.Entry(self.Change_password_window, font=('Arial', 12))
        new_value_entry.pack(pady=10)
        
        def submit_changes():
            new_value = new_value_entry.get()
            self.__inc.set_password(new_value_entry.get())
            messagebox.showinfo("Info", "Password updated successfully!")
            self.Change_password_window.destroy()

        # Submit button
        submit_button = tk.Button(self.Change_password_window, text="Submit", command=submit_changes)
        submit_button.pack(pady=20)
        
    def Change_bill_rate(self):
        self.Change_bill_rate_window = tk.Toplevel(self)
        self.Change_bill_rate_window.title("Change bill rate")
        self.Change_bill_rate_window.geometry("230x310")
        self.entries = {}  
        self.entries["Customer Type"] = "personal"
        def set_type(e): e["Customer Type"] = ["personal","industry","education"][var.get()]
        var = tk.IntVar()
        
        b1 = tk.Radiobutton(self.Change_bill_rate_window, text="personal", variable=var, value=0, command=lambda: set_type(self.entries))
        b1.select()
        b1.grid(row=1, column=1, pady=10)
        b2 = tk.Radiobutton(self.Change_bill_rate_window, text="industry", variable=var, value=1, command=lambda: set_type(self.entries))
        b2.grid(row=1, column=2, pady=10)
        b3 = tk.Radiobutton(self.Change_bill_rate_window, text="education", variable=var, value=2, command=lambda: set_type(self.entries))
        b3.grid(row=1, column=3, pady=10)

        tk.Label(self.Change_bill_rate_window, text="Input bill rate index", font=('Arial', 12, 'bold')).grid(row=2, column=1, columnspan=3, pady=10)
        index_entry = tk.Entry(self.Change_bill_rate_window, font=('Arial', 12))
        index_entry.grid(row=3, column=1, columnspan=3, pady=10)

        tk.Label(self.Change_bill_rate_window, text="Input new bill rate", font=('Arial', 12, 'bold')).grid(row=4, column=1, columnspan=3, pady=10)
        new_value_entry = tk.Entry(self.Change_bill_rate_window, font=('Arial', 12))
        new_value_entry.grid(row=5, column=1, columnspan=3, pady=10)

        def submit_changes():
            rate = new_value_entry.get()
            idx = index_entry.get()
            type = self.entries["Customer Type"]
            self.__inc.set_bill_rate(type, int(idx)-1, int(rate))
            messagebox.showinfo("Info", "Bill rate updated successfully!")
            self.Change_bill_rate_window.destroy()

        submit_button = tk.Button(self.Change_bill_rate_window, text="Submit", command=submit_changes)
        submit_button.grid(row=6, column=1, columnspan=3, pady=20)
    def Generate_power(self):
        self.Generate_power_window = tk.Toplevel(self)
        self.Generate_power_window.title("Generate power")
        self.Generate_power_window.geometry("300x180")
        tk.Label(self.Generate_power_window, text="Input power", font=('Arial', 12, 'bold')).pack(pady=10)
        new_value_entry = tk.Entry(self.Generate_power_window, font=('Arial', 12))
        new_value_entry.pack(pady=10)
        
        def submit_changes():
            new_value = new_value_entry.get()
            self.__inc.inc_remain_usage(int(new_value))
            messagebox.showinfo("Info", "Power updated successfully!")
            self.Generate_power_window.destroy()

        submit_button = tk.Button(self.Generate_power_window, text="Submit", command=submit_changes)
        submit_button.pack(pady=20)
        
    def save_and_quit(self):
        with open("user_info.txt", "w") as f:
            f.write(self.__inc.get_ceo()+"\n")
            f.write(self.__inc.get_password()+"\n")
            d = self.__inc.get_bill_rate()
            for i in d["personal"]: f.write(str(i)+" ")
            for i in d["industry"]: f.write(str(i)+" ")
            for i in d["education"]: f.write(str(i)+" ")
            f.write("\n"+str(self.__inc.get_remain_usage())+"\n")
            strings = self.__inc.get_advice()
            for i in strings:
                for j in i:
                    if j != "\n": f.write(j)
                f.write("\0")
            f.write("\n")
            cnt = self.__inc.get_user_cnt()
            users = self.__inc.get_users()
            for i in range(cnt):
                v=users[i].get_visa()
                f.write(users[i].get_name()+"\n")
                f.write(users[i].get_password()+"\n")
                f.write(users[i].get_address()+"\n")
                f.write(users[i].get_customer_type()+"\n")
                f.write(v.get_account()+"\n")
                f.write(v.get_code()+"\n")
                f.write(str(v.get_deposit())+"\n")
                f.write(str(users[i].get_usage())+"\n")
                history = users[i].get_history_bill()
                for j in history: f.write(str(j)+" ")
                f.write("\n"+str(users[i].get_budget())+"\n")
        self.quit()

if __name__ == "__main__":
    app = GUI()
    app.mainloop()

#main = simulator()
#main.run()