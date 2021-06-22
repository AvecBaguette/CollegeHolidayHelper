from django.shortcuts import render, redirect
from user.models import Activity
from user.utils.db_utils import from_db_to_dict
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
import json


@login_required(login_url="user-login")
def home_view(request):
    selected_year = "anul-1"
    if "timetableYear" in request.GET:
        selected_year = request.GET["timetableYear"]
    existing_activities = Activity.objects.all()
    db_dict = {}
    for activity in existing_activities:
        db_dict = from_db_to_dict(activity, db_dict)
    context = {
        'db_dict': json.dumps(db_dict),
        'time_interval': ['08-09', '09-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18',
                          '18-19', '19-20', '20-21'],
        'week_days': ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri'],
        'groups_y1': {
            'A': ['411A', '412A', '413A', '414A'],
            'B': ['411Ba', '411Bb', '412Ba', '412Bb', '413Ba', '413Bb', '414Ba', '414Bb'],
            'C': ['411Ca', '411Cb', '412Ca', '412Cb', '413Ca', '413Cb', '414Ca', '414Cb'],
            'D': ['411D', '412D', '413D', '414D'],
            'E': ['411E', '412E', '413E', '414E'],
            'F': ['411Fa', '411Fb', '412Fa', '412Fb', '413Fa', '413Fb', '414Fa', '414Fb'],
            'G': ['411G', '412G', '413G']
        },
        'groups_y2': {
            'A': ['421Aa', '421Ab', '422Aa', '422Ab', '423Aa', '413Ab', '424Aa', '424Ab'],
            'B': ['421Ba', '421Bb', '422Ba', '422Bb', '423Ba', '423Bb', '424Ba', '424Bb'],
            'C': ['421Ca', '421Cb', '422Ca', '422Cb', '423Ca', '423Cb', '424Ca', '424Cb'],
            'D': ['421Da', '421Db', '422Da', '422Db', '423Da', '423Db', '424Da', '424Db', '425Da', '425Db'],
            'E': ['421Ea', '421Eb', '422Ea', '422Eb', '423Ea', '423Eb', '424Ea', '424Eb'],
            'F': ['421Fa', '421Fb', '422Fa', '422Fb', '423Fa', '423Fb', '424Fa', '424Fb', '425Fa', '425Fb'],
            'G': ['421Ga', '421Gb', '422Ga', '422Gb']
        },
        'groups_y3': {
            'A': ['431Aa', '431Ab', '432Aa', '432Ab', '433Aa', '433Ab', '434Aa', '434Ab', '435Aa', '435Ab'],
            'B': ['431Ba', '431Bb', '432Ba', '432Bb', '433Ba', '433Bb', '434Ba', '434Bb', '435Ba', '435Bb'],
            'C': ['431Ca', '431Cb', '432Ca', '432Cb', '433Ca', '433Cb', '434Ca', '434Cb', '435Ca', '435Cb'],
            'D': ['431Da', '431Db', '432Da', '432Db', '433Da', '433Db', '434Da', '434Db'],
            'E': ['431Ea', '431Eb', '432Ea', '432Eb', '433Ea', '433Eb', '434Ea', '434Eb', '435Ea', '435Eb'],
            'F': ['431Fa', '431Fb'],
            'G': ['431Ga', '431Gb', '432Ga', '432Gb']
        },
        'groups_y4': {
            'A': ['431Aa', '431Ab', '432Aa', '432Ab', '433Aa', '433Ab', '434Aa', '434Aa'],
            'B': ['431Ba', '431Bb', '432Ba', '432Bb', '433Ba', '433Bb', '434Ba', '434Bb', '435Ba'],
            'C': ['431Ca', '431Cb', '432Ca', '432Cb', '433Ca', '433Cb', '434Ca', '434Cb'],
            'D': ['431Da', '431Db', '432Da', '432Db', '433Da', '433Db', '434Da', '434Db'],
            'E': ['431Ea', '431Eb', '432Ea', '432Eb', '433Ea', '433Eb', '434Ea', '434Eb', '435Ea', '435Eb'],
            'F': ['431Fa', '431Fb'],
            'G': ['431Ga', '431Gb', '432Ga']
        },
        'selected_year': selected_year

    }
    return render(request, "home.html", context)


def registration_view(request):
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contul a fost creat cu succes. Vă puteţi loga.')
            return redirect('user-login')
    else:
        form = UserRegisterForm()

    return render(request, 'user/register.html', {'form': form})


def delete_event(request):
    if "data-to-delete" in request.POST:
        activity_to_delete = Activity.objects.filter(id=int(request.POST["data-to-delete"])).first()
        activity_to_delete.delete()
    return JsonResponse({}, status=200)


def save_event(request):
    data = json.loads(request.POST["data-for-db"])
    if check_for_overlapping_hours(data) == 0:
        messages.error(request, "Overlapping time interval!")
        return JsonResponse({"overlapping_error": True}, status=200)

    if "data-for-db" in request.POST:
        new_activity = Activity()
        new_activity.groups = str(data['groups'])
        new_activity.time_interval = data['timeInterval']
        new_activity.course_name = data['courseName']
        new_activity.activity_type = data['activityType']

        new_activity.teacher_name = data['teacherName']
        new_activity.day = data['day']
        new_activity.save()
        return JsonResponse({"created_id": new_activity.id}, status=200)
    return redirect("home_page")


def check_for_overlapping_hours(data_to_insert):
    all_activities = Activity.objects.filter(day=data_to_insert["day"])
    available_hours = {8: '1', 9: '1', 10: '1', 11: '1', 12: '1', 13: '1', 14: '1', 15: '1', 16: '1',
                       17: '1', 18: '1', 19: '1', 20: '1'}

    for activity in all_activities:
        if activity.teacher_name == data_to_insert["teacherName"]:
            time_interval = activity.time_interval
            first_hour = int(time_interval.split("-")[0])
            second_hour = int(time_interval.split("-")[1])
            if second_hour - first_hour > 1:
                available_hours[first_hour] = "0"
                available_hours[first_hour + 1] = "0"
            else:
                available_hours[first_hour] = "0"

    data_first_hour = int(data_to_insert["timeInterval"].split("-")[0])
    data_second_hour = int(data_to_insert["timeInterval"].split("-")[1])
    if data_second_hour - data_first_hour > 1:
        if available_hours[data_first_hour] == "0" or available_hours[data_first_hour + 1] == "0":
            return 0
    elif available_hours[data_first_hour] == "0":
        return 0
    return 1
