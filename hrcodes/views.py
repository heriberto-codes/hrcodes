from django.http import HttpResponse

import datetime


def hello_world(request):
    now = datetime.datetime.now()
    html = "<html><body>Hello World 👋 🌎 </body></html>"
    return HttpResponse(html)
