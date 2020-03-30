create database collegeweb;

create table collegeweb.user(
    uid int AUTO_INCREMENT,
    name varchar(100) NOT NULL,
    mail  varchar(100) NOT NULL UNIQUE,
    phone varchar(20) UNIQUE,
    password varchar(10) NOT NULL,
    type int NOT NULL,/* 1: faculty 2: student*/
    branch int NOT NULL, /* 1:CS 2:EC 3: ME */
    otp int, /* 4365 */
    isVerify int default 0,
    profile_pic varchar(100),
    PRIMARY KEY (uid)
);

create table collegeweb.question(
    qid int AUTO_INCREMENT,
    qus varchar(5000) NOT NULL,
    qus_date timestamp default CURRENT_TIMESTAMP,
    ask_by int,
    isActive int default 1,
    PRIMARY KEY (qid),
    FOREIGN KEY (ask_by) REFERENCES collegeweb.user(uid)
);

create table collegeweb.answer(
    aid int AUTO_INCREMENT,
    ans varchar(5000) NOT NULL,
    ans_date timestamp default CURRENT_TIMESTAMP,
    qus int,
    ans_by int,
    PRIMARY KEY (aid),
    FOREIGN KEY (qus) REFERENCES collegeweb.question(qid),
    FOREIGN KEY (ans_by) REFERENCES collegeweb.user(uid)
);

create table collegeweb.stuquestion(
    qid int AUTO_INCREMENT,
    qus varchar(5000) NOT NULL,
    qus_date timestamp default CURRENT_TIMESTAMP,
    ask_by int,
    isActive int default 1,
    PRIMARY KEY (qid),
    FOREIGN KEY (ask_by) REFERENCES collegeweb.user(uid)
);

create table collegeweb.stuanswer(
    aid int AUTO_INCREMENT,
    ans varchar(5000) NOT NULL,
    ans_date timestamp default CURRENT_TIMESTAMP,
    qus int,
    ans_by int,
    PRIMARY KEY (aid),
    FOREIGN KEY (qus) REFERENCES collegeweb.stuquestion(qid),
    FOREIGN KEY (ans_by) REFERENCES collegeweb.user(uid)
);

create table collegeweb.contact(
    cid int AUTO_INCREMENT,
    name varchar(100) NOT NULL,
    email varchar(100) NOT NULL,
    phone varchar(20) NOT NULL,
    subject varchar(1000) NOT NULL,
    message varchar(5000) NOT NULL,
    PRIMARY KEY (cid);
);