from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register',views.register),
    path('login', views.login_page),
    path('login_process', views.login_process),
    path('dashboard', views.dashboard),
    path('clear', views.clear),
    path('edit_account/<int:id>', views.edit_account),
    path('updated_account/<int:id>', views.updated_account),
    path('add_quote', views.add_quote),
    path('view_account/<int:id>', views.view_account),
    path('delete/<int:id>', views.delete)

]