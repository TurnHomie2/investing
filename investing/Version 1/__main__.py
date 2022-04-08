import tkinter as tk
from Settings import *
from utils import load_image
import os
import random

def windowsize(window,width,height): # set window height and width and center in screen
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    window.geometry('%dx%d+%d+%d' % (width, height, (screenWidth / 2) - (width / 2), (screenHeight / 2) - (height / 2)))

def clear(window,type):
    for widget in window.winfo_children():
        if type == 'pack':
            widget.pack_forget()
        elif type == 'place':
            widget.place_forget()
        elif type == 'grid':
            widget.grid_forget()
        elif type == 'all':
            for widget2 in window.winfo_children():
                widget2.pack_forget()
                widget2.grid_forget()
                widget2.place_forget()

def delete(window):
    for widget in window.winfo_children():
        widget.destroy()


class cashflow_item:
    def __init__(self, text, amount):
        self.text = text
        self.amount = amount
    def update_label(self, location):
        self.text_label = tk.Label(location, text=self.text, font=(FONT, TEXTSIZE))
        self.amount_label = tk.Label(location, text=f'${self.amount:,.2f}', font=(FONT, TEXTSIZE))

class real_estate:
    def __init__(self, name, value, style='none',interest_rate=.1, months_down_pmt = 180):
        if style == 'residential':
            self.picture = load_image('house', 'jpg', 100, 100)
        elif style == 'commercial':
            self.picture = load_image('shop', 'jpg', 100, 100)
        elif style == 'industrial':
            self.picture = load_image('factory', 'jpg', 100, 100)

        self.name = name
        self.value = value
        self.months_till_owned = months_down_pmt
        self.interest_rate = interest_rate
        self.rent = round(self.value*.012378, 2)
        self.down_pmt = round(self.value*.24732, 2)
        self.total_mortgage = round(self.value*.81978, 2)
        self.total_owed = 0
        self.emi = self.total_mortgage * self.interest_rate/12 * (1+self.interest_rate/12)**self.months_till_owned/((1+self.interest_rate/12)**self.months_till_owned-1)
        self.owned = False
        self.mortgage_bool = False
        self.mortgage_payment = cashflow_item(f'{self.name} mortgage payment', self.emi)
    def update_label(self, location):
        self.location = location
        self.frame = tk.Frame(self.location)
        self.picture_label = tk.Label(self.frame, image=self.picture)
        self.name_label = tk.Label(self.frame, text=self.name, font=(FONT, TEXTSIZE))
        self.value_label = tk.Label(self.frame, text=f'Worth ${self.value:,.2f}', font=(FONT, TEXTSIZE))
        self.rent_label = tk.Label(self.frame, text=f'Rent ${self.rent:,.2f}', font=(FONT, TEXTSIZE))
        self.down_pmt_label = tk.Label(self.frame, text=f'Down payment ${self.down_pmt:,.2f}', font=(FONT, TEXTSIZE))
        self.months_till_owned_label = tk.Label(self.frame, font=(FONT, TEXTSIZE), text=f'{self.months_till_owned} months till owned')
        self.emi_label = tk.Label(self.frame, text=f'EMI ${self.emi:,.2f}', font=(FONT, TEXTSIZE))
        self.pay_down_pmt_button = tk.Button(self.frame, text='Pay down pmt', font=(FONT, TEXTSIZE),command=lambda: self.pay('down_pmt'))
        self.pay_full_pmt_button = tk.Button(self.frame, text='Pay full pmt', font=(FONT, TEXTSIZE), command=lambda: self.pay('full_pmt'))

        if m.login_info['balance'] < self.down_pmt:
            self.pay_down_pmt_button.config(state=tk.DISABLED)

        if m.login_info['balance'] < self.value:
            self.pay_full_pmt_button.config(state='disabled')

        self.name_label.grid(row=0, column=0)
        self.picture_label.grid(row=0, column=1, columnspan=3, rowspan=3)
        self.value_label.grid(row=1, column=0)
        self.rent_label.grid(row=2, column=0)
        self.down_pmt_label.grid(row=3, column=0)
        self.months_till_owned_label.grid(row=4, column=0)
        self.emi_label.grid(row=5, column=0)
        self.pay_down_pmt_button.grid(row=6, column=0)
        self.pay_full_pmt_button.grid(row=6, column=1)
    def pay(self, payment):
        self.month_bought_on = m.login_info['month']
        if payment == 'down_pmt':
            self.owned = True
            self.mortgage_bool = True
            self.total_owed = self.total_mortgage

            self.rent = cashflow_item(f'{self.name} rent', self.rent)
            m.login_info['balance'] -= self.down_pmt
            m._place_widgets('home')
            m.save()
        elif payment == 'full_pmt':
            self.total_owed = 0
            self.owned = True
            self.rent = cashflow_item(f'{self.name} rent', self.rent)
            m.login_info['balance'] -= self.value
            m._place_widgets('home')
            m.save()




