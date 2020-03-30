from django.shortcuts import render
from django.conf import settings

def home1(request):
    name = request.session['userdata'].get('name')
    branch = request.session['userdata'].get('branch')

    query = "select name,mail,phone from user where branch={0} and type=2".format(branch)

    cnn = settings.CONNECTION()
    cr = cnn.cursor()
    cr.execute(query)

    students = cr.fetchall()

    return render(request,"fachome1.html",{"name":name,"students":students,"branch":branch})

def answer1(request):
    branch = request.session['userdata'].get('branch')
    fid = request.session['userdata'].get('id')
    cnn = settings.CONNECTION()
    cr = cnn.cursor()

    if request.method=="POST":
        answer = request.POST.get('answer')
        qus = request.POST.get('qus')
        query = "insert into answer(ans,qus,ans_by) value('{0}','{1}',{2})".format(answer,qus,fid)
        cr.execute(query)
        cnn.commit()

    # subquery - nested query
    query = "select qid,qus,qus_date,name from question, user where ask_by in (select uid from user where branch={0} and type=2) and question.ask_by=user.uid".format(branch)

    cr.execute(query)
    questions = cr.fetchall()
    return render(request,'answer1.html',{'questions':questions})