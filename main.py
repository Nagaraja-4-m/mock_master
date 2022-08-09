from flask import *
from admin import *
from student import *
from accounts import *
from datetime import timedelta

app=Flask(__name__)
app.secret_key="GJAdf33dagsvdghadasasdasd4632"
app.permanent_session_lifetime=timedelta(days=24)

otp=""

#welcome  page
@app.route('/')
def welcome():
    return render_template('index.html')


#admin---------------------------------

#admin dashboard
@app.route('/admin/dashboard/')
def admin():
    if 'logged_admin' in session:
        new_queries=un_answered_queries()
        subs=total_subjects()
        stds=total_students()
        return render_template('/admin/admin_dashboard.html',queries=new_queries,subs=subs,stds=stds)
    else:
        return redirect(url_for('admin_login'))    

 

@app.route('/admin/dashboard/accounts')
def account_view():
    if 'logged_admin' in session:
        admin_details=get_admin_details("21ADMN_1")
        return render_template('/admin/admin_account_view.html',admin_details=admin_details)
    else:
        return redirect(url_for('admin_login'))    

'''#change password
@app.route('/admin/dashboard/<email>')
def account_chpass(email):
    otp=send_otp(email)
    if request.method=='POST':
        otp_obt=request.form['otp']
        if(int(otp)==int(otp_obt)):
            return "True"
        else:
            return "False"
    return render_template('/admin/admin_account_password_change.html')
'''

@app.route('/admin',methods=['POST','GET'])
def admin_login():
    if request.method=='POST':
        email=request.form['admin_email']
        password=request.form['admin_password']
        status=login_admin(email,password)
        if(status):
            session['logged_admin']=email
            return redirect(url_for('admin'))
        else:
            return render_template('/admin/admin_login.html',status="Invalid details")
    
    elif 'logged_admin' in session:
        return redirect(url_for('admin'))
    else:
        return render_template('/admin/admin_login.html')      


@app.route('/admin/logout')
def admin_logout():
    if 'logged_admin' in session:
        session.pop('logged_admin',None)
        return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))      
    


#acount edit
@app.route('/admin/dashboard/edit',methods=['POST','GET'])
def account_edit():
    if 'logged_admin' in session:
        admin_details=get_admin_details("21ADMN_1")
        if request.method == 'POST':
            new_details=[]
            new_details.append(request.form['admin_name'])
            new_details.append(request.form['admin_mobile'])
            new_details.append(request.form['admin_email'])
            admin_id=admin_details[0]
            update_status=update_admin(admin_id,new_details)
            if(update_status):
                return redirect(url_for('account_view'))
            else:
                return "Unable to update the details"
        return render_template('/admin/admin_account_edit.html',admin_details=admin_details)
    else:
        return redirect(url_for('admin_login'))      





#question
@app.route('/admin/dashboard/q')
def question():
    if 'logged_admin' in session:
        return render_template('/admin/admin_question.html')
    else:
        return redirect(url_for('admin_login'))      


#question add
@app.route('/admin/dashboard/qa', methods=['POST','GET'])
def question_add():
    if 'logged_admin' in session:
        if request.method == 'POST':
            question_details=[]
            question_details.append(request.form['subject_id'])
            question_details.append(request.form['question_id'])
            question_details.append(request.form['question'])
            question_details.append(request.form['option_1'])
            question_details.append(request.form['option_2'])
            question_details.append(request.form['option_3'])
            question_details.append(request.form['option_4'])
            question_details.append(request.form['correct_option'])
            question_details.append(request.form['solution'])
            question_add_status=add_question(question_details)
            if(question_add_status):
                return render_template('/admin/admin_question_add.html',subjects=get_subjectNames(),status="Question added successfuly")
            else:
                return render_template('/admin/admin_question_add.html',subjects=get_subjectNames(),status="Failed to add question details")
                
        return render_template('/admin/admin_question_add.html',subjects=get_subjectNames())
    else:
        return redirect(url_for('admin_login'))      



#question view
@app.route('/admin/dashboard/qv', methods=['POST','GET'])
def question_view():
    if 'logged_admin' in session:
        if request.method =='POST':
            sub_id=request.form['subject_name']
            questions=get_Questions(sub_id)
            if(questions==False):
                return "Failed to get"
            else:
                return render_template('/admin/admin_question_view.html',subjects=get_subjectNames(),question_details=questions)

        return render_template('/admin/admin_question_view.html',subjects=get_subjectNames())
    else:
        return redirect(url_for('admin_login'))      



