from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_movie, name='add_movie'),
    path('edit/<int:id>/', views.edit_movie, name='edit_movie'),
    path('delete/<int:id>/', views.delete_movie, name='delete_movie'),
    path('report/', views.report, name='report'),
    path('export/', views.export_movies, name='export_movies'),
    path('watch/<int:id>/', views.watch_movie, name='watch_movie'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    path('export/xls/', views.export_xls, name='export_xls'),
]
