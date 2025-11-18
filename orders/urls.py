from django.urls import path

from . import views

urlpatterns = [
    # common
    path('', views.OrderList.as_view()),
    path('<uuid:pk>/', views.OrderDetail.as_view()),
]
