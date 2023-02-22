from flask import *
from database import *

admin=Blueprint('admin',__name__) #creating blueprint for admin page


@admin.route('/admin',methods=['get','post'])
def adminhome():
    if 'user-search' in request.form:
        name=request.form['user-search-name']
        
        q="select * from user where user_name='%s'"%(name)
        if name=='all':
            q="select * from user"
        res=select(q)
        print(res)
        return render_template('adminhome.html',data=res)
    return render_template('adminhome.html')







