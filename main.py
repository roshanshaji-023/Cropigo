from flask import Flask
from public import public
from admin import admin
from user import user

app=Flask(__name__) #object for flask
app.secret_key = 'cropigo'

app.register_blueprint(public) #registering blueprint of public with main
app.register_blueprint(admin)
app.register_blueprint(user)

app.run(debug=True)#to run app