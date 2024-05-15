from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductDetailSerializer, ProductSerializer, ProductCommentSerializer, ProductRatingSerializer
from rest_framework.permissions import IsAuthenticated
from score.models import ProductRating
from comments.models import ProductComment
from .filters import ProductFilter


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    lookup_field = 'id'  # Use 'id' as the lookup field for retrieving products

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProductsListView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


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


# class RateOrCommentProductAPIView(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         product_id = request.data.get('productId')
#         rate = request.data.get('rate')
#         comment = request.data.get('comment')
#
#         if product_id is None or (rate is None and comment is None):
#             return Response({'error': 'productId, rate, and/or comment are missing.'},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         # if not user.products.filter(id=product_id).exists():
#         #     return Response({'error': 'You have not purchased this product yet.'}, status=status.HTTP_403_FORBIDDEN)
#
#         if rate is not None:
#             rating_data = {'user': user.id, 'product': product_id, 'rating': rate}
#             rating_serializer = ProductRatingSerializer(data=rating_data)
#             if rating_serializer.is_valid():
#                 rating_serializer.save()
#             else:
#                 return Response(rating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         if comment is not None:
#             comment_data = {'user': user.id, 'product': product_id, 'text': comment}
#             comment_serializer = ProductCommentSerializer(data=comment_data)
#             if comment_serializer.is_valid():ProductCommentSerializer
#                 comment_serializer.save()
#             else:
#                 return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         return Response({'success': 'Rating and/or comment added successfully.'}, status=status.HTTP_201_CREATED)


class ProductRatingView(CreateAPIView):
    queryset = ProductRating.objects.all()
    serializer_class = ProductRatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Assign the current logged-in user to the rating
        serializer.save(user=self.request.user)


class ProductCommentCreateView(CreateAPIView):
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductFilterView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
