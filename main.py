from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

class BankAccount:
    def __init__(self, account_type):
        self.account_type = account_type
        self.balance = 0.0
        self.details = {}

    def add_details(self, **kwargs):
        self.details.update(kwargs)

    def view_details(self):
        return self.details, self.balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

# In-memory storage for user accounts
user_accounts = {
    "savings": BankAccount("Savings"),
    "current": BankAccount("Current"),
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/account/<account_type>', methods=['GET', 'POST'])
def account(account_type):
    account = user_accounts.get(account_type)
    if request.method == 'POST':
        action = request.form.get('action')
        amount = float(request.form.get('amount', 0))
        detail_key = request.form.get('detail_key')
        detail_value = request.form.get('detail_value')

        if action == 'deposit':
            account.deposit(amount)
        elif action == 'withdraw':
            account.withdraw(amount)
        elif action == 'add_detail' and detail_key and detail_value:
            account.add_details(**{detail_key: detail_value})

    details, balance = account.view_details()
    return render_template('account.html', account=account, details=details, balance=balance)

if __name__ == "__main__":
    app.run(debug=True)


