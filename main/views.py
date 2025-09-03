from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'npm' : '2406397196',
        'name': 'Refki Septian',
        'class': 'PBP C'
    }

    return render(request, "main.html", context)