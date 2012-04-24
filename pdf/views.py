from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template.context import RequestContext
from django.shortcuts import get_object_or_404

def home(request):
     return redirect('/admin/')