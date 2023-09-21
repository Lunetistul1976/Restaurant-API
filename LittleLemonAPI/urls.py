from django.urls import path
from . import views

urlpatterns = [
 path("menu-items",views.MenuItemView.as_view()),
 path("menu-items/<int:pk>",views.SingleMenuItemView.as_view()),
 path("orders",views.OrderItemView.as_view()),
 path("orders/<int:pk>",views.OrderView.as_view()),
 path("cart/menu-items",views.CartView.as_view()),
 path('category', views.CategoriesView.as_view()),
 path("groups/manager/users",views.managers_function),
 path("groups/delivery-crew/users",views.delivery_function),


]