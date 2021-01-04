from django.http  import HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to use this page')
        return wrapper_func
    return decorator

def pgo_only(view_func):
    def wrapper_function(request, *args, **kwargs):

        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'Super Admin':
            return redirect('home_superadmin')

        #Sekum Divisi It (0)
        if group == 'Sekum Divisi IT':
            return redirect('home0')

        if group == 'GH Sekum Divisi IT':
            return redirect('home_gh_0')

        #Project Management (1)
        if group == 'Project Management':
            return redirect('home1')

        if group == 'GH Project Management':
            return redirect('home_gh_1')        

        #Business Intelligence & Analythic (2)
        if group == 'Business Intelligence & Analythic':
            return redirect('home2')

        if group == 'GH Business Intelligence & Analythic':
            return redirect('home_gh_2')

        #Business Application Management Core & Non Core (3)
        if group == 'Application Management Core & Non Core':
            return redirect('home3')

        if group == 'GH Application Management Core & Non Core':
            return redirect('home_gh_3')

        #Network, Security & Risk Management (4)
        if group == 'Network, Security & Risk Management':
            return redirect('home4')

        if group == 'GH Network, Security & Risk Management':
            return redirect('home_gh_4')

        #Operation Management DC & DRC (5)
        if group == 'Operation Management DC & DRC':
            return redirect('home5')

        if group == 'GH Operation Management DC & DRC':
            return redirect('home_gh_5')

        #Helpdesk & Support (6)
        if group == 'Helpdesk & Support':
            return redirect('home6')

        if group == 'GH Helpdesk & Support':
            return redirect('home_gh_6')

        #Planning and Governance
        if group == 'GH Planning and Governance':
            return redirect('home_gh_pgo')

        if group == 'Planning and Governance':
            return view_func(request, *args, **kwargs)
    return wrapper_function