#setting up admin account

import MySQLdb
import getpass

conn=MySQLdb.connect(host='localhost',database='quiz',user='root',password='zxcvbnm')
cusror=conn.cursor()

flag=False

try:
    cusror.execute("SELECT * FROM quiz.admin_table;")
    nor=cusror.rowcount
    if(nor>=1):
        flag=True
except:
    print("Unable to process the request!")

if(not flag):
    print("#"*10,end='')
    print(" SETUP ADMIN ACCOUNT ",end='')
    print("#"*10)
    print()
    admin_details=[]
    admin_details.append(str(input("Create an ID:")))
    admin_details.append(str(input("Full name:")))
    admin_details.append(str(input("Mobile number:")))
    admin_details.append(str(input("Email ID:")))
    admin_details.append(str(getpass.getpass('Create Password:')))
    admin_details.append(str(getpass.getpass('Confirm Password:')))
    if(admin_details[4]==admin_details[5]):
        try:
            cusror.execute("INSERT INTO `quiz`.`admin_table` (`admin_id`, `admin_fname`, `admin_mobile`, `admin_email`, `admin_password`) VALUES ('{}', '{}', '{}', '{}', '{}');".format(admin_details[0],admin_details[1],admin_details[2],admin_details[3],admin_details[4]))
            conn.commit()
            print("\n Admin account settuped.")
        except:
            conn.rollback()
            print("\n Error occured while settuping..")
    else:
        print("\nTypeError: Password mismatch..")
    
else:
    print("\n Admin account already setuped. \n\n Try logging in at '127.0.0.1:5000/admin' ")

