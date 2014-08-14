from django.shortcuts import render_to_response
from django.template import RequestContext, loader
# Create your views here.

def index(request):
    context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
    return render_to_response('cookingnutritious/index.html',
                             context_instance=context)
