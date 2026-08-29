from django.shortcuts import render, redirect

# Create your views here.
def search_results(request):
    rezultate = request.POST.get('rezultate', [])
    return render(request, 'results.html', {'rezultate': rezultate})