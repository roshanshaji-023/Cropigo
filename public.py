from flask import Flask,Blueprint,render_template,request,session,url_for,redirect
from database import *
import re
public=Blueprint('public',__name__) #creating blueprint for public page


@public.route('/')
def home():

    return render_template('home.html')

@public.route('/login',methods=['get','post'])
def login():
    if 'login' in request.form:
        a=request.form['username']
        b=request.form['password']
        print(a,b)
        q="select * from user_login where user_name='%s' and password='%s'"%(a,b)
        res=select(q)
        if res:
            if res[0]['user_type']=="admin":
                return redirect(url_for('admin.adminhome'))
            elif res[0]['user_type']=="user":
                uname=res[0]['user_name']
                upassword=res[0]['password']
                session['loggedin'] = True
                session['userid'] = res[0]['id']
                session['name'] = res[0]['full_name']
                session['email'] = res[0]['email_id']
                if uname==a and upassword==b:
                    return redirect(url_for('user.userdashboard'))
    return render_template('login.html')

@public.route('/signup',methods=['get','post'])#/signup is name given for route
def signup():
    if 'signup' in request.form:
        n=request.form['name']
        e=request.form['email']
        q=request.form['username']
        r=request.form['password']
        print(n,e,q,r)
        q="insert into user_login(user_type,user_name,password,full_name,email_id) values('user','%s','%s','%s','%s')"%(q,r,n,e)
        res=insert(q)
        
    return render_template('signup.html')



