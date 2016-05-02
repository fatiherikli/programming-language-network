import re
import logging
import json
import datetime
import settings
import urllib
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Snippet
from api.serializers import SnippetSerializer

from api.models import URL_Queue_DB as URL_Queue

import mimetypes
from cStringIO import StringIO

#old# from extraction.nlp_entities import Extraction_Tool


# LOAD GLOBAL MODULES
    


class NestedDict(dict):
    def __getitem__(self, key):
        if key in self: return self.get(key)
        return self.setdefault(key, NestedDict())
    


@api_view(['GET', 'POST'])
def list_features(request):
    """
    List all snippets, or create a new snippet.
    """
    
    if request.method == 'GET':
        sample="""
        [{
            "url": "http://www.sportsnet.ca/baseball/mlb/blue-jays-victories-in-bronx-came-in-all-shapes-and-forms",
            "action": "fetch",
            "api_key": "SecretEncryptionKey",
            "verbose":"True"
        } ]
        """
        sample=re.sub(r'\n','',sample)
        

        
        return Response('Expecting: '+sample)
    elif request.method == 'POST':
        ET=False
        out_dict=NestedDict()
        out_dict['Status']=['No request passed']
        if request.data:
            api_key=''
            action=''
            url=''
            verbose=True
            try:
                api_key=request.data[0]['api_key']
                action=request.data[0]['action']
                url=request.data[0]['url']
                verbose=request.data[0]['verbose']
            except: pass
            
            out_dict['People']=[]
            out_dict['Organizations']=[]
            out_dict['Locations']=[]

            #Run extraction
            if url:
                ET=Extraction_Tool()
                if ET.url2entities(url):
                    out_dict['People']=ET.dump_type('People')
                    out_dict['Organizations']=ET.dump_type('Organizations')
                    out_dict['Locations']=ET.dump_type('Locations')
                    out_dict['Status']=['Ok']
                else:
                    out_dict['Status']=['No entities found or error']
            else:
                out_dict['Status']=['No url given']

        square_wrap=[]
        square_wrap.append(out_dict)
        out_json=json.dumps(square_wrap) 
        
        if ET: ET.store_results(out_json)

        return Response(square_wrap)



@api_view(['GET', 'POST'])
def snippet_list(request):
    """
    List all snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


