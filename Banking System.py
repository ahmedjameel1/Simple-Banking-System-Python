from datetime import datetime
from string import digits
import json
import re

class Accounts:
    now = datetime.now()
    def __init__(self, fname, sname, balance=0):
        self._fname = fname
        self._sname = sname
        self._balance = balance
        self._interest = 0.5
        self._created = Accounts.now.strftime("%d/%m/%Y %H:%M:%S")

    @property
    def name(self):
        return self._fname + ' ' + self._sname

    @name.setter
    def name(self, name):
        fname, sname = name
        self._fname = name[0].strip()
        self._sname = name[1].strip()
        return 

    @property
    def balance(self):
        return self._balance

    @classmethod
    def interest_rate(cls):
        return cls._interest

    def deposit(self, amount):
        self._balance += amount
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        transaction_id = str(self._fname[0])+str(id(self))
        confirmation_code = str('D-'+str(id(self))+'-'+str(''.join(c for c in dt_string if c in digits))+'-'+str(transaction_id))
        transaction = {str(confirmation_code):{'id': transaction_id,
                        'time': now.strftime("%d/%m/%Y %H:%M:%S"), 'amount': amount,'account_id':id(self)}}
        f = open('transactions.txt', 'a')
        f.write('\n')
        f.write(json.dumps(transaction))

    def withdraw(self, amount):
        if self._balance - amount < 0:
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            transaction_id = str(self._fname[0])+str(id(self))
            confirmation_code = str('X-'+str(id(self))+'-'+str(''.join(c for c in dt_string if c in digits))+'-'+str(transaction_id))
            transaction = {str(confirmation_code):{'id': transaction_id,
                            'time': now.strftime("%d/%m/%Y %H:%M:%S"), 'amount': amount,'account_id':id(self)}}
            f = open('transactions.txt', 'a')
            f.write('\n')
            f.write(json.dumps(transaction))

        else:
            self._balance -= amount
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            transaction_id = str(self._fname[0])+str(id(self))
            confirmation_code = str('W-'+str(id(self))+'-'+str(''.join(c for c in dt_string if c in digits))+'-'+str(transaction_id))
            transaction = {str(confirmation_code):{'id': transaction_id,
                            'time': now.strftime("%d/%m/%Y %H:%M:%S"), 'amount': amount,'account_id':id(self)}}
            f = open('transactions.txt', 'a')
            f.write('\n')
            f.write(json.dumps(transaction))


    def pay_interest(self):
        now = datetime.now()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        transaction_id = str(self._fname[0])+str(id(self))
        confirmation_code = str('I-'+str(id(self))+'-'+str(''.join(c for c in dt_string if c in digits))+'-'+str(transaction_id))
        transaction = {str(confirmation_code):{'id': transaction_id,
                        'time': now.strftime("%d/%m/%Y %H:%M:%S"),
                         'amount': self._balance*self._interest,'account_id':id(self)}}
        f = open('transactions.txt', 'a')
        f.write('\n')
        f.write(json.dumps(transaction))
        self._balance = self._balance + self._balance*self._interest

    @classmethod
    def get_transaction(cls, confirmation_code):
        with open('transactions.txt', 'r') as file:
            data = file.read()
            data = '[' + re.sub(r'\}\s\{', '},{', data) + ']'
            transactions = json.loads(data)
            for i in transactions:
                for key, value in i.items():
                    if key == confirmation_code:
                        transaction = i[key]
            return transaction
        







