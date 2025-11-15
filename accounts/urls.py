from django.urls import path

from . import views

urlpatterns = [
    # common
    path('', views.UserList.as_view()),
    path('<uuid:pk>/', views.UserDetail.as_view()),
]
