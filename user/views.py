from django.shortcuts import render


def home_view(request):
    table_data = {
        'time_interval': ['08-09', '09-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18',
                          '18-19', '19-20', '20-21'],
        'week_days': ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri']}
    return render(request, "home.html", table_data)
