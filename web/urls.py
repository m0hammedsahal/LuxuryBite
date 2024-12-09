from django.urls import path
from . import views

app_name = "web"


urlpatterns = [
    path('', views.index, name='index'),
    path('product-list/', views.product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:id>/', views.add_cart, name='add_to_cart'),
    path('cart/', views.cart_page, name='cart_page'),
    path('cart/update/<int:id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('cart/remove/<int:id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('all-orders/', views.all_orders, name='all_orders'),
    path('order-confirmation/<int:id>/', views.order_confirmation, name='order_confirmation'),
    path('track-order/<int:order_id>/', views.track_order, name='track_order'),
]