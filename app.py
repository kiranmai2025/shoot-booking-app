from flask import Flask, render_template, request
import gspread
import os
import json
from google.oauth2.service_account import Credentials

app = Flask(__name__, template_folder='.')

# Defines permissions for accessing Google Sheets and Drive
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Automatically switches between local testing and Render environment variables
if os.path.exists('credentials.json'):
    creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPE)
else:
    creds_dict = json.loads(os.environ.get('GOOGLE_CREDS'))
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)

client = gspread.authorize(creds)
sheet = client.open("Shoot Bookings").sheet1

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        stype = request.form.get('stype')
        
        # Appends the form data as a new row in your Google Sheet
        sheet.append_row([name, phone, stype])
        
        return "<h1>Booking Success! We will call you soon.</h1>"
    return render_template('/index.html')

if __name__ == "__main__":
    app.run(debug=True)