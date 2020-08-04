from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgred@localhost/height_collector' #connect to the local postgresql app to the database with an address of: username@password.localhost/name_of_database (of postresql)
app.config['SQLALCHEMY_DATABASE_URI']='postgres://ubweqwxgrqgmpj:1a450c945e3928503aa5bc8ca25b2d93034e38030b50393ea0eed0e61d8426d5@ec2-34-237-89-96.compute-1.amazonaws.com:5432/d3vhdu0g1o1l5b?sslmode=require'
db=SQLAlchemy(app) #sqlalchemy object

class Data(db.Model): #sqlalchemy connect to the database
    __tablename__="data" #create the table in database
    id=db.Column(db.Integer, primary_key=True) #id column as primary key
    email_=db.Column(db.String(120),unique=True) #email column with a maximum limit of characters of 120, string type
    height_=db.Column(db.Integer) #height column with a data type as integer


    def __init__(self,email_,height_): #initialize the table
        self.email_=email_
        self.height_=height_

#to commit the table in the database, go to terminal and enter the python shell and write: from app (python file) import db and after d.create_all() and it will create the tables in the database

@app.route("/")

def index():
    return render_template("index.html")

@app.route("/success", methods=['POST']) #decorator to access the url /success

def success():
    if request.method == 'POST':
        email=request.form["email_address"]
        height=request.form["height"]

        if db.session.query(Data).filter(Data.email_==email).count() == 0: #filtering the column if the email is already in the database
            data=Data(email,height) #initiate the class and the values will be recognise by the sqlalchemy add method
            db.session.add(data) #add the values to the database
            db.session.commit() #commit the changes to the database
            avarege_height=db.session.query(func.avg(Data.height_)).scalar()
            avarege_height=round(avarege_height,1)
            count=db.session.query(Data.height_).count()
            send_email(email, height,avarege_height, count) #use the send_email file to access to the credential of the email address used to send email to the user and the avarege_height

            return render_template("success.html")
    return render_template("index.html", text="Seems this email address was already used!")

if __name__ == '__main__':

    app.debug=True
    app.run()
