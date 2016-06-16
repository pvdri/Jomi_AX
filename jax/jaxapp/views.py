from django.shortcuts import render
from models import det_ax, cli_ax
from webform import orgform


def home(request):
    form = orgform()
    return render(request, 'jaxapp/index.html', {'dropdownform': form})

def detail(request):
    if request.method == 'POST':
        form =  orgform(request.POST)

    if form.is_valid():
        org_id = form.cleaned_data['organization']
        orgname = cli_ax.objects.filter(id=org_id)[0].org
        detail_data = det_ax.objects.filter(org=orgname)
        count_data = det_ax.objects.filter(org=orgname).count()

    return render(request, 'jaxapp/detail_view.html', {'detail_form' : detail_data, 'ip_name' : orgname,'count' : count_data})

def summary(request):
    if request.method == 'POST':
        form =  orgform(request.POST)

    if form.is_valid():
      org_id = form.cleaned_data['organization']
      orgname = cli_ax.objects.filter(id=org_id)[0].org
      monthly = det_ax.objects.values("month").distinct()
      yearly = det_ax.objects.values("year").distinct()

      newdict = []
      for y in monthly:
        for z in yearly:
            a = det_ax.objects.filter(org=orgname).filter(month=y["month"]).filter(year=z["year"]).count()
            b = det_ax.objects.filter(org=orgname).filter(month=y["month"]).filter(year=z["year"]).values('ip').distinct()
            if a > 0:
                newdict.append([y["month"], " ", z["year"], " => ", " Unique: IPs: ", len(b), "/ Session IDs:  ", a])
    return render(request, 'jaxapp/summary_view.html', {"sum_dict" : newdict, 'ip_name' : orgname})


def ip_add(request):
    if request.method == 'POST':
        form =  orgform(request.POST)

    if form.is_valid():
        org_id = form.cleaned_data['organization']
        orgname = cli_ax.objects.filter(id=org_id)[0].org
        ip_data = det_ax.objects.filter(org=orgname).values('ip').distinct()
        count_data = det_ax.objects.filter(org=orgname).values('ip').distinct().count()

    return render(request, 'jaxapp/ip_add.html', ({'ip_details' : ip_data, 'ip_name' : orgname, 'count' : count_data}))
