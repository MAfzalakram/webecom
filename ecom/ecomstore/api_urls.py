from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import  CatagoryListAPIView, ProductDetailAPIView,ProductListCreateAPIView


urlpatterns = [
    path('products/', ProductListCreateAPIView.as_view()),
    path('catagory/', CatagoryListAPIView.as_view()),
    path('products/<int:pk>/', ProductDetailAPIView.as_view()),
    path('token/', obtain_auth_token, name= 'api_auth_token'),
]