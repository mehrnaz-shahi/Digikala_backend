from rest_framework.generics import RetrieveAPIView
from .models import Retailer
from .serializers import RetailerSerializer


class RetailerDetailView(RetrieveAPIView):
    queryset = Retailer.objects.all()
    serializer_class = RetailerSerializer
    lookup_field = 'id'  # Use 'id' as the lookup field for retrieving retailers
