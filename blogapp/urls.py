from django.urls import path
from . import views

urlpatterns = [
# General
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login_view'),
    path('signout/', views.signout, name = 'logout'),

# Admin Urls
    path('adminregister/', views.adminregister, name='adminregister'),
    path('adminblogs/', views.AdminBlogListView, name='adminblogs'),
    path('admineditpost/<int:_id>/', views.admineditpost, name='admineditpost'),
    path('admindeletepost/<int:_id>/', views.admindeletepost, name='admindeletepost'),
    path('adminblog/<int:_id>', views.AdminBlogDetailView, name='adminblog'),
    path('admindelete/<int:_id>/', views.admindeletecomment, name='admindeletecomment'),
    path('admineditcomment/<int:_id>/', views.admineditcomment, name='admineditcomment'),
    path('adminaboutus/', views.adminaboutus, name='adminaboutus'),
    path('admincontactus/', views.admincontactus, name='admincontactus'),
    path('adminaddpost/', views.adminaddpost, name='adminaddpost'),
    path('users/', views.user, name='user'),
    path('deleteusers/<int:_id>/', views.deleteuser, name='deleteuser'),
    path('makeuseradmin/<int:_id>/', views.adminate, name='adminate'),

# Writer Urls
    path('writerregister/', views.writerregister, name='writerregister'),
    path('writerblogs/', views.WriterBlogListView, name='writerblogs'),
    path('writerblog/<int:_id>', views.WriterBlogDetailView, name='writerblog'),
    path('writerblogger/<int:_id>', views.WriterBloggerDetailView, name='writerblogger'),
    path('writerdelete/<int:_id>/', views.writerdeletecomment, name='writerdeletecomment'),
    path('writereditcomment/<int:_id>/', views.writereditcomment, name='writereditcomment'),
    path('writermanagecomment/<int:_id>/', views.writermanagecomment, name='writermanagecomment'),
    path('writeraboutus/', views.writeraboutus, name='writeraboutus'),
    path('writercontactus/', views.writercontactus, name='writercontactus'),
    path('managepost/', views.writermanagepost, name='writermanagepost'),
    path('writereditpost/<int:_id>/', views.writereditpost, name='writereditpost'),
    path('writerdeletepost/<int:_id>/', views.writerdeletepost, name='writerdeletepost'),
    path('writeraddpost/', views.writeraddpost, name='writeraddpost'),

# Reader Urls
    path('readerregister/', views.readerregister, name='readerregister'),
    path('readerblogs/', views.ReaderBlogListView, name='readerblogs'),
    path('readerblog/<int:_id>', views.ReaderBlogDetailView, name='readerblog'),
    path('readerdelete/<int:_id>/', views.readerdeletecomment, name='readerdeletecomment'),
    path('readereditcomment/<int:_id>/', views.readereditcomment, name='readereditcomment'),
    path('readermanagecomment/<int:_id>/', views.readermanagecomment, name='readermanagecomment'),
    path('readeraboutus/', views.readeraboutus, name='readeraboutus'),
    path('readercontactus/', views.readercontactus, name='readercontactus'),

]