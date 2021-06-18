from django.shortcuts import render


def home_view(request):
    table_data = {
        'time_interval': ['08-09', '09-10', '10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18',
                          '18-19', '19-20', '20-21'],
        'week_days': ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri'],
        'groups_y1': ['411A', '412A', '413A', '414A', '411Ba', '411Bb', '412Ba', '412Bb', '413Ba', '413Bb', '414Ba',
                      '414Bb', '411Ca', '411Cb', '412Ca', '412Cb', '413Ca', '413Cb', '414Ca', '414Cb', '411D', '412D',
                      '413D', '414D', '411E', '412E', '413E', '414E', '411Fa', '411Fb', '412Fa', '412Fb', '413Fa',
                      '413Fb', '414Fa', '414Fb', '411G', '412G', '413G']
    }
    return render(request, "home.html", table_data)
