from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permissions import IsSeller, IsFarmer

from .models import Product
from .serializers import ProductSerializer, ProductCreateSerializer, ProductUpdateSerializer


class ProductList(APIView):
    """
    Endpoint to handle both fetching all products and creating a new product.
    """

    allowed_methods = ['GET', 'POST']
    parser_classes = [FormParser, MultiPartParser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsFarmer()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductSerializer

    def get(self, request):
        """
        Get the product list
        """
        products = Product.objects.all()
        serializer = self.get_serializer_class()(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new product
        """
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            serializer.save(seller_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductDetail(APIView):
    """
    Retrieve, update, or delete a product.
    """

    allowed_methods = ['GET', 'PUT', 'DELETE']
    parser_classes = [FormParser, MultiPartParser]

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAuthenticated(), IsSeller()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ProductSerializer
        elif self.request.method == 'PUT':
            return ProductUpdateSerializer
        return None

    def get_object(self, pk):
        obj = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk):
        """
        Get a Product's details
        """
        product = self.get_object(pk)
        serializer = self.get_serializer_class()(product)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a Product
        """
        product = self.get_object(pk)
        serializer = self.get_serializer_class()(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a product
        """
        product = self.get_object(pk)
        product.delete()
        return Response({"detail": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
