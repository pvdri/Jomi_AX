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

    return render(request, 'jaxapp/detail_view.html', {'detail_form' : detail_data})

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
            if a > 0:
                newdict.append([orgname,": ", z["year"], " / ", y["month"], " => ", "Unique Session IDs: ", a])
    return render(request, 'jaxapp/summary_view.html', {"sum_dict" : newdict})
