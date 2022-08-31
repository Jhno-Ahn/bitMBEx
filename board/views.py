from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse
from board.models import Board
import logging
from django.utils.dateformat import DateFormat
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger( __name__ )

PAGE_SIZE = 5
PAGE_BLOCK = 3

class DetailView( View ) :
    def get(self, request ) :
        num = request.GET["num"]
        pagenum = request.GET["pagenum"]
        number = request.GET["number"]
        dto = Board.objects.get( num = num )
        if dto.ip != request.META.get( "REMOTE_ADDR" ) :
            dto.readcount += 1
            dto.save()
        context = {
            "num" : num,
            "pagenum" : pagenum,
            "number" : number,
            "dto" : dto,
            }
        template = loader.get_template( "detailarticle.html" )
        return HttpResponse( template.render( context, request ) )
        
    def post(self, request) :
        pass

class WriteView( View ) :    
    @method_decorator( csrf_exempt )
    def dispatch(self, request, *args, **kwargs):
        return super( WriteView, self ).dispatch( request, *args, **kwargs)
    def get(self, request) :        
        ref = 1
        restep = 0
        relevel = 0
        num = request.GET.get("num")        # MultiValueDictKeyError 초기값 에러 방지
        if num == None :
            # 제목글
            try :
                # 글이 있는 경우
                maxnum = Board.objects.order_by( "-num" ).values()[0]["num"]
                ref = maxnum + 1            # 그룹화아이디 = 글번호최대값 + 1
            except IndexError :
                # 글이 없는 경우
                ref = 1    
        else :
            # 답변글
            ref = request.GET["ref"]
            restep = request.GET["restep"]
            relevel = request.GET["relevel"]         
            res = Board.objects.filter( ref__exact=ref ).filter( restep__gt=restep )
            for re in res :
                re.restep = int( re.restep ) + 1
                re.save()
            restep = int( restep ) + 1
            relevel = int( relevel ) + 1     
               
        template = loader.get_template( "writearticle.html" )
        context = {
            "num" : num,
            "ref" : ref,
            "restep" : restep,
            "relevel" : relevel,
            }
        return HttpResponse( template.render( context, request ) )
    def post(self, request ) :
        dto = Board(
            writer = request.POST["writer"],
            subject = request.POST["subject"],
            passwd = request.POST["passwd"],
            content = request.POST["content"],
            readcount=0,
            ref = request.POST["ref"],
            restep = request.POST["restep"],
            relevel = request.POST["relevel"],
            regdate = DateFormat( datetime.now() ).format( "Ymd" ),
            ip = request.META.get( "REMOTE_ADDR" )
            )
        dto.save()
        return redirect( "board:list" )

class ListView( View ) :
    def get(self, request ) :
        template = loader.get_template( "list.html" )
        count = Board.objects.all().count()
        
        pagenum = request.GET.get( "pagenum" )
        if not pagenum :
            pagenum = "1"
        pagenum = int( pagenum )
        
        start = ( pagenum - 1 ) * int(PAGE_SIZE)        # ( 5 - 1 ) * 10  + 1    41
        end = start + int(PAGE_SIZE)                    # 41 + 10 - 1            50
        if end > count :
            end = count
            
        logger.info( str(start) + " : " + str( end ) )
        dtos = Board.objects.order_by( "-ref", "restep" )[start:end]
        number = count - ( pagenum - 1 ) * int(PAGE_SIZE)
        
        startpage = pagenum // int(PAGE_BLOCK) * int(PAGE_BLOCK) + 1      # 9 // 10 * 10 + 1    1
        if pagenum % int(PAGE_BLOCK) == 0 :
            startpage -= int(PAGE_BLOCK)
        endpage = startpage + int(PAGE_BLOCK) - 1                         # 1 + 10 -1           10
        pagecount = count // int(PAGE_SIZE)
        if count % int(PAGE_SIZE) > 0 :
            pagecount += 1
        if endpage > pagecount :
            endpage = pagecount  
        pages = range( startpage, endpage+1 )    
        context = {
            "count" : count,
            "dtos" : dtos,
            "pagenum" : pagenum,
            "number" : number,
            "pages" : pages,
            "startpage" : startpage,
            "endpage" : endpage,
            "pageblock" : PAGE_BLOCK,
            "pagecount" : pagecount,
            }
        return HttpResponse( template.render( context, request ) )
    def post(self, request ) :
        pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    