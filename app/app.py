#importing required libraries
import numpy as np
import pickle
from feature import FeatureExtraction
import joblib
from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3
import re
import warnings
from gmail_extraction import clean_email_body, fetch_latest_email
warnings.filterwarnings('ignore')

app = Flask(__name__)

DATABASE = 'database.db'

def create_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT,
                  email TEXT, 
                  mobile INTEGER, 
                  username TEXT UNIQUE, 
                  password TEXT)''')
    conn.commit()
    conn.close()

def insert_user(name, email, mobile, username, password):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    sql_query = "INSERT INTO users (name, email, mobile, username, password) VALUES (?, ?, ?, ?, ?)"
    params = (name, email, mobile, username, password)
    print("SQL Query:", sql_query)
    print("Parameters:", params)
    c.execute(sql_query, params)
    conn.commit()
    conn.close()


def get_user(username):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form['name'] 
        email = request.form['email']
        mobile = request.form['mobile']
        username = request.form['username']
        password = request.form['password']
        
        if get_user(username):
            message = "User already exists!"
            return render_template('signup.html', message=message)
        insert_user(name, email, mobile, username, password)
        message = "Account successfully created"
        return render_template('signup.html', message=message)
    return render_template('signup.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)

        if user and user[5] == password:
            session['username'] = username
        
            return redirect(url_for('index'))
        return render_template('login.html', message="Invalid username or password!")
    return render_template('login.html')


@app.route("/logout")
def logout():
    session.clear()
    session.pop('username', None)
    return render_template("landing.html")


@app.route("/")
def home():
    return render_template("landing.html")

@app.route('/landing')
def landing():
    return render_template("landing.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/contactus', methods=['GET', 'POST'])
def contactus():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        conn = sqlite3.connect(
            'database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_query (name, email, subject, message) VALUES (?, ?, ?, ?)",
                       (name, email, subject, message))
        conn.commit()
        conn.close()

        message = "We have received your response, Our team will contact you shortly."

        return render_template('contactus.html',  message = message)

    return render_template('contactus.html')



############# Code Started

file = open("pickle/model.pkl","rb")
gbc = pickle.load(file)
file.close()

@app.route("/urlPhishing", methods=['GET', 'POST'])
def urlPhishing():

    if request.method == "POST":
        url = request.form["url"]
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1,30) 
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]

        percentage = round(y_pro_non_phishing * 100)

        if 0 <= percentage < 50:
            percentage = 100 - percentage
            prediction_label = f"Website is {percentage:.2f}% unsafe to use..."
            blocked = True
        else:
            prediction_label = f"Website is {percentage:.2f}% safe to use..."
            blocked = False

        if blocked:
            prediction_label += " Website is blocked."
            url = ""

        return render_template('urlPhishing.html', prediction_label=prediction_label, url=url)
    return render_template("urlPhishing.html")




loaded_model = joblib.load('model/spam_classifier_model.joblib')
loaded_vectorizer = joblib.load('model/vectorizer.joblib')

def clean_comment(comment):
    # Remove URLs
    comment = re.sub(r'http\S+|www\S+|https\S+', '', comment, flags=re.MULTILINE)
    # Remove special characters and numbers
    comment = re.sub(r'\@\w+|\#','', comment)
    comment = re.sub(r'[^A-Za-z\s]', '', comment)
    # Convert to lowercase
    comment = comment.lower()
    return comment

def predict_comment(comment):
            cleaned_comment = clean_comment(comment)
            vect_comment = loaded_vectorizer.transform([cleaned_comment])
            prediction = loaded_model.predict(vect_comment)
            return 'spam' if prediction[0] == 1 else 'ham'

# @app.route("/emailSpam", methods=['GET', 'POST'])
# def emailSpam():

#     if request.method == "POST":
#         username = "mani3catrat3@gmail.com"
#         password = "hdau sotj edmh zzir"

#         email_data, error = fetch_latest_email(username, password)
#         if error:
#           print(f"Error: {error}")
#         else:
#           cleaned_text = clean_email_body(email_data['text'])
#           print("Subject:", email_data['subject'])
#           print("Cleaned Text:", cleaned_text)

#         body = request.form["body"]
        
#         prediction = predict_comment(body)
#         print(prediction)

#         return render_template('emailSpam.html', x = prediction)
#     return render_template("emailSpam.html")
  
  
# @app.route('/emailSpam', methods=['GET', 'POST'])
# def emailSpam():
#     if request.method == "POST":
#         if 'fetchGmail' in request.form:  # This runs when "Enter the Gmail Recent message" button is clicked
#             username = "mani3catrat3@gmail.com"
#             password = "hdau sotj edmh zzir"
#             print("I am here")

#             # Fetch the latest email
#             email_data, error = fetch_latest_email(username, password)
#             if error:
#                 print(f"Error: {error}")
#                 return render_template('emailSpam.html', email_body='', subject='', x="Error fetching email")

#             # Clean the email body
#             cleaned_text = clean_email_body(email_data['text'])
#             print("Subject:", email_data['subject'])
#             print("Cleaned Text:", cleaned_text)

#             # Render the template with the fetched email details
#             return render_template('emailSpam.html', email_body=cleaned_text, subject=email_data['subject'], x="Fetched Gmail message")

#         if 'manualSubmit' in request.form:  # This runs when user manually enters body and clicks submit
#             body = request.form["body"]
            
#             # Call the prediction function with the manually entered body
#             prediction = predict_comment(body)
#             print(prediction)
            
#             # Render the template with prediction results
#             return render_template('emailSpam.html', email_body=body, x=prediction)
    
#     # Initial GET request
#     return render_template("emailSpam.html", email_body='', subject='', x='')


@app.route('/emailSpam', methods=['GET', 'POST'])
def emailSpam():
    if request.method == "POST":
        if 'gmailAddress' in request.form and 'gmailPassword' in request.form:  # This runs when Gmail credentials are submitted
            username = request.form['gmailAddress']
            password = request.form['gmailPassword']
            print(f"Gmail Address: {username}")
            print("I am here")

            # Fetch the latest email
            email_data, error = fetch_latest_email(username, password)
            if error:
                print(f"Error: {error}")
                return render_template('emailSpam.html', email_body='', subject='', x="Error fetching email")

            # Clean the email body
            cleaned_text = clean_email_body(email_data['text'])
            print("Subject:", email_data['subject'])
            print("Cleaned Text:", cleaned_text)

            # Render the template with the fetched email details
            return render_template('emailSpam.html', email_body=cleaned_text, subject=email_data['subject'], x="Fetched Gmail message")

        if 'manualSubmit' in request.form:  # This runs when user manually enters body and clicks submit
            body = request.form["body"]
            
            # Call the prediction function with the manually entered body
            prediction = predict_comment(body)
            print(prediction)
            
            # Render the template with prediction results
            return render_template('emailSpam.html', email_body=body, x=prediction)
    
    # Initial GET request
    return render_template("emailSpam.html", email_body='', subject='', x='')



@app.route("/spamSMS", methods=['GET', 'POST'])
def spamSMS():

    if request.method == "POST":

        body = request.form["body"]

        prediction = predict_comment(body)

        return render_template('spamSMS.html', x = prediction)
    return render_template("spamSMS.html")

if __name__ == "__main__":
    app.secret_key = 'fgxfhcgjvhkbl8674566ohihi987r6754'
    app.run(debug=True,port=8080, use_reloader=False)
    
    

