from django.urls import path
from core import views


urlpatterns = [
    path('create-source/', views.CreateSourceView.as_view(), name='create-source'),
    path('source-list/', views.SourceListView.as_view(), name='source-list'),
    path('source/<int:pk>/', views.SourceDetailView.as_view(), name='source'),
]
