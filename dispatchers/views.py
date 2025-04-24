import html
from django.http import JsonResponse, HttpResponse
import json
from django.shortcuts import render, redirect
from .models import Handover
from .forms import HandoverForm

def check_json(json_data):
    """Check the JSON to ensure its proper"""
    try:
        json_string = html.unescape(json_data)
        return json.loads(json_string)
    except json.JSONDecodeError:
        return []

def zip_json(json_data, title_names: list):
    """Zip the JSON file with a title, so its easier to view in database"""
    return [dict(zip(title_names, v)) for v in
                                 json_data] if json_data else []


def handover_view_create(request):
    full_name = f"{request.user.first_name} {request.user.last_name}"

    if request.method == "POST":
        form = HandoverForm(request.POST)

        if form.is_valid():
            handover = form.save(commit=False)

            non_standard_flights_json = request.POST.get("non_standard_flights_json", "[]")
            non_standard_json = check_json(non_standard_flights_json)
            handover.non_standard_flights = zip_json(json_data=non_standard_json, title_names=["flight", "alternate", "extra"])

            naifr = request.POST.get("naifr_flights_json", "[]")
            naifr_json = check_json(naifr)
            handover.naifr = zip_json(json_data=naifr_json, title_names=["flight", "destination"])

            aog = request.POST.get("aog_flights_json", "[]")
            aog_json = check_json(aog)
            handover.aog = zip_json(json_data=aog_json, title_names=["tail", "issue", "fob"])

            com = request.POST.get("com_flights_json", "[]")
            comat_flights_json = check_json(com)
            handover.comat_flights = zip_json(json_data=comat_flights_json, title_names=["flight", "remark"])


            handover.save()

            # return redirect("home")
        else:
            print(form.errors)

    else:
        form = HandoverForm(initial={"dispatcher_name": full_name})

    return render(request, "handover.html", {"form": form, "full_name": full_name})

def previous_data_loader(request):
    if request.method == "GET":
        selected_date = request.GET.get("shift_date")
        selected_shift = request.GET.get("shift_type")

        if not selected_date or not selected_shift:
            return JsonResponse({"error": "Please enter date and shift parameters"}, status=400)


        handover_entries = Handover.objects.filter(shift_date=selected_date, shift=selected_shift)
        data = list(handover_entries.values('shift_date', 'shift', 'aog', 'mels', 'procedural_changes', 'navblue_tickets', 'operational_notams'))


        return JsonResponse({"data": data})



def handover_view_selection(request):
    if request.method == "GET":
        selected_date = request.GET.get("shift_date")
        selected_shift = request.GET.get("shift_type")

        if not selected_date or not selected_shift:
            return JsonResponse({"error": "Please enter date and shift parameters"}, status=400)

        handover_entries = Handover.objects.filter(shift_date=selected_date, shift=selected_shift)
        data = list(handover_entries.values())

        return JsonResponse({"data": data})

def handover_viewer_view(request):
    return render(request, 'handover_viewer.html')