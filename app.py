from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgred@localhost/height_collector' #connect to the postgresql app to the database with an address of: username@password.localhost/name_of_database (of postresql)
db=SQLAlchemy(app) #sqlalchemy object

class Data(db.Model): #sqlalchemy connect to the database
    __tablename__="data" #create the table in database
    id=db.Column(db.Integer, primary_key=True) #id column as primary key
    email_=db.Column(db.String(120),unique=True) #email column with a maximum limit of characters of 120, string type
    height_=db.Column(db.Integer) #height column with a data type as integer


    def __init__(self,email_,height_): #initialize the table
        self.email=email_
        self.height=height_

#to commit the table in the database, go to terminal and enter the python shell and write: from app (python file) import db and after d.create_all() and it will create the tables in the database

@app.route("/")

def index():
    return render_template("index.html")

@app.route("/success", methods=['POST']) #decorator to access the url /success

def success():
    if request.method == 'POST':
        email=request.form["email_address"]
        height=request.form["height"]

        return render_template("success.html")

if __name__ == '__main__':
    app.debug=True
    app.run()
