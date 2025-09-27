# BookVana Library Management System
# File structure:
# bookvana/
# ├── app.py
# ├── requirements.txt
# ├── static/
# │   ├── css/
# │   │   └── style.css
# │   ├── js/
# │   │   └── script.js
# │   └── sounds/
# │       ├── click.mp3
# │       ├── success.mp3
# │       └── error.mp3
# └── templates/
#     ├── base.html
#     ├── index.html
#     ├── books.html
#     ├── members.html
#     └── transactions.html

# app.py - Main Flask Application
from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime, timedelta
import json
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import sqlite3
import psycopg2
from urllib.parse import urlparse

app = Flask(__name__)


def get_db():
    """Get database connection based on environment."""
    if os.environ.get('DATABASE_URL'):
        # PostgreSQL connection from DATABASE_URL
        url = urlparse(os.environ['DATABASE_URL'])
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        return conn
    else:
        # Local SQLite
        return sqlite3.connect('bookvana.db')

# Initialize database
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Determine ID definition based on database
    id_def = 'SERIAL PRIMARY KEY' if os.environ.get('DATABASE_URL') else 'INTEGER PRIMARY KEY AUTOINCREMENT'

    # Books table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS books (
            id {id_def},
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE,
            category TEXT NOT NULL,
            copies_total INTEGER DEFAULT 1,
            copies_available INTEGER DEFAULT 1,
            price REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Members table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS members (
            id {id_def},
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT,
            membership_type TEXT DEFAULT 'Regular',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Transactions table
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS transactions (
            id {id_def},
            book_id INTEGER,
            member_id INTEGER,
            transaction_type TEXT NOT NULL,
            issue_date TIMESTAMP,
            due_date TIMESTAMP,
            return_date TIMESTAMP,
            fine_amount REAL DEFAULT 0.0,
            status TEXT DEFAULT 'Active',
            FOREIGN KEY (book_id) REFERENCES books (id),
            FOREIGN KEY (member_id) REFERENCES members (id)
        )
    ''')

    # Insert sample data only if tables are empty
    cursor.execute('SELECT COUNT(*) FROM books')
    count = cursor.fetchone()[0]
    if count == 0:
        # Sample books
        books_data = [
            ('The Great Gatsby', 'F. Scott Fitzgerald', '978-0-7432-7356-5', 'Fiction', 5, 5, 10.99),
            ('To Kill a Mockingbird', 'Harper Lee', '978-0-06-112008-4', 'Fiction', 3, 3, 8.99),
            ('1984', 'George Orwell', '978-0-452-28423-4', 'Fiction', 4, 4, 9.99)
        ]
        for book in books_data:
            if os.environ.get('DATABASE_URL'):
                cursor.execute('''
                    INSERT INTO books (title, author, isbn, category, copies_total, copies_available, price)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', book)
            else:
                cursor.execute('''
                    INSERT INTO books (title, author, isbn, category, copies_total, copies_available, price)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', book)

        # Sample members
        members_data = [
            ('John Doe', 'john@example.com', '1234567890', '123 Main St', 'Regular'),
            ('Jane Smith', 'jane@example.com', '0987654321', '456 Elm St', 'Premium')
        ]
        for member in members_data:
            if os.environ.get('DATABASE_URL'):
                cursor.execute('''
                    INSERT INTO members (name, email, phone, address, membership_type)
                    VALUES (%s, %s, %s, %s, %s)
                ''', member)
            else:
                cursor.execute('''
                    INSERT INTO members (name, email, phone, address, membership_type)
                    VALUES (?, ?, ?, ?, ?)
                ''', member)

    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Book categories
BOOK_CATEGORIES = [
    'Fiction', 'Non-Fiction', 'Science Fiction', 'Fantasy', 'Mystery', 'Romance', 'Thriller',
    'Biography', 'History', 'Science', 'Technology', 'Philosophy', 'Psychology', 'Health',
    'Cooking', 'Travel', 'Art', 'Music', 'Poetry', 'Drama', 'Comedy', 'Adventure',
    'Self-Help', 'Business', 'Economics', 'Politics', 'Religion', 'Spirituality',
    'Education', 'Reference', 'Encyclopedia', 'Dictionary', 'Atlas', 'Textbook',
    'Children', 'Young Adult', 'Comics', 'Graphic Novels', 'Manga', 'Photography',
    'Gardening', 'Sports', 'Fitness', 'Medicine', 'Engineering', 'Mathematics',
    'Physics', 'Chemistry', 'Biology', 'Astronomy', 'Geography', 'Archaeology',
    'Anthropology', 'Sociology', 'Law', 'Architecture', 'Design', 'Fashion'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books():
    return render_template('books.html', categories=BOOK_CATEGORIES)

@app.route('/members')
def members():
    return render_template('members.html')

@app.route('/transactions')
def transactions():
    return render_template('transactions.html')

# API Routes
@app.route('/api/books', methods=['GET', 'POST'])
def api_books():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM books ORDER BY title')
        books = cursor.fetchall()
        book_list = []
        for book in books:
            book_list.append({
                'id': book[0], 'title': book[1], 'author': book[2],
                'isbn': book[3], 'category': book[4], 'copies_total': book[5],
                'copies_available': book[6], 'price': book[7]
            })
        conn.close()
        return jsonify(book_list)

    elif request.method == 'POST':
        data = request.json
        if os.environ.get('DATABASE_URL'):
            cursor.execute('''
                INSERT INTO books (title, author, isbn, category, copies_total, copies_available, price)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (data['title'], data['author'], data['isbn'], data['category'],
                  data['copies_total'], data['copies_available'], data['price']))
        else:
            cursor.execute('''
                INSERT INTO books (title, author, isbn, category, copies_total, copies_available, price)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (data['title'], data['author'], data['isbn'], data['category'],
                  data['copies_total'], data['copies_available'], data['price']))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Book added successfully!'})

@app.route('/api/members', methods=['GET', 'POST'])
def api_members():
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'GET':
        cursor.execute('SELECT * FROM members ORDER BY name')
        members = cursor.fetchall()
        member_list = []
        for member in members:
            member_list.append({
                'id': member[0], 'name': member[1], 'email': member[2],
                'phone': member[3], 'address': member[4], 'membership_type': member[5]
            })
        conn.close()
        return jsonify(member_list)
    
    elif request.method == 'POST':
        data = request.json
        if os.environ.get('DATABASE_URL'):
            cursor.execute('''
                INSERT INTO members (name, email, phone, address, membership_type)
                VALUES (%s, %s, %s, %s, %s)
            ''', (data['name'], data['email'], data['phone'], data['address'], data['membership_type']))
        else:
            cursor.execute('''
                INSERT INTO members (name, email, phone, address, membership_type)
                VALUES (?, ?, ?, ?, ?)
            ''', (data['name'], data['email'], data['phone'], data['address'], data['membership_type']))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Member added successfully!'})

@app.route('/api/issue-book', methods=['POST'])
def issue_book():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if book is available
    if os.environ.get('DATABASE_URL'):
        cursor.execute('SELECT copies_available FROM books WHERE id = %s', (data['book_id'],))
    else:
        cursor.execute('SELECT copies_available FROM books WHERE id = ?', (data['book_id'],))
    result = cursor.fetchone()
    
    if result and result[0] > 0:
        # Issue the book
        issue_date = datetime.now()
        due_date = issue_date + timedelta(days=14)  # 14 days loan period
        
        if os.environ.get('DATABASE_URL'):
            cursor.execute('''
                INSERT INTO transactions (book_id, member_id, transaction_type, issue_date, due_date, status)
                VALUES (%s, %s, 'ISSUE', %s, %s, 'Active')
            ''', (data['book_id'], data['member_id'], issue_date, due_date))
        else:
            cursor.execute('''
                INSERT INTO transactions (book_id, member_id, transaction_type, issue_date, due_date, status)
                VALUES (?, ?, 'ISSUE', ?, ?, 'Active')
            ''', (data['book_id'], data['member_id'], issue_date, due_date))
        
        # Update book availability
        if os.environ.get('DATABASE_URL'):
            cursor.execute('''
                UPDATE books SET copies_available = copies_available - 1 WHERE id = %s
            ''', (data['book_id'],))
        else:
            cursor.execute('''
                UPDATE books SET copies_available = copies_available - 1 WHERE id = ?
            ''', (data['book_id'],))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Book issued successfully!'})
    else:
        conn.close()
        return jsonify({'success': False, 'message': 'Book not available!'})

@app.route('/api/return-book', methods=['POST'])
def return_book():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    
    # Find active transaction
    if os.environ.get('DATABASE_URL'):
        cursor.execute('''
            SELECT id, due_date FROM transactions 
            WHERE book_id = %s AND member_id = %s AND status = 'Active'
            ORDER BY issue_date DESC LIMIT 1
        ''', (data['book_id'], data['member_id']))
    else:
        cursor.execute('''
            SELECT id, due_date FROM transactions 
            WHERE book_id = ? AND member_id = ? AND status = 'Active'
            ORDER BY issue_date DESC LIMIT 1
        ''', (data['book_id'], data['member_id']))
    
    result = cursor.fetchone()
    if result:
        transaction_id, due_date = result
        return_date = datetime.now()
        if isinstance(due_date, str):
            due_date = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        else:
            due_date = due_date
        
        # Calculate fine if overdue
        fine_amount = 0.0
        if return_date > due_date:
            days_overdue = (return_date - due_date).days
            fine_amount = days_overdue * 5.0  # ₹5 per day fine
        
        # Update transaction
        if os.environ.get('DATABASE_URL'):
            cursor.execute('''
                UPDATE transactions SET return_date = %s, fine_amount = %s, status = 'Returned'
                WHERE id = %s
            ''', (return_date, fine_amount, transaction_id))
        else:
            cursor.execute('''
                UPDATE transactions SET return_date = ?, fine_amount = ?, status = 'Returned'
                WHERE id = ?
            ''', (return_date, fine_amount, transaction_id))
        
        # Update book availability
        if os.environ.get('DATABASE_URL'):
            cursor.execute('''
                UPDATE books SET copies_available = copies_available + 1 WHERE id = %s
            ''', (data['book_id'],))
        else:
            cursor.execute('''
                UPDATE books SET copies_available = copies_available + 1 WHERE id = ?
            ''', (data['book_id'],))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Book returned successfully! Fine: ₹{fine_amount}'})
    else:
        conn.close()
        return jsonify({'success': False, 'message': 'No active transaction found!'})

@app.route('/api/transactions', methods=['GET'])
def api_transactions():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM transactions ORDER BY issue_date DESC')
    transactions = cursor.fetchall()
    transaction_list = []
    for trans in transactions:
        transaction_list.append({
            'id': trans[0], 'book_id': trans[1], 'member_id': trans[2],
            'transaction_type': trans[3], 'issue_date': trans[4],
            'due_date': trans[5], 'return_date': trans[6],
            'fine_amount': trans[7], 'status': trans[8]
        })
    conn.close()
    return jsonify(transaction_list)

@app.route('/api/stats', methods=['GET'])
def api_stats():
    conn = get_db()
    cursor = conn.cursor()
    
    # Total books
    cursor.execute('SELECT COUNT(*) FROM books')
    total_books = cursor.fetchone()[0]
    
    # Active members (all members for simplicity)
    cursor.execute('SELECT COUNT(*) FROM members')
    total_members = cursor.fetchone()[0]
    
    # Books issued (active transactions)
    cursor.execute('SELECT COUNT(*) FROM transactions WHERE status = "Active"')
    books_issued = cursor.fetchone()[0]
    
    conn.close()
    return jsonify({
        'totalBooks': total_books,
        'activeMembers': total_members,
        'booksIssued': books_issued
    })

@app.route('/api/download-bill/<int:transaction_id>')
def download_bill(transaction_id):
    conn = get_db()
    cursor = conn.cursor()
    
    # Get transaction details
    if os.environ.get('DATABASE_URL'):
        cursor.execute('''
            SELECT t.*, b.title, b.author, b.price, m.name, m.email, m.phone
            FROM transactions t
            JOIN books b ON t.book_id = b.id
            JOIN members m ON t.member_id = m.id
            WHERE t.id = %s
        ''', (transaction_id,))
    else:
        cursor.execute('''
            SELECT t.*, b.title, b.author, b.price, m.name, m.email, m.phone
            FROM transactions t
            JOIN books b ON t.book_id = b.id
            JOIN members m ON t.member_id = m.id
            WHERE t.id = ?
        ''', (transaction_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        # Create PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        
        # Header
        p.setFont("Helvetica-Bold", 20)
        p.drawString(200, 750, "🌿 BookVana Library 🌿")
        
        p.setFont("Helvetica", 12)
        p.drawString(50, 700, f"Transaction ID: {result[0]}")
        p.drawString(50, 680, f"Member: {result[11]} ({result[12]})")
        p.drawString(50, 660, f"Phone: {result[13]}")
        p.drawString(50, 640, f"Book: {result[9]} by {result[10]}")
        p.drawString(50, 620, f"Issue Date: {result[4]}")
        p.drawString(50, 600, f"Due Date: {result[5]}")
        
        if result[6]:  # Return date exists
            p.drawString(50, 580, f"Return Date: {result[6]}")
            p.drawString(50, 560, f"Fine Amount: ₹{result[7]}")
        
        p.drawString(50, 520, f"Book Price: ₹{result[8]}")
        
        # Footer
        p.setFont("Helvetica-Italic", 10)
        p.drawString(200, 50, "Made with ❤️ by Saket")
        
        p.save()
        buffer.seek(0)
        
        return send_file(buffer, as_attachment=True, download_name=f'bill_{transaction_id}.pdf', mimetype='application/pdf')
    
    return jsonify({'error': 'Transaction not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
