# 🌿 BookVana - Forest Library Management System 📚

A beautiful, interactive library management system with a magical forest theme. Built with Flask, HTML5, CSS3, and JavaScript.

## ✨ Features

- 🌲 **Beautiful Forest Theme** - Animated butterflies, floating leaves, trees, and forest animals
- 📚 **Complete Book Management** - Add, edit, search, and categorize books
- 👥 **Member Management** - Handle member registrations and profiles  
- 📊 **Transaction Tracking** - Issue/return books, calculate fines, generate bills
- 💰 **Fine Management** - Automatic calculation of overdue fines (₹5/day)
- 📄 **PDF Bill Generation** - Download transaction receipts
- 🔊 **Interactive Sound Effects** - Touch sounds for better user experience
- 📱 **Responsive Design** - Works perfectly on mobile and desktop
- 🎨 **Modern UI/UX** - Glassmorphism effects, smooth animations
- 📈 **Analytics Dashboard** - View library statistics and reports

## 📁 File Structure

```
bookvana/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── bookvana.db           # SQLite database (auto-created)
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── script.js     # JavaScript functionality
│   └── sounds/           # Sound effects (optional)
│       ├── click.mp3
│       ├── success.mp3
│       └── error.mp3
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Dashboard
    ├── books.html        # Book management
    ├── members.html      # Member management
    └── transactions.html # Transaction tracking
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+ installed
- pip (Python package manager)

### Step 1: Create Project Directory
```bash
mkdir bookvana
cd bookvana
```

### Step 2: Set up Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv bookvana_env

# Activate virtual environment
# Windows:
bookvana_env\Scripts\activate
# Linux/Mac:
source bookvana_env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create Directory Structure
```bash
mkdir static
mkdir static/css
mkdir static/js
mkdir static/sounds
mkdir templates
```

### Step 5: Copy Files
Copy all the provided files to their respective directories:

- `app.py` → root directory
- `requirements.txt` → root directory  
- `style.css` → `static/css/`
- `script.js` → `static/js/`
- `base.html` → `templates/`
- `index.html` → `templates/`
- `books.html` → `templates/`
- `members.html` → `templates/`
- `transactions.html` → `templates/`

### Step 6: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## 🎮 Usage Guide

### Dashboard
- View library statistics (total books, members, transactions)
- Quick actions for common tasks
- Recent activity feed
- Settings for sound effects and loan periods

### Book Management
- **Add Books**: Click "Add Book" to add new books with details
- **Search & Filter**: Find books by title, author, ISBN, or category  
- **Edit/Delete**: Manage existing book records
- **Issue Books**: Directly issue available books to members

### Member Management
- **Add Members**: Register new library members
- **Membership Types**: Regular, Premium, Student
- **Search Members**: Find members by name, email, or phone
- **Member Details**: View complete member information

### Transactions
- **Issue Books**: Assign books to members with due dates
- **Return Books**: Process returns and calculate fines automatically
- **View Reports**: Track all transactions and generate analytics
- **Download Bills**: PDF receipts for transactions
- **Overdue Management**: Track and manage overdue books

## 🎨 Customization

### Adding Sound Effects
Place sound files in `static/sounds/`:
- `click.mp3` - Button click sounds
- `success.mp3` - Success operation sounds  
- `error.mp3` - Error notification sounds

### Modifying Categories
Edit the `BOOK_CATEGORIES` list in `app.py` to add/remove book categories.

### Changing Fine Amount
Default fine is ₹5 per day. Modify in:
- `app.py` - Backend calculation
- `script.js` - Frontend calculation
- Settings modal - User preference

### Theme Customization
Edit CSS variables in `style.css`:
```css
:root {
    --forest-green: #2d5016;
    --leaf-green: #4a7c59;
    --light-green: #8bc34a;
    /* Add your colors */
}
```

## 🗄️ Database Schema

The system uses SQLite with three main tables:

### Books Table
- `id` - Primary key
- `title` - Book title
- `author` - Author name
- `isbn` - ISBN number (optional)
- `category` - Book category
- `copies_total` - Total copies owned
- `copies_available` - Available copies
- `price` - Book price in ₹
- `created_at` - Creation timestamp

### Members Table
- `id` - Primary key
- `name` - Member full name
- `email` - Email address (unique)
- `phone` - Phone number
- `address` - Address
- `membership_type` - Regular/Premium/Student
- `created_at` - Registration date

### Transactions Table
- `id` - Primary key
- `book_id` - Foreign key to books
- `member_id` - Foreign key to members
- `transaction_type` - ISSUE/RETURN
- `issue_date` - Book issue date
- `due_date` - Return due date
- `return_date` - Actual return date
- `fine_amount` - Fine amount in ₹
- `status` - Active/Returned

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///bookvana.db
```

### Production Deployment
For production deployment:
1. Set `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn
3. Set up proper database backups
4. Configure HTTPS and security headers

## 🐛 Troubleshooting

### Common Issues

**Database errors on first run:**
- The database is auto-created on first run
- Ensure write permissions in the project directory

**Sound effects not working:**
- Check if sound files exist in `static/sounds/`
- Verify browser audio permissions
- Use MP3 format for compatibility

**Responsive issues:**
- Clear browser cache
- Check viewport meta tag in templates
- Verify CSS media queries

**PDF generation errors:**
- Ensure reportlab is installed: `pip install reportlab`
- Check file system permissions for temp files

## 📞 Support & Contact

Created with ❤️ by **Saket**

For issues or feature requests, please check the troubleshooting section first.

## 🎯 Future Enhancements

- 📱 Progressive Web App (PWA) support
- 📧 Email notifications for due dates
- 📊 Advanced analytics and charts
- 🔐 User authentication and roles
- 📚 Book reservation system
- 🌐 Multi-language support
- 📱 Mobile app integration



Feel free to share reviews and suggestions over saket.sharma.cse@gmail.com

**Happy Library Management! 🌿📚** 