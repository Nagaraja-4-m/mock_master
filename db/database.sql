create database quiz;
use quiz;


##admin account
create table admin( 
id int  auto_increment,
admin_id varchar(20),
admin_name varchar(100),
admin_mobile varchar(10),
admin_email varchar(100),
admin_password varchar(16),
admin_gender varchar(40),
primary key(id)
);

##users account
create table users( 
id int  auto_increment,
user_name varchar(100),
user_mobile varchar(10),
user_email varchar(100),
user_password varchar(16),
user_gender varchar(40),
participation varchar(4000),
primary key(id)
);


## table subjects
create table subjects(
id int auto_increment,
subject_id varchar(10),
subject_name varchar(50),
subject_category varchar(50),
subject_description varchar(500),
primary key(id)
);



#questions table
create table questions
(
id int auto_increment,
subject_id varchar(18),
question_id varchar(18),
question varchar(1000),
option_1 varchar(1000),
option_2 varchar(1000),
option_3 varchar(1000),
option_4 varchar(1000),
correct_option varchar(1000),
solution varchar(10000),
primary key(id)
);


#feedback table
create table feedback
(
	id int auto_increment,
    user_name varchar(100),
    user_email varchar(100),
    user_subject varchar(100),
    user_message varchar(1000),
    primary key(id)
);

#admin table
create table admin_table
(
	 id int auto_increment,
     admin_id varchar(100),
     admin_fname varchar(100),
     admin_mobile varchar(100),
     admin_email varchar(100),
     admin_password varchar(100),
     primary key(id)
);

#query table
create table queries
(
id int auto_increment,
user_email varchar(100),
q_subject varchar(200),
q_query varchar(1000),
q_r_status varchar(2),
q_replay varchar(1000),
primary key(id)
);


ALTER TABLE `quiz`.`users` 
CHANGE COLUMN `user_email` `user_email` VARCHAR(100) NOT NULL ,
DROP PRIMARY KEY,
ADD PRIMARY KEY (`id`, `user_email`);
;