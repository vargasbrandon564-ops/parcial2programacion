from django.shortcuts import render


def home_view(request):
    """Vista de la página de inicio"""
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('dashboard')
    return render(request, 'home.html')
