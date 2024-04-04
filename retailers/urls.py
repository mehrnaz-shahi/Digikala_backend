from django.urls import path
from .views import RetailerDetailView

urlpatterns = [
    path('<int:id>/', RetailerDetailView.as_view(), name='retailer-detail'),
]
