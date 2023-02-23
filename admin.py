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
    if 'complaint-check' in request.form:
        c="select * from complaint where reply='pending'"
        cmp=select(c)
        return render_template('adminhome.html',complaint_data=cmp)
    
    if 'reply' in request.form:
        reply=request.form['reply-message']
        cid=request.form['complaintid']
        q="update complaint SET reply='%s' WHERE complaint_id='%s'"%(reply,cid)
        update(q)

    
    return render_template('adminhome.html')







