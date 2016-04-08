from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse


def htmt_page(request):
    the_url=""
    static_dir="/static/htmt/" #http://127.0.0.1:8080/static/htmt/assets/lib/fuzzy.min.js
    return render_to_response('htmt_index.html', {
                           'the_url': the_url,
                           'static_dir': static_dir,
                           }, context_instance=RequestContext(request))
