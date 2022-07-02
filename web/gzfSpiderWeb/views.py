import datetime

from django.shortcuts import render
from gzfSpiderWeb.models import Myapp001Mydata, Mydjangowebapphouse2Id


# Create your views here.
def index(request):
    return render(request, 'index.html')


# 获取两个日期间的所有日期
def getEveryDay(begin_date, end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


def selectDate(request):
    front_start_time = str(datetime.date.today())
    front_ending_time = str(datetime.date.today())
    if request.method == 'POST':
        front_start_time = request.POST.get('front_start_time')
        front_ending_time = request.POST.get('front_ending_time')

    data_list = getEveryDay(front_start_time, front_ending_time)
    house_list = []
    for eachData in data_list:
        house_obj = Myapp001Mydata.objects.raw(
            "SELECT * FROM myApp001_mydata WHERE id in (SELECT MAX(id) FROM myApp001_mydata WHERE get_time LIKE '%%%%%s%%%%' GROUP BY house_source)" % eachData)
        for house in house_obj:
            house2id_obj = Mydjangowebapphouse2Id.objects.get(house_id=house.house_id)
            house_name = house2id_obj.house_name
            dic = {"date": house.get_time.split()[0], "houseName": house_name,
                   "getTime": house.get_time}
            house_list.append(dic)
    data = {"houses": house_list, "query_begin_data": front_start_time, "query_ending_data": front_ending_time}
    return render(request, 'select.html', data)
