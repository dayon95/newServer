from django.shortcuts import render, redirect

from data01.models import pd1_time
from data01.models import pd2
from data01.models import feedbackpost, feedback
from datetime import datetime, timedelta
from django.db.models import Q

from django import forms
from data01.forms import feedbackForm

# Create your views here.

def test(request):
    return render(request,'data01/test.html',{})

def test_pd1_time(request):
    time=pd1_time.objects.exclude(title__exact='')
    return render(request,'data01/test_pd1_time.html',{'time':time})

def test_pd2(request):
    time=pd1_time.objects.exclude(title__exact='')
    return render(request,'data01/test_pd2.html',{'two':two})

#아래에 있는 함수는 PosterData의 when을 datafield로 변경된 후에 실행가능함.
def index_tutorial(request):
    #today, tomorrow, this_week에는 오늘, 내일, 이번주의 주 번호가 들어감
    #주 번호는 52주 중 몇번째 주인지 나타내는 번호임
    #이 세개 변수는 python의 datetime 모듈을 사용했음.
    today=datetime.today()
    tomorrow=today+timedelta(days=1)
    this_week=today.isocalendar()[1] #week number
    date_KOR=["월", "화", "수", "목", "금", "토", "일"]
    date=date_KOR[today.weekday()]
    #today_list, tomorrow_list, this_week_list에는 각각 오늘 내일 이번주 강연 데이터가 들어있음
    #각각 조건에 맞는 filter를 이용하였음.
    today_list=pd1_time.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day)
    tomorrow_list=pd1_time.objects.filter(date__year=tomorrow.year, date__month=tomorrow.month, date__day=tomorrow.day)
    this_week_list=pd1_time.objects.filter(date__week=this_week)
    #return render(request,'data01/index.html',today_list)
    contents={'date':date, 'today_list':today_list,'tomorrow_list':tomorrow_list,'this_week_list':this_week_list}
    return render(request,'data01/index_tutorial.html',contents)

def index(request):
    today=datetime.today()
    tomorrow=today+timedelta(days=1)
    this_week=today+timedelta(days=6)
    date_KOR=["월","화","수","목","금","토","일"]
    date=date_KOR[today.weekday()]

    today_list=pd2.objects.filter(Q(startdate__lte=today)&(Q(enddate__gte=today)|Q(enddate=None)))
    tomorrow_list=pd2.objects.filter(Q(startdate__lte=tomorrow)&(Q(enddate__gte=tomorrow)|Q(enddate=None)))
    this_week_list=pd2.objects.filter(Q(startdate__lte=this_week)&(Q(enddate__gte=today)|Q(enddate=None)))

    contents={'date':date, 'today_list':today_list,'tomorrow_list':tomorrow_list,'this_week_list':this_week_list}
    return render(request,'data01/index.html',contents)


def about(request):
    return render(request,'data01/about.html')

def feedback_index(request):
    feedback_list = feedbackpost.objects.all()
    return render(request, 'data01/feedback_index.html', {'feedback_list':feedback_list,})

def feedback_detail(request, pk):
    feedback_post = feedbackpost.objects.get(pk=pk)

    return render(request, 'data01/feedback_detail.html', {'feedback_post':feedback_post,})

def feedback_new(request, pk):
    if request.method == 'POST':
        form = feedbackForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = feedbackpost.objects.get(pk=pk)
            comment.save()
            return redirect('detail', pk=pk)
    else:
      form = feedbackForm()

    return render(request, 'data01/feedback_form.html', {'form':form,})
