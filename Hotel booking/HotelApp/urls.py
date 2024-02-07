#definisem url

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView

app_name = 'hotel'

urlpatterns = [
    path('', views.index, name='index'), 
    path('registration', views.registration, name='registration'),
    path('logout', views.logout, name='logout'),
    path('reservation', views.reservation, name='reservation'),
    path('search/', views.search, name='search'),
    path('search/index', views.index, name='index'),
    path('search/search', views.search, name='search'),
    path('search/login', views.login, name='login'),
    path('hotel/login', views.login, name='login'),
    path('hotel/search', views.search, name='search'),
    path('hotel/index', views.index, name='index'),
    
    path('hotel/<int:hotel_id>', views.hotel_details, name='hotel_details'),
   path('hotel/add_comment/<int:hotel_id>/', views.add_comment, name='add_comment'),
    path('hotel/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +\
              static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)