from flask import Flask,Blueprint,render_template,request

admin=Blueprint('admin',__name__) #creating blueprint for admin page

@admin.route('/admin',methods=['get','post'])
def adminhome():
    if 'product' in request.form:
        name=request.form['productname']
        type=request.form['type']
        print(name,type)
    return render_template('adminhome.html')

@admin.route('/adminlogin',methods=['get','post'])
def adminlogin():
    if 'login' in request.form:
        name=request.form['username']
        type=request.form['password']
        print(name,type)
    return render_template('adminlogin.html')





