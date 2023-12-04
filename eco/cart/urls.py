
from django.urls import path
from. import views
# from .views import CartView

app_name = 'cart'

urlpatterns = [
    path('add/<int:prd_id>/',views.add_cart,name='add_cart'),
    path('',views.cart_detail,name='cart_detail'),
    path('remove/<int:prd_id>/',views.cart_remove,name='cart_remove'),
    path('full_remove/<int:prd_id>/', views.full_remove,name='full_remove'),
    path('order/<int:prd_id>/', views.create_order, name='create_order'),
    path('myorder/', views.myorder, name='myorder'),
]
