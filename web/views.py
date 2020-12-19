from django.shortcuts import render , redirect
#from django.http import HttpResponse
from django.conf import settings

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from random import randint

def home(request):
    return render(request,"home.html")

def about(request):
    return render(request,"about.html")

def gallery1(request):
    return render(request,"gallery1.html")

def contact1(request):
    return render(request,"contact1.html")   

def saveContact(request):
    name = request.POST.get("cname")
    mail = request.POST.get("email")
    phone = request.POST.get("phone")
    sub = request.POST.get("subject")
    msg = request.POST.get("message")
    
    query = "insert into contact(name,email,phone,subject,message) value('{0}','{1}','{2}','{3}','{4}')".format(name,mail,phone,sub,msg)

    cnn = settings.CONNECTION()

    cr = cnn.cursor()
    cr.execute(query)
    cnn.commit()
    #print(name,mail,phone,sub,msg)
    context = "Contact Saved!"
    return render(request,"contact1.html",{"messages":context})
    
def login1(request): # /college/login
    msg = ""
    err = request.GET.get("error")
    if err is not None:
        msg = "Invalid User!"
    
    return render(request,"login1.html",{"msg":msg})   

def register(request):
    name = request.POST.get('username')
    email = request.POST.get('email')
    pwd = request.POST.get('pwd')
    type = request.POST.get('type')
    branch = request.POST.get('branch')

    #mail = request.session['userdata'].get('email')
    #if email!=mail:
    otp = sendMail(name,email)
    query = "insert into user(name,mail,password,type,branch,otp) value('{0}','{1}','{2}',{3},{4},{5})".format(name,email,pwd,type,branch,otp)
    cnn = settings.CONNECTION()
    cr = cnn.cursor()
    cr.execute(query)
    cnn.commit()
    reg = "Registration Success!"
    return render(request,"login1.html",{"reg":reg})
    #else:
        #return render(request,"login1.html")

def loginuser(request):
    email = request.POST.get('email')
    pwd = request.POST.get('pwd')

    query = "select * from user where mail='{0}' and password='{1}'".format(email,pwd)

    cnn = settings.CONNECTION()

    cr = cnn.cursor()
    cr.execute(query)        

    record = cr.fetchone()
    #print("Record: ",record)
    if record is None:
        msg = "Login Failed!"
        return redirect('/college/login1?error=1')    
    else:
        id = record[0]
        name = record[1]
        email = record[2]
        phone = record[3]
        branch = record[6]
        type = record[5] 

        isVerify = record[8] # 0
        if isVerify==0:
            return redirect('/college/verify1') 
        else: 
            user = {"id":id,"name":name,"email":email,"phone":phone,"branch":branch,"type":type}

            request.session['userdata'] = user

            if type==1: # faculty
                return redirect('/faculty/home1')  
            else: # student
                return redirect('/student/home1')

def resetpw(request):
    if request.method=="GET":
        return render(request,'resetpw.html')
    else:
        MAIL = request.POST.get('MAIL')
        np = request.POST.get('np')
        PWD = request.POST.get('PWD')
        if np==PWD:
            query = "update user set password='{1}' where mail='{0}'".format(MAIL,np)
            cnn = settings.CONNECTION()
            cr = cnn.cursor()
            cr.execute(query)
            cnn.commit()
            return redirect('/college/login1')
        else:
            msg = "Password NOT matched!"
            return render(request,'resetpw.html',{"msg":msg})

def verify1(request):
    if request.method=="GET":
        return render(request,'verify1.html')
    else:
        otp = request.POST.get('otp')       
        mail = request.POST.get('email')
        #password = request.POST.get('password')
        query = "update user set isVerify=1 where mail='{0}' and otp={1}".format(mail,otp)
        cnn = settings.CONNECTION()
        cr = cnn.cursor()
        cr.execute(query)
        #record = cr.fetchone() 
        #type = record[5]
        cnn.commit()
        #msg = "Invalid OTP"
        return redirect('/college/login1')   

def resend(request):
        name = request.POST.get('NAME')
        email = request.POST.get('EMAIL')
        otp = sendMail(name,email)
        print(name, email, otp)
        #query = "update user set name=NULL, email=NULL,otp=NULL where email='{1}'".format(email,otp)
        query = "update user set otp={1} where mail='{0}'".format(email,otp)
        cnn = settings.CONNECTION()
        cr=cnn.cursor()
        cr.execute(query)
        cnn.commit()
        msg = "OTP Sent!"
        return render(request,'verify1.html',{"msg":msg})

def logout(request):
    del request.session['userdata']
    return redirect('/college/login1')

def sendMail(name,mail):
    otp = randomdigit(6)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "OTP Verification"
    msg['From'] = 'en17cs301180@medicaps.ac.in'
    msg['To'] = mail
    
    html = """
        <html>        
          <body>
            <h1 style='color:red'>Email Confirmation</h1>
            <hr>
            <b>Welcome {0}!</b>
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            Your registration is successfully done, please verify your email with the OTP <b>{1}</b>.
            <br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <b>NOTE:</b> The above OTP will expire in 15 minutes.
            <br><br>
            Thanks!
          </body>
        </html>
        """.format(name,otp)
    part2 = MIMEText(html, 'html')
    msg.attach(part2)


    fromaddr = 'en17cs301180@medicaps.ac.in'
    toaddrs  = mail
    username = 'en17cs301180@medicaps.ac.in'
    password = 'put_your_password_here'
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()
    return otp

def randomdigit(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)    
