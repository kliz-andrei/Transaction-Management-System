from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

transactions = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transactions', methods=['GET', 'POST'])
def get_transactions():
    sort_by = request.args.get('sort_by', 'date_desc')
    if sort_by == 'date_asc':
        transactions_sorted = sorted(transactions, key=lambda x: x['date'])
    elif sort_by == 'date_desc':
        transactions_sorted = sorted(transactions, key=lambda x: x['date'], reverse=True)
    elif sort_by == 'amount_asc':
        transactions_sorted = sorted(transactions, key=lambda x: x['amount'])
    elif sort_by == 'amount_desc':
        transactions_sorted = sorted(transactions, key=lambda x: x['amount'], reverse=True)
    else:
        transactions_sorted = transactions
    return render_template('transactions.html', transactions=transactions_sorted)

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        date = request.form['date']
        amount = request.form['amount']
        category = request.form['category']
        tags = request.form['tags'].split(',')
        tags = [tag.strip() for tag in tags]

        try:
            amount = float(amount)
            date = datetime.strptime(date, '%Y-%m-%d')
            transaction = {
                'id': len(transactions) + 1,
                'date': date,
                'amount': amount,
                'category': category,
                'tags': tags
            }
            transactions.append(transaction)
            return redirect(url_for('get_transactions'))
        except ValueError:
            flash("Please enter a valid date and numeric amount.")
            return redirect(url_for('add_transaction'))
    return render_template('add_transaction.html')

@app.route('/edit_transaction/<int:transaction_id>', methods=['GET', 'POST'])
def edit_transaction(transaction_id):
    transaction = next((t for t in transactions if t['id'] == transaction_id), None)
    if not transaction:
        return "Transaction not found", 404

    if request.method == 'POST':
        date = request.form['date']
        amount = request.form['amount']
        category = request.form['category']
        tags = request.form['tags'].split(',')
        tags = [tag.strip() for tag in tags]

        try:
            amount = float(amount)
            date = datetime.strptime(date, '%Y-%m-%d')
            transaction['date'] = date
            transaction['amount'] = amount
            transaction['category'] = category
            transaction['tags'] = tags
            return redirect(url_for('get_transactions'))
        except ValueError:
            flash("Please enter a valid date and numeric amount.")
            return redirect(url_for('edit_transaction', transaction_id=transaction_id))
    
    return render_template('edit_transaction.html', transaction=transaction)

@app.route('/delete_transaction/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    global transactions
    transactions = [t for t in transactions if t['id'] != transaction_id]
    return redirect(url_for('get_transactions'))

@app.route('/filter_transactions', methods=['POST'])
def filter_transactions():
    min_amount = request.form['min_amount']
    max_amount = request.form['max_amount']

    try:
        min_amount = float(min_amount)
        max_amount = float(max_amount)
        filtered_transactions = [t for t in transactions if min_amount <= t['amount'] <= max_amount]
        return render_template('transactions.html', transactions=filtered_transactions)
    except ValueError:
        flash("Please enter valid numeric values for min and max amounts.")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