#question delete
@app.route('/admin/dashboard/qd<q_id>')
def question_delete(q_id):
    if 'logged_admin' in session:
        del_status=delete_question(q_id)
        if(del_status):
            return redirect(url_for('question_view'))
        else:
            return "Unable to delete"
    else:
        return redirect(url_for('admin_login'))      

    
#question update
@app.route('/admin/dashboard/qu<q_id>',methods=['POST','GET'])
def question_update(q_id):
    if 'logged_admin' in session:
        if request.method =='POST':
            new_details=[]
            new_details.append(request.form['question_id'])
            new_details.append(request.form['question'])
            new_details.append(request.form['option_1'])
            new_details.append(request.form['option_2'])
            new_details.append(request.form['option_3'])
            new_details.append(request.form['option_4'])
            new_details.append(request.form['correct_option'])
            new_details.append(request.form['solution'])
            update_status=update_question(q_id,new_details)
            if(update_status):
                return redirect(url_for('question_view'))
            else:
                return "Not able to Update "
    else:
        return redirect(url_for('admin_login'))      

#question edit
@app.route('/admin/dashboard/qe<q_id>')
def question_edit(q_id):
    if 'logged_admin' in session:
        q_details=qID_to_qDetails(q_id)
        return render_template('/admin/admin_question_edit.html',q_details=q_details)
    else:
        return redirect(url_for('admin_login'))      
 




#subject 
@app.route('/admin/dashboard/s')
def subject():
    if 'logged_admin' in session:
        return render_template('/admin/admin_subject.html')
    else:
        return redirect(url_for('admin_login'))      



#subject  add
@app.route('/admin/dashboard/sa' , methods=['POST','GET'])
def subject_add():
    if 'logged_admin' in session:
        if request.method =='POST':
            sub_name=request.form['subject_name']
            sub_id=request.form['subject_id']
            sub_category=request.form['subject_category']
            sub_desc=request.form['subject_description']
            subject_add_status=add_subject(sub_id,sub_name,sub_category, sub_desc)
            if(subject_add_status==None):
                return render_template('/admin/admin_subject_add.html',status="Subject ID Already exists")
            elif(subject_add_status==0):
                return render_template('/admin/admin_subject_add.html',status="Unable to add subject details")
            elif(subject_add_status==1):
                return render_template('/admin/admin_subject_add.html',status="Subject details added succesfuly")
        return render_template('/admin/admin_subject_add.html')
    else:
        return redirect(url_for('admin_login'))      


#subject delete
@app.route('/admin/dashboard/sd<sub_id>')
def subject_delete(sub_id):
    if 'logged_admin' in session:
        del_status=delete_subject(sub_id)
        if(del_status):
            return redirect(url_for('subject_view'))
        else:
            return "Unable to delete"
    else:
        return redirect(url_for('admin_login'))      
 

 #subject  view
@app.route('/admin/dashboard/sv')
def subject_view():
    if 'logged_admin' in session:
        subject_details,no_of_questions=view_subject()
        #return coll_list
        return render_template('/admin/admin_subject_view.html',sub_list=subject_details,No_Questions=no_of_questions)
    else:
        return redirect(url_for('admin_login'))      


#subject edit
@app.route('/admin/dashboard/se<sub_id>')
def subject_edit(sub_id):
    if 'logged_admin' in session:
        sub_details=subID_to_subDetails(sub_id)
        return render_template('/admin/admin_subject_edit.html',subject_details=sub_details)
    else:
        return redirect(url_for('admin_login'))      


#subject update
@app.route('/admin/dashboard/su<sub_id>',methods=['POST','GET'])
def subject_update(sub_id):
    if 'logged_admin' in session:    
        if request.method =='POST':
            new_details=[]
            new_details.append(request.form['subject_id'])
            new_details.append(request.form['subject_name'])
            new_details.append(request.form['subject_category'])
            new_details.append(request.form['subject_description'])
            update_status=update_subject(sub_id,new_details)
            if(update_status):
                return redirect(url_for('subject_view'))
            else:
                return "Not able to Update "

        #return redirect(url_for('subject_view'))
    else:
        return redirect(url_for('admin_login'))      

