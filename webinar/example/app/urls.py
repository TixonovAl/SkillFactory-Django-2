from django.urls import path
from .views import index, StartView, ProductListView, ProductCreateView

app_name = 'app'
urlpatterns = [
    path('', index, name='index'),
    path('base/', StartView.as_view(), name='start'),
    path('product/', ProductListView.as_view(), name='products'),
    path('product/create/', ProductCreateView.as_view(), name='create'),
]