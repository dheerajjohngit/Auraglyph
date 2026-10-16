from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('phones/', views.phones, name='phones'),
    path('accessories/', views.accessories, name='accessories'),
    path('audio/', views.audio, name='audio'),
    path('watch/', views.watch, name='watch'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('cmf/', views.cmf, name='cmf'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:id>/',views.remove_from_wishlist,name='remove_from_wishlist'),
    path('add-to-cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
    path('remove-from-cart/<int:id>/',views.remove_from_cart,name='remove_from_cart'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('orders/', views.my_orders, name='orders'),
    path('analytics/',views.analytics_dashboard,name='analytics'),
    path('buy-now/<int:id>/',views.buy_now,name='buy_now'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)