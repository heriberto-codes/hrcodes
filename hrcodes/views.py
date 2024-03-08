from django.shortcuts import render

def four_zero_four_page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def five_zero_five_page_not_found_view(request, exception):
    return render(request, '404.html', status=500)
