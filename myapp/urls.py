from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('signin', views.signin, name = 'signin'),
    path('signup', views.signup, name = 'signup'),
    path('logout', views.logout, name = 'logout'),
    path('blog', views.blog, name = 'blog'),
    path('create', views.create, name = 'create'),
    path('profile/<int:id>', views.profile, name = 'profile'),
    path('profile/edit/<int:id>', views.profileedit, name = 'profileedit'),
    path('increaselikes<int:id>', views.increaselikes, name = 'increaselikes'),
    path('post/<int:id>', views.post, name = 'post'),
    path('post/comment/<int:id>', views.savecomment, name = 'savecomment'),
    path('post/comment/delete/<int:id>', views.deletecomment, name = 'deletecomment'),
    path('post/edit/<int:id>', views.editpost, name = 'editpost'),
    path('post/delete/<int:id>', views.deletepost, name = 'deletepost'),
    path('contact', views.contact_us, name = 'contact'),
]
