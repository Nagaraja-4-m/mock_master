import MySQLdb
import smtplib 
import random as r

conn=MySQLdb.connect(host='localhost',database='quiz',user='root',password='zxcvbnm')
cursor=conn.cursor()
def admin_dashboard():
    pass


#subject -----------------------------------------
#add subject
def add_subject(sub_id,sub_name,sub_category,sub_descr):
    try:
        cursor.execute("SELECT subject_id FROM quiz.subjects")
        rows=cursor.fetchall()
        for row in rows:
            if(row[0]==sub_id):
               return None 
        else:
            try:
                cursor.execute("INSERT INTO `quiz`.`subjects` (`subject_id`, `subject_name`, `subject_category`,`subject_description`) VALUES ('{}', '{}', '{}','{}');".format(sub_id,sub_name,sub_category,sub_descr))
                conn.commit()
                return 1
            except:
                conn.rollback()
                return 0
    except:
        return 0

#update subject
def update_subject(sub_id,new_details):
    try:
        cursor.execute("UPDATE `quiz`.`subjects` SET `subject_id` = '{}', `subject_name` = '{}', `subject_category` = '{}',`subject_description`='{}' WHERE (`subject_id` = '{}')".format(new_details[0],new_details[1],new_details[2],new_details[3],sub_id))
        conn.commit()
        return True
    except:
       conn.rollback()
       return False


#delete subject
def delete_subject(sub_id):
    try:
        cursor.execute("DELETE FROM `quiz`.`subjects` WHERE (`subject_id` = '{}')".format(sub_id))
        conn.commit()
        return True
    except:
       conn.rollback()
       return False

#view subjects
def view_subject():
    result=[]
    total_qs=[]
    try:
        cursor.execute("SELECT subject_id,subject_name,subject_category FROM quiz.subjects order by subject_category ASC")
        rows=cursor.fetchall()
        for row in rows:
            try:
                cursor.execute("SELECT  count(*) FROM quiz.questions where subject_id='{}'".format(row[0]))
                temp=cursor.fetchone()
                total_qs.append(temp[0])
            except:
                pass
            result.append(row)
    except:
       pass
    return result,total_qs


#subjectId to sujectdetails
def subID_to_subDetails(sub_id):
    sub_details=[]
    try:
        cursor.execute("SELECT subject_id,subject_name,subject_category,subject_description FROM quiz.subjects where subject_id='{}'".format(sub_id))
        row=cursor.fetchone()
        for i in row:
            sub_details.append(i)
    except:
       pass
    return sub_details

#subject delete
def delete_subject(sub_id):
    try:
        cursor.execute("DELETE FROM `quiz`.`subjects` WHERE (`subject_id` = '{}')".format(sub_id))
        conn.commit()
        return True
    except:
       conn.rollback()
       return False


def get_Categories():
    categories=[]
    try:
        cursor.execute("SELECT subject_category FROM quiz.subjects group by subject_category")
        rows=cursor.fetchall()
        for item in rows:
            categories.append(item[0])
    except:
        return False
    return categories

def get_subjectNames():
    subjects=[]
    try:
        cursor.execute("SELECT subject_id,subject_name FROM quiz.subjects group by subject_name order by subject_name ASC")
        rows=cursor.fetchall()
        for item in rows:
            subjects.append(item)
    except:
        return False
    return subjects
#subject -----------------------------------------


#question---------------------------------------------------

#get question details
def get_Questions(sub_id):
    questions=[]
    try:
        cursor.execute("SELECT * FROM quiz.questions where subject_id='{}'".format(sub_id))
        rows=cursor.fetchall()
        for item in rows:
            questions.append(item)
    except:
        return False
    return questions   


