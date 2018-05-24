from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.template.loader import get_template
from django.shortcuts import render

import io as BytesIO
from xhtml2pdf import pisa
from django.template import Context
from cgi import escape

from .models import Form, Vehicle, Driver
from .forms import TravelForm

def get_form_info_by_id(formID):
    form = Form.objects.get(id=formID)
    date = form.date
    driver = form.driver
    vehicle = form.vehicle
    odometer_before = form.odometer_before
    odometer_after = form.odometer_after
    distance = odometer_after - odometer_before
    fuel_given = form.fuel_given
    fuel_before = form.fuel_before
    fuel_after = form.fuel_after
    fuel_used = fuel_given + fuel_before - fuel_after
    if(distance == 0):
        fuel_norm = 0
    else:   
        fuel_norm = fuel_used / distance * 100

    travel_info = {}
    travel_info["date"] = date
    travel_info["driver"] = driver
    travel_info["vehicle"] = vehicle
    travel_info["formID"] = formID
    travel_info["odometer_before"] = odometer_before
    travel_info["odometer_after"] = odometer_after
    travel_info["distance"] = distance
    travel_info["fuel_given"] = fuel_given
    travel_info["fuel_before"] = fuel_before
    travel_info["fuel_after"] = fuel_after
    travel_info["fuel_used"] = fuel_used
    travel_info["fuel_norm"] = fuel_norm

    return {
        'travel_info': travel_info
    }

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = context_dict
    html = template.render(context)
    result = BytesIO.BytesIO()

    pdf = pisa.pisaDocument(html, result, encoding="UTF-8", path=".")
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('Error has occured<pre>%s</pre>' % escape(html))

def get_form(request, formID):
    travel_context = get_form_info_by_id(formID)
    return render(request, 'fillForm/results.html', {
        'travel_info': travel_context['travel_info']
    })

def fill_form(request):
    travel_form = TravelForm()
    if request.method == 'POST':
        travel_form_info = TravelForm(request.POST)
        filledDate = travel_form_info["filled_date"].value()
        driver = Driver.objects.get(id=travel_form_info["driver"].value())
        vehicle = Vehicle.objects.get(id=travel_form_info["vehicle"].value())
        odometer_before = travel_form_info["odometer_before"].value()
        odometer_after = travel_form_info["odometer_after"].value()
        fuel_given = travel_form_info["fuel_given"].value()
        fuel_before = travel_form_info["fuel_before"].value()
        fuel_after = travel_form_info["fuel_after"].value()

        Form.create(filledDate, vehicle, driver, odometer_before, odometer_after, fuel_given, fuel_before, fuel_after).save()

    return render(request, 'fillForm/formFilling.html', {
        'travel_form': travel_form,
    })

def get_forms(request):
    forms = Form.objects.all()
    context = {
        'forms': forms
    }
    return render(request, 'fillForm/forms.html', context)

def get_pdf(request, formID):
    info = get_form_info_by_id(formID)
    return render_to_pdf( 'fillForm/results.html',{
        'travel_info': info['travel_info']
    })