#students 
@app.route('/admin/dashboard/students')
def student_view():
    if 'logged_admin' in session:
        student_details=get_students()
        return render_template('/admin/admin_student_view.html',std_det=student_details)
    else:
        return redirect(url_for('admin_login'))      
#students performance
@app.route('/admin/dashboard/performance_<sid>')
def student_performances(sid):
    if 'logged_admin' in session:
        profile_details=get_user_details(sid)
        student_performace=exract_user_performace(profile_details[4])
        return render_template('/admin/admin_student_view_performace.html',student_performace=student_performace)
    else:
        return redirect(url_for('admin_login'))      



@app.route('/admin/dashboard/student<u_email>',methods=['POST','GET'])
def student_email(u_email):
    if 'logged_admin' in session:
        if request.method=='POST':
            to=request.form['email_to']
            subject=request.form['email_subject']
            msg=request.form['email_body']
            status=send_email(to,subject,msg)
            if(status):
                return redirect(url_for('student_view'))
            else:
                return "Email not sent"
        return render_template('/admin/admin_student_push_email.html',email=u_email)
    else:
        return redirect(url_for('admin_login'))      


#student view




#feedback
@app.route('/admin/dashboard/querys',methods=['POST','GET'])
def querys():
    if 'logged_admin' in session:
        queries=get_all_queries()
        if(queries):
            return render_template('/admin/admin_query.html',queries=queries)
        else:
            return render_template('/admin/admin_query.html') 
    else:
        return redirect(url_for('admin_login'))      

#admin ends
@app.route('/admin/dashboard/<email>_<sub>',methods=['POST','GET'])
def update_query(email,sub):
    if 'logged_admin' in session:
        if request.method=='POST':
            replay=request.form['replay']
            if(len(replay)>1):
                query_update(email,sub,replay)
        return redirect(url_for('querys'))
    else:
        return redirect(url_for('admin_login'))      

# admin -------------------------------------



#student -------------------------------------
@app.route('/student/dashboard')
def student_dashboard():
    if 'logged_email' in session:
        name=get_user_details(session['logged_email'])
        name=name[0]
        return render_template('/student/student_dashboard.html',cats=get_subject_categories(),name=name)
    else:
        return redirect(url_for('welcome'))

@app.route('/student/<sub_cat>')
def student_subjects(sub_cat):
    if 'logged_email' in session:
        return render_template('/student/student_subjects.html',subs=get_subjects(sub_cat))
    else:
       return redirect(url_for('welcome'))  

@app.route('/student/test_instructions_<sub_id>')
def student_test_instructions(sub_id):
    if 'logged_email' in session:
        questions=get_Questions(sub_id)
        total=len(questions)
        return render_template('/student/student_test_instruction.html',sub_details=subID_to_subDetails(sub_id),total=total)
    else:
       return redirect(url_for('welcome'))  

@app.route('/student/Test_<sub_id>')
def student_test(sub_id):
    if 'logged_email' in session:
        questions=get_Questions(sub_id)
        total=len(questions)
        return render_template('/student/student_test.html',questions=questions,subject_name=subID_to_subDetails(sub_id),total=total)
    else:
       return redirect(url_for('welcome'))  


@app.route('/student/Test_Results_<sub_id>',methods=['POST','GET'])
def student_test_results(sub_id):
    if 'logged_email' in session:
        questions=get_Questions(sub_id)
        if request.method=='POST':
            response=[]
            for i in questions:
                temp=[]
                temp.append(i[2])
                temp.append(i[8])
                temp.append(request.form[i[2]])
                response.append(temp)
            result,t_correct=get_result(sub_id,session['logged_email'],response)
            return render_template('/student/student_result.html',res=response,correct=t_correct,questions=questions)
    else:
       return redirect(url_for('welcome'))  


@app.route('/student/profile')
def student_profile():
    if 'logged_email' in session:
        profile_details=get_user_details(session['logged_email'])
        return render_template('/student/student_profile.html',details=profile_details)
    else:
       return redirect(url_for('welcome'))  


