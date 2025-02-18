from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'dhrubasaha204'  # Required for flash messages

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'bank_management'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        name = request.form['name']
        initial_deposit = float(request.form['initial_deposit'])
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO accounts (name, balance) VALUES (%s, %s)', (name, initial_deposit))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Account created successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('create_account.html')

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        account_id = int(request.form['account_id'])
        amount = float(request.form['amount'])
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE accounts SET balance = balance + %s WHERE account_id = %s', (amount, account_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Deposit successful!', 'success')
        return redirect(url_for('home'))
    return render_template('deposit.html')

@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        account_id = int(request.form['account_id'])
        amount = float(request.form['amount'])
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT balance FROM accounts WHERE account_id = %s', (account_id,))
        balance = cursor.fetchone()[0]
        if balance >= amount:
            cursor.execute('UPDATE accounts SET balance = balance - %s WHERE account_id = %s', (amount, account_id))
            conn.commit()
            flash('Withdrawal successful!', 'success')
        else:
            flash('Insufficient balance!', 'danger')
        cursor.close()
        conn.close()
        return redirect(url_for('home'))
    return render_template('withdraw.html')

@app.route('/view_accounts')
def view_accounts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM accounts')
    accounts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_accounts.html', accounts=accounts)

@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    if request.method == "POST":
        account_id = request.form["account_id"]

        conn = get_db_connection() 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE account_id = %s", (account_id,))
        account = cursor.fetchone()

        if account:
            cursor.execute("DELETE FROM accounts WHERE account_id = %s", (account_id,))
            conn.commit()
            flash("Account deleted successfully!", "success")
        else:
            flash("Account ID not found!", "danger")

        cursor.close()
        conn.close()
        return redirect(url_for("delete_account"))

    return render_template("delete_account.html")

if __name__ == '__main__':
    app.run(debug=True)


