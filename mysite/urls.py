from app01 import views
from django.urls import path,re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('', views.home_view, name='home'),
    path('uploadImg/', views.uploadImg),
    path('showImg/', views.showImg),
    path('showImg/deleteImg/', views.deleteImg),
    path('showImg/detectImg/', views.detectImg),
    path('<int:sid>/queryImg/', views.queryImg),
    path('register/', views.register),
    # path('<int:sid>/queryImg/', views.queryImg),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]