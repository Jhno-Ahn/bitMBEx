from django.urls.conf import path
from django.views.generic.base import TemplateView
from member import views

urlpatterns = [
    path( "main", TemplateView.as_view( template_name="main.html" ) ),  
    path( "write", views.WriteView.as_view(), name="write" )
    ]