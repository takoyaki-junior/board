from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "board"
urlpatterns = [
    path('', views.index, name="index"),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('create/', views.create, name='create'),
    path('terms/', TemplateView.as_view(template_name='base/terms.html'), name='terms'),
]