#add question
def add_question(q_details):
    try:
        cursor.execute("INSERT INTO `quiz`.`questions` (`subject_id`, `question_id`, `question`, `option_1`, `option_2`, `option_3`, `option_4`, `correct_option`, `solution`) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(q_details[0],q_details[1],q_details[2],q_details[3],q_details[4],q_details[5],q_details[6],q_details[7],q_details[8]))
        conn.commit()
        return True
    except:
         conn.rollback()
         return False

#update question details
def update_question(q_id,new_details):
     try:
        cursor.execute("UPDATE `quiz`.`questions` SET `question_id` = '{}', `question` = '{}', `option_1` = '{}', `option_2` = '{}', `option_3` = '{}', `option_4` = '{}', `correct_option` = '{}', `solution` = '{}' WHERE (`question_id` = '{}');".format(new_details[0],new_details[1],new_details[2],new_details[3],new_details[4],new_details[5],new_details[6],new_details[7],q_id))
        conn.commit()
        return True
     except:
       conn.rollback()
       return False

#delete question details
def delete_question(q_id):
    try:
        cursor.execute("DELETE FROM `quiz`.`questions` WHERE (`question_id` = '{}')".format(q_id))
        conn.commit()
        return True
    except:
       conn.rollback()
       return False


def qID_to_qDetails(q_id):
    q_details=[]
    try:
        cursor.execute("SELECT * FROM quiz.questions where question_id='{}'".format(q_id))
        row=cursor.fetchone()
        for i in row:
            q_details.append(i)
    except:
       pass
    return q_details
#question---------------------------------------------------



#query -----------------------------------------------
def get_all_queries():
    queries=[]
    try:
        cursor.execute("SELECT * FROM quiz.queries  order by q_r_status ASC")
        rows=cursor.fetchall()
        for row in rows:
            row=list(row)
            row.append(student_email_to_name(row[1]))
            queries.append(row)
        return queries
    except:
        return False

def query_update(email,sub,replay):
    try:
        cursor.execute("UPDATE `quiz`.`queries` SET `q_replay` = '{}',`q_r_status`='1' WHERE (`user_email` = '{}' and `q_subject`='{}');".format(replay,email,sub))
        conn.commit()
    except:
        conn.rollback()
            
#query -----------------------------------------------

#admin -----------------------------------------------
def get_admin_details(admin_id):
    admin_details=[]
    try:
        cursor.execute("SELECT admin_id,admin_fname,admin_mobile,admin_email FROM quiz.admin_table")
        row=cursor.fetchone()
        for i in row:
            admin_details.append(i)
    except:
       pass
    return admin_details  

def update_admin(admin_id,admin_details):
    try:
        cursor.execute("UPDATE `quiz`.`admin_table` SET `admin_fname` = '{}', `admin_mobile` = '{}', `admin_email` = '{}' WHERE (`admin_id` = '{}')".format(admin_details[0],admin_details[1],admin_details[2],admin_id))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def login_admin(email,password):
    try:
        cursor.execute("SELECT * FROM quiz.admin_table where admin_email='{}' and admin_password='{}';".format(email,password))
        row=cursor.fetchone()
        if(row):
            return True 
        else:
            return False
    except :
        return False
        
#admin -----------------------------------------------


#student----------------------------
def get_students():
    std_lst=[]
    try:
        cursor.execute("SELECT user_name,user_gender,user_mobile,user_email,participation FROM quiz.users")
        rows=cursor.fetchall()
        for row in rows:
            std_lst.append(row)
        return std_lst
    except:
        return False

#email
def send_email(to,subject,msg):
    try:
        server=smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login('mastermock016@gmail.com','MockMaster@321')
        msg="Subject:{}\n\n{}".format(subject,msg)
        server.sendmail('mastermock016@gmail.com',to,msg)
        #print("Message sent")
        server.quit()
        return True
    except Exception:
        return False

#generate OTP
def generate_otp():
    otp=""
    for i in range(4):
        otp=otp+str(r.randint(1, 9))
    return otp

#email to name
def student_email_to_name(email):
    try:
        cursor.execute("SELECT user_name FROM quiz.users where user_email='{}';".format(email))
        row=cursor.fetchone()
        return row[0]
    except:
        return False
#student-----------------------------


#dashboard---
def un_answered_queries():
    try:
        cursor.execute("SELECT count(user_email) FROM quiz.queries where q_r_status='0';")
        result=cursor.fetchone()
        return result[0]
    except:
        return 0

def total_subjects():
    try:
        cursor.execute("SELECT count(subject_id) FROM quiz.subjects;")
        result=cursor.fetchone()
        return result[0]
    except:
        return 0

def total_students():
    try:
        cursor.execute("SELECT count(user_email) FROM quiz.users;")
        result=cursor.fetchone()
        return result[0]
    except:
        return 0


#x=["None","None","None","None","None","None","None","None","None"]
#print(add_question(x))
#print(view_subject_details())
#print(subID_to_subDetails("dfsd"))
#print(get_students())
#print(update_admin("21ADMN_1",admin_details=["Nani","875","nplk321@yahoo.com"]))
#print( get_all_queries())
#print(un_answered_queries())
#print(login_admin("nplk321@gmail.com","123@12"))