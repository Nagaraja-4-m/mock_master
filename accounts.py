from admin import generate_otp,send_email
import MySQLdb

conn=MySQLdb.connect(host='localhost',database='quiz',user='root',password='zxcvbnm')
cursor=conn.cursor()


#forgot password
def forgott_password(email):
    try:
        cursor.execute("SELECT user_email FROM quiz.users where user_email='{}'".format(email))
        row=cursor.fetchone()
        if(row):
            otp=generate_otp()
            subject="OTP to change the password"
            msg="Dear user, \n\nWe got a password change request from you,\n\n '{}' is the OTP to change the password. \n\n\n Note: \n Please do not share the OTP with anyone.".format(otp)
            send_status=send_email(email,subject,msg)
            if(send_status):
                return True,otp
            else: 
                return False,None
        else:
            return False,None
             
    except:
        return False


#change password
def change_password(password,email):
    try:
        cursor.execute("UPDATE `quiz`.`users` SET `user_password` = '{} '  WHERE `user_email` = '{}'".format(password,email))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False


#check email 
def check_email_existance(email_id):
    try:
        cursor.execute("SELECT user_email FROM quiz.users where user_email='{}';".format(email_id))
        row=cursor.fetchone()
        if(row==None):
            return False
        else:
            return True
    except:
        return True

#registration
def user_register(user_details):
    try:
        cursor.execute("INSERT INTO `quiz`.`users` (`user_name`, `user_gender`, `user_mobile`, `user_email`, `user_password`,`participation`) VALUES ('{}', '{}', '{}', '{}', '{}',' ')".format(user_details[0],user_details[1],user_details[2],user_details[3],user_details[4]))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

#login
def user_login(email,password):
    try:
        cursor.execute("SELECT user_email FROM quiz.users where( user_email='{}' and user_password='{}');".format(email,password))
        row=cursor.fetchone()
        if(row):
            return True
        else:
            return False
    except:
        return False

#xyz=['Anjali', 'Female', '8889898', 'Npll@dfjsd.co', '123456']
#print(register(xyz))
#print(user_login("nplk321@gmail.com","173456"))
