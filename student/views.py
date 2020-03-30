from django.shortcuts import render
from django.conf import settings

def home1(request):
    name = request.session['userdata'].get('name')
    branch = request.session['userdata'].get('branch')
    id = request.session['userdata'].get('id')

    query = "select name,mail,phone from user where branch={0} and type=2 and uid!={1}".format(branch,id)

    cnn = settings.CONNECTION()
    cr = cnn.cursor()
    cr.execute(query)

    names = cr.fetchall()

    return render(request,"studhome1.html",{"name":name,"branch":branch,"names":names})

def question1(request):    
    con = settings.CONNECTION()
    cr = con.cursor()
    id = request.session['userdata'].get('id')
    if request.method=='POST':
        qus = request.POST.get('qus')
        query = "insert into question(qus,ask_by) value('{0}',{1})".format(qus,id)                
        cr.execute(query)
        con.commit()        
    # get all question ..        
    query = "select * from question where ask_by={0} order by qid DESC".format(id)
    cr.execute(query)
    questions = cr.fetchall()

    finaldata = []
    for qus in questions:
        lst = list(qus)
        qid = lst[0]
        query = "select ans,ans_date,name from answer,user where qus={0} and answer.ans_by=user.uid".format(qid)
        cr.execute(query)
        a = cr.fetchall()
        lst.append(a)
        finaldata.append(lst)

    print(finaldata)        

    con.close()
    return render(request,"question1.html",{"questions":finaldata})

def stuquestion1(request):
    con = settings.CONNECTION()
    cr = con.cursor()
    id = request.session['userdata'].get('id')
    if request.method=='POST':
        qus = request.POST.get('qus')
        #uid = request.session['userdata'].get('id')
        query = "insert into stuquestion(qus,ask_by) value('{0}',{1})".format(qus,id)                
        cr.execute(query)
        con.commit()        
    # get all question ..        
    query = "select * from stuquestion where ask_by={0} order by qid DESC".format(id)
    cr.execute(query)
    questions = cr.fetchall()

    finaldata = []
    for qus in questions:
        lst = list(qus)
        qid = lst[0]
        query = "select ans,ans_date,name from stuanswer, user where qus={0} and stuanswer.ans_by=user.uid".format(qid)
        cr.execute(query)
        a = cr.fetchall()
        lst.append(a)
        finaldata.append(lst)

    #print(finaldata)        

    con.close()
    return render(request,"stuquestion1.html",{"questions":finaldata})

def stuanswer1(request):
    branch = request.session['userdata'].get('branch')
    sid = request.session['userdata'].get('id')
    cnn = settings.CONNECTION()
    cr = cnn.cursor()

    if request.method=="POST":
        answer = request.POST.get('answer')
        qus = request.POST.get('qus')
        query = "insert into stuanswer(ans,qus,ans_by) value('{0}','{1}',{2})".format(answer,qus,sid)
        cr.execute(query)
        cnn.commit()


    # subquery - nested query
    query = "select qid,qus,qus_date,name from stuquestion, user where ask_by in (select uid from user where branch={0} and type=2 and uid!={1}) and stuquestion.ask_by=user.uid".format(branch,sid)
    
    cr.execute(query)

    questions = cr.fetchall()
    return render(request,'stuanswer1.html',{'questions':questions})