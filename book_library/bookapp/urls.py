from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('website_template/', views.website_template, name='website_template'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('test/', views.test, name='test'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('listing/', views.browse_listings, name='search'),
    path('listing/add/', views.add_listing, name='add_listing'),
    path('forgotPassword/', views.forgot, name='forgotPassword'),
    path('resetPassword/', views.resetpw, name='resetPassword'),
    path('bookinfo/<str:id>/', views.bookinfo, name='bookinfo'),
    path('cart/', views.cart, name='cart'),
]
