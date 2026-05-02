import sqlite3
import os
from flask import Flask, request, redirect

app = Flask(__name__)

# --- 1. DATABASE LOGIC (Glitch-Free Storage) ---
def get_db_connection():
    conn = sqlite3.connect('shoots.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the table if it doesn't exist
with get_db_connection() as conn:
    conn.execute('CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, phone TEXT, type TEXT)')

# --- 2. CLIENT BOOKING PAGE ---
@app.route('/')
def home():
    return '''
    <body style="font-family:sans-serif; background:#f0f2f5; display:flex; justify-content:center; align-items:center; height:100vh; margin:0;">
        <div style="background:white; padding:40px; border-radius:20px; box-shadow:0 10px 25px rgba(0,0,0,0.1); width:350px; text-align:center;">
            <h1 style="color:#1c1e21; margin-bottom:10px;">📸 ShootBook</h1>
            <p style="color:#606770; margin-bottom:25px;">Fast & Professional Booking</p>
            <form action="/submit" method="POST">
                <input type="text" name="phone" placeholder="Mobile Number" required style="width:100%; padding:15px; margin-bottom:15px; border-radius:8px; border:1px solid #ddd; box-sizing:border-box;">
                <input type="text" name="details" placeholder="Shoot Type (e.g. Wedding)" required style="width:100%; padding:15px; margin-bottom:20px; border-radius:8px; border:1px solid #ddd; box-sizing:border-box;">
                <button type="submit" style="width:100%; padding:15px; background:#007bff; color:white; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">Book Now</button>
            </form>
        </div>
    </body>
    '''

# --- 3. SUBMIT LOGIC ---
@app.route('/submit', methods=['POST'])
def submit():
    phone = request.form['phone']
    details = request.form['details']
    with get_db_connection() as conn:
        conn.execute('INSERT INTO bookings (phone, type) VALUES (?, ?)', (phone, details))
        conn.commit()
    return '<h2>Booking Confirmed!</h2><p>Your request has been sent.</p><a href="/">Go Back</a>'

# --- 4. ADMIN DASHBOARD (For your friend) ---
@app.route('/admin-dashboard-secret')
def admin():
    with get_db_connection() as conn:
        bookings = conn.execute('SELECT * FROM bookings').fetchall()
    
    rows = ""
    for b in bookings:
        rows += f"<tr><td style='padding:12px; border-bottom:1px solid #ddd;'>{b['phone']}</td><td style='padding:12px; border-bottom:1px solid #ddd;'>{b['type']}</td></tr>"

    return f'''
    <body style="font-family:sans-serif; padding:20px; background:#f0f2f5;">
        <div style="max-width:600px; margin:auto; background:white; padding:30px; border-radius:15px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
            <h2 style="color:#333;">Current Bookings</h2>
            <table style="width:100%; border-collapse:collapse;">
                <tr style="background:#007bff; color:white; text-align:left;">
                    <th style="padding:12px;">Phone</th><th style="padding:12px;">Type</th>
                </tr>
                {rows if rows else "<tr><td colspan='2' style='padding:20px; text-align:center;'>No bookings yet</td></tr>"}
            </table>
        </div>
    </body>
    '''

if __name__ == '__main__':
    app.run(debug=True)