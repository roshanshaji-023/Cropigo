from flask import *
from database import *

admin=Blueprint('admin',__name__) #creating blueprint for admin page

@admin.route('/admin',methods=['get','post'])
def adminhome():
    if 'product' in request.form:
        name=request.form['productname']
        type=request.form['type']
        print(name,type)
    return render_template('adminhome.html')







