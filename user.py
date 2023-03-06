from flask import Flask,Blueprint,render_template,request, session,url_for,redirect
from datetime import date
from database import *
# Importing libraries
from sklearn.ensemble import RandomForestClassifier
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn import tree
import warnings
warnings.filterwarnings('ignore')

user=Blueprint('user',__name__) #creating blueprint for user dashboard page@public.route('/userdashboard')

@user.route('/userdashboard',methods=['get','post'])
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
    
@user.route('/gencropprediction',methods=['get','post'])
def gencropprediction():
        if 'crop-predict' in request.form:
            nitrogen=request.form.get('nitrogen',type=int)
            phosphorus=request.form.get('phosphorus',type=int)
            potassium=request.form.get('potassium',type=int)
            temperature=request.form.get('temperature',type=float)
            humidity=request.form.get('humidity',type=float)
            ph=request.form.get('ph',type=float)
            rainfall=request.form.get('rainfall',type=float)
            
            # Dump the trained Naive Bayes classifier with Pickle
            RF_pkl_filename = 'static\RandomForest.pkl'
            # Open the file to load pkl file

            with  open(RF_pkl_filename, 'rb') as RF_Model_pkl:
                RF=pickle.load(RF_Model_pkl)
            data = np.array([[nitrogen,phosphorus, potassium, temperature, humidity, ph, rainfall]])
            prediction = RF.predict(data)
            print(prediction)
            result="The best crop to cultivate predicted is %s"%prediction[0]
            print(result)
            return render_template('/gencropprediction.html',data=result)
        return render_template('/gencropprediction.html')
    