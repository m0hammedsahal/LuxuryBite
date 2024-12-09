from django.urls import path
from manager import views

app_name = "manager"


urlpatterns = [
    path("", views.index, name="index"),
    path("unauthorized_access/", views.unauthorized_access, name="unauthorized_access"),
    
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:id>/', views.delete_category, name='delete_category'),
    
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:id>/', views.delete_product, name='delete_product'),

    path('orders/', views.orders_list, name='orders_list'),

    path("order/Track/<int:id>/", views.order_track, name="order_track"),
    path("order/Cancel/<int:id>/", views.cancel_order, name="cancel_order"),

]