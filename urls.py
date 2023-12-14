from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as views_auth


urlpatterns = [
    path('', views.index, name="index"),
    path('home', views.home, name="home"),
    path('log_out', views.log_out, name="log_out"),
    path('signup', views.signup, name="signup"),
    path('password_change', 
         views_auth.PasswordChangeView.as_view(template_name="wangdo/password_change.html", success_url="password_change_done"), 
         name="password_change_view"),
    path('password_change_done', views_auth.PasswordChangeDoneView.as_view(template_name="wangdo/password_change_done.html"), 
         name="password_Change_done"),
    path('password_reset', 
         views_auth.PasswordResetView.as_view(template_name= "wangdo/password_reset.html"), 
         name="password_reset"),
    path('password_reset_done', 
         views_auth.PasswordResetDoneView.as_view(template_name= "wangdo/password_reset_done.html"), 
         name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>', 
         views_auth.PasswordResetConfirmView.as_view(template_name= "wangdo/password_reset_confirm.html"), 
         name="password_reset_confirm"),
    path('password_reset_complete', 
         views_auth.PasswordResetCompleteView.as_view(template_name= "wangdo/password_reset_complete.html"), 
         name="password_reset_complete"),
     path('products', views.products, name="products"),
     path('product/<int:id>', views.product, name="product"),
     path('cart', views.cart, name="cart"),

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)