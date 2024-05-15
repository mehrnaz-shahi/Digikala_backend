from django.urls import path
from .views import ProductDetailView, DiscountedProductListView,\
    HighDiscountPercentage, ProductSearchAPIView, ProductsListView, ProductRatingView, ProductCommentCreateView, ProductFilterView

urlpatterns = [
    path('<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('discounted/', DiscountedProductListView.as_view(), name='discounted-products'),
    path('high-discount/', HighDiscountPercentage.as_view(), name='high-discount-products'),
    path('search/', ProductSearchAPIView.as_view(), name='product-search'),
    # path('rate-comment/', RateOrCommentProductAPIView.as_view(), name='product-rate-comment-create'),
    path('all/', ProductsListView.as_view(), name='products-list'),
    path('rate-product/', ProductRatingView.as_view(), name='rate-product'),
    path('comment-product/', ProductCommentCreateView.as_view(), name='comment-product'),
    path('price-filtering/', ProductFilterView.as_view(), name='price-filtering'),

]
