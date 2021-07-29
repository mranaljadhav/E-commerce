from django.contrib.auth import views as auth_views 
from django.urls import path
from . import views
urlpatterns = [
    path('', views.store, name = 'store'),
    path('cart', views.cart, name = 'cart'),
    path('checkout', views.checkout, name = 'checkout'),
    path('update_order', views.updateOrder, name = 'update_order'),
    path('processOrder', views.processOrder, name = 'processOrder'),
    path('register', views.register, name = 'register'),
    path('login', views.loginPage, name = 'login'),
    path('logout', views.logoutPage ,name = 'logout'),
    path('setting', views.setting ,name = 'setting'),

    path('reset_password', 
        auth_views.PasswordResetView.as_view(template_name = 'reset_password.html'), name = 'reset_password'),
    path('reset_password_sent', 
        auth_views.PasswordResetDoneView.as_view(template_name = 'password_reset_done.html'), name = 'password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('reset_password_complete', 
        auth_views.PasswordResetCompleteView.as_view(template_name = 'reset_password_complete.html'), name = 'password_reset_complete')
]