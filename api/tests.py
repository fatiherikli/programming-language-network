#Not setup!
import os
import re
import logging
import json
import datetime
import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from api.models import Snippet
from api.serializers import SnippetSerializer

from api.models import URL_Queue_DB as URL_Queue

#import main_nlp2
#from main_nlp2 import Blob_Fetch
#from main_nlp2 import Structure_Analysis
#from main_nlp2 import Keyword_Scorer
#from main_nlp2 import Extract_Topics
#from main_nlp2 import Extract_Entities


import mimetypes
from cStringIO import StringIO



def test_main(request):
    #Java imports
    from nltk.tag.stanford import NERTagger
    java_path="C:/Program Files/Java/jre1.8.0_31/bin/java.exe"
    os.environ['JAVAHOME']=java_path
    stanford_jar=settings.BASE_DIR+'/../nltk_data/stanford-ner-2015-01-30/stanford-ner.jar'
    stanford_trained=settings.BASE_DIR+'/../nltk_data/stanford-ner-2015-01-30/classifiers/english.all.7class.distsim.crf.ser.gz'

    NER_Tagger = NERTagger(stanford_trained, stanford_jar)

    phrases="once upon a midnight dreary"
    tags=NER_Tagger.tag(phrases) #Above imported
    print "Got "+str(tags)
    return HttpResponse(str(tags))