class main:
    def __init__(self, master):
        self.root = master
        self._create_variables()
        self._init_root()
        self.load_pics()
        self._create_objects()
        self._create_widgets()
        self._place_widgets('start')


    def _create_variables(self):
        self.user_list = os.listdir('users')
        temporary_user_list = []
        for user in self.user_list:
            temporary_user_list.append(user.lower())
        self.user_list = temporary_user_list

        self.income_list = []
        self.expenses_list = []
        self.real_estate_list = []
        self.income_collected = None
        self.expenses_paid = None
        self.random_expense_month = False
        self.total_income = 0
        self.total_expense = 0

    def _init_root(self):
        self.root.title(TITLE+' login')
        self.root.config(bg=BACKGROUND_COLOR)
        windowsize(self.root, SCREENWIDTH, SCREENHEIGHT)

        self.root.bind('<Escape>',lambda x: self.root.destroy())

    def load_pics(self):
        self.money_background = load_image('money_background', 'jfif', 1400, 900)
        self.wallet_pic = load_image('wallet_picture', 'jpg', 100, 100)
        self.for_sale_pic = load_image('for_sale_sign', 'jpg', 100, 100)
        self.financial_statement_picture = load_image('financial_statement', 'jpg', 100, 100)
        self.stock_chart_pic = load_image('stock_chart', 'png', 100, 100)
        self.pass_pic = load_image('PASS', 'jpg', 200, 100)

    def _create_objects(self):
        self.RE_small_house = real_estate('Small house', 281962.05, 'residential', months_down_pmt=6)
        self.RE_apartment = real_estate('Apartment', 912138.87, 'residential')
        self.RE_donut_store = real_estate('Donut store', 486973.81, 'commercial')
        self.RE_phone_factory = real_estate('Phone factory', 1382971.86, 'industrial')

        self.salary = cashflow_item('Salary', SALARY)

        self.income_tax = cashflow_item('Income tax %25', round(SALARY*.25, 2))


        self.income_list.append(self.salary)

        self.expenses_list.append(self.income_tax)

        self.real_estate_list.append(self.RE_small_house)
        self.real_estate_list.append(self.RE_apartment)
        self.real_estate_list.append(self.RE_donut_store)
        self.real_estate_list.append(self.RE_phone_factory)

    def _create_widgets(self):
        # Frames
        self.title_label_frame = tk.Frame(self.root, bg=BACKGROUND_ACCENT_COLOR, bd=TEXTSIZE/2,relief=tk.SUNKEN)
        self.game_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.r_or_l_frame = tk.Frame(self.game_frame, bg=BACKGROUND_ACCENT_COLOR, bd=10, relief=tk.RAISED)
        self.info_frame = tk.Frame(self.root, bg=BACKGROUND_COLOR)
        self.income_frame = tk.Frame(self.game_frame, bg='light grey', relief=tk.RAISED)
        self.expenses_frame = tk.Frame(self.game_frame, bg='light grey', relief=tk.RAISED)
        self.real_estate_frame = tk.Frame(self.game_frame, bg='light grey', relief=tk.RAISED)


        # Labels
        self.title_label = tk.Label(self.title_label_frame,text=TITLE, font=(FONT, TEXTSIZE*3,'bold'),relief=tk.RAISED)
        self.login_info_label = tk.Label(self.r_or_l_frame, font=(FONT, TEXTSIZE), relief=tk.FLAT, bg=BACKGROUND_ACCENT_COLOR)
        self.background_label = tk.Label(self.game_frame, image=self.money_background)
        self.welcome_label = tk.Label(self.title_label_frame, font=(FONT, TEXTSIZE))
        self.balance_label = tk.Label(self.info_frame, font=(FONT, TEXTSIZE))
        self.current_month_label = tk.Label(self.info_frame, font=(FONT, TEXTSIZE), bg='Dark grey')
        self.total_income_label = tk.Label(self.income_frame, font=(FONT, TEXTSIZE), fg='green')
        self.total_expense_label = tk.Label(self.expenses_frame, font=(FONT, TEXTSIZE), fg='red')
        self.total_balance_label = tk.Label(self.info_frame, font=(FONT, TEXTSIZE), bg='Dark grey')
        self.cashflow_label = tk.Label(self.game_frame, font=(FONT, TEXTSIZE))

        #  Buttons
        self.click_login_button = tk.Button(self.r_or_l_frame, bg=LOGIN_BACKGROUND_COLOR, text='Already have account', font=(FONT, TEXTSIZE, 'bold'), command=lambda: self._place_widgets('login'))
        self.click_register_button = tk.Button(self.r_or_l_frame, bg=LOGIN_BACKGROUND_COLOR, text='Register new account', font=(FONT, TEXTSIZE, 'bold'), command=lambda: self._place_widgets('register'))
        self.login_button = tk.Button(self.r_or_l_frame, bg=LOGIN_BACKGROUND_COLOR, text='Login', font=(FONT, TEXTSIZE, 'bold'), command=lambda: self.r_or_l('login'))
        self.register_button = tk.Button(self.r_or_l_frame, bg=LOGIN_BACKGROUND_COLOR, text='Register', font=(FONT, TEXTSIZE, 'bold'), command=lambda: self.r_or_l('register'))
        self.income_and_expenses_button = tk.Button(self.game_frame, image=self.wallet_pic, command=lambda: self._place_widgets('income_and_expenses'))
        self.real_estate_button = tk.Button(self.game_frame, image=self.for_sale_pic, command=lambda: self._place_widgets('real_estate'))
        self.financial_statement_button = tk.Button(self.game_frame, image=self.financial_statement_picture, command=lambda: self._place_widgets('financial_statement'))
        self.investing_button = tk.Button(self.game_frame, image=self.stock_chart_pic, command=lambda: self._place_widgets('investing'))
        self.pass_button = tk.Button(self.game_frame, image=self.pass_pic, command=self.pass_month)

        self.collect_income_button = tk.Button(self.income_frame, text='Collect', font=(FONT, TEXTSIZE), command=lambda: self.income_expenses('income'))
        self.pay_expenses_button = tk.Button(self.expenses_frame, text='Pay', font=(FONT, TEXTSIZE), command=lambda: self.income_expenses('expenses'))


        self.log_out_button = tk.Button(self.title_label_frame, text='Log out', command=self.log_out)
        self.back_button = tk.Button(self.game_frame, text='<<<', font=(FONT, TEXTSIZE*3), command=lambda: self._place_widgets('home'))
        # Login and register
        self.first_name_box_input = tk.StringVar
        self.first_name_box = tk.Entry(self.r_or_l_frame, bg=LOGIN_BACKGROUND_COLOR, font=(FONT, TEXTSIZE), textvariable=self.first_name_box_input, width=30)
        self.first_name_label = tk.Label(self.r_or_l_frame, bg=LOGIN_BACKGROUND_COLOR, text='First name', font=(FONT, TEXTSIZE))

        self.last_name_box_input = tk.StringVar
        self.last_name_box = tk.Entry(self.r_or_l_frame, bg=LOGIN_BACKGROUND_COLOR, font=(FONT, TEXTSIZE), textvariable=self.last_name_box_input, width=30)
        self.last_name_label = tk.Label(self.r_or_l_frame, bg=LOGIN_BACKGROUND_COLOR, text='Last name', font=(FONT, TEXTSIZE))

        self.email_box_input = tk.StringVar
        self.email_box = tk.Entry(self.r_or_l_frame, bg=LOGIN_BACKGROUND_COLOR, font=(FONT, TEXTSIZE), textvariable=self.email_box_input, width=30)
        self.email_label = tk.Label(self.r_or_l_frame, bg=LOGIN_BACKGROUND_COLOR, text='Email', font=(FONT, TEXTSIZE))

        self.username_box_input = tk.StringVar
        self.username_box = tk.Entry(self.r_or_l_frame, bg=LOGIN_BACKGROUND_COLOR, font=(FONT, TEXTSIZE), textvariable=self.username_box_input, width=30)
        self.username_label = tk.Label(self.r_or_l_frame, bg=LOGIN_BACKGROUND_COLOR, text='Username', font=(FONT, TEXTSIZE))

        self.password_box_input = tk.StringVar
        self.password_box = tk.Entry(self.r_or_l_frame, bg=LOGIN_BACKGROUND_COLOR, font=(FONT, TEXTSIZE), textvariable=self.password_box_input, width=30, show='*')
        self.password_label = tk.Label(self.r_or_l_frame, bg=LOGIN_BACKGROUND_COLOR, text='Password', font=(FONT, TEXTSIZE))

        self.retype_password_box_input = tk.StringVar
        self.retype_password_box = tk.Entry(self.r_or_l_frame, bg=LOGIN_BACKGROUND_COLOR, font=(FONT, TEXTSIZE), textvariable=self.retype_password_box_input, width=30, show='*')
        self.retype_password_label = tk.Label(self.r_or_l_frame, bg=LOGIN_BACKGROUND_COLOR, text='Retype Password', font=(FONT, TEXTSIZE))

    def _place_widgets(self, command):
        if command == 'start':
            clear(self.root, 'all')
            clear(self.r_or_l_frame, 'all')
            clear(self.game_frame, 'all')
            self.welcome_label.grid_forget()
            self.log_out_button.grid_forget()
            # Labels
            self.title_label.grid(row=0, column=0)
            self.login_info_label.grid(row=1,column=0)

            # Buttons
            self.click_login_button.grid(row=0, column=0)
            self.click_register_button.grid(row=0, column=1)

            # Frames
            self.title_label_frame.pack()
            self.game_frame.pack(pady=75)
            self.r_or_l_frame.pack()
        elif command == 'register':
            clear(self.r_or_l_frame, 'all')
            self.login_info_label.configure(text='')
            self.root.bind('<Return>', lambda x: self.r_or_l('register'))
            self.click_login_button.grid(row=0,column=0)

            self.first_name_label.grid(row=1,column=0, pady=10)
            self.first_name_box.grid(row=1, column=1, pady=10)

            self.last_name_label.grid(row=2, column=0, pady=10)
            self.last_name_box.grid(row=2, column=1, pady=10)

            self.email_label.grid(row=3, column=0, pady=10)
            self.email_box.grid(row=3, column=1, pady=10)

            self.username_label.grid(row=4, column=0, pady=10)
            self.username_box.grid(row=4, column=1, pady=10)

            self.password_label.grid(row=5, column=0, pady=10)
            self.password_box.grid(row=5, column=1, pady=10)

            self.retype_password_label.grid(row=6, column=0, pady=10)
            self.retype_password_box.grid(row=6, column=1, pady=10)

            self.register_button.grid(row=7, column=0, pady=10)
            self.login_info_label.grid(row=8, column=0)
        elif command == 'login':
            clear(self.r_or_l_frame, 'all')
            self.login_info_label.configure(text='')
            self.root.bind('<Return>', lambda x: self.r_or_l('login'))
            self.click_register_button.grid(row=0,column=0)

            self.username_label.grid(row=1, column=0, pady=10)
            self.username_box.grid(row=1, column=1, pady=10)

            self.password_label.grid(row=2, column=0, pady=10)
            self.password_box.grid(row=2, column=1, pady=10)

            self.login_button.grid(row=3, column=0, pady=10)
            self.login_info_label.grid(row=4, column=0)
        elif command == 'home':
            clear(self.game_frame, 'all')
            self.root.title(TITLE+' home')
            self.game_frame.pack_forget()
            self.info_frame.pack()
            self.game_frame.pack()
            self.current_month_label['text'] = 'Month: ' + str(self.login_info['month'])
            self.total_balance_label['text'] = f'Total balance: ${self.login_info["balance"]:,.2f}'

            self.current_month_label.grid(row=0, column=0, padx=10)
            self.total_balance_label.grid(row=0, column=1, padx=10)
            self.log_out_button.grid(row=0, column=1, padx=20)
            self.welcome_label.grid(row=0, column=2)
            self.welcome_label.config(text=self.username)
            self.background_label.grid(row=0, column=0, columnspan=10, rowspan=10)
            self.income_and_expenses_button.grid(row=0, column=7)
            self.real_estate_button.grid(row=3, column=7)
            self.financial_statement_button.grid(row=0, column=2)
            self.investing_button.grid(row=3, column=2)
            self.pass_button.grid(row=2, column=4)
            m.save()
        elif command == 'income_and_expenses':
            self.root.title(TITLE + ' income and expenses')

            clear(self.game_frame, 'all')
            clear(self.income_frame, 'all')
            clear(self.expenses_frame, 'all')
            self.background_label.grid(row=0, column=0, columnspan=10, rowspan=10)
            self.back_button.grid(row=0, column=0)
            self.income_frame.grid(row=1, column=3)
            self.expenses_frame.grid(row=1, column=5)

            self.income_frame.tkraise()
            self.expenses_frame.tkraise()

            self.total_income = 0
            self.total_expense = 0

            if not self.income_collected:
                self.collect_income_button.config(state=tk.NORMAL)

            if not self.expenses_paid:
                self.pay_expenses_button.config(state=tk.NORMAL)

            for item in self.income_list:
                item.update_label(self.income_frame)
                item.text_label.grid(row=self.income_list.index(item), column=0)
                item.amount_label.grid(row=self.income_list.index(item), column=1)
                self.total_income += item.amount


            for item in self.expenses_list:
                item.update_label(self.expenses_frame)
                item.text_label.grid(row=self.expenses_list.index(item), column=0)
                item.amount_label.grid(row=self.expenses_list.index(item), column=1)

                self.total_expense += item.amount
            if self.total_expense > self.login_info['balance']:
                self.pay_expenses_button.config(state='disabled')


            self.cashflow = self.total_income - self.total_expense
            self.cashflow_label.config(text=f'Cashflow: ${self.cashflow:,.2f}')
            self.cashflow_label.grid(row=2, column=4)

            self.total_income_label.config(text=f'Total income: ${self.total_income:,.2f}')
            self.total_income_label.grid(row=self.income_list.index(self.income_list[-1])+1, column=0, pady=15)
            self.collect_income_button.grid(row=self.income_list.index(self.income_list[-1])+2, column=0)

            self.total_expense_label.config(text=f'Total expenses: ${self.total_expense:,.2f}')
            self.total_expense_label.grid(row=self.expenses_list.index(self.expenses_list[-1])+1, column=0, pady=15)
            self.pay_expenses_button.grid(row=self.expenses_list.index(self.expenses_list[-1]) + 2, column=0)
            m.save()
        elif command == 'real_estate':
            self.root.title(TITLE+' real estate')
            clear(self.game_frame, 'all')
            clear(self.real_estate_frame, 'all')
            self.background_label.grid(row=0, column=0, columnspan=10, rowspan=10)
            self.back_button.grid(row=0, column=0)

            self.real_estate_frame.grid(row=0, column=4)
            self.real_estate_frame.tkraise()

            for item in self.real_estate_list:
                if not item.owned:
                    item.update_label(self.real_estate_frame)
                    item.frame.grid(row=self.real_estate_list.index(item)//3, column=self.real_estate_list.index(item)%3, padx=15, pady=15)
        elif command == 'financial_statement':
            self.root.title(TITLE+' Financial statement')
            clear(self.game_frame, 'all')
            self.background_label.grid(row=0, column=0, columnspan=10, rowspan=10)
            self.back_button.grid(row=0, column=0)
        elif command == 'investing':
            self.root.title(TITLE+' investing')
            clear(self.game_frame, 'all')
            self.background_label.grid(row=0, column=0, columnspan=10, rowspan=10)
            self.back_button.grid(row=0, column=0)

    def r_or_l(self, r_or_l):
        if r_or_l == 'register':
            self.username = self.username_box.get().lower()
            self.psw = self.password_box.get()
            self.retype_psw = self.retype_password_box.get()
            self.first_name = self.first_name_box.get()
            self.last_name = self.last_name_box.get()
            self.email = self.email_box.get()
            # Check for no first name
            if len(self.first_name) == 0:
                self.login_info_label.configure(text='First name required', fg='red', bg='snow')

            # Check for no last name
            elif len(self.last_name) == 0:
                self.login_info_label.configure(text='Last name required', fg='red', bg='snow')

            # Check for no email
            elif len(self.email) == 0:
                self.login_info_label.configure(text='Email required', fg='red', bg='snow')

            # Check for no username
            elif len(self.username) == 0:
                self.login_info_label.configure(text='Username required', fg='red', bg='snow')

            # Check for no password
            elif len(self.psw) == 0:
                self.login_info_label.configure(text='Password required', fg='red', bg='snow')

            # Check for no retype password
            elif len(self.retype_psw) == 0:
                self.login_info_label.configure(text='Retype password required', fg='red', bg='snow')

            # Check for username already existing
            elif self.username in self.user_list:
                self.login_info_label.configure(text='Username already taken', fg='red', bg='snow')

            # Check for password and retype password same
            elif self.psw != self.retype_psw:
                self.login_info_label.configure(text='Retype your passwords', fg='red', bg='snow')

            else:
                os.mkdir('users/'+str(self.username))
                login_info_file = open('users/' + str(self.username)+'/login_info.txt', 'a')

                login_info_file.write('first_name:' + str(self.first_name))
                login_info_file.write('\nlast_name:' + str(self.last_name))
                login_info_file.write('\nemail:' + str(self.email))
                login_info_file.write('\nusername:' + str(self.username))
                login_info_file.write('\npassword:' + str(self.psw))
                login_info_file.write('\nbalance:25000')
                login_info_file.write('\nmonth:1')
                login_info_file.write('\nincome_collected:False')
                login_info_file.write('\nexpenses_paid:False')
                for RE in self.real_estate_list:
                    login_info_file.write(f'\n{RE.name}_owned:False')
                    login_info_file.write(f'\n{RE.name}_mortgage:{RE.total_owed}')
                    login_info_file.write(f'\n{RE.name}_month_bought_on:None')
                login_info_file.close()


                self.login_info_label.configure(text='Account succesfully created', fg='light green', bg='snow')
                self._place_widgets('start')

        elif r_or_l == 'login':
            self.username = 'turnhomie'#self.username_box.get().lower()
            self.psw = '100149'#self.password_box.get()


            # check for no username
            if len(self.username) == 0:
                self.login_info_label.configure(text='Username required', fg='red', bg='snow')
            elif len(self.psw) == 0:
                self.login_info_label.configure(text='Password required', fg='red', bg='snow')
            elif self.username not in self.user_list:
                self.login_info_label.configure(text='No username found', fg='red', bg='snow')
            elif self.username in self.user_list:
                self.login_info = {}

                file = open('users/' + str(self.username) + '/login_info.txt')
                for line in file:
                    k, v = line.strip().split(':')
                    self.login_info[k.strip()] = v.strip()
                file.close()
                if self.psw == self.login_info['password']:
                    self.login_info_label.config(text='')
                    self.login_info['month'] = int(self.login_info['month'])
                    self.login_info['balance'] = float(self.login_info['balance'])
                    for RE in self.real_estate_list:
                        RE.total_owed = round(float(self.login_info[RE.name+'_mortgage']), 2)
                        if self.login_info[RE.name+'_owned'] == 'True':
                            RE.owned = True
                            RE.rent = cashflow_item(f'{RE.name} rent', RE.rent)
                            self.income_list.append(RE.rent)
                            if RE.total_owed >= 1:
                                RE.mortgage_bool = True
                                RE.mortgage_payment = cashflow_item(f'{RE.name} mortgage', RE.emi)
                                self.expenses_list.append(RE.mortgage_payment)

                        else:
                            RE.owned = False
                        if self.login_info[f'{RE.name}_month_bought_on'] != 'None':
                            RE.month_bought_on = int(self.login_info[f'{RE.name}_month_bought_on'])


                    if self.login_info['expenses_paid'] == 'True':
                        self.expenses_paid = True
                        self.pay_expenses_button.config(state=tk.DISABLED)
                    else:
                        self.expenses_paid = False

                    if self.login_info['income_collected'] == 'True':
                        self.income_collected = True
                        self.collect_income_button.config(state=tk.DISABLED)
                    else:
                        self.income_collected = False

                    self._place_widgets('home')
                elif self.psw != self.login_info['password']:
                    self.login_info_label.config(text='Incorrect password', fg='red', bg='snow')

    def log_out(self):
        self.save()
        self._place_widgets('start')

    def income_expenses(self, command):
        if command == 'income':
            self.income_collected = True
            self.login_info['balance'] += self.total_income
            self.collect_income_button.config(state=tk.DISABLED)
            self.total_balance_label['text'] = f'Total balance: ${self.login_info["balance"]:,.2f}'
            if self.expenses_paid == False:
                if self.total_expense > self.login_info['balance']:
                    self.pay_expenses_button.config(state='disabled')
            self.save()
        elif command == 'expenses':
            for item in self.real_estate_list:
                if item.mortgage_bool == True:
                    if item.total_owed >= item.emi:
                        item.total_owed -= (item.emi-item.total_owed*item.interest_rate/12)
                    elif item.total_owed < (item.emi - item.total_owed*item.interest_rate/12) and item.total_owed > 0:
                        item.total_owed = 0
                    if item.total_owed <= 0:
                        item.mortgage_bool = False
                        self.expenses_list.remove(item.mortgage_payment)


            self.expenses_paid = True
            self.login_info['balance'] -= self.total_expense
            for item in self.real_estate_list:
                if item.total_owed <= item.mortgage_payment.amount - (item.total_owed*item.interest_rate/12) and item.total_owed > 0:
                    item.mortgage_payment.amount = item.total_owed + item.total_owed * item.interest_rate/12


            self.pay_expenses_button.config(state=tk.DISABLED)
            self.total_balance_label['text'] = f'Total balance: ${self.login_info["balance"]:,.2f}'
            self.save()

    def pass_month(self):
        if self.income_collected and self.expenses_paid:
            self.login_info['month'] += 1
            for item in self.real_estate_list:
                if item.owned:
                    if item.month_bought_on + 1 == self.login_info['month']:
                        if item.mortgage_bool == True:
                            self.expenses_list.append(item.mortgage_payment)
                        self.income_list.append(item.rent)
            self.income_collected = False
            self.expenses_paid = False
            self.random_expense_month = False
            try:
                self.expenses_list.remove(self.random_expense)
            except:
                pass
            self.current_month_label.config(text='Month: '+str(self.login_info['month']))
            list = []
            for i in range(8):
                list.append(i)
            num = random.choice(list)
            if num == 0:
                self.random_expense_month = True
                self.random_expense_amount = random.randrange(2000, 10000)
                self.random_expense = cashflow_item('Random expense', self.random_expense_amount)
                self.expenses_list.append(self.random_expense)
            self.save()

    def save(self):
        file = open(f'users/{self.username}/login_info.txt', 'w')
        file.write(f'first_name:{self.login_info["first_name"]}\n')
        file.write(f'last_name:{self.login_info["last_name"]}\n')
        file.write(f'email:{self.login_info["email"]}\n')
        file.write(f'username:{self.login_info["username"]}\n')
        file.write(f'password:{self.login_info["password"]}\n')
        file.write(f'balance:{self.login_info["balance"]}\n')
        file.write(f'month:{self.login_info["month"]}\n')
        file.write(f'income_collected:{self.income_collected}\n')
        file.write(f'expenses_paid:{self.expenses_paid}\n')
        for RE in self.real_estate_list:
            file.write(f'{RE.name}_owned:{RE.owned}\n')
            file.write(f'{RE.name}_mortgage:{RE.total_owed}\n')
            try:
                file.write(f'{RE.name}_month_bought_on:{RE.month_bought_on}\n')
            except:
                file.write(f'{RE.name}_month_bought_on:None\n')


        file.close()


if __name__ == '__main__':
    root = tk.Tk()
    m = main(root)
    root.mainloop()
