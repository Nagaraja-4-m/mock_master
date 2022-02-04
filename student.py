import MySQLdb
import simplejson

conn=MySQLdb.connect(host='localhost',database='quiz',user='root',password='zxcvbnm')
cursor=conn.cursor()


def get_subject_categories():
    cats=[]
    try:
        cursor.execute("SELECT subject_category,subject_description FROM quiz.subjects group by subject_category;")
        rows=cursor.fetchall()
        for item in rows:
            cats.append(item)
        return cats
    except:
       return False

def get_subjects(sub_cat):
    subs=[]
    try:
        cursor.execute("SELECT subject_id,subject_name FROM quiz.subjects where subject_category='{}'".format(sub_cat))
        rows=cursor.fetchall()
        for item in rows:
            subs.append(item)
        return subs
    except:
       return False


def get_Questions(sub_id):
    questions=[]
    try:
        cursor.execute("SELECT * FROM quiz.questions where subject_id='{}'".format(sub_id))
        rows=cursor.fetchall()
        for item in rows:
           questions.append(item)
        return questions
    except:
        return False


def get_result(sub_id,user_email,response):
    result=[]
    total_correct=0
    for i in response:
        if(i[1]==i[2]):
            i.append(True)
            result.append(i)
            total_correct=total_correct+1
        else:
            i.append(False)
            result.append(i)
    put_results(sub_id,user_email,total_correct,len(response))
    return result,total_correct

def put_results(subject_id,email_id,score,total):
    try:
        cursor.execute("SELECT `participation` FROM quiz.users WHERE `user_email` = '{}';".format(email_id))
        row=cursor.fetchone()
        subject_name=subID_to_subName(subject_id)
        if(row[0]):
            new_value=row[0]+"{},{},{}:::".format(subject_name,score,total)
        else:
            new_value="{},{},{}:::".format(subject_name,score,total)
        print(new_value)
        cursor.execute("UPDATE `quiz`.`users` SET `participation`= '{}' WHERE (`user_email` = '{}');".format(new_value,email_id))
        conn.commit()
    except:
        conn.rollback()
       

def get_user_details(email):
    try:
        cursor.execute("SELECT user_name,user_gender,user_mobile,user_email,participation FROM quiz.users where user_email='{}';".format(email))
        row=cursor.fetchone()
        return row
    except:
        return False

def exract_user_performace(string):
    temp=string.split(':::')
    data=[]
    for x in temp[:len(temp)-1]:
        l=x.split(',')
        temp2=[l[0],int(l[1]),int(l[2])]
        data.append(list(temp2))
    # data=simplejson.dumps(data)
    # print(data)
    # print(type(data))
    return data

def subID_to_subName(sub_id):
    try:
        cursor.execute("SELECT subject_name FROM quiz.subjects where subject_id='{}'".format(sub_id))
        row=cursor.fetchone()
        return row[0]
    except:
       return False

def send_query(email,sub,qry):
    try:
        x=check_query_data_existance(email,sub,qry)
        if(x==True):
            pass
        elif(x==False):
            cursor.execute("INSERT INTO `quiz`.`queries` (`user_email`, `q_subject`, `q_query`,`q_r_status`) VALUES ('{}', '{}', '{}','0');".format(email,sub,qry))
            conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_replays(email):
    replays=[]
    try:
        cursor.execute("SELECT q_r_status,user_email,q_subject,q_query,q_replay FROM quiz.queries where user_email='{}'; ".format(email))
        rows=cursor.fetchall()
        for row in rows:
            replays.append(row)
        return replays
    except:
        return False

def check_query_data_existance(email,sub,qry):
    try:
        cursor.execute("SELECT q_subject,q_query FROM quiz.queries where user_email='{}'; ".format(email))
        rows=cursor.fetchall()
        for row in rows:
            if(row[0]==sub and row[1]==qry):
                return True
        else:
            return False
    except:
        return False
#print(get_subject_categories())
#print(get_subjects("Aptitude"))
#print(get_Questions("APTPERENL")[0])
#print(get_result([['PERENL001', '1', '1'], ['PERENL002', '3', '4'], ['PERENL003', '1', '1'], ['PERENL004', '4', '2'], ['PERENL005', '3', '4']] ))
#print(get_user_details("anjung@yahoo.in"))

#put_results("subject_id", "nplk321@gmail.com", 10, 30)
#print(get_replays("a@a.a"))
#print(send_query("a@a.a","How many?","This many..??"))