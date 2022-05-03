from django.urls import path
from . import views
app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.MyLoginView.as_view(), name="login"),
    path('logout/', views.MyLogoutView.as_view(), name="logout"),
    path('profile/', views.UserProfileView.as_view(), name="profile"),
    path('profile_change/', views.MyUserChangeView.as_view(), name="profile_change"),
    path('password_change/', views.MyPasswordChangeView.as_view(),
         name="password_change"),
    path('password_change_done/', views.MyPasswordChangeDoneView.as_view(),
         name="password_change_done"),
]
