from django.urls import path

from . import views
# from products.views import productform
# from products.views import product_view, delete_product
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('register/',views.register, name='register'),
    path('', views.home, name='home'),
    path('new/',views.new,name='new'),
    path('myfiles/<str:pk>/',views.folders, name='myfiles'),
    path('create_folder/<int:folder_id>/', views.create_folder, name='create_folder'),    
    path('upload/<int:pk>/',views.uploading, name='upload'),
    path('uploads/<int:pk>', views.uploads, name='uploads'),
    path('folder/<int:folder_id>/', views.folder_contents, name='folder_contents'),
    path('delete/<int:pk>/',views.delete_file, name='delete'),
    path('delete-folder/<int:pk>/' ,views.delete_folder, name='delete_folder'),
    path('login/',views.login,name='login'),
    path('logout/', views.logout, name='logout'),
]