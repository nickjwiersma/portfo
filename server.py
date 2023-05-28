# create the virtual envoirment using $ Python3 -m venv "name of directory" | in this case $ Python3 -m venv web_server
# ^^^ this creates the neccesary files for the python virtual envoirment
# activate the server by $ . "folder name"/bin/activate | in this case $ . bin/activate
# first run $ export FLASK_APP=server.py
# to run in debug mode $ flask --app server.py run --debug

# Using templates to import to the website
# importing flask
# requesting info in a submitted form
# redirecting after submitting
from flask import Flask, render_template, url_for, request, redirect
from flask_mail import Mail, Message
# import CSV to write into csv files
import csv


app = Flask(__name__)

# setup for the email server
app.config['MAIL_SERVER'] = 'smtp.live.com' # gmail
## 1 in error try: 
#app.config['MAIL_PORT'] = 465
## 2 in error try: 
app.config['MAIL_PORT'] = 587
## 1 in error try: 
#app.config['MAIL_USE_SSL'] = True
## 2 in error try: 
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '***'
app.config['MAIL_PASSWORD'] = '***'

# Initialize the mail object with the Flask application
mail = Mail(app)

# defining the standard route
@app.route("/")
def my_home():
    return render_template('index.html')


# this code will make a redirection to all the html files in the templates folder
@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)

# write to a csv database
def write_to_csv(data):
    with open('database.csv', mode='a') as database:
        name = data["name"]
        email = data["email"]
        message = data["message"]
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name, email, message])



# Making the form ready for sending emails
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)

        name = data["name"]
        email = data["email"]
        category = data["category"]  # Retrieve the category from the form data
        message = data["message"]

        subject = f"New Form Submission - Category: {category}"  # Include the category in the subject

        msg = Message(subject, recipients=['recipient@example.com'], sender=email)
        msg.body = f"From: {name}\nEmail: {email}\nCategory: {category}\n\n{message}"


# This redirects to the thankyou.html page after submitting the form
# also redirects to the error.html page after something went wrong
        try:
            mail.send(msg)
            return redirect('/thankyou.html')
        except Exception as e:
            print(e)
            return redirect('/error.html')
    else:
        return redirect('/error.html')


if __name__ == '__main__':
    app.run()

### Add to WSGI file for flask mail:
#import sys
#
## Add your app's directory to the Python path
#path = '/home/your_username/your_app_directory'
#if path not in sys.path:
#    sys.path.append(path)
#
## Set up the Flask app
#from your_app_file import app as application


# $ pip freeze > requirements.txt
# ^^^ creates a text file that gives pythonanywhere info on which packages are needed