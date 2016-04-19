import os
import re
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.files.base import ContentFile


from htmt_prep import rawtxt2gml
from jgraphml2json import main as jmain


def htmt_page(request):
    the_url=""
    static_dir="/static/htmt/" #http://127.0.0.1:8080/static/htmt/assets/lib/fuzzy.min.js
    return render_to_response('htmt_index.html', {
                           'the_url': the_url,
                           'static_dir': static_dir,
                           }, context_instance=RequestContext(request))
    

def run_command(command):
    # p = sub.Popen(command,stdout=sub.PIPE,stderr=sub.PIPE)
    # output, errors = p.communicate()
    p = os.popen(command,"r")
    while 1:
        line = p.readline()
        if not line: break
        line=re.sub(r'\n','',line) 
        yield line
    return
    
def process_file_render(contentfile_contents):
    
    #1/  Create gml (assumes format)
    from htmt_prep import rawtxt2gml
    filename="144cutoff.txt" #web2file
    oa,valid,gml_filename=rawtxt2gml(filename,contentfile_contents)
    gml_filename="jout.gml"
    
    #2/  Pass through gelphi toolkit
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
    output_filename=BASE_DIR+"/out.gexf"
    
    try: os.remove(output_filename)
    except:pass
    
    
    cmd="c:/jython2.2.1/jython "+BASE_DIR+"/pygephi/gephi.py "+BASE_DIR+"/"+gml_filename+" "+output_filename
    print "Running jython: "+cmd
    for line in run_command(cmd):
        print line
        
    jmain()
    
    return

def upload_page( request ):
    #/inventory/upload
    #https://docs.djangoproject.com/en/1.9/ref/files/file/
    print "Upload manager"
    if request.method == 'POST':
        #File for user or default
        username="default"
        
        print ('Raw Data: "%s"' % request.body   )
        file_bytes=request.body
        contentfile_contents = ContentFile(file_bytes) #ContentFile type
        
        process_file_render(contentfile_contents)
    
        if False:
            #Delete all records
            Inventory_File.objects.filter(username=username).delete()
            instance = Inventory_File()
            instance.username=username
            instance.file.save("default_template.csv",contentfile_contents)
    
            instance.save()
            print ("Saved")

    return HttpResponse("")



if __name__ == "__main__":
    dev_file="144cutoff.txt"
    process_file_render("")
    