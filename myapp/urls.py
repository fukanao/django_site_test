
# myapp/urls.py
from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path('', views.PortalView.as_view(), name='portal'),
    path('blog_form/', views.blog_form, name='blog_form'),
    path('edit_blog_form/', views.edit_blog_form, name='edit_blog_form'),
    path('list/', views.list_data, name='list_data'),
    path('select/', views.select, name='select'),
    path('show_data/', views.show_data, name='show_data'),
]

