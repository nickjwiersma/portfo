


# create the virtual envoirment using $ Python3 -m venv "name of directory" | in this case $ Python3 -m venv web_server
# ^^^ this creates the neccesary files for the python virtual envoirment
# activate the server by $ . "folder name"/bin/activate | in this cane $ pop
# first run $ export FLASK_APP=server.py
# to run in debug mode $ flask --app server.py run --debug

# Using templates to import to the website
# importing flask
# requesting info in a submitted form
# redirecting after submitting
from flask import Flask, render_template, url_for, request, redirect

# import CSV to write into csv files
import csv
app = Flask(__name__)


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
    with open('database.csv', mode='a') as database2:
        name = data["name"]
        email = data["email"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name, email, message])

# This redirects to the thankyou.html page after submitting the form
# also redirects to the error.html page after something went wrong
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('/thankyou.html')
    else:
        return redirect('/error.html')
    
# $ pip freeze > requirements.txt
# ^^^ creates a text file that gives pythonanywhere onfo on which packages are needed