from flask import Flask, render_template, request, redirect, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from today_date import today_date
from datetime import datetime
import requests
import json
import logging
import sys
import os
import sqlite3
from email1 import send_simple_message, welcome_message
import random


app = Flask(__name__, static_url_path="", static_folder="static")
#app._static_folder = "/flaskenv/static"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    age = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(20),unique=True, nullable=False)
    email = db.Column(db.String(60),unique=True, nullable=False)
    district = db.Column(db.String(50), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    avail = db.Column(db.Boolean, nullable=False)
    data = db.Column(db.String(50),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    response = ''
    age_limit=0
    if request.method=='POST':
        name = request.form['name']
        age = request.form['age']
        phone = request.form['phone']
        email = request.form['email']
        district =request.form['district']
        pincode  =request.form['pincode']
        #todo = Todo(name=name, phone=phone,age = age, email=email,district= district,pincode=pincode,data="NA")
        
        ##########api request########
        #print(pincode)
        # print(type(pincode))
        params = (
            ('pincode', pincode),
            ('date', today_date()),
        )
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        }
        
        response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin', headers=headers, params=params)
        print(response.text)
        response = response.text  # RESPONSE TEXT WITHOUT STATUS CODE
        dic=json.loads(response)
        if("errorCode" in dic):
            return "<center><h2> Error in data you submitted! </h2></center>"
        vaccine18 = 0
        vaccine45 = 0
        response = dic
        ##### scraping data from Api response ####
        centre = dic["centers"]
        # print(type(centre))
        for li in centre:
            # print(type(li))
            print("Centre Name:", li['name'], "\nCentre Address:", li['address'], li['block_name'], li['district_name'], li['pincode'],"\nFee Type:",li['fee_type']) #, li["'sessions'"][0]['date'], li["'sessions'"][0]['date'], li["'sessions'"][0]['available_capacity'], li["'sessions'"][0]['min_age_limit'])
            # print(li[""'sessions'""])
            print("Date        Availability    Minimum Age   Vaccine")
            for session in li["sessions"]:
                print(session['date'],"      ", session['available_capacity'],"        ", session['min_age_limit'],"            ", session['vaccine'])
                if(session['min_age_limit'] < 45):
                    vaccine18=vaccine18+session['available_capacity']
                else: 
                    vaccine45= vaccine45+session['available_capacity']   
                age_limit = session['min_age_limit']  
        print("Vacc 18: " + str(vaccine18) + " " + str(vaccine45))
        #avail=bool(1)
        # print("\n",vaccine18, "\n")
        # print(vaccine45,'\n')
        if( (  int(age) < 45  and vaccine18 > 0 ) or (int(age) > 44 and vaccine45 > 0)  ):
            avail=bool(1)
            send_simple_message(email,name, str(pincode))
        else:
            avail=bool(0)
            welcome_message(email, name)


        todo = Todo(name=name, phone=phone,age = age, email=email,district= district,pincode=pincode,data="NA",avail= avail)
        if len(centre)==0:                    # check is response if empty/ no centre available
            response={"centers":-1}
        try:
            db.session.add(todo)
            db.session.commit()
        except:
            response= {"centers":-300}   
        
    # allTodo = Todo.query.all() 
    #return render_template('index1.html', allTodo=response) #for check
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)
    return render_template('index.html', allTodo=response) # response in json


