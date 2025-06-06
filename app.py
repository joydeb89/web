from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    vendor = data['vendor']
    date = data['date']
    total = data['total']
    items = data['items']

    conn = sqlite3.connect('sales.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor TEXT,
            date TEXT,
            total REAL
        )
    ''')

    cursor.execute('''
        INSERT INTO sale_records (vendor, date, total) VALUES (?, ?, ?)
    ''', (vendor, date, total))

    sale_id = cursor.lastrowid

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER,
            item TEXT,
            qty INTEGER,
            rate REAL,
            total REAL
        )
    ''')

    for item in items:
        cursor.execute('''
            INSERT INTO sale_items (sale_id, item, qty, rate, total) VALUES (?, ?, ?, ?, ?)
        ''', (sale_id, item['item'], item['qty'], item['rate'], item['total']))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Record saved to SQLite DB successfully'})

if __name__ == '__main__':
    app.run(debug=True)
