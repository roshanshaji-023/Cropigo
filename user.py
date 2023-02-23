from flask import Flask,Blueprint,render_template,request, session,url_for,redirect
from datetime import date
from database import *
user=Blueprint('user',__name__) #creating blueprint for user dashboard page@public.route('/userdashboard')
@user.route('/userdashboard')
def userdashboard():

    return render_template('userdashboard.html')

@user.route('/usercomplaints',methods=['get','post'])
def usercomplaints():
    if 'complaint-submit' in request.form:
        complaint=request.form['complaint-data']
        today=date.today() #for date
        querry="insert into complaint(user_id,complaint,reply,date) values('%s','%s','pending','%s')"%(session['userid'],complaint,today)
        insert(querry)
        
        #check if a button is clicked
    if 'reply-check' in request.form:
           
        q="select complaint,date,reply from complaint WHERE user_id='%s'"%(session['userid'])
        res=select(q)
        print(res)
        return render_template('usercomplaints.html',data=res)
    return render_template('usercomplaints.html')
    