@app.route('/mail_16575/<key>')
def mail(key):
    if (key == "538508ea-b3c5-11eb-8529-0242ac130003"):
        user = Todo.query.filter_by(avail=0).all()
        age_limit=0
        for user1 in user:
            params = (
                ('pincode', user1.pincode),
                ('date', today_date()),
            )
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            }
            response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin', headers=headers, params=params)
            response=response.text
            dic = json.loads(response)   #generate error if no response from server/api
            response = dic
            centre = dic["centers"]
            vaccine18 =0
            vaccine45=0
            for li in centre:
                # print(type(li))
                print("Centre Name:", li['name'], "\nCentre Address:", li['address'], li['block_name'], li['district_name'], li['pincode'],"\nFee Type:",li['fee_type']) #, li["'sessions'"][0]['date'], li["'sessions'"][0]['date'], li["'sessions'"][0]['available_capacity'], li["'sessions'"][0]['min_age_limit'])
                # print(li[""'sessions'""])
                print("Date        Availability    Minimum Age   Vaccine")
                for session in li["sessions"]:
                    print(session['date'],"      ", session['available_capacity'],"        ", session['min_age_limit'],"            ", session['vaccine'])
                    if(session['min_age_limit'] < 45):
                        vaccine18=vaccine18+session['available_capacity']
                    else: 
                        vaccine45= vaccine45+session['available_capacity']   
                    age_limit = session['min_age_limit']     
            
            if((  int(user1.age) < 45  and vaccine18 > 0 ) or (int(user1.age) > 44 and vaccine45 > 0)  ):
                avail=bool(1)
            else:
                avail=bool(0)
            if(avail == 1):
                #send email to api 
                # email code
                #db.session.delete(sno=user1.sno)
                send_simple_message(user1.email, user1.name, str(user1.pincode))
                avail_update = Todo.query.filter_by(email=user1.email).first()
                avail_update.avail = bool(1)
                db.session.commit()
                print("mail sent")
            else:
                print ("still not available")
            
        return render_template('dbout.html',user=user)
    else:
        return "<center><h1>Sorry Page doesn't exist</h1></center>"



@app.route('/mail_random/<key>')
def mail_random(key):
    if (key == "dec55b5e-b414-11eb-8529-0242ac130003"):
        user = Todo.query.filter_by(avail=0).all()
        # print("user: " + str(type(user)))
        random.shuffle(user)
        age_limit=0
        for user1 in user:
            params = (
                ('pincode', user1.pincode),
                ('date', today_date()),
            )
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
            }
            response = requests.get('https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin', headers=headers, params=params)
            response=response.text
            dic = json.loads(response)   #generate error if no response from server/api
            response = dic
            centre = dic["centers"]
            vaccine18 =0
            vaccine45=0
            for li in centre:
                # print(type(li))
                print("Centre Name:", li['name'], "\nCentre Address:", li['address'], li['block_name'], li['district_name'], li['pincode'],"\nFee Type:",li['fee_type']) #, li["'sessions'"][0]['date'], li["'sessions'"][0]['date'], li["'sessions'"][0]['available_capacity'], li["'sessions'"][0]['min_age_limit'])
                # print(li[""'sessions'""])
                print("Date        Availability    Minimum Age   Vaccine")
                for session in li["sessions"]:
                    print(session['date'],"      ", session['available_capacity'],"        ", session['min_age_limit'],"            ", session['vaccine'])
                    if(session['min_age_limit'] < 45):
                        vaccine18=vaccine18+session['available_capacity']
                    else: 
                        vaccine45= vaccine45+session['available_capacity']   
                    age_limit = session['min_age_limit']     
            if((  int(user1.age) < 45  and vaccine18 > 0 ) or (int(user1.age) > 44 and vaccine45 > 0)  ):
                avail=bool(1)
            else:
                avail=bool(0)
            if(avail == 1):
                #send email to api 
                # email code
                #db.session.delete(sno=user1.sno)
                send_simple_message(user1.email, user1.name, str(user1.pincode))
                avail_update = Todo.query.filter_by(email=user1.email).first()
                avail_update.avail = bool(1)
                db.session.commit()
                print("mail sent")
            else:
                print ("still not available")
            
        return render_template('dbout.html',user=user)
    else:
        return "<center><h1>Sorry Page doesn't exist</h1></center>"

#Viewing all data
@app.route('/all_17569/<key>')
def mail_all(key):
    if (key == "499fb411-8fc1-47c6-9697-f6cf122500a2"):
        user = Todo.query.all()
        # print(user)
            
        return render_template('dbout.html',user=user)
    else:
        return "<center><h1>Sorry Page doesn't exist</h1></center>"

#about route
@app.route('/about.html')
def about():
    return render_template('about.html')




port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
    app.run(debug=True, port=port)

# if __name__ == "__main__": 
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)    
