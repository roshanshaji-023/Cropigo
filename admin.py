from flask import *
from database import *

admin=Blueprint('admin',__name__) #creating blueprint for admin page


@admin.route('/admin',methods=['get','post'])
def adminhome():
    if 'user-search' in request.form:
        name=request.form['user-search-name']
        type='user'
        q="select * from user_login where user_name='%s' and user_type='%s'"%(name,type)
        if name=='all':
            q="select * from user_login"
        res=select(q)
        print(res)
        return render_template('adminhome.html',data=res)
    return render_template('adminhome.html')







