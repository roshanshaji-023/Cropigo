from flask import Flask,Blueprint,render_template,request,url_for,redirect
from database import *
user=Blueprint('user',__name__) #creating blueprint for user dashboard page@public.route('/userdashboard')
@user.route('/userdashboard')
def userdashboard():

    return render_template('userdashboard.html')