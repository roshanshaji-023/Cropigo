from flask import Flask,Blueprint,render_template,request,session,url_for,redirect
from database import *
import re
public=Blueprint('public',__name__) #creating blueprint for public page


@public.route('/')
def home():

    return render_template('home.html')

@public.route('/about')
def about():
    return render_template('about.html')

@public.route('/login',methods=['get','post'])
def login():
    if 'login' in request.form:
        a=request.form['username']
        b=request.form['password']
        print(a,b)
        q="select * from login where user_name='%s' and password='%s'"%(a,b)
        res=select(q)
        if res:
            print(res)
            login_id=res[0]['login_id']
            if res[0]['user_type']=="admin":#for admin login
                session['loggedin'] = True
                session['name'] = res[0]['user_name']
                
                return redirect(url_for('admin.adminhome'))
            elif res[0]['user_type']=="user": #for user login
                
                p="select * from user where user_name='%s' and login_id='%s'"%(a,login_id)
                res1=select(p)
                uname=res[0]['user_name']
                upassword=res[0]['password']
                

                session['loggedin'] = True
                session['name'] =res1[0]['full_name']
                session['loginid']=res[0]['login_id']
                session['userid']=res1[0]['user_id']
                
                if uname==a and upassword==b:
                    return redirect(url_for('user.userdashboard'))
        else:
            message="Error | Invalid username or password!"
            return render_template("login.html",message=message)
    return render_template('login.html')

# Make function for logout session
@public.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    session.pop('name', None)
    return redirect('/')

@public.route('/signup',methods=['get','post'])#/signup is name given for route
def signup():
    if 'signup' in request.form:
        name=request.form['name']
        email=request.form['email']
        username=request.form['username']
        password=request.form['password']
        place=request.form['place']
        phone_number=request.form['phone_number']

        querry="select * from login where user_name='%s'"%(username)
        result=select(querry)
        if result:
            message="Account Already Exists!"
            return render_template('signup.html',message=message)
        else:
            q="insert into login(user_type,user_name,password) values('user','%s','%s')"%(username,password)
            res=insert(q)
            q="insert into user(login_id,full_name,place,phone_number,email_id,user_name) values('%s','%s','%s','%s','%s','%s')"%(res,name,place,phone_number,email,username)
            insert(q)
            message="Account Created Succesfully!!"
            return render_template('signup.html',message=message)
        
    return render_template('signup.html')



