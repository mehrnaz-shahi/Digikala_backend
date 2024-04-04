from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductDetailSerializer, ProductSerializer


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'  # Use 'id' as the lookup field for retrieving products


class DiscountedProductListView(ListAPIView):
    queryset = Product.objects.filter(is_discounted=True)
    serializer_class = ProductSerializer


class HighDiscountPercentage(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        min_discount_percentage = self.request.query_params.get('min_dp')
        queryset = Product.objects.filter(is_discounted=True)
        if min_discount_percentage:
            queryset = queryset.filter(discount_percentage__gte=min_discount_percentage)
        return queryset


class ProductSearchAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q')  # Get the search query from query parameters
        # Filter products by name containing the query OR categories with name containing the query
        print(query)
        return Product.objects.filter(name__icontains=query) | \
            Product.objects.filter(categories__name__icontains=query)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