@app.route('/student/profileEdit')
def student_profile_edit():
    if 'logged_email' in session:
        return render_template('/student/student_profile_edit.html')
    else:
       return redirect(url_for('welcome'))  


@app.route('/student/help',methods=['POST','GET'])
def student_help():
    if 'logged_email' in session:
        if request.method=='POST':
            sub=request.form['subject']
            qry=request.form['query']
            status=send_query(session['logged_email'],sub,qry)
            return render_template('/student/student_help.html',status="Query sent successfuly.")
        return render_template('/student/student_help.html')
    else:
       return redirect(url_for('welcome'))  


@app.route('/student/replays',methods=['POST','GET'])
def student_help_replay():
    if 'logged_email' in session:
        replays=get_replays(session['logged_email'])
        if request.method=='POST':
            sub=request.form['q_subject']
            for i in replays:
                if(sub in i):
                    return render_template('/student/student_help_replay.html',selected_query=i,replay=replays)
        return render_template('/student/student_help_replay.html',replay=replays)
    else:
       return redirect(url_for('welcome'))  

@app.route('/student/performance')
def student_performance():
    if 'logged_email' in session:
        profile_details=get_user_details(session['logged_email'])
        user_performace=exract_user_performace(profile_details[4])
        #user_performace.insert(0,['Subject', 'Correct Answers', 'Total Questions'])
        return render_template('/student/student_result_grpahical.html',user_test_data=user_performace)
    else:
       return redirect(url_for('welcome'))  
#student ------------------------------------



#authentication and registration......................

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        registration_details=[]
        registration_details.append(request.form['full_name'])
        registration_details.append(request.form['gender'])
        registration_details.append(request.form['mobile_number'])
        registration_details.append(request.form['email'])
        registration_details.append(request.form['password'])
        cpass=request.form['cpassword']
        if(registration_details[4]==cpass):
            if(not check_email_existance(registration_details[3])):
                if(user_register(registration_details)):
                    return render_template('/register.html',r_status="Your registration was successful.")
                else:
                    return render_template('/register.html',r_status="Unable to complete yout registration,try again... ")
            else:
                return render_template('/register.html',r_status="Email ID already exists.")
        else:
            return render_template('/register.html',r_status="Password and confirm password mismatched.")
            
    return render_template('/register.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        session.permanent=True
        email_id=request.form['email']
        password=request.form['password']
        if(user_login(email_id, password)):
            session['logged_email']=email_id
            return redirect(url_for('student_dashboard'))
        else: 
            return render_template('/login.html',status="Invalid details")
    elif 'logged_email' in session:
        return redirect(url_for('student_dashboard'))
    else:
        return render_template('/login.html')

@app.route('/logout')
def logout():
    session.pop('logged_email',None)
    return redirect(url_for('welcome'))

@app.route('/forgot_password',methods=['POST','GET'])
def forgot_password():
    if request.method=='POST':
        global otp
        user_email_id=request.form['email']
        status,otp=forgott_password(user_email_id)
        if(status):
            session['forg_email']=user_email_id
            return render_template('/forgot_password.html',status=status)
        else:
            return render_template('/forgot_password.html',status=status)

    return render_template('/forgot_password.html',status=None)

@app.route('/change_password',methods=['POST','GET'])
def  password_change():
    if 'forg_email' in session:
        obt_otp=request.form['obt-otp']
        global otp
        if(otp==None):
            return "None"
        else:
            if(otp==obt_otp):
                otp=""
                return render_template('/forgot_password.html',status='Done',cp=True)

            else:
                return render_template('/forgot_password.html',status='Done',cp=False)
    else:
        return redirect(url_for('forgot_password'))

@app.route('/change_passwords',methods=['POST','GET'])
def pass_change():
    if 'forg_email' in session:
        password=request.form['password']
        cpassword=request.form['cpassword']
        if(password==cpassword):
            pass_status=change_password(password,session['forg_email'])
            session.pop('forg_email',None)
            return render_template('/forgot_password.html',status='Done',pass_status=True)
        else:
            return render_template('/forgot_password.html',status='Done',pass_status=False)
    else:
        return redirect(url_for('forgot_password'))
   
@app.route('/about_us')
def about_us():
    return render_template('/about_us.html')

if __name__=='__main__':
    app.run(debug=False)