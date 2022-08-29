from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse

import logging
from member.models import Member
from django.utils.dateformat import DateFormat
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
logger = logging.getLogger( __name__ )

# Create your views here.
class WriteView( View ) :
    @method_decorator( csrf_exempt )
    def dispatch( self, request, *args, **kwargs ) :
        return super( WriteView, self ).dispatch( request, *args, **kwargs )
    def get(self, request ) :
        template = loader.get_template( "write.html" )
        context = {}
        return HttpResponse( template.render( context, request ) )
    def post(self, request ) :
        tel = ""
        tel1 = request.POST["tel1"]
        tel2 = request.POST["tel2"]
        tel3 = request.POST["tel3"]
        if tel1 and tel2 and tel3 :
            tel = tel1 + "-" + tel2 + "-" + tel3 
        
        dto = Member(
            id = request.POST["id"],
            passwd = request.POST["passwd"],
            name = request.POST["name"],
            email = request.POST["email"],
            tel = tel,
            depart = request.POST["depart"],
            logtime = DateFormat( datetime.now() ).format( "Y-m-d" )            
            )
        dto.save()
        logger.info( "write : ", id )
        return redirect( "login" )
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        