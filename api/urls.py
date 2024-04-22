from django.urls import path
from . import views 


urlpatterns = [
	path('identify/', views.index_view, name="index")
]