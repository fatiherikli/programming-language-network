import re
import logging
import json
import datetime
import urllib

from rest_framework import status
from api.models import Snippet
from api.serializers import SnippetSerializer
from api.models import URL_Queue_DB as URL_Queue

from rest_framework.decorators import api_view
from rest_framework.response import Response


class NestedDict(dict):
    def __getitem__(self, key):
        if key in self: return self.get(key)
        return self.setdefault(key, NestedDict())


@api_view(['GET', 'POST'])
def request_stack(request):
    """
    Standard interface for api module calling
    """
    if request.method == 'GET':
        return Response("Blank")
    elif request.method == 'POST':
        title=""
        action=""
        out_dict=NestedDict()
        if request.data:
            if 'title' in request.data[0]: title=request.data[0]['title']
            if 'action' in request.data[0]: action=request.data[0]['action']
            if 'api_key' in request.data[0]: api_key=request.data[0]['api_key']
            
        if action=='summarize':
            out_dict['extracted']=sentence2nn(title)
        
        square_wrap=[]
        square_wrap.append(out_dict)
        
        return Response(square_wrap)




def sentence2nn(sentence):
    # Given string sentence, return POS tagged nouns
    #0v1# JC May 19, 2015
    # - leverage same source of existing tagger
    nn_string=""
    nn_list=[]
    valid_nn=['NNP','NNPS','NN','NNS']

    #Do with new tagger
    tags=Tagger.tag_it([sentence])
    print "GOT: "+str(tags)
    for word,tag in tags:
        if tag in valid_nn:
            nn_list.append(word)
            
#Internal tagger            
#    #Dfrom nltk.tag import ClassifierBasedTagger, pos_tag
#    from clean_nlp import Structure_Analysis
#    SE=Structure_Analysis()
#    for tag_word in SE.tag_words(blob=sentence,lowercase=False,stopwords=False):
#        print "OK: "+str(tag_word)
#        if tag_word['pos'] in valid_nn:
#            nn_list.append(tag_word['word'])
    
    nn_string=" ".join(nn_list)
    return nn_string


if __name__ == '__main__':            
    #request_stack('')
    sentence="Hubble Finds Massive Halo Around The Andromeda Galaxy"
    nn_string=sentence2nn(sentence)
    print "GOT: "+nn_string
    
