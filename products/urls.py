from django.urls import path
from .views import ProductDetailView, DiscountedProductListView,\
    HighDiscountPercentage, ProductSearchAPIView, RateOrCommentProductAPIView, ProductsListView

urlpatterns = [
    path('<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('discounted/', DiscountedProductListView.as_view(), name='discounted-products'),
    path('high-discount/', HighDiscountPercentage.as_view(), name='high-discount-products'),
    path('search/', ProductSearchAPIView.as_view(), name='product-search'),
    path('rate-comment/', RateOrCommentProductAPIView.as_view(), name='product-rate-comment-create'),
    path('all/', ProductsListView.as_view(), name='products-list'),

]
