from flask import Flask,Blueprint,render_template,request, session,url_for,redirect
from datetime import date
from database import *
# Importing libraries
from sklearn.ensemble import RandomForestClassifier
import pickle
import pandas as pd
import numpy as np
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



#crop prediction dashboard to select two ways(4/4/23)
@user.route('/croppredict',methods=['get','post'])
def croppredict():
    return render_template('croppredict.html')

#crop prediction using village name
@user.route('/village',methods=['get','post'])
def village():
    if 'crop-predict' in request.form:
        villagename=request.form.get('inputVillage')
        print(villagename)

        # load the village dataset
        village_data= pd.read_csv("static\cropigovillage.csv")
        
        #take values from csv
        nitrogen=village_data[village_data['VILLAGES'] == villagename]['N'].values[0]
        phosphorus=village_data[village_data['VILLAGES'] == villagename]['P'].values[0]
        potassium=village_data[village_data['VILLAGES'] == villagename]['K'].values[0]
        temperature=village_data[village_data['VILLAGES'] == villagename]['temperature'].values[0]
        humidity=village_data[village_data['VILLAGES'] ==villagename]['humidity'].values[0]
        ph=village_data[village_data['VILLAGES'] == villagename]['ph'].values[0]
        rainfall=village_data[village_data['VILLAGES'] == villagename]['rainfall'].values[0]

        RF_pkl_filename = 'static\RandomForest.pkl'
        # Open the file to load pkl file

        with  open(RF_pkl_filename, 'rb') as RF_Model_pkl:
            RF=pickle.load(RF_Model_pkl)
        data = np.array([[nitrogen,phosphorus, potassium, temperature, humidity, ph, rainfall]])
        prediction = RF.predict(data)
        print(prediction)
        crop=prediction[0]
        print(crop)
        #adding imagpath
        con=''.join(prediction)
        image=con+'.jpg'
        # load the fertilizer and season dataset
        fertilizer_season= pd.read_csv('static\cropfertilizer&season.csv')

        fertilizer = fertilizer_season[fertilizer_season['Crop'] == crop]['Fertilizer'].values[0]
        season = fertilizer_season[fertilizer_season['Crop'] == crop]['Season'].values[0]
           
            
        return render_template('/resultpage.html',crop=crop,fertilizer=fertilizer,season=season,path=image)
    return render_template('village.html')


#general crop prediction by user inputs manually 
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
            crop=prediction[0]
            print(crop)
            #adding imagpath
            con=''.join(prediction)
            image=con+'.jpg'
            # load the fertilizer and season dataset
            fertilizer_season= pd.read_csv('static\cropfertilizer&season.csv')

            fertilizer = fertilizer_season[fertilizer_season['Crop'] == crop]['Fertilizer'].values[0]
            season = fertilizer_season[fertilizer_season['Crop'] == crop]['Season'].values[0]
           
            
            return render_template('/resultpage.html',crop=crop,fertilizer=fertilizer,season=season,path=image)
        return render_template('/gencropprediction.html')

#result of crop prediction by user inputs manually 
@user.route('/resultpage',methods=['get','post'])
def resultpage():
    return render_template('/resultpage.html')

    